import streamlit as st
import pdfplumber
from groq import Groq, GroqError
from fpdf import FPDF
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text.strip()

# Function to generate questions using Groq API
def generate_questions(text):
    prompt = f"Generate a list of 15 quiz questions from the following content:\n\n{text}"
    
    # Split the content into smaller chunks if it exceeds the token limit
    max_chunk_size = 6000
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    
    # Initialize the Groq client with your API key
    try:
        client = Groq(api_key="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")  # Replace with your Groq API key
    except GroqError as e:
        st.error(f"Error initializing Groq client: {str(e)}")
        return None

    question_bank = ""

    # Process each chunk separately
    for chunk in chunks:
        try:
            # Make the API call to generate questions for each chunk
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Use the correct model name
                messages=[{"role": "system", "content": "You are an AI that creates educational quizzes."},
                          {"role": "user", "content": f"Generate a list of quiz questions from the following content:\n\n{chunk}"}],
                temperature=0.7,
                max_completion_tokens=1000,
                top_p=1,
                stream=True
            )

            # Process the streamed response
            for chunk_response in completion:
                question_bank += chunk_response.choices[0].delta.content or ""

        except Exception as e:
            st.error(f"Error generating questions: {str(e)}")
            return None

    return question_bank

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
st.title("📚 Upload Learning Material ")
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

        if question_bank:
            st.text_area("Generated Question Bank", question_bank, height=300)

            # Save as PDF
            pdf_path = create_pdf(question_bank)

            # Layout with columns
            col1,col2 = st.columns(2)
            # Download Button
            with col1:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Question Bank",
                        data=file,
                        file_name="Adaptify_Question_Bank.pdf",
                        mime="application/pdf",
                        use_container_width=True  # Ensures the button spans the entire column width
            )
        # Start Adaptive Assessment
            with col2:
                if st.button("🚀 Start Assessment", key="assessment_button", use_container_width=True):
                    st.session_state['questions'] = question_bank.split("\n")  # Store questions for assessment page
                    st.switch_page("assessment.py")  # Redirect to assessment page

    else:
        st.error("Failed to extract text from the PDF. Please upload a valid document.")
