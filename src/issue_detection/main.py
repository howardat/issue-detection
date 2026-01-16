import copy
import json

from fetch_data import get_reviews
from tag_generation import batch_processing

def main():
    data = get_reviews('70000001109579027')
    
    tags = batch_processing(data)

    data_with_tags = copy.deepcopy(data)
    for i, item in enumerate(data_with_tags):
        item['tags'] = tags[i]

    with open('../../tests/json/reviews_with_tags.json', 'w') as f:
        json.dump(data_with_tags, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()