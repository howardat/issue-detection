import json
import numpy as np

def extract_negative(arr):
    cleaned_arr = []
    cleaned_arr = [item['text'] for item in arr if item['rating'] < 4]
    return cleaned_arr
    
if __name__ == '__main__':
    with open('../data/reviews.json', 'r') as f:
        data = json.load(f)
    arr = np.array(data)

    print(len(extract_negative(arr)))