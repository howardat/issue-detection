import requests
import json
from time import sleep

def get_reviews(organisation_id: str, offset: int = 0):
    URL = f'https://public-api.reviews.2gis.com/3.0/branches/{organisation_id}/reviews?fields=meta.providers%2Cmeta.branch_rating%2Cmeta.branch_reviews_count%2Cmeta.total_count%2Creviews.hiding_reason%2Creviews.emojis%2Creviews.trust_factors&is_advertiser=false&key=6e7e1929-4ea9-4a5d-8c05-d601860389bd&limit=50&locale=ru_KZ&offset={offset}&rated=true&sort_by=date_edited&without_my_first_review=false'

    response = requests.get(URL).json()

    review_count = response.get('meta', {}).get('total_count', 0)

    while offset + 50 < review_count:
        offset += 50
        next_url = f'https://public-api.reviews.2gis.com/3.0/branches/{organisation_id}/reviews?fields=meta.providers%2Cmeta.branch_rating%2Cmeta.branch_reviews_count%2Cmeta.total_count%2Creviews.hiding_reason%2Creviews.emojis%2Creviews.trust_factors&is_advertiser=false&key=6e7e1929-4ea9-4a5d-8c05-d601860389bd&limit=50&locale=ru_KZ&offset={offset}&rated=true&sort_by=date_edited&without_my_first_review=false'
        next_response = requests.get(next_url).json()
        response['reviews'].extend(next_response.get('reviews', []))
        sleep(0.5)  # To avoid hitting the API rate limit

    data = [{'text': r.get('text', []), 'date_created': r.get('date_created', [])} for r in response.get('reviews', [])]

    with open('/Users/oljk/Projects/issue-detection/tests/json/test.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data

if __name__ == "__main__":
    print("fetch_data.py is running")