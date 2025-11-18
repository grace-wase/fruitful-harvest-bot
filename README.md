# Fruitful Harvest - Farmer Teaching Bot

## Setup
1. Install Python 3.7+
2. Run: `pip install -r requirements.txt`
3. Start application:
   - **Desktop mode**: `python app.py`
   - **Web mode**: 
     ```bash
     export FLASK_APP=app.py
     flask run
     ```

## Adding New Languages
1. Create new folder in `data/lessons/` (use ISO 639-1 code, e.g. `fr` for French)
2. Add translated JSON files for each fruit
3. Update language names in `config.py`

## Adding New Fruits
1. Create JSON files in all language folders
2. Add to fruit selector in `chat.html`