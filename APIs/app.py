# FastAPI turns python-application(app.py) into a API.
from fastapi import FastAPI
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import uvicorn
import os
from dotenv import load_dotenv

from dotenv import load_dotenv
# Load environment varibales from ".env file"
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# Initialize app.py as API.
app = FastAPI(
    title='LLM API',
    version='1.0',
    description= 'This API allows users to interact with various Large Language Models (LLMs) for different natural language processing tasks'   
)

# Define Prompt-Templates.
gemma2_p = ChatPromptTemplate.from_template('{query}')
llama2_p = ChatPromptTemplate.from_template('{query}') 

# Create LLM-Models.
llama2 = ChatGroq(
    groq_api_key = os.getenv('GROQ_API_KEY'),
    model = "llama-3.1-70b-versatile",
    temperature = 0,
)

gemma2 = ChatGroq(
    groq_api_key = os.getenv('GROQ_API_KEY'),
    model = 'gemma2-9b-it',
    temperature = 0,
)

# Add Routes
add_routes(
    app,
    llama2_p | llama2,
    path='/llama2'
)

add_routes(
    app,
    gemma2_p | gemma2,
    path='/gemma2'
)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)

