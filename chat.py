from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from dotenv import load_dotenv
import os
import argparse
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
)

# --- Environment and API Key Setup ---
load_dotenv(dotenv_path='.env')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables or .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

# --- Initialize LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
)

def get_loader(file_path: str):
    """
    Returns the appropriate LangChain DocumentLoader based on the file extension.
    """
    if file_path.endswith(".txt"):
        return TextLoader(file_path)
    elif file_path.endswith(".pdf"):
        return PyPDFLoader(file_path)
    elif file_path.endswith(".csv"):
        return CSVLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def prompt_from_file(file_path: str, user_prompt: str = "Summarize the following document:"):
    """
    Loads a document from a file, combines its content with a user prompt,
    and sends it to the language model.
    """
    try:
        loader = get_loader(file_path)
        documents = loader.load()
        file_content = "\n".join([doc.page_content for doc in documents])
        
        full_prompt = f"{user_prompt}\n\n{file_content}"
        
        response = llm.invoke(full_prompt)
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"

def prompt_from_text(text: str):
    """
    Sends a text prompt to the language model.
    """
    if not isinstance(text, str):
        raise ValueError("Input to prompt() must be a string.")
    response = llm.invoke(text)
    return response.content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Interact with the Generative AI model.")
    parser.add_argument("--file", type=str, help="Path to a file to be processed.")
    parser.add_argument("--prompt", type=str, default="Summarize the following document:", help="The prompt to use with the file content.")
    parser.add_argument("--text", type=str, help="A direct text prompt to the model.")

    args = parser.parse_args()

    if args.file:
        print(prompt_from_file(args.file, args.prompt))
    elif args.text:
        print(prompt_from_text(args.text))
    else:
        print("Please provide either a file path with --file or a text prompt with --text.")