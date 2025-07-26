# pages/2_API_Keys.py

import streamlit as st
from dotenv import load_dotenv
import os

# --- Page Configuration ---
st.set_page_config(page_title="API Keys", page_icon="🔑")
st.title("🔑 API Key Management")

# --- Auto-loading from .env file ---
# This block runs once per session to automatically load keys from the .env file.
if "env_loaded" not in st.session_state:
    load_dotenv()  # Load environment variables from a .env file if it exists
    
    # List to keep track of which keys were loaded from the environment
    loaded_keys_messages = []

    # Check for and load Google API Key if not already in session state
    if "GOOGLE_API_KEY" not in st.session_state:
        google_key_from_env = os.getenv("GOOGLE_API_KEY")
        if google_key_from_env:
            st.session_state["GOOGLE_API_KEY"] = google_key_from_env
            loaded_keys_messages.append("Google AI API Key")

    # Check for and load Hugging Face Token if not already in session state
    if "HUGGINGFACEHUB_API_TOKEN" not in st.session_state:
        hf_token_from_env = os.getenv("HUGGINGFACEHUB_API_TOKEN")
        if hf_token_from_env:
            st.session_state["HUGGINGFACEHUB_API_TOKEN"] = hf_token_from_env
            loaded_keys_messages.append("Hugging Face Hub API Token")

    # Display a one-time message about the auto-loaded keys
    if loaded_keys_messages:
        st.success(f"Automatically loaded: **{', '.join(loaded_keys_messages)}** from your `.env` file.")
    
    # Set a flag to ensure this block doesn't run again in the same session
    st.session_state["env_loaded"] = True

# --- Main Page Content ---
st.info(
    "Your API keys are stored securely in your browser's session storage for this session only. "
    "They are not saved on any server."
)

# --- Google AI API Key Section ---
st.header("1. Google AI API Key")
st.markdown(
    "This is required for the application's core functionality."
    "\n\n"
    "You can get your free Google AI API key from **[Google AI Studio](https://aistudio.google.com/app/apikey)**."
)

# Input for the Google API key, pre-filled from session state
google_api_key = st.text_input(
    "Enter your Google AI API Key:",
    type="password",
    key="google_api_key_input",
    value=st.session_state.get("GOOGLE_API_KEY", "")
)

if st.button("Save Google Key"):
    st.session_state["GOOGLE_API_KEY"] = google_api_key
    st.success("Google AI API Key saved for this session.")


# --- Hugging Face Hub API Token Section ---
st.header("2. Hugging Face Hub API Token")
st.markdown(
    "This is optional. It's needed if you want to use models hosted on Hugging Face."
    "\n\n"
    "You can get your free Hugging Face Hub Token from **[your Hugging Face settings](https://huggingface.co/settings/tokens)**."
)

# Input for the Hugging Face token, pre-filled from session state
hugging_face_token = st.text_input(
    "Enter your Hugging Face Hub API Token:",
    type="password",
    key="hugging_face_token_input",
    value=st.session_state.get("HUGGINGFACEHUB_API_TOKEN", "")
)

if st.button("Save Hugging Face Token"):
    st.session_state["HUGGINGFACEHUB_API_TOKEN"] = hugging_face_token
    st.success("Hugging Face Token saved for this session.")


# --- Current Status Section ---
st.header("Current Status")
if st.session_state.get("GOOGLE_API_KEY"):
    st.success("✅ Google AI API Key is set.")
else:
    st.warning("❌ Google AI API Key is not set. The chat functionality will be disabled.")

if st.session_state.get("HUGGINGFACEHUB_API_TOKEN"):
    st.success("✅ Hugging Face Token is set.")
else:
    st.info("ℹ️ Hugging Face Token is not set (optional).")