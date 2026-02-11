import streamlit as st
import requests
import json
from datetime import datetime
import os



# Page configuration
st.set_page_config(
    page_title="n8n Workflow Manager",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
with st.sidebar:
    st.title("🔗 Webhook Manager")
    st.markdown("---")
    
    # Webhook Configuration
    st.subheader("Webhook Settings")
    webhook_base_url = st.text_input(
        "Webhook Base URL",
        value=os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook"),
        key="webhook_base_url",
        help="Base URL for webhook triggers (e.g., http://localhost:5678/webhook)"
    )
    
    # Test connection button
    if st.button("Test n8n Connection", key="test_conn"):
        try:
            # Test by trying to access health endpoint
            n8n_instance = webhook_base_url.replace("/webhook", "").replace("/webhook-test", "")
            response = requests.get(
                f"{n8n_instance}/health",
                timeout=5
            )
            if response.status_code == 200:
                st.success("✅ Connected to n8n successfully!")
            else:
                st.error(f"❌ Connection failed: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Make sure n8n is running and the webhook URL is correct.")


# Main content area
st.title("🚀 n8n Workflow Manager")
st.markdown("Manage and execute n8n workflows directly from Streamlit")
st.markdown("---")

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Workflows", 
    "▶️ Execute Workflow", 
    "📊 Executions", 
    "⚙️ Settings"
])

# Tab 1: List Workflows
with tab1:
    st.subheader("Webhook Execution Guide")
    
    st.info("""
    📌 **Webhook-Based Execution**
    
    To execute workflows, you need their webhook URLs from n8n:
    
    1. Open your workflow in n8n
    2. Find the **Webhook** trigger node
    3. Copy the webhook URL (looks like: `/webhook/xxxx-xxxx-xxxx`)
    4. Paste it in the **Execute Workflow** tab
    5. Send JSON data to trigger it
    
    **Example Webhook URL:**
    ```
    http://localhost:5678/webhook/79ff58c5-a7d9-4d7a-8338-8be46dffdbba
    ```
    """)
    
    st.markdown("---")
    st.subheader("Quick Reference")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Webhook Types:**")
        st.write("- 🔗 Regular: `/webhook/ID`")
        st.write("- 🧪 Test: `/webhook-test/ID`")
    
    with col2:
        st.write("**Common Endpoints:**")
        st.write(f"- Base: {webhook_base_url}")
        st.write("- Health: Check n8n running status")


# Tab 2: Execute Workflow
with tab2:
    st.subheader("▶️ Execute Workflow via Webhook")
    
    # Quick Execute Button
    st.markdown("**⚡ Quick Execute**")
    
    st.warning("""
    ⚠️ **Before clicking the button:**
    
    In n8n (http://localhost:5678):
    1. Open your workflow
    2. Click the **"Execute Workflow"** button on the Webhook trigger node (blue button on canvas)
    3. Immediately come back and click the button below
    
    OR activate the workflow:
    - Click the **"Activate"** toggle (top-right) to make it always available
    """)
    
    

    
    if st.button("▶️ Activate Webhook", key="quick_execute_btn", type="primary"):
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                "http://localhost:5678/webhook/c8615654-34f3-400a-a4e4-db90161dda20"
                , json={"data": '5'})
                
            if response.status_code in [200, 201]:
                st.success("✅ Webhook activated successfully!")
                try:
                    st.json(response.json())
                except:
                    st.write(response.text)
            else:
                st.error(f"❌ Failed: {response.status_code}")
                st.write(response.text)
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to n8n at localhost:5678")
            st.warning("""
            **n8n is not running!**
                
            Start it with:
            ```bash
            docker-compose up -d n8n
            ```
                
            Or access it at: http://localhost:5678 (once running)
            """)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    
    st.markdown("---")
    


# Tab 3: Webhook History
with tab3:
    st.subheader("📝 Webhook History")
    
    st.info("""
    **Webhook Execution Logs**
    
    The responses from your recent webhook executions appear above when you execute workflows.
    
    **Tips:**
    - Copy webhook URLs directly from your n8n workflow
    - Test webhooks with simple JSON first: `{}`
    - Check n8n logs if execution fails
    - Ensure webhook trigger is activated in n8n
    """)

# Tab 4: Settings
with tab4:
    st.subheader("⚙️ Settings & Documentation")
    
    st.write("**Webhook Configuration:**")
    st.write(f"Base URL: `{webhook_base_url}`")
    
    st.markdown("---")
    st.subheader("🚀 How to Execute Workflows")
    st.markdown("""
    ### 1. Find Your Webhook URL
    
    In n8n:
    - Open your workflow
    - Add a **Webhook** trigger node
    - Copy the webhook URL (looks like `/webhook/xxxxx-xxxxx-xxxxx`)
    - Full URL: `http://localhost:5678/webhook/xxxxx-xxxxx-xxxxx`
    
    ### 2. Execute from Streamlit
    
    - Go to **▶️ Execute Workflow** tab
    - Paste your webhook URL
    - Add JSON input data (optional)
    - Click **Execute Workflow**
    
    ### 3. View Response
    
    - See immediate response from n8n
    - Response data displayed as JSON
    
    **Example Workflow URL:**
    ```
    http://localhost:5678/webhook/79ff58c5-a7d9-4d7a-8338-8be46dffdbba
    ```
    """)
    
    st.markdown("---")
    st.subheader("📚 Getting Started with n8n")
    st.markdown("""
    **Start n8n with Docker:**
    ```bash
    docker-compose up n8n
    ```
    
    **Access n8n:** http://localhost:5678
    
    **Create a Workflow:**
    1. Click "+ New"
    2. Add a Webhook trigger
    3. Add nodes to process data
    4. Activate the workflow
    5. Copy the webhook URL
    6. Use it in this app!
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center'><small>n8n Webhook Manager | Powered by Streamlit</small></div>",
    unsafe_allow_html=True
)
