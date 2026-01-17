import copy
import streamlit as st
import re

from fetch_data import get_reviews
from tag_generation import batch_processing

st.title('2GIS Organisation Reviews')

url = st.text_input('Enter 2GIS URL:')

organisation_id = re.search(r'(/firm/\d{15,17})', url).group(1) if url else ''
st.write(f'Organisation ID: {organisation_id}')

if organisation_id:
    data = get_reviews(organisation_id=organisation_id)
    tags = batch_processing(data)

    data_with_tags = copy.deepcopy(data)
    for i, item in enumerate(data_with_tags):
        item['tags'] = tags[i]

    st.json(data_with_tags)

    st.bar_chart(data_with_tags, x='date_created', y='tags')