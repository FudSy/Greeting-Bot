import json

PHRASES_FILE = './static/phrases.json'

async def load_phrases():
    with open(PHRASES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

async def save_phrases(data):
    with open(PHRASES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)