import streamlit as st
import torch
import utils
import style_transfer
from PIL import Image
import os

def get_image_list(folder):
    image_dir = os.path.join(os.path.dirname(__file__), '..', 'images', folder)
    st.write(f"Looking for images in: {image_dir}")
    
    if not os.path.exists(image_dir):
        st.error(f"Directory not found: {image_dir}")
        return {}
    
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return {f"Image {i+1}": os.path.join(image_dir, f) for i, f in enumerate(images)}

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

    # Inspiration Gallery
    st.subheader("Inspiration Gallery")
    cols = st.columns(3)
    for i, (name, path) in enumerate(list(pre_generated_outputs.items())[:9]):  # Display up to 9 images
        with cols[i % 3]:
            try:
                st.image(Image.open(path), caption=name, use_column_width=True)
            except Exception as e:
                st.error(f"Error loading image {name}: {str(e)}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Select Silhouette")
        silhouette_options = list(silhouettes.keys())
        if silhouette_options:
            content_file = st.selectbox("Choose a silhouette", silhouette_options, key="silhouette")
            try:
                st.image(Image.open(silhouettes[content_file]), caption=content_file)
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
                st.image(Image.open(styles[style_file]), caption=style_file)
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
                    st.image(output_pil, caption="Your Styled Design", width=600, use_column_width=False)
                except Exception as e:
                    st.error(f"An error occurred during the style transfer process: {str(e)}")

if __name__ == "__main__":
    main()