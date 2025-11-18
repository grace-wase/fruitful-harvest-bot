from flask import Flask, render_template, jsonify, request
import os
import json
import re
from rapidfuzz import process, fuzz

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load knowledge files
KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "data", "knowledge")
KNOWLEDGE = {}

for lang, file_path in [("en", "en.json"), ("ny", "ny.json")]:
    full_path = os.path.join(KNOWLEDGE_DIR, file_path)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            KNOWLEDGE[lang] = json.load(f)
        print(f"✅ Loaded {lang} knowledge with {len(KNOWLEDGE[lang].get('responses', {}))} entries")
    except Exception as e:
        print(f"❌ Failed to load {lang}: {e}")
        KNOWLEDGE[lang] = {"greetings": [], "responses": {"default": "Error loading answers."}}

# UI Texts — CLEANED WELCOME MESSAGE
UI_TEXTS = {
    "en": {
        "title": "🌱 Fruitful Harvest Assistant",
        "subtitle": "Your personal farming guide - Ask anything about growing fruits!",
        "placeholder": "Ask about any fruit growing method...",
        "send_button": "Send",
        "welcome_message": """Hello! 👋 I'm your Fruitful Harvest assistant. Just ask about any fruit — I'm here to help!"""
    },
    "ny": {
        "title": "🌱 Fruitful Harvest Assistant",
        "subtitle": "Wothandizira wa ulimi - Funsani chilichonse za kulumiza zipatso!",
        "placeholder": "Funsani za njira zilizonse zokulitsira zipatso...",
        "send_button": "Tumizani",
        "welcome_message": """Moni! 👋 Ndine Fruitful Harvest assistant. Funsani chilichonse — ndinapangidwa!"""
    }
}

# Enhanced fruit detection (same as before)
ENHANCED_FRUITS = {
    "mango": ["mango", "mangwanje"],
    "banana": ["banana", "nthochi", "nthochi ya m'madzi"],
    "avocado": ["avocado", "avokado"],
    "orange": ["orange", "malamulo"],
    "apple": ["apple", "mapere"],
    "strawberry": ["strawberry", "sitiroberi"],
    "pineapple": ["pineapple", "nanazi"],
    "passion_fruit": ["passion fruit", "passionfruit", "zipatso za passion"],
    "watermelon": ["watermelon", "mtedza"],
    "grape": ["grape", "mphesa"],
    "blueberry": ["blueberry", "mphesa wa blue"],
    "cherry": ["cherry", "cheri"],
    "coconut": ["coconut", "nkhungu"],
    "papaya": ["papaya", "popo"],
    "guava": ["guava", "mapela"],
    "soursop": ["soursop", "mphala ya m'madzi"],
    "tamarind": ["tamarind", "mkoko"],
    "baobab": ["baobab", "m'phala"],
    "cashew": ["cashew", "kashu"],
    "jackfruit": ["jackfruit", "nkhwani"],
    "kigelia": ["kigelia", "nkhokwe"],
    "kiwi": ["kiwi", "kiwi fruit"],
    "pear": ["pear", "pea"],
    "peach": ["peach", "m'phala ya m'madzi"],
    "plum": ["plum", "m'phala ya m'madzi"],
    "raisin": ["raisin", "mphesa ya m'madzi"],
    "cantaloupe": ["cantaloupe", "m'tedza ya m'madzi"],
    "lemon": ["lemon", "ndimu"],
    "lime": ["lime", "ndimu ya m'madzi"],
    "bergamot": ["bergamot", "bergamot"],
    "cranberry": ["cranberry", "mphesa ya m'madzi"],
    "elderberry": ["elderberry", "mphesa ya m'madzi"],
    "blackberry": ["blackberry", "mphesa ya m'madzi"],
    "raspberry": ["raspberry", "mphesa ya m'madzi"],
    "nectarine": ["nectarine", "m'phala ya m'madzi"],
    "honeydew": ["honeydue", "m'tedza ya m'madzi"],
    "quince": ["quince", "m'phala ya m'madzi"],
    "tomato": ["tomato", "m'tedza ya m'madzi"],
    "eggplant": ["eggplant", "m'tedza ya m'madzi"],
    "chili_pepper": ["chili pepper", "chili", "ndimu ya m'madzi"],
    "tamarillo": ["tamarillo", "m'tedza ya m'madzi"],
    "carambola": ["carambola", "starfruit"],
    "dragon_fruit": ["dragon fruit", "pitaya", "dragon"],
    "salak": ["salak", "snake fruit"],
    "rambutan": ["rambutan", "rambutan"],
    "breadfruit": ["breadfruit", "nkhokwe ya m'madzi"],
    "jabuticaba": ["jabuticaba", "jabuticaba"],
    "feijoa": ["feijoa", "pineapple guava"],
    "moringa": ["moringa", "moringa fruit"],
    "pawpaw": ["pawpaw", "papaya"],
    "saba_banana": ["saba banana", "saba nthochi"],
    "acai": ["acai", "acai berry"],
    "cupuaçu": ["cupuaçu", "cupuaçu"]
}

