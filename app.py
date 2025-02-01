import streamlit as st
import fitz  # PyMuPDF
import requests
import json
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Adaptify - Smart Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'current_level' not in st.session_state:
    st.session_state.current_level = 'intermediate'
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'questions_asked' not in st.session_state:
    st.session_state.questions_asked = 0
if 'performance_history' not in st.session_state:
    st.session_state.performance_history = []
if 'content' not in st.session_state:
    st.session_state.content = None

# Constants
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"
GROQ_API_KEY = "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" 
DIFFICULTY_LEVELS = {
    'beginner': {'next': 'intermediate', 'prev': None},
    'intermediate': {'next': 'advanced', 'prev': 'beginner'},
    'advanced': {'next': None, 'prev': 'intermediate'}
}

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF."""
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text[:4000]  # Limit text length for API
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return None

def generate_question(content, level):
    """Generate a question using Groq's Llama API."""
    try:
        prompt = f"""Generate a {level}-level multiple choice question based on this content:
        {content}
        
        Format:
        - Question should be clear and specific
        - Provide 4 options (A, B, C, D)
        - Include the correct answer and explanation
        
        Return as JSON with these keys:
        - question
        - options (array of 4 choices)
        - correct_answer
        - explanation
        """

        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-2-70b-chat",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )
        
        return json.loads(response.json()['choices'][0]['message']['content'])
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return None

def adjust_difficulty(correct_answer):
    """Adjust difficulty based on user performance."""
    current = st.session_state.current_level
    
    # Update score
    st.session_state.score += 1 if correct_answer else 0
    st.session_state.questions_asked += 1
    
    # Calculate accuracy
    accuracy = st.session_state.score / st.session_state.questions_asked
    
    # Record performance
    st.session_state.performance_history.append({
        'time': datetime.now(),
        'level': current,
        'correct': correct_answer,
        'accuracy': accuracy
    })
    
    # Adjust level based on recent performance (last 3 questions)
    recent_correct = sum(1 for x in st.session_state.performance_history[-3:] if x['correct'])
    
    if recent_correct >= 2 and DIFFICULTY_LEVELS[current]['next']:
        return DIFFICULTY_LEVELS[current]['next']
    elif recent_correct <= 1 and DIFFICULTY_LEVELS[current]['prev']:
        return DIFFICULTY_LEVELS[current]['prev']
    return current

def main():
    # Custom CSS
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .question {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("📚 Adaptify")
        st.markdown("---")
        st.subheader("👤 Student Profile")
        name = st.text_input("Name")
        grade = st.selectbox("Grade", ["9th", "10th", "11th", "12th"])
        subject = st.selectbox("Subject", ["Mathematics", "Science", "History", "English"])
        
        # Display current stats
        st.markdown("---")
        st.subheader("📊 Current Stats")
        st.write(f"Level: {st.session_state.current_level.title()}")
        if st.session_state.questions_asked > 0:
            accuracy = (st.session_state.score / st.session_state.questions_asked) * 100
            st.write(f"Accuracy: {accuracy:.1f}%")
    
    # Main content
    st.title("🎯 Adaptive Learning Assessment")
    
    # File upload section
    st.header("📑 Upload Learning Material")
    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    
    if uploaded_file:
        if st.session_state.content is None:
            with st.spinner("Processing document..."):
                st.session_state.content = extract_text_from_pdf(uploaded_file)
                if st.session_state.content:
                    st.success("Document processed successfully!")
    
    # Question generation and assessment
    if st.session_state.content:
        if st.button("Generate Question"):
            with st.spinner("Generating question..."):
                question_data = generate_question(st.session_state.content, st.session_state.current_level)
                
                if question_data:
                    st.markdown("### Question")
                    with st.container():
                        st.markdown(f"**{question_data['question']}**")
                        answer = st.radio("Select your answer:", question_data['options'])
                        
                        if st.button("Submit Answer"):
                            is_correct = answer == question_data['correct_answer']
                            
                            if is_correct:
                                st.success("✅ Correct! " + question_data['explanation'])
                            else:
                                st.error("❌ Incorrect. " + question_data['explanation'])
                            
                            # Adjust difficulty
                            st.session_state.current_level = adjust_difficulty(is_correct)
                            
                            # Show progress
                            if st.session_state.performance_history:
                                st.markdown("---")
                                st.subheader("📈 Progress")
                                
                                # Create performance graph
                                df = pd.DataFrame(st.session_state.performance_history)
                                fig = px.line(df, y='accuracy', title='Learning Progress')
                                fig.update_layout(yaxis_title='Accuracy', xaxis_title='Questions')
                                st.plotly_chart(fig)
                                
                                # Show recommendations
                                st.subheader("📋 Recommendations")
                                recent_accuracy = sum(1 for x in st.session_state.performance_history[-5:] if x['correct']) / 5
                                
                                if recent_accuracy < 0.4:
                                    st.warning("Consider reviewing basic concepts before proceeding.")
                                elif recent_accuracy < 0.7:
                                    st.info("You're making progress! Focus on understanding the explanations.")
                                else:
                                    st.success("Excellent work! You're ready for more challenging questions.")

if __name__ == "__main__":
    main()