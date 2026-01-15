**Why am I making this project?**
It is a personal project that should get me a job. Also, I want to learn to create end-to-end ML projects and learn NLP.

**Who is this project for?**
This project is for AI integrators and sales directors or other managers who possess big piles of user feedback data and they want to get insights from this data.

**What is going to make it valuable?**
I believe that getting insights from user feedback data can help in business decision making. So since the goal of my project is to find a cutting-edge of insight extraction this should be valuable.

**MVP DRAFT**
Functional Requierments:

User story:

- As a User, I want to get a trends of reviews from 2GIS organisation
- Display of dynamics of quantity of negative reviews in monthly intervals
- Filter by topics/tags

Technical tasks:

1. Fetch data from 2GIS

   - Data fetcher pipline
   - Preprocess and filter data (keep time stamps, text, rating)
   - Filter by rating

2. Assign tags to each review

   - Batch processing (?)

3. Create charts

   - Bar chart
   - Tag filter

4. Display charts

   - Streamlit

5. Deploy using Streamlit
