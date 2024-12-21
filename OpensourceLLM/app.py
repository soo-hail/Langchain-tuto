import os
import time
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader # Load(Scrap) webpage
from langchain.text_splitter import RecursiveCharacterTextSplitter # Tokanization.
from langchain.embeddings import OllamaEmbeddings # Embbeding
from langchain_community.vectorstores import FAISS # Vector-Store
# with list of documents(context) builds a prompt for retriever. 
from langchain.chains.combine_documents import create_stuff_documents_chain
# Takes user query and pass to retriever.
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Create 'Session_Sate'. Session_state is a feature in Langchain that allow to track variables or conversation throughtout a session.
if 'db' not in st.session_state:
    # Load Webpage
    st.session_state.loader = WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs = st.session_state.loader.load()
    
    # Data Transformation(Tokenization).
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200) # Create Instance.
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    
    # Embedding
    st.session_state.embeddings = OllamaEmbeddings()
    st.session_state.db = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings) # Vector Store.

st.title("RAG With ChatGroq Demo")
input_text = st.text_input("Ask Groq About Langsmith")

# Initialize LLM-model.
llm = ChatGroq(
    groq_api_key = os.getenv('GROQ_API_KEY'),
    model = "llama-3.1-70b-versatile",
    temperature = 0,
)

# Create Prompt
prompt = ChatPromptTemplate.from_template(
"""
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}

"""
)

# Create Prompt for LLM with Context(provin' external-data).
document_chain = create_stuff_documents_chain(llm, prompt)
# Create Retriever.
retriever = st.session_state.db.as_retriever()
# Combine Query and Prompt.
retrieval_chain = create_retrieval_chain(retriever, document_chain)

if input_text:
    response = retrieval_chain.invoke({'input': input_text})
    
    # Track Processing Time
    start_time = time.process_time()
    print(f'Response Time: {time.process_time() - start_time}')
    st.write(response['answer']) # Output generated by genrative-Model(llama3).
    
    # With a Streamlit Expander - show page-content loaded by retriver-model.
    with st.expander("Document Similarity Search"):
        # Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")
    
    



