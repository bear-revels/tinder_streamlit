import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie

class Lottie:
    def __init__(self):
        pass

    @staticmethod
    def load_from_file(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    @staticmethod
    def load_from_url(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    @staticmethod
    def display_lottie(lottie_data, quality="heigh", height=None, width=None, key=None):
        st_lottie(
            lottie_data,
            quality=quality,
            height=height,
            width=width,
            key=key
        )


#usage
lottie = Lottie()
lottie_file = lottie.load_from_file("animations/hourglass.json")

st.title("Test Lottie Animation")
lottie.display_lottie(lottie_file)