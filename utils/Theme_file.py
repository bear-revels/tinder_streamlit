import json
import streamlit as st

class ThemeManager:
    def __init__(self, theme_file):
        self.theme_file = theme_file
        self.themes = self.load_themes()
        #self.current_theme = self.themes.get("default", {})

    def load_themes(self):
        with open(self.theme_file, 'r') as file:
            return json.load(file)

    def apply_theme(self, theme_name):
        if theme_name in self.themes:
            self.current_theme = self.themes[theme_name]
            self._apply_custom_css()
        else:
            raise ValueError(f"Theme '{theme_name}' not found in {self.theme_file}")

    def _apply_custom_css(self):
        st.markdown(
            f"""
            <style>
            .reportview-container {{
                background-color: {self.current_theme['backgroundColor']};
                color: {self.current_theme['textColor']};
                font-family: "{self.current_theme['font']}";
            }}
            .sidebar .sidebar-content {{
                background-color: {self.current_theme['secondaryBackgroundColor']};
                color: {self.current_theme['textColor']};
            }}
            .stButton > button {{
                color: {self.current_theme['buttonText']};
                background-color: {self.current_theme['buttonColor']};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


    def get_property(self, property_name):
        return self.current_theme.get(property_name)
