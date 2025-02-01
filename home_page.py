import streamlit as st
from PIL import Image

# Set page title and configuration
st.set_page_config(page_title="ADAPTIFY", page_icon="🎓", layout="wide")

# Apply custom CSS for modern UI aesthetics
st.markdown(
    """
    <style>
        /* Global Styles */
        .stApp {
            background-color: #e6f3ff;
        }
        
        /* Hero Section Styles */
        .hero-container {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(160deg, #ffffff 60%, #e6f3ff 40%);
            border-radius: 20px;
            margin-bottom: 40px;
        }
        
        .main-title {
            font-size: 64px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            font-family: 'Audrey', sans-serif;
            text-align: center;
        }
        
        .tagline {
            font-size: 28px;
            color: #34495e;
            margin-bottom: 30px;
            font-family: 'Helvetica Neue', sans-serif;
            line-height: 1.4;
        }
        
        /* Overview Section Styles */
        .overview-box {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        }
        
        .overview-title {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .overview-text {
            font-size: 18px;
            color: #34495e;
            line-height: 1.6;
        }
        
        /* CTA Button Styles */
        .cta-button {
            display: inline-block;
            background: linear-gradient(30deg, #3498db, #2980b9);
            color: white !important; /* Ensure text color is white */
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 20px;
            font-weight: bold;
            text-decoration: none;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
            transition: transform 0.3s ease;
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
        }
        
        /* Feature Box Styles */
        .feature-box {
            background-color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            margin: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            height: 100%;
        }
        
        .feature-icon {
            font-size: 40px;
            margin-bottom: 15px;
        }
        
        /* Subscription Plan Styles */
        .plan-box {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            text-align: center;
        }
        
        .plan-title {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        }
        
        .plan-price {
            font-size: 32px;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 20px;
        }
        
        .plan-features {
            list-style-type: none;
            padding: 0;
            margin-bottom: 20px;
            text-align: left;
        }
        
        .plan-features li {
            font-size: 16px;
            color: #34495e;
            margin-bottom: 10px;
        }

        /* Footer Styles */
        .footer {
            text-align: center;
            padding: 20px;
            background-color: #e6f3ff;
            margin-top: 40px;
            border-top: 1px solid #ccc;
        }
        
        .footer p {
            margin: 5px 0;
            color: #34495e;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Hero Section
st.markdown(
    """
    <div class="hero-container">
        <h1 class="main-title">ADAPTIFY</h1>
        <p class="tagline">Revolutionize Your Learning Journey with AI-Powered Assessments</p>
        <a href="#" class="cta-button">Start Your Assessment</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Main content columns
col1, col2 = st.columns([6, 4])

with col1:
    st.markdown(
        """
        <div class="overview-box">
            <h2 class="overview-title">Transform Your Educational Experience</h2>
            <p class="overview-text">
                Adaptify uses cutting-edge AI technology to create personalized learning experiences 
                that evolve with you. Our intelligent assessment system adapts in real-time to your 
                unique learning style, ensuring optimal comprehension and retention.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    # Image Section
    try:
        st.image("flight.jpg", width=400)
    except FileNotFoundError:
        st.warning("Please check if the image file exists in the correct location")

# Key Features Section
st.markdown("<h2 style='text-align: center; color: #2c3e50; margin: 40px 0 20px;'>Why Choose Adaptify?</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

features = [
    {
        "icon": "🎯",
        "title": "Personalized Learning",
        "description": "AI-powered assessments that adapt to your unique learning style and pace"
    },
    {
        "icon": "📊",
        "title": "Real-time Analytics",
        "description": "Detailed insights into your progress and areas for improvement"
    },
    {
        "icon": "🚀",
        "title": "Rapid Progress",
        "description": "Accelerate your learning with targeted assessments and feedback"
    }
]

for col, feature in zip([col1, col2, col3], features):
    with col:
        st.markdown(
            f"""
            <div class="feature-box">
                <div class="feature-icon">{feature['icon']}</div>
                <h3 style="color: #2c3e50; margin-bottom: 10px;">{feature['title']}</h3>
                <p style="color: #34495e;">{feature['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Subscription Plans Section
st.markdown("<h2 style='text-align: center; color: #2c3e50; margin: 40px 0 20px;'>Choose Your Plan</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

plans = [
    {
        "title": "Individual",
        "price": "₹5000/month",
        "features": [
            "Personalized learning paths",
            "Real-time progress tracking",
            "Access to basic analytics",
            "Monthly progress reports",
            "24/7 Customer support"
        ],
        "button": "Get Started"
    },
    {
        "title": "Educators",
        "price": "₹10000/month",
        "features": [
            "Classroom management tools",
            "Student performance analytics",
            "Customizable assessments",
            "Collaboration tools",
            "Dedicated support"
        ],
        "button": "Get Started"
    },
    {
        "title": "Researchers",
        "price": "₹20000/month",
        "features": [
            "Advanced data analytics",
            "Custom research tools",
            "Access to raw data",
            "Collaboration with other researchers",
            "Priority support"
        ],
        "button": "Get Started"
    }
]

for col, plan in zip([col1, col2, col3], plans):
    with col:
        st.markdown(
            f"""
            <div class="plan-box">
                <h3 class="plan-title">{plan['title']}</h3>
                <div class="plan-price">{plan['price']}</div>
                <ul class="plan-features">
                    {''.join(f'<li>{feature}</li>' for feature in plan['features'])}
                </ul>
                <a href="#" class="cta-button">{plan['button']}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

# Final CTA Section
st.markdown(
    """
    <div style="text-align: center; margin: 60px 0;">
        <h2 style="color: #2c3e50; margin-bottom: 20px;">Ready to Transform Your Learning?</h2>
        <a href="#" class="cta-button">Get Started Now</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer Section
st.markdown(
    """
    <div class="footer">
        <p>&copy; 2025 Adaptify. All rights reserved.</p>
        <p>Terms of Service | Privacy Policy</p>
    </div>
    """,
    unsafe_allow_html=True
)
