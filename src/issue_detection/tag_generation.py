import ollama
from pathlib import Path
import json
import pandas as pd
import time

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_FOLDER = BASE_DIR / "prompts"

def get_prompts(file_name):
    file_path = PROMPTS_FOLDER / file_name
    with open(file_path, 'r') as f:
        return f.read()

def generate_tags(data):
    inference = ollama.chat(model='gemma3:4b', messages=[
        {
            'role': 'system', 'content': get_prompts('sentiment.txt')
        },
        {
            'role': 'user', 'content': data
        }
    ])
    return inference['message']['content']

def batch_processing(data):
    # Check if data is a path (string) and load it if necessary
    if isinstance(data, str):
        if data.endswith('.json'):
            data = pd.read_json(data)
        elif data.endswith('.csv'):
            data = pd.read_csv(data)

    all_tags_list = []
    reviews = data['Описание'].tolist() if isinstance(data, pd.DataFrame) else data.tolist()

    total_start_time = time.perf_counter() # Start total timer

    for i, text in enumerate(reviews):
        batch_content = [{"review": text}]
        clean_reviews = json.dumps(batch_content, ensure_ascii=False, indent=4)
        
        print(f"🔄 Processing review {i+1}/{len(reviews)}...")
        
        query_start_time = time.perf_counter() # Start per-query timer
        
        try:
            response_text = generate_tags(clean_reviews)
            
            # Calculate duration
            query_duration = time.perf_counter() - query_start_time
            print(f"⏱️ Query took: {query_duration:.2f} seconds")

            clean_response = response_text.replace('```json', '').replace('```', '').strip()
            batch_data = json.loads(clean_response) 
            all_tags_list.append(batch_data.get('tags', []))

        except Exception as e:
            print(f"❌ Error at index {i}: {e}")
            all_tags_list.append([])
        
    total_duration = time.perf_counter() - total_start_time
    print(f"\n✅ Total processing time: {total_duration:.2f} seconds")
    print(f"📊 Average speed: {total_duration/len(reviews):.2f}s per review")
        
    return all_tags_list

if __name__ == '__main__':
    # Make sure to pass a DataFrame or Series, not just the path string
    test_data = pd.Series(["The service was great!", "I hate this product."])
    batch_processing(test_data)