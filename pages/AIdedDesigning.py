import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["image-gen-key"]

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
        background-color: #FD913C;
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
</style>
""", unsafe_allow_html=True)

def generate_image(prompt):
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            n=1
        )
        image_url = response['output']['url']
        return image_url
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def create_image_variations(image):
    try:
        response = openai.Image.create_variation(
            model="dall-e-3",
            image=image,
            n=4
        )
        return [variation['output']['url'] for variation in response['data']]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.markdown("""
    <div class="header">
        <div class="title">StyleUp</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="center-title">AIded Designing</h1>', unsafe_allow_html=True)
    st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

    st.markdown("""
    Let DALL-E generate a unique look. Explore the possibilities of AI-generated fashion and find inspiration for your next design.
    """)

    cloth_type = st.selectbox("Select clothing type", ["T-shirt", "Dress", "Pants", "Jacket", "Skirt"])
    color = st.color_picker("Select color", "#000000")
    pattern = st.selectbox("Select pattern", ["Solid", "Striped", "Floral", "Geometric", "Abstract"])

    if st.button("Generate Design"):
        prompt = f"A {color} {pattern.lower()} {cloth_type.lower()} design, fashion illustration style"
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
    st.markdown('<div class="footer">© 2024 StyleUp. All rights reserved.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
