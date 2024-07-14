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
    }
    .content {
        margin-top: 120px; /* Adjust margin to ensure content is below fixed header */
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
        background-color: #f9f9f9;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
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
    .color-strip {
        height: 5px;
        background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        margin: 20px 0; /* Adjust margin to add spacing around the color strip */
    }
    </style>
    """, unsafe_allow_html=True)

    # Header with Myntra logo image and StyleUp text
    st.markdown(
    """
    <div class="header">
        <img src="Myntra-Logo.png" alt="Myntra Logo">
        <div class="title">StyleUp</div>
    </div>
    """,
    unsafe_allow_html=True
    )

    # Main content
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # DESIGNER HUB title
    st.markdown('<h1 class="center-title">DESIGNER HUB</h1>', unsafe_allow_html=True)

    # Color strip
    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    # Lorem Ipsum block
    st.markdown("""
    <div class="lorem-ipsum">
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris. Vivamus hendrerit arcu sed erat molestie vehicula. Sed auctor neque eu tellus rhoncus ut eleifend nibh porttitor. Ut in nulla enim. Phasellus molestie magna non est bibendum non venenatis nisl tempor. Suspendisse dictum feugiat nisl ut dapibus. Mauris iaculis porttitor posuere. Praesent id metus massa, ut blandit odio. Proin quis tortor orci. Etiam at risus et justo dignissim congue. Donec congue lacinia dui, a porttitor lectus condimentum laoreet. Nunc eu ullamcorper orci. Quisque eget odio ac lectus vestibulum faucibus eget in metus. In pellentesque faucibus vestibulum. Nulla at nulla justo, eget luctus tortor.
    </div>
    """, unsafe_allow_html=True)

    # Create Your Own Designs section
    st.write("")
    st.write("")
    st.header("Create Your Own Designs")

    # File uploaders
    col1, col2 = st.columns(2)
    with col1:
        content_file = st.file_uploader("Choose a content image", type=["png", "jpg", "jpeg"])
    with col2:
        style_file = st.file_uploader("Choose a style image", type=["png", "jpg", "jpeg"])

    if content_file and style_file:
        if st.button("Design It!"):
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
