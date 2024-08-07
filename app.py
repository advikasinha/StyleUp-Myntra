import streamlit as st

st.set_page_config(page_title="DesignerHub", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
        color: #29303E;
        background-color: #f8f8f8;
    }
    .stApp {
    background-color: #FFFFFF;
}
.header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #29303E;
    color: #F13AB1;
    padding: 20px 30px; /* Adjust padding as needed /
    display: flex;
    align-items: center;
    z-index: 1000;
}
.header .title {
    font-size: 18; / Adjust font size /
    font-weight: bold;
    color: #F13AB1;
    margin-right: auto; / Align title to the left */
}
           
                .nav-item {
        display: inline-block;
        margin-right: 20px;
        color: #FFFFFF;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    .nav-item:hover {
        color: #FF3F6C;
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
   
    .lorem-ipsum {
    background-color: #f0f0f0;
    padding: 20px;
    margin: 20px 0;
    color: #29303E;
}
    .feature-description {
        color: #29303E;
        font-size: 1em;
        line-height: 1.6;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #29303E;
        font-weight: 300;
    }
    .myntra-gradient {
        background: linear-gradient(90deg, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        height: 5px;
        margin: 30px 0;
    }
    .feature-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px 10px 0 0;
    }
    .feature-button {
        background: linear-gradient(90deg, #F13AB1, #E72744);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: transform 0.3s ease;
        display: block;
        width: 100%;
        margin-top: 15px;
    }
    .feature-button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <span class="logo">StyleUp</span>
</div>
""", unsafe_allow_html=True)

st.title("Welcome to DesignerHub")

st.markdown('<div class="myntra-gradient"></div>', unsafe_allow_html=True)
st.markdown("""
    <div class="lorem-ipsum">
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Welcome to <strong>Designer Hub</strong>, your ultimate playground on Myntra! Designed for both budding designers and fashion enthusiasts, this platform eliminates the need for traditional mockups.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;"><strong><em>Explore our innovative fashion design tools and features and:</em></strong></p>
        <p style="text-align: center; font-size: 24px; line-height: 1.6; background: linear-gradient(90deg, #F13AB1, #E72744, #FD913C, #F05524, #29303E); -webkit-background-clip: text; color: transparent;"><strong>LET'S STYLE UP!</strong></p>
    </div>
    """, unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <img src="https://images.unsplash.com/photo-1557777586-f6682739fcf3?q=80&w=1935&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Create Your Own" class="feature-image">
        <div class="feature-title">Create Your Own</div>
        <div class="feature-description">Transform your designs with AI-powered style transfer. Unleash your creativity and bring your unique fashion ideas to life.</div>
        <button class="feature-button">Start Creating</button>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-box">
        <img src="https://preview.redd.it/just-came-across-these-amazing-ai-generated-dresses-on-v0-tyjw9bjx88h91.jpg?auto=webp&s=7ee40126482dfb83b8de5f2a1d6bf2d818ba39c6" alt="AI-aided Designing" class="feature-image">
        <div class="feature-title">AI-ded Designing</div>
        <div class="feature-description">Let DALL-E generate a unique look. Explore the possibilities of AI-generated fashion and find inspiration for your next design.</div>
        <button class="feature-button">Generate Designs</button>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-box">
        <img src="https://images.unsplash.com/photo-1702661159134-2e8d4dcf0231?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dmlicmFudCUyMGNsb3RoZXN8ZW58MHx8MHx8fDA%3D" alt="Mix It Up" class="feature-image">
        <div class="feature-title">Mix It Up</div>
        <div class="feature-description">Choose from Myntra's own exquisite collection. Combine and customize pieces to create your perfect outfit.</div>
        <button class="feature-button">Explore Collection</button>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)