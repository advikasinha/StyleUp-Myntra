import streamlit as st
import torch
from PIL import Image
import style_transfer
import utils

st.set_page_config(page_title="DesignerHub", layout="wide")

def main():
    # Custom CSS with all Myntra logo colors and updated header styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    .header {
        padding: 10px 16px;
        background: #29303E;
        color: white;
        top: 0;
        width: 100%;
        z-index: 1000;
        display: flex;
        align-items: center;
    }
    .logo-container {
        display: flex;
        align-items: center;
    }
    .logo-image {
        height: 40px;
        margin-right: 10px;  /* Reduced margin */
    }
    .app-name {
        font-size: 24px;
        color: #FD913C;
        margin-left: 0;  /* Removed left margin */
    }
    .content {
        padding: 16px;
        margin-top: 10px;
    }
    .sidebar {
        background-color: #f9f9f9;
        padding: 20px;
        border-right: 1px solid #e9e9e9;
    }
    .main-content {
        padding: 20px;
    }
    .product-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
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
        background-color: #E72744;
    }
    .upload-text {
        color: #29303E;
        font-weight: bold;
    }
    .color-strip {
        height: 5px;
        background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with Myntra logo image and DesignerHub text
    logo_path = "Myntra-Logo.png"
    st.markdown(f"""
    <div class="header">
        <div class="logo-container">
            <img src="{logo_path}" class="logo-image" alt="Myntra Logo">
            <span class="app-name">DesignerHub</span>
        </div>
    </div>
    <div class="color-strip"></div>
    """, unsafe_allow_html=True)


    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.markdown('<div class="product-title">Style Transfer</div>', unsafe_allow_html=True)
        st.markdown('<p class="upload-text">Choose a content image</p>', unsafe_allow_html=True)
        content_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="content_upload")
        st.markdown('<p class="upload-text">Choose a style image</p>', unsafe_allow_html=True)
        style_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="style_upload")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        if content_file is not None and style_file is not None:
            col_a, col_b = st.columns(2)
            with col_a:
                content_image = Image.open(content_file)
                st.image(content_image, caption="Content Image", use_column_width=True)
            with col_b:
                style_image = Image.open(style_file)
                st.image(style_image, caption="Style Image", use_column_width=True)
        
            if st.button("Generate Styled Image", key="generate_button"):
                with st.spinner("Generating styled image..."):
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    content_img, style_img = utils.load_images(content_file, style_file, device)
                    output_c = style_transfer.run_style_transfer(content_img, style_img, num_steps=500)
                    output = style_transfer.enhance_silhouette(output_c, content_img)
                    output_pil = utils.tensor_to_pil(output)
                    st.image(output_pil, caption="Styled Image", use_column_width=True)
        else:
            st.markdown('<p class="upload-text">Upload both content and style images to see the result.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()