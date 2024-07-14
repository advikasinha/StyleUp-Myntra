import streamlit as st
import torch
from PIL import Image
import style_transfer
import utils

st.set_page_config(page_title="DesignerHub", layout="wide")

def main():
    # Custom CSS
    st.markdown("""
    <style>
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
        padding: 10px 16px;
        display: flex;
        align-items: center;
        z-index: 1000;
    }
    .header img {
        width: 100px;
        margin-right: 20px;
    }
    .header .title {
        font-size: 36px;
        font-weight: bold;
        color: #F13AB1;
    }
    .content {
        margin-top: 40px;
        padding: 0 16px;
    }
    .center-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin: 0;
        color: #29303E;
    }
    .lorem-ipsum {
        background-color: #f0f0f0;
        padding: 20px;
        margin: 20px 0;
        color: #29303E;
    }
    .stButton>button {
        background-color: #F13AB1;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #FD913C;
    }
    .upload-label {
        color: black; 
        text-align: center;
    }
    .color-strip {
        height: 5px;
        background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        margin: 20px 0; /* Adjust margin to add spacing around the color strip */
    }
    </style>
    """, unsafe_allow_html=True)

    # # Header with Myntra logo image and StyleUp text
    st.markdown(
    """
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <img src="Myntra_Logo.png" alt="Myntra Logo" style="width: 100px; margin-right: 10px;">
        <h1 style="font-size: 36px; font-weight: bold; color: #F13AB1;">StyleUp</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

    st.image("Myntra_Logo.png", caption="Myntra Logo", width=100)

    # Main content
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # DESIGNER HUB title
    st.markdown('<h1 class="center-title" style="font-size: 40px;">DESIGNER HUB</h1>', unsafe_allow_html=True)

    # Color strip
    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: #F13AB1; text-align: center; font-size: 28px;">Create Your Own Designs</h2>', unsafe_allow_html=True)

    # Lorem Ipsum block
    st.markdown("""
    <div class="lorem-ipsum">
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Welcome to <strong>Designer Hub</strong>, your ultimate playground on Myntra! Designed for both budding designers and fashion enthusiasts, this platform eliminates the need for traditional mockups.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;"><strong><em>Create Your Own Design</em></strong> empowers you to unleash your creativity effortlessly. Simply upload your unique silhouette and pair it with a light-colored style photo to watch your ideas come to life in vibrant, personalized fashion statements!</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E; text-align: center;">Dive in and let your imagination run wild!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # File uploaders
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="upload-label">Upload your Silhouette</span>', unsafe_allow_html=True)
        content_file = st.file_uploader('', type=["png", "jpg", "jpeg"], key='content-file')  # Empty string for label
    with col2:
        st.markdown('<span class="upload-label">Upload your Style</p>', unsafe_allow_html=True)
        style_file = st.file_uploader('', type=["png", "jpg", "jpeg"], key='style-file')

    if content_file and style_file:
        if st.button("Design It!", key="design_button", help="Click to design your image"):
            with st.spinner("Designing your image..."):
                try:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    content_img, style_img = utils.load_images(content_file, style_file, device)
                    output_c = style_transfer.run_style_transfer(content_img, style_img, num_steps=500)
                    output = style_transfer.enhance_silhouette(output_c, content_img)
                    output_pil = utils.tensor_to_pil(output)
                    st.image(output_pil, caption="Your Styled Design", use_column_width=True)
                except Exception as e:
                    st.error(f"An error occurred during the style transfer process: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
