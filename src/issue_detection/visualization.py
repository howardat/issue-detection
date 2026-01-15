import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

# 1. Load data
def visualize(output_path):

    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Count pairs
    pair_counts = Counter()
    unique_tags = set()

    for item in data:
        tags = item.get('tags', [])
        unique_tags.update(tags)
        # Get all combinations of 2 tags within one review
        for pair in combinations(sorted(tags), 2):
            pair_counts[pair] += 1

    # 3. Create an empty DataFrame (Matrix)
    tags_list = sorted(list(unique_tags))
    matrix = pd.DataFrame(0, index=tags_list, columns=tags_list)

    # 4. Fill the matrix
    for (tag1, tag2), count in pair_counts.items():
        matrix.loc[tag1, tag2] = count
        matrix.loc[tag2, tag1] = count  # Mirror it for a full heatmap

    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, cmap="YlGnBu", cbar=True)

    plt.title('Tag Co-occurrence Heatmap\n(Which issues happen together?)')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    INPUT_FILE = '../../tests/json/tags.json'

    def generate_combined_report(json_path):
        # 1. Load and parse data
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_tags = []
        pair_counts = Counter()
        
        for item in data:
            tags = item.get('tags', [])
            # Normalization: Ensure tags is a list
            if isinstance(tags, str): 
                tags = [tags]
            
            all_tags.extend(tags)
            
            # Get unique pairs for co-occurrence
            unique_item_tags = sorted(list(set(tags)))
            for pair in combinations(unique_item_tags, 2):
                pair_counts[pair] += 1

        if not all_tags:
            print("No data found.")
            return

        # 2. Data Preparation for Frequency
        tag_counts = Counter(all_tags)
        df_freq = pd.DataFrame(tag_counts.items(), columns=['Topic', 'Mentions']).sort_values('Mentions', ascending=False)

        # 3. Data Preparation for Heatmap
        unique_tags = sorted(list(set(all_tags)))
        matrix = pd.DataFrame(0, index=unique_tags, columns=unique_tags)
        for (t1, t2), count in pair_counts.items():
            matrix.loc[t1, t2] = count
            matrix.loc[t2, t1] = count

        # 4. Create Figure with 2 Subplots (1 row, 2 columns)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # --- Left: Frequency Bar Chart ---
        sns.barplot(x='Mentions', y='Topic', data=df_freq, palette='viridis', ax=ax1)
        ax1.set_title('Frequency: Which issues are most common?', fontsize=16, pad=20)
        ax1.grid(axis='x', linestyle='--', alpha=0.6)
        # Add number labels to bars
        for i in ax1.containers:
            ax1.bar_label(i, padding=5, fontsize=12)

        # --- Right: Co-occurrence Heatmap ---
        sns.heatmap(matrix, annot=True, cmap='YlGnBu', fmt='d', cbar=True, square=True, ax=ax2)
        ax2.set_title('Correlation: Which issues happen together?', fontsize=16, pad=20)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

        # Final layout adjustments
        plt.suptitle(f'Customer Complaint Analysis (Sample Size: {len(data)})', fontsize=20, y=1.05)
        plt.show()

    generate_combined_report(INPUT_FILE)