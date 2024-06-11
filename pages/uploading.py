import streamlit as st

# Password for accessing the page
PASSWORD = "BeCode24"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def main():
    # Check if the user is authenticated
    if st.session_state.authenticated:
        # Display the upload form
        st.title("Upload Image")
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            label = st.selectbox("Is this image AI-generated or real?", ("Select", "AI", "Real"))
            if st.button("Submit"):
                if label != "Select":
                    # Store the image
                    save_uploaded_file(uploaded_file)
                    st.success("Image uploaded successfully!")
                else:
                    st.error("Please select if the image is AI-generated or real.")
    else:
        # Display the password form
        st.title("Authentication Required")
        password = st.text_input("Enter Password", type="password")
        if st.button("Submit"):
            if password == PASSWORD:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Invalid password. Please try again.")

def save_uploaded_file(uploaded_file):
    # Save the uploaded file
    with open(f"./images/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success("Saved file :{} in ./images".format(uploaded_file.name))

if __name__ == "__main__":
    main()
