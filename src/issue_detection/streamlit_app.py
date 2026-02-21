import streamlit as st
import pandas as pd
import json
from fetch_data import get_reviews
from tag_generation import batch_processing

st.set_page_config(page_title="Issue Detector", layout="wide")
st.title("🎫 Ticket Issue Detection")

# 1. Load Data
# Use .empty check instead of 'if df'
df = get_reviews('../../data/tickets.csv')


with st.status("Processing tags... this may take a moment") as status:
    # 2. Process Tags
    tags_list = batch_processing(df)
    
    # 3. Create the combined DataFrame
    df_result = df.copy()
    
    # Ensure length matches before assignment
    if len(tags_list) == len(df_result):
        df_result['tags'] = tags_list
    else:
        st.error(f"Mismatch: {len(df_result)} reviews vs {len(tags_list)} tags.")
        df_result['tags'] = [[] for _ in range(len(df_result))]
        
    status.update(label="Processing complete!", state="complete")

# 4. Display Logic
st.subheader("Analysis Results")
st.dataframe(df_result, use_container_width=True)

# 5. Native Python Conversion for st.json
try:
    # to_json handles complex types better than to_dict
    raw_json_str = df_result.to_json(orient='records', force_ascii=False)
    clean_json_data = json.loads(raw_json_str)

    with st.expander("🔍 View Raw JSON Data"):
        st.json(clean_json_data)
        
except Exception as e:
    st.error(f"JSON Display Error: {e}")
else:
    st.info("Waiting for data... Please check if '../../data/tickets.csv' exists.")