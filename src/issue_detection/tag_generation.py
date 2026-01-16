import ollama
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_FOLDER = BASE_DIR / "prompts"

def get_prompts(file_name):
    file_path = PROMPTS_FOLDER / file_name
    with open(file_path, 'r') as f:
        return f.read()

def generate_tags(data):
    inference = ollama.chat(model='gemma3:4b', messages=[
        {
            'role': 'system', 'content': get_prompts('tagger.txt')
        },
        {
            'role': 'user', 'content': data
        }
    ])
    return inference['message']['content']

def batch_processing(data):
    all_tags_list = []

    for i in range(0, len(data), 1):
        batch = data[i : i + 1]
        batch_content = [{"review": item.get('text', '')} for item in batch]
        
        clean_reviews = json.dumps(batch_content, ensure_ascii=False, indent=4)
        
        try:
            clean_response = generate_tags(clean_reviews).replace('```json', '').replace('```', '').strip()

            batch_data = json.loads(clean_response)  # Validate JSON
            all_tags_list.append(batch_data.get('tags', []))

        except json.JSONDecodeError as e:
            print(f"JSON decoding error for batch starting at index {i}: {e}")
        
    return all_tags_list
    
if __name__ == '__main__':
    batch_processing('../../tests/json/test.json')