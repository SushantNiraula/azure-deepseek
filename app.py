import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# 🎨 Set page layout
st.set_page_config(page_title="Azure AI Chatbot", layout="wide")

# Azure API Setup
if "AZURE_INFERENCE_CREDENTIAL" not in st.secrets:
    st.error("API key missing! Add it in Streamlit Secrets.")
    st.stop()

api_key = st.secrets["AZURE_INFERENCE_CREDENTIAL"]
endpoint = "https://DeepSeek-R1-sushant.eastus2.models.ai.azure.com"
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# 🔄 Session state initialization
if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {}
if "selected_chat" not in st.session_state:
    st.session_state["selected_chat"] = None

# 🎯 Sidebar - Chat History
with st.sidebar:
    st.title("📜 Chat History")

    # ➕ New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        chat_id = f"Chat {len(st.session_state['chat_sessions']) + 1}"
        st.session_state["chat_sessions"][chat_id] = []
        st.session_state["selected_chat"] = chat_id
        st.rerun()

    # 📂 File Upload
    uploaded_file = st.file_uploader("📁 Upload File", type=["txt", "pdf", "csv", "json"])

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

    # 🔘 Select Chat Session
    if st.session_state["chat_sessions"]:
        selected_chat = st.radio("Select a chat:", list(st.session_state["chat_sessions"].keys()))
        st.session_state["selected_chat"] = selected_chat
    else:
        st.session_state["selected_chat"] = None

# 🎯 Main Chat Interface
st.title("💬 Azure AI Chatbot - DeepSeek")

if st.session_state["selected_chat"]:
    chat_history = st.session_state["chat_sessions"][st.session_state["selected_chat"]]
else:
    chat_history = []

# 💬 Display Chat Messages
for msg in chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 📝 User Input Box (Fixed at Bottom)
user_input = st.chat_input("Type a message...")

if user_input:
    if st.session_state["selected_chat"] is None:
        st.warning("Start a new chat before sending messages.")
        st.stop()

    # Append user message
    chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Prepare API request
    payload = {"messages": chat_history, "max_tokens": 2048}

    # Generate AI Response
    try:
        response = client.complete(payload)

        if response and hasattr(response, "choices") and response.choices:
            ai_response = response.choices[0].message["content"]

            # Append AI response
            chat_history.append({"role": "assistant", "content": ai_response})
            with st.chat_message("assistant"):
                st.write(ai_response)

            # Update session state
            st.session_state["chat_sessions"][st.session_state["selected_chat"]] = chat_history

        else:
            st.error("No response received. Check API settings.")
    except Exception as e:
        st.error(f"API Error: {e}")
