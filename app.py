import streamlit as st
import torch
from PIL import Image
import style_transfer
import utils

st.set_page_config(page_title="DesignerHub", layout="wide")

def main():
    # Header
    st.markdown("""
    <style>
    .header {
        padding: 10px 16px;
        background: #ffffff;
        color: #f1f1f1;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 1000;
    }
    .content {
        padding: 16px;
        margin-top: 60px;
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
    }
    .button-primary {
        background-color: #ff3f6c;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="header">
        <h1 style="color: #ff3f6c;">DesignerHub</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    content_file = None
    style_file = None

    with col1:
        st.markdown('<div class="sidebar">', unsafe_allow_html=True)
        st.markdown('<div class="product-title">Style Transfer</div>', unsafe_allow_html=True)
        content_file = st.file_uploader("Choose a content image", type=["png", "jpg", "jpeg"])
        style_file = st.file_uploader("Choose a style image", type=["png", "jpg", "jpeg"])
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
                    output = style_transfer.run_style_transfer(content_img, style_img)
                    output_pil = utils.tensor_to_pil(output)
                    st.image(output_pil, caption="Styled Image", use_column_width=True)
        else:
            st.markdown("Upload both content and style images to see the result.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()