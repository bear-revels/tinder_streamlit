import streamlit as st
import os


with open('./animations/style.css') as f:
           st.markdown(f'<style>(f.read)<style>', unsafe_allow_html=True)

# Password for accessing the page
PASSWORD = "test"

# Initialize session state
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'upload_mode' not in st.session_state:
    st.session_state.upload_mode = None
if 'upload_again' not in st.session_state:
    st.session_state.upload_again = False
if 'last_image_number' not in st.session_state:
    st.session_state.last_image_number = 0

def main():
    st.markdown("""
        <style>
        /* Change the background of the main area */
        .stapp {
            background: img(./animations/background.avif);
            background-size: cover;
        }
        </style>
        """, unsafe_allow_html=True)
    if not st.session_state.name:
        st.title("Enter your name")
        name = st.text_input("Name")
        if st.button("Submit"):
            if name:
                st.session_state.name = name
                st.experimental_rerun()
            else:
                st.error("Please enter your name.")
    elif not st.session_state.authenticated:
        st.title("Authentication Required")
        password = st.text_input("Enter Password", type="password")
        if st.button("Submit"):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Invalid password. Please try again.")
    else:
        if st.session_state.upload_again:
            st.session_state.upload_again = False
            st.session_state.upload_mode = None
            st.experimental_rerun()
        
        if st.session_state.upload_mode is None:
            st.title("Select Image Type")
            if st.button("AI"):
                st.session_state.upload_mode = "AI"
                st.experimental_rerun()
            if st.button("Real"):
                st.session_state.upload_mode = "Real"
                st.experimental_rerun()
        
        if st.session_state.upload_mode:
            st.title(f"Upload {st.session_state.upload_mode} Images")
            uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
            if uploaded_files:
                if st.button("Submit"):
                    save_uploaded_files(uploaded_files, st.session_state.upload_mode, st.session_state.name)
                    st.success("Thank you! Your images have been uploaded!")
                elif st.button("Upload Another Image"):
                    st.session_state.upload_again = True
                    st.experimental_rerun()
                

def save_uploaded_files(uploaded_files, label, username):
    # Ensure the uploads directory exists
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')

    for i, uploaded_file in enumerate(uploaded_files, start=1):
        st.session_state.last_image_number += 1
        file_name = f"{label}_{username}_image_{st.session_state.last_image_number}.jpg"
        with open(f"./uploads/{file_name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Saved file: {file_name} in ./uploads")

if __name__ == "__main__":
    main()
