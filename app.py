import streamlit as st

st.set_page_config(page_title="DesignerHub")

st.title("Welcome to DesignerHub")

st.write("Explore our innovative fashion design tools and features:")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Style Transfer")
    st.write("Transform your designs with AI-powered style transfer.")
    if st.button("Try Style Transfer"):
        st.switch_page("pages/CreateYourOwn/app.py")

with col2:
    st.subheader("Feature 2")
    st.write("Let DALL-E generate a unique look.")
    if st.button("Explore Feature 2"):
        st.switch_page("pages/AIdedDesigining/app.py")

with col3:
    st.subheader("Feature 3")
    st.write("Choose from Myntra's own exquisite collection.")
    if st.button("Discover Feature 3"):
        st.switch_page("pages/MixItUp/app.py")

st.markdown("---")
st.write("DesignerHub: Empowering fashion designers with cutting-edge AI tools.")