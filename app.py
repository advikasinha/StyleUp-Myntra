import streamlit as st

st.set_page_config(page_title="DesignerHub", page_icon="👚", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
        color: #29303E;
        background-color: #f8f8f8;
    }

    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
    }

    h1 {
        color: #F13AB1;
        font-size: 3.5em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    h3 {
        color: #E72744;
        font-size: 1.8em;
        font-weight: 400;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    .feature-box {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .feature-box:hover {
        transform: translateY(-5px);
    }

    .feature-title {
        color: #FD913C;
        font-size: 1.4em;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .feature-description {
        color: #29303E;
        font-size: 1em;
        line-height: 1.6;
    }

    .footer {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        color: white;
        font-weight: 300;
        margin-top: 50px;
    }

    .myntra-gradient {
        background: linear-gradient(90deg, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        height: 5px;
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("Welcome to DesignerHub")

st.markdown('<div class="myntra-gradient"></div>', unsafe_allow_html=True)

st.write("Explore our innovative fashion design tools and features:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">Create Your Own</div>
        <div class="feature-description">Transform your designs with AI-powered style transfer. Unleash your creativity and bring your unique fashion ideas to life.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">AI-aided Designing</div>
        <div class="feature-description">Let DALL-E generate a unique look. Explore the possibilities of AI-generated fashion and find inspiration for your next design.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-title">Mix It Up</div>
        <div class="feature-description">Choose from Myntra's own exquisite collection. Combine and customize pieces to create your perfect outfit.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="myntra-gradient"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)