import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

from langchain_core.prompts import PromptTemplate
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("models/gemini-2.5-flash")


def generate_content(prompt):
    result=model.generate_content(prompt)
    return result


while True:
    user_input=input("Ask any question:")
    if user_input =='exit':
        break
    print("User:",user_input)
    response=generate_content(user_input)
    print("AI:",response.text)
    