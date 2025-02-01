import streamlit as st
import os
import pdfplumber
import requests
import json
from fpdf import FPDF

# Your Groq API key (Store it securely, do not hardcode in production)
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

# Function to generate questions using Groq Llama API
def generate_questions(text):
    prompt = f"Generate a list of quiz questions from the following content:\n\n{text}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3-8b",  # Use the model available in Groq Cloud
        "messages": [{"role": "system", "content": "You are an AI that creates educational quizzes."},
                     {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

# Function to create a downloadable PDF of questions
def create_pdf(question_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, question_text)
    
    pdf_path = "generated_question_bank.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Streamlit UI
st.title("📚 Upload Learning Material & Generate Question Bank")
st.write("Upload a textbook or chapter, and AI will generate a question bank.")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting content from PDF..."):
        text_content = extract_text_from_pdf(uploaded_file)
    
    if text_content:
        st.success("Text extracted successfully! Generating questions...")

        with st.spinner("Generating AI-powered question bank..."):
            question_bank = generate_questions(text_content)

        st.text_area("Generated Question Bank", question_bank, height=300)

        # Save as PDF
        pdf_path = create_pdf(question_bank)

        # Download Button
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="📥 Download Question Bank",
                data=file,
                file_name="Adaptify_Question_Bank.pdf",
                mime="application/pdf"
            )

        # Start Adaptive Assessment
        if st.button("🚀 Start Adaptive Assessment"):
            st.session_state['questions'] = question_bank.split("\n")  # Store questions for assessment page
            st.switch_page("assessment.py")  # Redirect to assessment page

    else:
        st.error("Failed to extract text from the PDF. Please upload a valid document.")
