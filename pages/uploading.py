import streamlit as st
import os

# Password for accessing the page
PASSWORD = "BeCode24"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'upload_mode' not in st.session_state:
    st.session_state.upload_mode = None
if 'upload_again' not in st.session_state:
    st.session_state.upload_again = False

def main():
    if st.session_state.authenticated:
        if st.session_state.upload_mode is None or st.session_state.upload_again:
            st.session_state.upload_again = False
            st.title("Select Image Type")
            if st.button("AI"):
                st.session_state.upload_mode = "AI"
            if st.button("Real"):
                st.session_state.upload_mode = "Real"

        if st.session_state.upload_mode:
            st.title(f"Upload {st.session_state.upload_mode} Image")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
                if st.button("Submit"):
                    save_uploaded_file(uploaded_file, st.session_state.upload_mode)
                    st.success("Thank you! Your image has been uploaded!")
                    if st.button("Upload Another Image"):
                        st.session_state.upload_again = True
                        st.session_state.upload_mode = None
                        st.experimental_rerun()
    else:
        st.title("Authentication Required")
        password = st.text_input("Enter Password", type="password")
        if st.button("Submit"):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Invalid password. Please try again.")

def save_uploaded_file(uploaded_file, label):
    # Ensure the uploads directory exists
    if not os.path.exists('./uploads'):
        os.makedirs('./uploads')
    
    # Save the uploaded file
    with open(f"./uploads/{label}_{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"Saved file: {uploaded_file.name} in ./uploads")

if __name__ == "__main__":
    main()
