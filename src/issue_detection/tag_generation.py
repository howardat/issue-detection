import ollama
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_FOLDER = BASE_DIR / "prompts"

def get_prompts(file_name):
    file_path = PROMPTS_FOLDER / file_name
    with open(file_path, 'r') as f:
        return f.read()

def extract_tags(data):
    inference = ollama.chat(model='gemma3:4b', messages=[
        {
            'role': 'system', 'content': get_prompts('tagger.txt')
        },
        {
            'role': 'user', 'content': data
        }
    ])
    return inference['message']['content']

if __name__ == '__main__':
    response = 'hey'
    print(response['message']['content'])