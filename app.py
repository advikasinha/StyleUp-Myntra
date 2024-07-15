import streamlit as st

st.set_page_config(page_title="DesignerHub", layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.markdown("""
<div class="header">
    <span class="logo">StyleUp</span>
    <a href="#" class="nav-item">View Catalogue</a>
    <a href="#" class="nav-item">Look Of The Week</a>
    <a href="#" class="nav-item">Trending</a>
    <a href="#" class="nav-item">My Designs</a>
    <a href="#" class="nav-item">Help</a>
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