ENHANCED_TOPICS = {
    "planting": ["plant", "planting", "grow", "kulumiza", "kulima"],
    "soil": ["soil", "chisaka", "land", "earth", "mchisaka"],
    "fertilizer": ["fertilizer", "manure", "kuyesa", "compost", "m'yesa"],
    "water": ["water", "watering", "kumutha", "irrigation", "madzi"],
    "pests": ["pest", "disease", "tizilombo", "insect", "zotizilombo"],
    "harvest": ["harvest", "ripe", "kuputula", "mature", "kuvuna"],
    "care": ["care", "maintain", "kukhalitsa", "prune", "kuchulitsa"]
}

FRUIT_EMOJIS = {
    "mango": "🥭",
    "banana": "🍌",
    "avocado": "🥑",
    "orange": "🍊",
    "apple": "🍎",
    "strawberry": "🍓",
    "pineapple": "🍍",
    "passion_fruit": "🥝",
    "watermelon": "🍉",
    "grape": "🍇",
    "blueberry": "🫐",
    "cherry": "🍒",
    "coconut": "🥥",
    "papaya": "🍈",
    "guava": "🍈",
    "soursop": "🍏",
    "tamarind": "🌱",
    "baobab": "🌳",
    "cashew": "🥜",
    "jackfruit": "🌿",
    "kigelia": "🌸",
    "kiwi": "🥝",
    "pear": "🍐",
    "peach": "🍑",
    "plum": "🍒",
    "raisin": "🍇",
    "cantaloupe": "🍈",
    "lemon": "🍋",
    "lime": "🍋",
    "bergamot": "🍊",
    "cranberry": "🫐",
    "elderberry": "🫐",
    "blackberry": "🫐",
    "raspberry": "🍓",
    "nectarine": "🍑",
    "honeydew": "🍈",
    "quince": "🍏",
    "tomato": "🍅",
    "eggplant": "🍆",
    "chili_pepper": "🌶️",
    "tamarillo": "🍅",
    "carambola": "⭐",
    "dragon_fruit": "🐉",
    "salak": "🐍",
    "rambutan": "🌰",
    "breadfruit": "🍞",
    "jabuticaba": "🍇",
    "feijoa": "🍈",
    "moringa": "🌱",
    "pawpaw": " papaya ",
    "saba_banana": "🍌",
    "acai": "🟣",
    "cupuaçu": "🍈"
}

def detect_language_from_message(message):
    chichewa_keywords = ["bwanji", "chiti", "kuti", "ndi", "za", "monga", "moni", "uli", "muli", "ndik", "m'madzi", "kum", "kulu", "nthochi", "mango", "mangwanje", "avokado", "nkhungu", "mapere", "mphesa"]
    return "ny" if any(kw in message.lower() for kw in chichewa_keywords) else "en"

