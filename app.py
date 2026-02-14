import streamlit as st
import requests
import json
from datetime import datetime
import os
import urllib3
# Page configuration

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
st.set_page_config(
    page_title="sentiment analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Main content area
st.title("Sentiment analysis tool")
st.markdown("Manage and execute n8n workflow for sentiment analysis directly from Streamlit")
st.markdown("---")

st.subheader("Execute Workflow via Webhook")

# Quick Execute Button
st.markdown("**Quick Execute**")

st.warning("""
Activate the workflow:
- Click the **"Analyze Sentiments"** toggle (top-right) to make it always available
""")



user_input = st.text_input("Enter company you want to find sentiment of:", placeholder="Type here...")
if st.button("Analyze Sentiments", key="as", type="primary"):
    try:
        if not user_input:
            raise ValueError("input must not be empty")
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            "http://marna-petroleous-tenley.ngrok-free.dev/webhook/c8615654-34f3-400a-a4e4-db90161dda20"
            , json={"data": '5'})
            
        if response.status_code in [200, 201]:
            st.success("Webhook activated successfully!")
            try:
                st.json(response.json())
            except:
                st.write(response.text)
        else:
            st.error(f"Failed: {response.status_code}")
            st.write(response.text)
    except requests.exceptions.ConnectionError as e:
        st.error(e)
        st.warning("""
        **n8n is inactive**
        """)
    except Exception as e:
        st.error(f"Error: {str(e)}")


st.markdown("---")
