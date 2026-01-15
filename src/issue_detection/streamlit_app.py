import streamlit as st

from issue_detection.fetch_data import get_reviews

st.title('2GIS Organisation Reviews')

url = st.text_input('Enter 2GIS URL:')

organisation_id = url.split('/')[7][:17] if url else ''
st.write(f'Organisation ID: {organisation_id}')

if organisation_id:
    st.json(get_reviews(organisation_id=organisation_id))
    # st.write(test_function())