# import streamlit as st
# import torch
# from PIL import Image
# import style_transfer
# import utils
# import os

# st.set_page_config(page_title="DesignerHub", layout="wide")

# def main():
#     # Custom CSS with all Myntra logo colors
#     st.markdown("""
#     <style>
#     .stApp {
#         background-color: #FFFFFF;
#     }
#     .header {
#         padding: 10px 16px;
#         background: #29303E;
#         color: white;
#         top: 0;
#         width: 100%;
#         z-index: 1000;
#         display: flex;
#         align-items: center;
#     }
#     .app-name {
#         font-size: 24px;
#         color: #FD913C;
#         margin-left: 20px;
#     }
#     .content {
#         padding: 16px;
#         margin-top: 10px;
#     }
#     .sidebar {
#         background-color: #f9f9f9;
#         padding: 20px;
#         border-right: 1px solid #e9e9e9;
#     }
#     .main-content {
#         padding: 20px;
#     }
#     .product-title {
#         font-size: 24px;
#         font-weight: bold;
#         margin-bottom: 10px;
#         color: #29303E;
#     }
#     .stButton>button {
#         background-color: #F13AB1;
#         color: white;
#         font-weight: bold;
#         border: none;
#         border-radius: 4px;
#         padding: 10px 20px;
#     }
#     .stButton>button:hover {
#         background-color: #E72744;
#     }
#     .upload-text {
#         color: #29303E;
#         font-weight: bold;
#     }
#     .color-strip {
#         height: 5px;
#         background: linear-gradient(to right, #F13AB1, #E72744, #FD913C, #F05524, #29303E);
#         margin-bottom: 20px;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Header with Myntra logo image and DesignerHub text
#     col1, col2 = st.columns([1, 5])
#     with col1:
#         logo_path = "Myntra-Logo.png"
#         st.image(logo_path, width=100)
        
#     with col2:
#         st.markdown('<span class="app-name">StyleUp</span>', unsafe_allow_html=True)

#     st.markdown('<div class="color-strip"></div>', unsafe_allow_html=True)

#     col1, col2 = st.columns([1, 2])

#     with col1:
#         st.markdown('<div class="sidebar">', unsafe_allow_html=True)
#         st.markdown('<div class="product-title">Style Transfer</div>', unsafe_allow_html=True)
#         st.markdown('<p class="upload-text">Choose a content image</p>', unsafe_allow_html=True)
#         content_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="content_upload")
#         st.markdown('<p class="upload-text">Choose a style image</p>', unsafe_allow_html=True)
#         style_file = st.file_uploader("", type=["png", "jpg", "jpeg"], key="style_upload")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col2:
#         st.markdown('<div class="main-content">', unsafe_allow_html=True)
#         if content_file is not None and style_file is not None:
#             col_a, col_b = st.columns(2)
#             with col_a:
#                 content_image = Image.open(content_file)
#                 st.image(content_image, caption="Content Image", use_column_width=True)
#             with col_b:
#                 style_image = Image.open(style_file)
#                 st.image(style_image, caption="Style Image", use_column_width=True)
        
#             if st.button("Generate Styled Image", key="generate_button"):
#                 with st.spinner("Generating styled image..."):
#                     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#                     content_img, style_img = utils.load_images(content_file, style_file, device)
#                     output_c = style_transfer.run_style_transfer(content_img, style_img, num_steps=500)
#                     output = style_transfer.enhance_silhouette(output_c, content_img)
#                     output_pil = utils.tensor_to_pil(output)
#                     st.image(output_pil, caption="Styled Image", use_column_width=True)
#         else:
#             st.markdown('<p class="upload-text">Upload both content and style images to see the result.</p>', unsafe_allow_html=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

import streamlit as st
import torch
from PIL import Image
import style_transfer
import utils
import os
import base64

st.set_page_config(page_title="DesignerHub", layout="wide")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    # Get the base64 string of the logo
    logo_path = "myntra_logo.png"
    if os.path.exists(logo_path):
        logo_base64 = get_base64_of_bin_file(logo_path)
    else:
        st.error("Logo file not found. Please make sure 'myntra_logo.png' is in the same directory as this script.")
        return

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
        color: white;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        z-index: 1000;
    }
    .logo-image {
        height: 30px;
        margin-right: 10px;
    }
    .app-name {
        font-size: 24px;
        color: #FD913C;
        font-weight: bold;
    }
    .content {
        margin-top: 60px;
        padding: 16px;
    }
    .center-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin: 20px 0;
        color: #29303E;
    }
    .lorem-ipsum {
        background-color: #f9f9f9;
        padding: 20px;
        margin: 20px 0;
        border-radius: 5px;
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
    </style>
    """, unsafe_allow_html=True)

    # Header with Myntra logo image and StyleUp text
    st.markdown(f"""
    <div class="header">
        <img src="data:image/png;base64,{logo_base64}" class="logo-image">
        <span class="app-name">StyleUp</span>
    </div>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown('<div class="content">', unsafe_allow_html=True)

    # DESIGNER HUB title
    st.markdown('<h1 class="center-title">DESIGNER HUB</h1>', unsafe_allow_html=True)

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