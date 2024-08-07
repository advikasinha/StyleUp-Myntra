import streamlit as st
import torch
from PIL import Image
import style_transfer
import utils

st.set_page_config(page_title="DesignerHub", layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    load_css()
    
    st.markdown(
"""
<div class="header">
    <div class="title">StyleUp</div>
</div>
""", unsafe_allow_html=True)
    st.markdown('<h1 class="center-title" style="font-size: 40px;">DESIGNER HUB</h1>', unsafe_allow_html=True)

    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: #F13AB1; text-align: center; font-size: 28px;">Create Your Own Designs</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lorem-ipsum">
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Welcome to <strong>Designer Hub</strong>, your ultimate playground on Myntra! Designed for both budding designers and fashion enthusiasts, this platform eliminates the need for traditional mockups.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;"><strong><em>Create Your Own Design</em></strong> empowers you to unleash your creativity effortlessly. Simply upload your unique silhouette and pair it with a light-colored style photo to watch your ideas come to life in vibrant, personalized fashion statements!</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E; text-align: center;">Dive in and let your imagination run wild!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")


    col1, col2 = st.columns(2)
    image_width=300
    with col1:
        st.markdown('<span class="upload-label">Upload your Silhouette</span>', unsafe_allow_html=True)
        content_file = st.file_uploader('', type=["png", "jpg", "jpeg"], key='content-file')  
        if content_file is not None:
            st.image(content_file, caption='Uploaded Silhouette', width=image_width)
    with col2:
        st.markdown('<span class="upload-label">Upload your Style</p>', unsafe_allow_html=True)
        style_file = st.file_uploader('', type=["png", "jpg", "jpeg"], key='style-file')
        if style_file is not None:
            st.image(style_file, caption='Uploaded Style', width=image_width)

    if content_file and style_file:
        if st.button("Design It!", help="Click to design your image"):
            with st.spinner("Designing your image..."):
                try:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    content_img, style_img = utils.load_images(content_file, style_file, device)
                    output_c = style_transfer.run_style_transfer(content_img, style_img, num_steps=500)
                    output = style_transfer.enhance_silhouette(output_c, content_img)
                    output_pil = utils.tensor_to_pil(output)
                    st.image(output_pil, caption="Your Styled Design", width=600, use_column_width=False)
                except Exception as e:
                    st.error(f"An error occurred during the style transfer process: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
