import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser

# Load environment varibales from ".env file"
load_dotenv()

# Langsmith tracking.
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Define Prompt Template. 
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpful assistant. Please response to the user queries'),
        ('user', 'Question: {question}')
    ]
)

st.title('Learning Langchain With LAMMA2 API')
input_text = st.text_input('Search') # Input-field.

# Initialize LLM-model.
llm = ChatGroq(
    groq_api_key = os.getenv('GROQ_API_KEY'),
    model = "llama-3.1-70b-versatile",
    temperature = 0,
)

# To convert raw ouputs of LLMs into plain text.
output_p = StrOutputParser()

# Chaining the steps - where output of one is passed to other(using pipe operator).
chain = prompt | llm | output_p

# Print the response
if input_text:
    st.write(chain.invoke({'question': input_text}))