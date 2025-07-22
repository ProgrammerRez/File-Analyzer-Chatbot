import streamlit as st
from chat import prompt_from_file # Assuming your 'chat.py' is in the same directory
import os
import tempfile

def generate_main_page():
    st.title('File_Analyzer_Chatbot')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display prior chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # The chat_input widget is now used for text input only.
    # We will use st.file_uploader for handling file uploads.
    uploaded_file = st.file_uploader("Upload a file (.txt, .pdf, .csv)", type=['txt', 'pdf', 'csv'])
    user_text_prompt = st.chat_input('Ask a question about the uploaded file...')

    if uploaded_file and user_text_prompt:
        # To handle the uploaded file, it needs to be saved to a temporary location
        # so that your `prompt_from_file` function can access it by its path.
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        # Add user's message to the chat history
        st.session_state.messages.append({'role': 'user', 'content': user_text_prompt})
        with st.chat_message('user'):
            st.markdown(user_text_prompt)

        # Get the bot's response
        with st.spinner("Analyzing the file and generating a response..."):
            bot_response = prompt_from_file(file_path=tmp_file_path, user_prompt=user_text_prompt)

        # Add bot's response to the chat history and display it
        st.session_state.messages.append({'role': 'Chatbot', 'content': bot_response})
        with st.chat_message('assistant'):
            st.markdown(bot_response)

        # Clean up the temporary file
        os.remove(tmp_file_path)

if __name__ == '__main__':
    generate_main_page()