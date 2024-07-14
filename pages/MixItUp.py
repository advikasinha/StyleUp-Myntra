import streamlit as st
import torch
import utils
import style_transfer
import requests
from io import BytesIO
from PIL import Image

# Base URL for your GitHub raw content
BASE_URL = "https://raw.githubusercontent.com/advikasinha/StyleUp-Myntra/main/images/"
def get_image_list(folder):
    url = f"{BASE_URL}{folder}/"
    response = requests.get(url)
    if response.status_code == 200:
        files = [f for f in response.text.split('\n') if f.endswith(('.jpg', '.png', '.jpeg'))]
        return {f"Image {i+1}": f"{url}{f}" for i, f in enumerate(files)}
    else:
        st.error(f"Failed to fetch images from {url}")
        return {}

silhouettes = get_image_list("silhouettes")
styles = get_image_list("styles")
pre_generated_outputs = get_image_list("outputs")

def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def main():
    st.title("Fashion Style Transfer")

    # Carousel for pre-generated outputs
    st.subheader("Inspiration Gallery")
    cols = st.columns(3)
    for i, (name, url) in enumerate(list(pre_generated_outputs.items())[:9]):  # Display up to 9 images
        with cols[i % 3]:
            st.image(load_image(url), caption=name, use_column_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Select Silhouette")
        content_file = st.selectbox("Choose a silhouette", list(silhouettes.keys()), key="silhouette")
        st.image(load_image(silhouettes[content_file]), caption=content_file)

    with col2:
        st.subheader("Select Style")
        style_file = st.selectbox("Choose a style", list(styles.keys()), key="style")
        st.image(load_image(styles[style_file]), caption=style_file)

    if content_file and style_file:
        if st.button("Design It!", key="design_button", help="Click to design your image"):
            with st.spinner("Designing your image..."):
                try:
                    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                    content_img = load_image(silhouettes[content_file])
                    style_img = load_image(styles[style_file])
                    content_tensor, style_tensor = utils.load_images(content_img, style_img, device)
                    output_c = style_transfer.run_style_transfer(content_tensor, style_tensor, num_steps=500)
                    output = style_transfer.enhance_silhouette(output_c, content_tensor)
                    output_pil = utils.tensor_to_pil(output)
                    st.image(output_pil, caption="Your Styled Design", width=600, use_column_width=False)
                except Exception as e:
                    st.error(f"An error occurred during the style transfer process: {str(e)}")

if __name__ == "__main__":
    main()