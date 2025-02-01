import streamlit as st

# Set page title and configuration
st.set_page_config(page_title="Login - Adaptify", page_icon="🔐", layout="centered")

# Apply custom CSS for modern UI aesthetics
st.markdown(
    """
    <style>
        /* Global Styles */
        .stApp {
            background-color: #e6f3ff;
        }
        
        /* Login Container */
        .login-container {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            margin: auto;
        }
        
        .login-title {
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .login-input {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }
        
        .login-button {
            width: 100%;
            background: linear-gradient(30deg, #3498db, #2980b9);
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .login-button:hover {
            transform: translateY(-4px);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Login Page Content
st.markdown(
    """
    <div class="login-container">
        <h2 class="login-title">Login to Adaptify</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Input fields
st.markdown("<p style='font-size: 12px; font-weight: bold; font-color: black;'>Email/Username</p>", unsafe_allow_html=True)
email_username = st.text_input("", key="login_email_username font-color:black", placeholder="Enter your email or username")

st.markdown("<p style='font-size: 12px; font-weight: bold;'>Password</p>", unsafe_allow_html=True)
password = st.text_input("", key="login_password", type="password", placeholder="Enter your password")

# Login button
col1, col2 = st.columns([3, 1])
if st.button("Sign In", key="login_button"):
    if email_username and password:
        st.markdown("<p style='color: black;'>Login successful! Redirecting...</p>", unsafe_allow_html=True)
    else:
        st.error("Please fill in all fields.")

# Link to Signup page
st.markdown(
    """
    <div style="text-align: right; margin-top: 20px; color:#2c3e50;">
        <p>Don't have an account? <a href="/signup" target="_self">Sign up</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
