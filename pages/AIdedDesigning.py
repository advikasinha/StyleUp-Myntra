import streamlit as st
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

# Set your OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai"]["image-gen-key"])
st.set_page_config(page_title="DesignerHub", layout="wide")

# Custom CSS (same as previous pages)
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
        padding: 10px 10px;
        display: flex;
        align-items: center;
        z-index: 1000;
    }
    .center-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin: 0;
        color: #29303E;
    }
    .header .title {
        font-size: 40px;
        font-weight: bold;
        color: #F13AB1;
        margin-right: auto;
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
        background-color: #29303E;
    }
    .color-strip {
        height: 5px;
        background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
        margin: 20px 0;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #29303E;
        font-weight: 300;
    }
    .lorem-ipsum {
    background-color: #f0f0f0;
    padding: 20px;
    margin: 20px 0;
    color: #29303E;
}
            .upload-label {
    color: black; 
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

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
            st.error("We've reached our daily limit for image generation. Please try again tomorrow or contact support.")
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
        prompt = f"A {color} {pattern.lower()} {cloth_type.lower()} design, {custom_specification}, fashion illustration style"
        image_url = generate_image(prompt)

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

    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)
    st.markdown("""
<div class="footer">
    DesignerHub: Empowering fashion designers with cutting-edge AI tools.
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
