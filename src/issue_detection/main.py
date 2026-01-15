import json
import numpy as np

from data_processing import extract_negative
from tag_generation import extract_tags
from visualization import visualize

OUTPUT_FILE = '../../tests/json/tags.json'

with open('../../data/reviews.json', 'r') as f:
    data = json.load(f)
arr = np.array(data)

negative_reviews = extract_negative(data)
sample_reviews = '\n\n'.join(sample_reviews)

tags = extract_tags(sample_reviews)

if tags.startswith("```json"):
    tags = tags[7:]  # Remove the first 7 characters
if tags.endswith("```"):
    tags = tags[:-3]  # Remove the last 3 characters

# Final trim to ensure no stray newlines remain
tags = tags.strip()

with open(OUTPUT_FILE, 'w') as f:
    f.write(tags)

visualize(OUTPUT_FILE)