# pages/2_API_Keys.py

import streamlit as st

st.set_page_config(page_title="API Keys", page_icon="🔑")

st.title("🔑 API Key Management")
st.info(
    "Your API keys are stored securely in your browser's session storage and are required for the app to function. "
    "They are not saved on any server."
)

st.header("1. Google AI API Key")
st.markdown(
    "This is required for generating the text embeddings."
    "\n\n"
    "You can get your free Google AI API key from **[Google AI Studio](https://aistudio.google.com/app/apikey)**."
)

# Input for the Google API key
google_api_key = st.text_input(
    "Enter your Google AI API Key:",
    type="password",
    key="google_api_key_input",
    # Pull from session_state to pre-fill the input
    value=st.session_state.get("GOOGLE_API_KEY", "")
)

if st.button("Save Google Key"):
    st.session_state["GOOGLE_API_KEY"] = google_api_key
    st.success("Google AI API Key saved for this session.")


st.header("2. Hugging Face Hub API Token")
st.markdown(
    "This is optional. It's needed if you want to use models hosted on Hugging Face instead of Google Gemini."
    "\n\n"
    "You can get your free Hugging Face Hub Token from **[your Hugging Face settings](https://huggingface.co/settings/tokens)**."
)

# Input for the Hugging Face token
hugging_face_token = st.text_input(
    "Enter your Hugging Face Hub API Token:",
    type="password",
    key="hugging_face_token_input",
    value=st.session_state.get("HUGGINGFACEHUB_API_TOKEN", "")
)

if st.button("Save Hugging Face Token"):
    st.session_state["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_token
    st.success("Hugging Face Token saved for this session.")


# Display current status of the keys
st.header("Current Status")
if st.session_state.get("GOOGLE_API_KEY"):
    st.success("✅ Google AI API Key is set.")
else:
    st.warning("❌ Google AI API Key is not set. The chat functionality will be disabled.")

if st.session_state.get("HUGGINGFACEHUB_API_TOKEN"):
    st.success("✅ Hugging Face Token is set.")
else:
    st.info("ℹ️ Hugging Face Token is not set (optional).")