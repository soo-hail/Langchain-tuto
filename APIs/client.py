import requests
import streamlit as st

def llama2_response(query):
    try:
        # Send the POST request to the FastAPI endpoint
        response = requests.post('http://localhost:8000/llama2/invoke', json={'input': {'query': query}})
        
        return response.json()['output']['content']
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def gemma2_response(query):
    try:
        # Send the POST request to the FastAPI endpoint
        response = requests.post('http://localhost:8000/gemma2/invoke', json={'input': {'query': query}})
        
        return response.json()['output']['content']
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Streamlit Web Interface
st.title('Building and Exploring Custom APIs')
input_llama2 = st.text_input('Interact with LLAMA2')
input_gemma2 = st.text_input('Interact with GEMMA2')

if input_llama2:
    st.write(llama2_response(input_llama2))
    
if input_gemma2:
    st.write(gemma2_response(input_gemma2))
