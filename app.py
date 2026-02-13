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
**Before clicking the button:**

In n8n (http://localhost:5678):
1. Open your workflow
2. Click the **"Execute Workflow"** button on the Webhook trigger node (blue button on canvas)
3. Immediately come back and click the button below

OR activate the workflow:
- Click the **"Activate"** toggle (top-right) to make it always available
""")




if st.button("Analyze Sentiments", key="as", type="primary"):
    try:
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
