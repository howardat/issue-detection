import copy
import streamlit as st
import re
import plotly.express as px

from fetch_data import get_reviews
from bar_chart import bar_chart
from tag_generation import batch_processing

st.title('2GIS Organisation Reviews')

url = st.text_input('Enter 2GIS URL:')

organisation_id = re.search(r'/firm/(\d{15,17})', url).group(1) if url else ''
st.write(f'Organisation ID: {organisation_id}')

if organisation_id:
    data = get_reviews(organisation_id=organisation_id)
    tags = batch_processing(data)

    data_with_tags = copy.deepcopy(data)
    for i, item in enumerate(data_with_tags):
        item['tags'] = tags[i]

    chart_data = bar_chart(data_with_tags)
    chart_data = chart_data.sort_values('month')

    fig = px.bar(
        chart_data, 
        x='month', 
        y='review_count', 
        color='tags',
        title="Negative Reviews",
        barmode='stack'
    )
    fig.update_xaxes(categoryorder='category ascending')
    st.plotly_chart(fig, use_container_width=True)

    st.json(data_with_tags)