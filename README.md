# 🤖 Advanced Document Chat

**Your personal AI analyst for any document. Ever wish you could just *talk* to your PDFs, CSVs, or code files? Now you can.**

This isn't just a chatbot; it's a multi-talented digital assistant that can read your documents and provide answers, generate expert-level analysis, or even help you write code based on the context you provide.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-green?style=for-the-badge&logo=langchain)](https://www.langchain.com/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_Pro-purple?style=for-the-badge&logo=google-gemini)](https://ai.google.dev/)

## 🚀 Live Demo

Don't just take our word for it. Deploy your own personal analyst with a single click.

### [➡️ Click Here to Launch the Live App ⬅️](https://fileanalyzerproject.streamlit.app/)

Watch as you upload a complex document, switch the AI's persona to "Expert Analysis," and get insights you never knew were hiding in your files.

![Demo GIF](https://i.imgur.com/REPLACE_WITH_YOUR_GIF.gif) 
*Pro-Tip: Create a GIF showing a user uploading a PDF, selecting 'Expert Analysis', and asking a complex question to showcase the app's power.*

---

## 🤔 What Does This Thing Actually Do?

This application is a powerful **Retrieval-Augmented Generation (RAG)** tool that lets you have an intelligent conversation with your documents. It's built to be robust, intuitive, and smart about its context.

### Key Features:

*   **📚 Multi-Format Document Support:** Upload and analyze a wide range of files, including:
    *   **PDFs:** Extract text from reports, papers, and books.
    *   **CSVs:** Analyze data tables and spreadsheets.
    *   **TXT & Code Files:** Chat with plain text files or your own source code (`.py`, `.js`, `.java`, etc.).

*   **🎭 Selectable AI Personas (Analysis Modes):** Command the AI to adopt a specific role for tailored responses:
    *   **Question Answering:** For quick, concise answers directly from the text.
    *   **Expert Analysis:** For in-depth insights, theme identification, and pattern recognition.
    *   **Code Generation:** For a senior software engineer to help you write, refactor, or explain code from the documents.

*   **🧠 Smart Context Management:** This is the secret sauce for reliability. The app is designed to prevent confusion:
    *   **Hard Resets:** Clicking "Process" starts a completely fresh session, clearing old chat history and document knowledge.
    *   **Context Invalidation:** If you change the uploaded files *after* processing, the app intelligently detects the mismatch, disables the chat, and prompts you to re-process. No more asking an AI about a document it no longer has!

---

## ⚙️ How It Works (The Technical Wizardry)

The app follows a clear, powerful workflow powered by Streamlit, LangChain, and Google's Gemini Pro.

1.  **Upload & Configure:** The user uploads one or more files via the Streamlit sidebar and chooses an "Analysis Mode."

2.  **Process & Vectorize:** When the "Process" button is hit:
    *   **Text Extraction:** The app uses libraries like `PyPDF2` and `Pandas` to extract raw text from the uploaded files.
    *   **Chunking:** The raw text is broken down into smaller, manageable chunks using `CharacterTextSplitter`.
    *   **Embedding & Storing:** Google's `GoogleGenerativeAIEmbeddings` model converts these text chunks into numerical vectors. These vectors are then stored in a `FAISS` vector store, which acts as a super-fast, searchable knowledge base for the documents.

3.  **The Conversational RAG Chain:** This is where the conversation happens.
    *   A **History-Aware Retriever** first looks at the new question and the chat history. It reformulates the user's latest question to be a standalone query, making it understandable without the full conversation context.
    *   The reformulated question is used to retrieve the most relevant document chunks from the `FAISS` vector store.
    *   A **Stuff Documents Chain** then "stuffs" these retrieved chunks, along with the chat history and the question, into a dynamically selected prompt template based on the chosen "Analysis Mode."
    *   Finally, the `gemini-1.5-pro` LLM generates a response based on this rich context.

4.  **Context Invalidation Logic:** On every user interaction, the app compares the IDs of the currently uploaded files with the IDs of the files that were processed. If they don't match, the RAG chain is immediately disabled to ensure the AI's knowledge is never out of sync with the user's expectations.

---

## 🛠️ How to Run This Marvel of Engineering

Want to get this running on your own machine? Easy.

1.  **Clone the Sacred Texts:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Set Up Your Environment:**
    A virtual environment is a sign of a true professional.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Provide the Secret Sauce (API Key):**
    The app's brain (Google Gemini) needs an API key to function.
    *   Create a file named `.env` in the root directory.
    *   Inside `.env`, add the following line:
        ```
        GOOGLE_API_KEY="your_super_secret_api_key_here"
        ```

4.  **LIFTOFF!**
    Run the Streamlit application from your terminal:
    ```bash
    streamlit run main.py
    ```
    Your browser will open with your very own document analyst, ready for duty.

---

### **Disclaimer**
This is a powerful demonstration application. While the analysis can be incredibly insightful, always use it as a co-pilot, not an autopilot. Verify critical information before making any important decisions.
