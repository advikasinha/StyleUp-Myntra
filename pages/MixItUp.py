import streamlit as st
import torch
import utils
import style_transfer
from PIL import Image
import os

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f0f5;
        padding: 2rem;
    }
    .stButton>button {
        background-color: #F13AB1;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #E72744;
    }
    .stSelectbox {
        background-color: white;
        border-radius: 4px;
        border: 1px solid #ddd;
    }
    h1 {
        color: #29303E;
        text-align: center;
        padding-bottom: 1rem;
    }
    h2 {
        color: #F05524;
        padding-top: 1rem;
    }
    .stImage {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .carousel {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
    }
    .gallery-image {
        transition: transform 0.3s ease-in-out;
    }
    .gallery-image:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

def get_image_list(folder):
    image_dir = os.path.join(os.path.dirname(__file__), '..', 'images', folder)
    st.write(f"Looking for images in: {image_dir}")
    
    if not os.path.exists(image_dir):
        st.error(f"Directory not found: {image_dir}")
        return {}
    
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return {os.path.splitext(f)[0]: os.path.join(image_dir, f) for f in images}

def main():
    st.title("StyleUp Fashion Design")

    st.write("Attempting to load images...")

    silhouettes = get_image_list("silhouettes")
    styles = get_image_list("styles")
    pre_generated_outputs = get_image_list("outputs")

    st.write(f"Number of silhouettes found: {len(silhouettes)}")
    st.write(f"Number of styles found: {len(styles)}")
    st.write(f"Number of pre-generated outputs found: {len(pre_generated_outputs)}")

    if not silhouettes or not styles or not pre_generated_outputs:
        st.error("One or more image directories could not be found or are empty. Please check your file structure and paths.")
        return

    # Carousel for pre-generated outputs
    st.subheader("Inspiration Gallery")
    st.markdown("<div class='carousel'>", unsafe_allow_html=True)
    output_images = list(pre_generated_outputs.items())
    current_image_index = st.session_state.get('current_image_index', 0)
    
    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        if st.button("Previous"):
            current_image_index = (current_image_index - 1) % len(output_images)
    with col2:
        name, path = output_images[current_image_index]
        st.image(Image.open(path), caption=name, use_column_width=True, output_format="PNG")
    with col3:
        if st.button("Next"):
            current_image_index = (current_image_index + 1) % len(output_images)
    
    st.session_state['current_image_index'] = current_image_index
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Select Silhouette")
        silhouette_options = list(silhouettes.keys())
        if silhouette_options:
            content_file = st.selectbox("Choose a silhouette", silhouette_options, key="silhouette")
            try:
                st.image(Image.open(silhouettes[content_file]), caption=content_file, use_column_width=True, output_format="PNG")
            except Exception as e:
                st.error(f"Error loading silhouette image: {str(e)}")
        else:
            st.error("No silhouettes available")

    with col2:
        st.subheader("Select Style")
        style_options = list(styles.keys())
        if style_options:
            style_file = st.selectbox("Choose a style", style_options, key="style")
            try:
                st.image(Image.open(styles[style_file]), caption=style_file, use_column_width=True, output_format="PNG")
            except Exception as e:
                st.error(f"Error loading style image: {str(e)}")
        else:
            st.error("No styles available")

    if silhouette_options and style_options:
        if st.button("Design It!", key="design_button", help="Click to design your image"):
            with st.spinner("Designing your image..."):
                try:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    content_img = Image.open(silhouettes[content_file])
                    style_img = Image.open(styles[style_file])
                    content_tensor, style_tensor = utils.load_images(content_img, style_img, device)
                    output_c = style_transfer.run_style_transfer(content_tensor, style_tensor, num_steps=500)
                    output = style_transfer.enhance_silhouette(output_c, content_tensor)
                    output_pil = utils.tensor_to_pil(output)
                    st.image(output_pil, caption="Your Styled Design", width=600, use_column_width=False, output_format="PNG")
                except Exception as e:
                    st.error(f"An error occurred during the style transfer process: {str(e)}")

if __name__ == "__main__":
    main()