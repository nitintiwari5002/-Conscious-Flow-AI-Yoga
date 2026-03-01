import streamlit as st

Home = st.Page("pages/Home.py", title = "Home")
Info = st.Page("pages/info.py", title = "Info")
About = st.Page("pages/About.py", title = "About")
Diet_Plan = st.Page("pages/Diet.py", title = "Diet Plan")
Yoga_Recommender = st.Page("pages/yoga_recommendation.py", title = "Yoga Recommender")
pg = st.navigation([Home , Info, About, Diet_Plan,Yoga_Recommender], position = "top")


pg.run()
