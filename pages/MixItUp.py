import streamlit as st
import torch
import utils
import style_transfer
from PIL import Image
import os

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
    padding: 20px 30px; /* Adjust padding as needed */
    display: flex;
    align-items: center;
    z-index: 1000;
}

.header .title {
    font-size: 18; /* Adjust font size */
    font-weight: bold;
    color: #F13AB1;
    margin-right: auto; /* Align title to the left */
}

    .stButton>button {
    background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 25px; /* Adjust border radius for a rounded button */
    padding: 16px 32px; /* Adjust padding for button size */
    margin: 0 auto; /* Center the button */
    display: block; /* Ensure it's a block element for margin auto to work */
    font-size: 18px; /* Adjust font size */
    cursor: pointer;
                
}
.stButton>button:hover {
    background-color: #FD913C;
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
            .color-strip {
    height: 5px;
    background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
    margin: 20px 0; /* Adjust margin to add spacing around the color strip */
}
        .footer {
        text-align: center;
        padding: 20px;
        color: #29303E;
        font-weight: 300;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<div class="header">
    <div class="title">StyleUp</div>
</div>
""", unsafe_allow_html=True)

def get_image_list(folder):
    image_dir = os.path.join(os.path.dirname(__file__), '..', 'images', folder)    
    images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return {os.path.splitext(f)[0]: os.path.join(image_dir, f) for f in images}

def main():

    st.markdown('<h1 class="center-title" style="font-size: 40px;">DESIGNER HUB</h1>', unsafe_allow_html=True)

    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: #F13AB1; text-align: center; font-size: 28px;">Mix It Up</h3>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lorem-ipsum">
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Welcome to <strong>Designer Hub</strong>, your ultimate playground on Myntra! Designed for both budding designers and fashion enthusiasts, this platform eliminates the need for traditional mockups.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;"><strong><em>Mix It Up</em></strong> allows you to browse through Myntra's exquisite collection to craft your perfect outfit. Here's how it works:</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Inspiration Gallery<strong>: Start by browsing our pre-generated designs in the Inspiration Gallery. Let these unique creations spark your imagination and guide your style choices.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Choose Your Canvas<strong>:Select a silhouette that speaks to you. This will be the foundation of your custom design.</p>        
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Add Your Flair<strong>:Pick a style that catches your eye. This will infuse your chosen silhouette with color, pattern, and personality.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E;"><strong>Design It!<strong>:With just a click, watch as AI technology blends your chosen silhouette and style into a one-of-a-kind fashion piece.</p>       
        <p style="font-size: 16px; line-height: 1.6; color: #29303E; text-align: center;">Ready to create? Let's Mix It Up!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    silhouettes = get_image_list("silhouettes")
    styles = get_image_list("styles")
    pre_generated_outputs = get_image_list("outputs")

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


    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

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

    st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()