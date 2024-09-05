import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI, OpenAIError

st.title("Document Question Answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get "
    "[here](https://platform.openai.com/account/api-keys)."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")

if openai_api_key:
    try:
        client = OpenAI(api_key=openai_api_key)
        client.models.retrieve(model="gpt-4o-mini")  # This checks if the API key is correct
        st.success("API key is valid!")

        uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=("txt", "pdf"))
        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1]
            if file_extension == 'txt':
                document = uploaded_file.read().decode()
            elif file_extension == 'pdf':
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                document = "".join([page.get_text() for page in doc])
                doc.close()
            else:
                st.error("Unsupported file type.")
                document = None

            if document:
                question = st.text_input(
                    "Now ask a question about the document!",
                    placeholder="Can you give me a short summary?"
                )
                if question:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"}],
                        stream=True,
                    )
                    for message in response:
                        if message["role"] == "system":
                            st.write(message["content"])
        else:
            st.info("Please upload a document to continue.", icon="🗂️")
    except OpenAIError as e:
        st.error(f"Failed to validate API key: {str(e)}")
else:
    st.info("Please add your OpenAI API key to continue.", icon="🔑")
