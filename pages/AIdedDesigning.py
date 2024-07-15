import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import os
import time

#OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai"]["image-gen-key"])
st.set_page_config(page_title="DesignerHub", layout="wide")

def load_css():
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def generate_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        error_message = str(e)
        if "billing_hard_limit_reached" in error_message:
            st.markdown('<div style="background-color: #29303e; padding: 10px; border-radius: 5px;">'
                        '<p style="color: f13ab1; text-align: center;">Sorry, we\'ve reached our daily limit for image generation.</p>'
                        '</div>', unsafe_allow_html=True)
        else:
            st.error(f"An error occurred: {error_message}")
        return None

def create_image_variations(image):
    try:
        response = client.images.create_variation(
            image=image,
            n=4,
            size="1024x1024"
        )
        return [variation.url for variation in response.data]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    load_css()

    st.markdown("""
    <div class="header">
        <div class="title">StyleUp</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="center-title" style="font-size: 40px;">DESIGNER HUB</h1>', unsafe_allow_html=True)
    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    st.markdown('<h3 style="color: #F13AB1; text-align: center; font-size: 28px;">AI-ded Designing</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lorem-ipsum">
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Welcome to <strong>Designer Hub</strong>, your ultimate playground on Myntra! Designed for both budding designers and fashion enthusiasts, this platform eliminates the need for traditional mockups.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;"><strong><em>AI-ded Designing</em></strong> lets DALL-E generate a unique look, allowing you to explore the possibilities of AI-generated fashion and find inspiration for your next design!</p>
        <p style="font-size: 16px; line-height: 1.6; color: #333;">Make your selections to bring your vision to life. View the generated design and create variations, exploring multiple renditions of your unique style.</p>
        <p style="font-size: 16px; line-height: 1.6; color: #29303E; text-align: center;">Craft stunning looks with the power of AI magic!</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<span class="upload-label">Select clothing type</span>', unsafe_allow_html=True)
        cloth_type = st.selectbox("", ["T-shirt", "Dress", "Pants", "Jacket", "Skirt"])
    with col2:
        st.markdown('<span class="upload-label">Select color</span>', unsafe_allow_html=True)
        color = st.color_picker("", "#000000")
    with col3:
        st.markdown('<span class="upload-label">Select pattern</span>', unsafe_allow_html=True)
        pattern = st.selectbox("", ["Solid", "Striped", "Floral", "Geometric", "Abstract"])

    custom_specification = st.text_area("Add any custom specifications", placeholder="e.g., Vintage style, asymmetrical cuts")

    if st.button("Generate Design"):
        prompt=f'Fashion illustration of {pattern.lower()} {color} colored {cloth_type.lower()}, high quality, detailed design, fashion illustration, abstract, professional, vibrant colors, artistic style, elegant, flowing fabric, intricate details, beautiful, modern, colorful, fashion design, stylish, high-res, intricate patterns, fashion illustration style, vibrant lighting'
        image_url = generate_image(prompt)
        if image_url is None:
            st.markdown("""<div class='lorem-ipsum'> <p style="font-size: 16px; line-height: 1.6; color: #333;">Explore our previous creations by the similar prompts meanwhile: </p>  
                </div>""", unsafe_allow_html=True)
                
            # Get the current script's directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct the path to the DALL-E-gen folder
            image_folder = os.path.join(current_dir, "DALL-E-gen")
            
            # Get all image files from the DALL-E-gen folder
            image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if image_files:
                image_container = st.empty()
                while True:
                    for image_file in image_files:
                        image_path = os.path.join(image_folder, image_file)
                        img = Image.open(image_path)
                        img.thumbnail((200, 200))  # Resize image to 500px max
                        image_container.image(img, use_column_width=True)
                        time.sleep(3)  # Display each image for 3 seconds
            else:
                st.write("No images found in the DALL-E-gen folder.")

        if image_url:
            st.image(image_url, caption="Generated Design", use_column_width=True)

            st.markdown("### Generate Variations")
            if st.button("Create Variations"):
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img_byte_arr = BytesIO()
                img.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                variations = create_image_variations(img_byte_arr)
                if variations:
                    cols = st.columns(2)
                    for i, var_url in enumerate(variations):
                        cols[i % 2].image(var_url, caption=f"Variation {i+1}", use_column_width=True)


    st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
