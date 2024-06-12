import streamlit as st

page_bg_img ="""
<style>
[data-test-id="stAppViewContainer"] {
background-image: url("https://drive.google.com/file/d/19X7ua2KP-KHydypkwEZHYDudXuR1hu1v/view?usp=drive_link");
background-size: cover;

}

[data-test-id="stHeader"] {
background-color : rgba(0,0,0,0);


}



</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.title ("TEST backgrounds")