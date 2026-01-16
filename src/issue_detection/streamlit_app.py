import copy
import streamlit as st

from issue_detection.fetch_data import get_reviews
from issue_detection.tag_generation import batch_processing

st.title('2GIS Organisation Reviews')

url = st.text_input('Enter 2GIS URL:')

organisation_id = url.split('/')[7][:17] if url else ''
st.write(f'Organisation ID: {organisation_id}')

if organisation_id:
    data = get_reviews(organisation_id=organisation_id)
    tags = batch_processing(data)

    data_with_tags = copy.deepcopy(data)
    for i, item in enumerate(data_with_tags):
        item['tags'] = tags[i]

    st.json(data_with_tags)
    # st.write(test_function())
