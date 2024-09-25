import streamlit as st
import openai
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import PyPDF2
import os

# OpenAI API Key
openai.api_key = 'your_openai_key'

def initialize_chroma_db():
    # Check if the vectorDB is already stored in session state
    if 'Lab4_vectorDB' not in st.session_state:
        # Setting up ChromaDB
        client = chromadb.Client(Settings(allow_reset=True))
        
        # Create a collection
        collection = client.create_collection("Lab4Collection")

        # Load all PDFs and extract text
        pdf_files = ['IST736-Text-Mining-Syllabus.pdf', 'IST691 Deep Learning in Practice Syllabus.pdf', 
                     'IST614 Info tech Mgmt & Policy Syllabus.pdf', 'IST 652 Syllabus.pdf', 
                     'IST688-BuildingHC-AIAppsV2.pdf', 'IST 644 Syllabus.pdf', 'IST 782 Syllabus.pdf']

        for pdf in pdf_files:
            # Extract text from PDF
            text = extract_text_from_pdf(f"/mnt/data/{pdf}")
            
            # Get embedding
            embedding = get_openai_embedding(text)
            
            # Add document to the ChromaDB collection
            collection.add([pdf], metadatas=[{"filename": pdf}], embeddings=[embedding])

        # Store the collection in session state
        st.session_state.Lab4_vectorDB = collection

def extract_text_from_pdf(file_path):
    # Read PDF file
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
        return text

def get_openai_embedding(text):
    # Generate embedding using OpenAI
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

def search_vector_db(query):
    if 'Lab4_vectorDB' in st.session_state:
        # Retrieve collection
        collection = st.session_state.Lab4_vectorDB
        
        # Get query embedding
        query_embedding = get_openai_embedding(query)
        
        # Search in the collection
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        
        return results['metadatas']
    else:
        st.write("ChromaDB not initialized yet.")

# Main chatbot function using Streamlit
def chatbot():
    st.title("Lab 4")
    
    # Initialize ChromaDB if not done yet
    initialize_chroma_db()

    # Text input for query
    user_input = st.text_input("Enter your search query:")
    
    if user_input:
        # Search the vector database
        results = search_vector_db(user_input)
        st.write("Top matching documents:")
        for result in results:
            st.write(result['filename'])
