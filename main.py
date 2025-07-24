# 1_Chat.py

import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- PAGE CONFIGURATION ---
# This command now reads its theme settings from the .streamlit/config.toml file
st.set_page_config(
    page_title="PDF Chat",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATA PROCESSING & CHAIN CREATION FUNCTIONS ---
def get_pdf_text(files):
    text = ""
    for pdf in files:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
        except Exception as e:
            st.error(f"Error reading {pdf.name}: {e}")
    return text

@st.cache_data
def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(raw_text)

def get_vectorstore(text_chunks):
    google_api_key = st.session_state.get("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("Google API Key is missing. Please set it on the 'API Keys' page.")
        return None
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_api_key)
        return FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    except Exception as e:
        st.error(f"Failed to create vector store: {e}")
        return None

def get_rag_chain(vectorstore):
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

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n\n{context}"),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    return create_retrieval_chain(history_aware_retriever, question_answer_chain)

# --- MAIN STREAMLIT APP ---
def main():
    st.header("Chat with Your Documents 💬")
    st.info("Upload documents and click 'Process' to start.")

    # Initialize session state
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask a question about your documents..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.rag_chain:
            with st.spinner("Thinking..."):
                chat_history = [HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]) for msg in st.session_state.messages[:-1]]
                result = st.session_state.rag_chain.invoke({"input": prompt, "chat_history": chat_history})
                response = result.get("answer", "Sorry, an error occurred.")
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Please upload and process your documents in the sidebar first.")

    # Sidebar for file upload and processing
    with st.sidebar:
        st.header("1. Document Upload")
        files = st.file_uploader('Upload PDFs here:', accept_multiple_files=True, type='pdf')
        
        st.header("2. Process Documents")
        if st.button('Process'):
            if not files:
                st.warning("Please upload at least one document.")
            elif not st.session_state.get("GOOGLE_API_KEY"):
                 st.error("Please go to the 'API Keys' page and set your Google API Key before processing.")
            else:
                with st.spinner('Processing documents... This may take a moment.'):
                    raw_text = get_pdf_text(files)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        vectorstore = get_vectorstore(text_chunks)
                        if vectorstore:
                            st.session_state.rag_chain = get_rag_chain(vectorstore)
                            st.success('Ready! Ask your questions in the main chat window.')
                    else:
                        st.error("Could not extract text from the PDF files.")

if __name__ == '__main__':
    main()