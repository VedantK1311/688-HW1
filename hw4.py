import streamlit as st
import openai
from chroma_py import ChromaDB
import pdfplumber  # To extract text from PDF

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ''
        for page in pdf.pages:
            full_text += page.extract_text()
    return full_text

# Function to create and populate the ChromaDB
def create_chromadb():
    if 'Lab4_vectorDB' not in st.session_state:
        # Initialize ChromaDB
        db = ChromaDB("Lab4_vectorDB")
        
        # Define the collection
        collection = db.create_collection("Lab4Collection", model="text-embedding-3-small")
        
        # List of PDF files
        pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf', 'file5.pdf', 'file6.pdf', 'file7.pdf']
        
        for pdf_file in pdf_files:
            text = extract_text_from_pdf(pdf_file)
            # Use OpenAI to get embeddings
            response = openai.Embedding.create(input=text, model="text-embedding-3-small")
            embedding = response['data']['embedding']
            
            # Add document to ChromaDB
            collection.add_document(pdf_file, embedding, metadata={'filename': pdf_file})
        
        st.session_state['Lab4_vectorDB'] = db

# Chatbot response function
def chatbot_response(query):
    if 'Lab4_vectorDB' in st.session_state:
        # Perform a search in the ChromaDB
        results = st.session_state['Lab4_vectorDB'].search(query, top_k=1)
        if results:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are an assistant trained on diverse topics."},
                          {"role": "user", "content": query},
                          {"role": "assistant", "content": results[0].text}]
            )
            return response.choices[0].message['content']
        else:
            return "No relevant data found."
    else:
        return "Database not initialized."

# Main Streamlit app
def main():
    st.title("Lab 4 App")

    # Button to create and load the database
    if st.button("Create/Load ChromaDB"):
        create_chromadb()
        st.success("ChromaDB is ready!")

    # Chat interface
    query = st.text_input("Ask something about your course:")
    if st.button("Ask"):
        reply = chatbot_response(query)
        st.text_area("Response:", value=reply, height=300)

    # Testing search functionality
    option = st.selectbox("Choose a topic to search:",
                          ["Generative AI", "Text Mining", "Data Science Overview"])
    if st.button("Search"):
        if 'Lab4_vectorDB' in st.session_state:
            results = st.session_state['Lab4_vectorDB'].search(option, top_k=3)
            for result in results:
                st.write(result.metadata['filename'])
        else:
            st.error("ChromaDB is not loaded. Please initialize the database first.")

if __name__ == "__main__":
    main()