def extract_fruit_and_topic(text, lang="en"):
    text_lower = text.lower()
    detected_fruit, detected_topic = None, None

    # Fruit detection
    for fruit, variations in ENHANCED_FRUITS.items():
        if any(var in text_lower for var in [v.lower() for v in variations]):
            detected_fruit = fruit
            break

    # Topic detection
    for topic, variations in ENHANCED_TOPICS.items():
        if any(var in text_lower for var in [v.lower() for v in variations]):
            detected_topic = topic
            break

    return detected_fruit, detected_topic

def clean_markdown_to_paragraph(text):
    """
    Convert structured text into one clean paragraph
    """
    if not isinstance(text, str) or not text:
        return ""

    # Remove checkmarks, cross marks, bullets
    text = re.sub(r'^\s*✅', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*❌', 'Mistake: ', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*•', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-', '', text, flags=re.MULTILINE)

    # Remove **bold** and __underline__
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)

    # Replace newlines and extra spaces
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Capitalize first letter
    if len(text) > 0:
        text = text[0].upper() + text[1:]

    return text

def is_greeting(text):
    text_lower = text.lower()
    greetings = [
        "hello", "hi", "hey", "good morning", "how are you", "what's up", "can you help me",
        "i need advice", "what should i do", "moni", "muli bwanji", "ndi m'madzi", "bwanji",
        "muli", "ndik", "ndi", "kuti", "za", "monga", "uli", "kum", "kulu", "m'madzi",
        "howdy", "yo", "greetings", "good day", "good afternoon", "good evening"
    ]
    return any(g in text_lower for g in greetings)

def get_bot_response(user_msg, lang="en"):
    user_msg = user_msg.strip()
    if not user_msg:
        return "Chonde lembani funso..." if lang == "ny" else "Please type a question..."

    # Auto-detect language
    if lang == "auto":
        lang = detect_language_from_message(user_msg)

    responses = KNOWLEDGE.get(lang, {}).get("responses", {})
    msg_lower = user_msg.lower()

    # Handle greetings
    if is_greeting(user_msg):
        if "how are you" in msg_lower:
            return "I'm doing great, thank you! 😊 How can I help you today?"
        elif "hello" in msg_lower or "hi" in msg_lower or "hey" in msg_lower:
            return "Hello! 👋 I'm your Fruitful Harvest assistant. Just ask about any fruit — I'm here to help!"
        else:
            return "Hi there! 👋 I'm ready to help you with fruit-growing tips. Ask me anything!"

    # Extract fruit and topic
    detected_fruit, detected_topic = extract_fruit_and_topic(user_msg, lang)

    # If both detected
    if detected_fruit and detected_topic:
        key = f"{detected_fruit}_{detected_topic}"
        if key in responses:
            raw_text = responses[key]
            clean_text = clean_markdown_to_paragraph(raw_text)
            emoji = FRUIT_EMOJIS.get(detected_fruit, "")
            return f"{emoji} {clean_text}"

    # Only fruit mentioned
    if detected_fruit:
        topics = "planting, soil, watering, fertilizer, pests, harvest, care"
        emoji = FRUIT_EMOJIS.get(detected_fruit, "")
        return f"{emoji} Ask me about {detected_fruit}: {topics}."

    # Only topic mentioned
    if detected_topic:
        return f"Which fruit do you want to know about {detected_topic} for?"

    # Fallback
    return clean_markdown_to_paragraph(responses.get("default", "I can help with fruit growing! Tell me which fruit you're interested in."))

# Routes
@app.route('/')
def chat():
    return render_template('chat.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.get_json() or {}
    msg = data.get('message', '')
    lang = data.get('language', 'en')
    reply = get_bot_response(msg, lang)
    return jsonify({"reply": reply})

@app.route('/ui-texts/<lang>')
def get_ui_texts(lang):
    return jsonify(UI_TEXTS.get(lang, UI_TEXTS["en"]))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌟 FRUITFUL HARVEST BOT - FINAL VERSION")
    print("✅ Clean welcome message")
    print("✅ Human-like greeting: 'Hello!', 'How are you?'")
    print("✅ Answers in NATURAL PARAGRAPHS (no bullets)")
    print("✅ Adds EMOJI for each fruit")
    print("="*60 + "\n")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)