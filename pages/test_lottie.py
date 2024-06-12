import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

class Lottie:
    def __init__(self):
        pass
    #opening the file with animation
    @staticmethod
    def load_from_file(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    #opening the file from animation
    # @staticmethod
    # def load_from_url(url: str):
    #     r = requests.get(url)
    #     if r.status_code != 200:
    #         return None
    #     return r.json()

    #changing the proportions/ratio of animation
    @staticmethod
    def display_lottie(lottie_data, width=None, height=None, key=None):
        # If both width and height are not provided, use default values
        if width is None and height is None:
            width = 300  # default width
        if width is not None and height is None:
            # Calculate height to maintain aspect ratio
            aspect_ratio = Lottie.calculate_aspect_ratio(lottie_data)
            height = int(width / aspect_ratio)
        elif height is not None and width is None:
            # Calculate width to maintain aspect ratio
            aspect_ratio = Lottie.calculate_aspect_ratio(lottie_data)
            width = int(height * aspect_ratio)

        
        st_lottie(
            lottie_data,
            height=height,
            width=width,
            key=key
        )
    #calculating existant ratio of amnimation
    @staticmethod
    def calculate_aspect_ratio(lottie_data):
        # Get the width and height from the first frame of the animation
        try:
            first_frame = lottie_data['layers'][0]
            width = first_frame['w']
            height = first_frame['h']
            return width / height
        except (KeyError, IndexError):
            # Fallback to a default aspect ratio if unable to determine
            return 1.0


#usage
lottie = Lottie()
lottie_file = lottie.load_from_file("./animations/hourglass.json")

#st.title("Test Lottie Animation")
#lottie.display_lottie(lottie_file, width=100)

#display animation at specific place via COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Left Column")

with col2:
    st.write("Center Column")
    lottie.display_lottie(lottie_file, width=100)  

with col3:
    st.write("Right Column")

#display the animation at a specific place in streamlit via CONTAINER:
with st.container():
    st.write("This is a container with the Lottie animation below:")
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <div>
                {st_lottie(lottie_file, width=100)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )