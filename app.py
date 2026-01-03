import streamlit as st

Home = st.Page("pages/Home.py", title = "Home")
Info = st.Page("pages/Info.py", title = "Info")
About = st.Page("pages/About.py", title = "About")
Diet_Plan = st.Page("pages/Diet.py", title = "Diet Plan")
pg = st.navigation([Home , Info, About, Diet_Plan], position = "top")

pg.run()