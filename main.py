# main.py (Original Code + New Context Management Features)

import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import io
import nest_asyncio

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Advanced Document Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATA PROCESSING & CHAIN CREATION FUNCTIONS ---
# (These functions are identical to your original code)
def get_files_text(files, file_type):
    text = ""
    for file in files:
        try:
            if file_type == 'PDF':
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text
            elif file_type == 'CSV':
                df = pd.read_csv(file)
                text += df.to_string()
            elif file_type in ['TXT', 'Programming Files']:
                stringio = io.StringIO(file.getvalue().decode("utf-8"))
                text += stringio.read()
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")
    return text

@st.cache_data
def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(raw_text)

@st.cache_resource
def get_vectorstore(_text_chunks):
    google_api_key = st.session_state.get("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("Google API Key is missing. Please set it on the 'API Keys' page.")
        return None
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
        return FAISS.from_texts(texts=_text_chunks, embedding=embeddings)
    except Exception as e:
        if "event loop" in str(e):
            st.error(f"Failed to create vector store due to an asyncio conflict: {e}")
        else:
            st.error(f"Failed to create vector store: {e}")
        return None

def get_rag_chain(vectorstore, analysis_mode):
    google_api_key = st.session_state.get("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("Google API Key is missing. Please set it on the 'API Keys' page.")
        return None
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=google_api_key, convert_system_message_to_human=True)
    retriever = vectorstore.as_retriever()
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", "Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    prompts = {
        "Question Answering": "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n\n{context}",
        "Expert Analysis": "You are an expert analyst. Provide a detailed and insightful analysis of the document based on the user's query. Go beyond the surface-level information and identify key themes, patterns, or implications from the provided context.\n\n{context}",
        "Code Generation": "You are a senior software engineer and coding assistant. Based on the provided code or context, help the user write, refactor, or explain code. Provide clean, efficient, and well-documented code snippets as requested.\n\n{context}"
    }
    system_prompt = prompts.get(analysis_mode, prompts["Question Answering"])
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    return create_retrieval_chain(history_aware_retriever, question_answer_chain)

# --- MAIN STREAMLIT APP ---
def main():
    nest_asyncio.apply()
    
    st.header("Chat with Your Documents 💬")
    st.info("Upload your documents, select the file type and analysis mode, then click 'Process'.")

    # Initialize session state (add `processed_files` for new logic)
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []

    # Sidebar for file upload and processing
    with st.sidebar:
        st.header("1. Document Setup")
        file_type = st.selectbox('Select file type:', ('PDF', 'CSV', 'TXT', 'Programming Files'))
        accept_types = {'PDF': ['pdf'], 'CSV': ['csv'], 'TXT': ['txt'], 'Programming Files': ['py', 'java', 'js', 'html', 'css', 'cpp', 'c', 'go', 'rb', 'php', 'swift']}.get(file_type, [])
        files = st.file_uploader(f'Upload {file_type} files here:', accept_multiple_files=True, type=accept_types)
        
        st.header("2. Analysis Mode")
        analysis_mode = st.radio("Choose the AI's role:", ("Question Answering", "Expert Analysis", "Code Generation"), key="analysis_mode_selector")
        
        if st.session_state.vectorstore:
            st.session_state.rag_chain = get_rag_chain(st.session_state.vectorstore, analysis_mode)

        st.header("3. Process Documents")
        if st.button('Process'):
            if not files:
                st.warning("Please upload at least one document.")
            elif not st.session_state.get("GOOGLE_API_KEY"):
                st.error("Please go to the 'API Keys' page and set your Google API Key before processing.")
            else:
                with st.spinner('Processing documents... This will start a new session.'):
                    # --- ADDITION 1: HARD RESET ON PROCESS ---
                    # Clear chat history, caches, and existing context
                    st.session_state.messages = []
                    st.cache_data.clear()
                    st.cache_resource.clear()

                    raw_text = get_files_text(files, file_type)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        st.session_state.vectorstore = get_vectorstore(text_chunks)
                        if st.session_state.vectorstore:
                            st.session_state.rag_chain = get_rag_chain(st.session_state.vectorstore, analysis_mode)
                            # Store the list of successfully processed files
                            st.session_state.processed_files = files 
                            st.success('Ready! Ask your questions in the main chat window.')
                            st.rerun() # Force a rerun to show the cleared chat immediately
                    else:
                        st.error("Could not extract text from the uploaded files.")

    # --- ADDITION 2: CONTEXT INVALIDATION LOGIC ---
    # Placed in the main app body to check on every interaction
    current_file_ids = {f.file_id for f in files}
    processed_file_ids = {f.file_id for f in st.session_state.processed_files}

    if st.session_state.rag_chain is not None and current_file_ids != processed_file_ids:
        st.warning("⚠️ The file list has changed. Please click 'Process' to start a new session with the current files.")
        st.session_state.rag_chain = None
        st.session_state.vectorstore = None
        st.session_state.processed_files = []
    # --- END OF ADDITIONS ---

    # Display chat history (Original code)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input (Original code)
    if prompt := st.chat_input("Ask a question, request code, or ask for analysis..."):
        # Check for rag_chain again in case it was invalidated
        if st.session_state.rag_chain:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Thinking..."):
                chat_history = [HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]) for msg in st.session_state.messages[:-1]]
                result = st.session_state.rag_chain.invoke({"input": prompt, "chat_history": chat_history})
                response = result.get("answer", "Sorry, an error occurred.")
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Please upload and process your documents in the sidebar first.")

if __name__ == '__main__':
    main()