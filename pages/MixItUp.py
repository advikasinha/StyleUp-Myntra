import streamlit as st
import torch
import torchvision
import utils2
import style_transfer
from PIL import Image
import os
import time

st.set_page_config(page_title="DesignerHub", layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.write("")

if 'last_run_time' not in st.session_state:
    st.session_state['last_run_time'] = 0
if 'output_image' not in st.session_state:
    st.session_state['output_image'] = None

st.markdown("""
<div class="header">
    <div class="title">StyleUp</div>
</div>
""", unsafe_allow_html=True)

def get_image_list(folder):
    image_dir = os.path.join(os.path.dirname(__file__), '..', 'images', folder)    
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return {os.path.splitext(f)[0]: os.path.join(image_dir, f) for f in images}

def perform_style_transfer(_content_tensor, _style_tensor, num_steps=500):
    output_c = style_transfer.run_style_transfer(_content_tensor, _style_tensor, num_steps=num_steps)
    return style_transfer.enhance_silhouette(output_c, _content_tensor)

def main():
    load_css()

    st.markdown('<h1 class="center-title" style="font-size: 40px;">DESIGNER HUB</h1>', unsafe_allow_html=True)

    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    st.markdown('<h2 style="color: #F13AB1; text-align: center; font-size: 28px;">Mix It Up</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lorem-ipsum">
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Welcome to <strong>Designer Hub</strong>, your ultimate playground on Myntra! Designed for both budding designers and fashion enthusiasts, this platform eliminates the need for traditional mockups.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;"><strong><em>Mix It Up</em></strong> allows you to browse through Myntra's exquisite collection to craft your perfect outfit. Here's how it works:</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Inspiration Gallery</strong>: Start by browsing our pre-generated designs in the Inspiration Gallery.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Choose Your Canvas</strong>: Select a silhouette that speaks to you. This will be the foundation of your custom design.</p>        
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Add Your Flair</strong>: Pick a style that catches your eye. This will infuse your chosen silhouette with color, pattern, and personality.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Design It!</strong>: With just a click, watch as AI technology blends your chosen silhouette and style into a one-of-a-kind fashion piece.</p>       
        <p style="font-size: 16px; line-height: 1.6; color: #29303E; text-align: center;">Ready to create? Let's Mix It Up!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    silhouettes = get_image_list("silhouettes")
    styles = get_image_list("styles")
    pre_generated_outputs = get_image_list("outputs")



    st.markdown('<h3 style="color: #F05524; text-align: center; font-size: 24px;">Inspiration Gallery</h3>', unsafe_allow_html=True)
    st.markdown("<div class='carousel-container'><div class='carousel'>", unsafe_allow_html=True)

    st.markdown('<div class="carousel-container">', unsafe_allow_html=True)

    output_images = sorted(list(pre_generated_outputs.items()))
    current_image_index = st.session_state.get('current_image_index', 0)

    col1, col2, col3 = st.columns([1, 3, 1]) 

    with col1:
        if st.button("Previous"):
            current_image_index = (current_image_index - 1) % len(output_images)

    with col2:
        name, path = output_images[current_image_index]
        st.image(Image.open(path), caption=name, width=500, use_column_width=False)

    with col3:
        if st.button("Next"):
            current_image_index = (current_image_index + 1) % len(output_images)

    st.session_state['current_image_index'] = current_image_index
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)



    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<span class="upload-label">Select Silhouette</span>', unsafe_allow_html=True)
        silhouette_options = list(silhouettes.keys())
        content_file = st.selectbox("Choose a silhouette", silhouette_options, key="silhouette")
        if content_file:
            content_path = silhouettes[content_file]
            content_img = Image.open(content_path).convert('RGB')
            st.image(content_img, caption=content_file, width=500, use_column_width=False, output_format="JPEG")

    with col2:
        st.markdown('<span class="upload-label">Select Style</span>', unsafe_allow_html=True)
        style_options = sorted(list(styles.keys())) 
        style_file = st.selectbox("Choose a style", style_options, key="style")
        if style_file:
            style_path = styles[style_file]
            style_img = Image.open(style_path).convert('RGB')
            st.image(style_img, caption=style_file, use_column_width=True, output_format="JPEG")

    if st.button("Design It!", key="design_button", help="Click to design your image"):
        if content_file and style_file:
            with st.spinner("Designing your image..."):
                try:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    
                    content_tensor, style_tensor = utils2.load_images(content_path, style_path, device)
                    output_tensor = perform_style_transfer(content_tensor, style_tensor)
                    output_pil = utils2.tensor_to_pil(output_tensor)
                    st.image(output_pil, caption="Your Styled Design",width=800, use_column_width=False, output_format="PNG")
            
                except Exception as e:
                    st.error(f"An error occurred during the style transfer process: {str(e)}")
                    st.exception(e)
        else:
            st.warning("Please select both a silhouette and a style before clicking 'Design It!'")

    st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()