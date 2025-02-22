import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Streamlit UI Config
st.set_page_config(page_title="Azure AI Chatbot", layout="wide")
st.title("💬 Azure AI Chatbot - DeepSeek")

# Get API key from Streamlit secrets
if "AZURE_INFERENCE_CREDENTIAL" not in st.secrets:
    st.error("API key missing! Add it in Streamlit Secrets.")
    st.stop()

api_key = st.secrets["AZURE_INFERENCE_CREDENTIAL"]
endpoint = "https://DeepSeek-R1-sushant.eastus2.models.ai.azure.com"

# Initialize Azure Chat Client
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# File upload section
uploaded_file = st.file_uploader("Upload a file (optional)", type=["txt", "pdf", "csv", "json"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Append user input to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Prepare payload for Azure API
    payload = {
        "messages": st.session_state["messages"],  # Send entire chat history
        "max_tokens": 2048
    }

    # Generate AI response using correct method
    try:
        response = client.complete(payload)  # ✅ Fixed API call

        if response and hasattr(response, "choices") and response.choices:
            ai_response = response.choices[0].message["content"]

            # Append AI response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": ai_response})
            st.chat_message("assistant").write(ai_response)
        else:
            st.error("No response received. Check API settings.")
    except Exception as e:
        st.error(f"API Error: {e}")
