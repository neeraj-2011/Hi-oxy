import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Configure your API key
api_key = st.secrets["GOOGLE_KEY"]
genai.configure(api_key=api_key)

# Function to fetch content from a website
def fetch_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        return f"Error fetching {url}: {e}"

# Define your knowledge base URLs
urls = [
    "https://oxyloans.com/",  # Replace with actual URLs
    "https://bmv.money/",
    "https://www.askoxy.ai/"
]

# Function to call the Google Generative AI model
def generate_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate(prompt=prompt)
    return response.text

# Streamlit app layout
st.title("Conversational Chatbot")
st.write("Ask me anything about our organization!")

# Input for user question
user_question = st.text_input("What would you like to know?")

if st.button("Get Answer"):
    if user_question:
        # Fetch content from URLs
        fetched_content = " ".join([fetch_website_content(url) for url in urls])
        
        # Combine the fetched content with the user question
        full_prompt = f"Context: {fetched_content}\n\nUser question: {user_question}"

        # Call the AI model
        response = generate_response(full_prompt)
        st.write(response)
    else:
        st.warning("Please enter a question!")

