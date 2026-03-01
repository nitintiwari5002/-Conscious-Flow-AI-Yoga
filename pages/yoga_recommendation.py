import streamlit as st
from utils.ollama_client import pose_predictor

a = st.text_input("Enter your problems to find the desired yoga pose...")
pose_predictor(a)
