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

# Ensure chat history exists in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages (before user input)
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user input to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Prepare payload for Azure API
    payload = {
        "messages": st.session_state["messages"],  # Send entire chat history
        "max_tokens": 2048
    }

    # Generate response (correct method call)
    try:
        response = client.complete(payload)  # ✅ Fixed method call

        if response and response.choices:
            ai_response = response.choices[0].message["content"]

            # Add AI response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": ai_response})
            st.chat_message("assistant").write(ai_response)
        else:
            st.error("No response received. Check API settings.")
    except AttributeError as e:
        st.error(f"API method issue: {e}. Ensure you have the correct SDK version.")
