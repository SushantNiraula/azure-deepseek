import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

# Streamlit UI Config
st.set_page_config(page_title="Azure AI Chatbot", layout="centered")
st.title("💬 Azure AI Chatbot")

# Get API key from Streamlit secrets
if "AZURE_INFERENCE_CREDENTIAL" not in st.secrets:
    st.error("API key not found! Add it in Streamlit Secrets.")
    st.stop()

api_key = st.secrets["AZURE_INFERENCE_CREDENTIAL"]
endpoint = "https://DeepSeek-R1-sushant.eastus2.models.ai.azure.com"

# Initialize Azure Chat Client
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

# Store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Generate response
    response = client.get_chat_completions(
        messages=st.session_state["messages"], max_tokens=2048
    )

    if response and response.choices:
        ai_response = response.choices[0].message["content"]
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").write(ai_response)
    else:
        st.error("No response received. Check API settings.")
