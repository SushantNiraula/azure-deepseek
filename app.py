import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Streamlit UI Config
st.set_page_config(page_title="Azure AI Chatbot", layout="wide")

# Sidebar - Chat History
st.sidebar.title("📜 Chat History")

# Initialize chat history in session state
if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {}

# Allow user to select a chat session
selected_chat = st.sidebar.selectbox("Select a chat:", list(st.session_state["chat_sessions"].keys()), index=0 if st.session_state["chat_sessions"] else None)

# New Chat Button
if st.sidebar.button("➕ New Chat"):
    chat_id = f"Chat {len(st.session_state['chat_sessions']) + 1}"
    st.session_state["chat_sessions"][chat_id] = []
    st.experimental_rerun()

# Load selected chat session
if selected_chat:
    st.session_state["messages"] = st.session_state["chat_sessions"][selected_chat]
else:
    st.session_state["messages"] = []

# File Upload
st.sidebar.title("📁 File Upload")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf", "csv", "json"])
if uploaded_file:
    st.sidebar.success(f"Uploaded: {uploaded_file.name}")

# Main Chat Interface
st.title("💬 Azure AI Chatbot - DeepSeek")

# Azure API Setup
if "AZURE_INFERENCE_CREDENTIAL" not in st.secrets:
    st.error("API key missing! Add it in Streamlit Secrets.")
    st.stop()

api_key = st.secrets["AZURE_INFERENCE_CREDENTIAL"]
endpoint = "https://DeepSeek-R1-sushant.eastus2.models.ai.azure.com"
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Display chat history
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Append user input to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Prepare API request payload
    payload = {
        "messages": st.session_state["messages"],
        "max_tokens": 2048
    }

    # Generate AI response
    try:
        response = client.complete(payload)  # ✅ Fixed API call

        if response and hasattr(response, "choices") and response.choices:
            ai_response = response.choices[0].message["content"]

            # Append AI response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": ai_response})
            st.chat_message("assistant").write(ai_response)

            # Save chat session
            st.session_state["chat_sessions"][selected_chat] = st.session_state["messages"]

        else:
            st.error("No response received. Check API settings.")
    except Exception as e:
        st.error(f"API Error: {e}")
