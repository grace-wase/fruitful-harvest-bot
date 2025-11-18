import json
import os
from datasets import Dataset

def main():
    print("⚠️  WARNING: Fine-tuning is NOT needed for detailed answers.")
    print("✅ Use your JSON knowledge base + LLM for better results.")
    print("✅ This approach is more flexible and cost-effective.")
    
    # Validate your knowledge files exist
    knowledge_dir = os.path.join(os.path.dirname(__file__), "data", "knowledge")
    
    for lang in ["en", "ny"]:
        file_path = os.path.join(knowledge_dir, f"{lang}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                responses = data.get("responses", {})
                print(f"✅ {lang.upper()}: Found {len(responses)} knowledge entries")
                
                # Check for long-form content
                long_entries = [k for k, v in responses.items() if len(str(v)) > 200]
                if long_entries:
                    print(f"✅ {lang.upper()}: Has {len(long_entries)} detailed guides ready for LLM")
                else:
                    print(f"⚠️  {lang.upper()}: No long-form content found - consider adding detailed guides")
                    
            except Exception as e:
                print(f"❌ {lang.upper()}: Error loading - {e}")
        else:
            print(f"❌ {lang.upper()}: File {file_path} not found")
    
    print("\n" + "="*50)
    print("🎯 SETUP INSTRUCTIONS:")
    print("1. Add OPENAI_API_KEY to your environment variables")
    print("2. Ensure your JSON has long-form content like:")
    print('   "mango_harvest": "Mangoes should be harvested when..."')
    print("3. Run the app - it will use LLM for detailed responses")
    print("="*50)

if __name__ == "__main__":
    main()