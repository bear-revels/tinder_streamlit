import streamlit as st

class Home:
    def __init__(self, db):
        """Initialize the Home class with a database instance."""
        self.db = db

    def display_home_page(self):
        """Display the home page with navigation tiles."""
        col1,col2 = st.columns(2)
        with col1:
            st.video("./animations/Olga.mp4", format="video/mp4")
            #display animation at specific place via COLUMNS
            col3, col4, col5, col6 = st.columns(4)
            with col3:
                if st.button("🎮 Facemash GAME"):
                    st.switch_page("./pages/1_🎮_Facemash_GAME.py")
            with col4:
                if st.button("🎮 Tinder GAME"):
                    st.switch_page("./pages/1_🎮_Tinder_GAME.py")
            with col5:
                if st.button("⬆️ Loading Images"):
                    st.switch_page("./pages/2_⬆️_Contribute.py")
            with col6:
                if st.button("🏆 Leader-board"):
                    st.switch_page("./pages/3_🏆_Leaderboard.py")
        with col2:
            st.write("  ")
            st.write("🚀 Dive into the exciting world where AI creativity meets interactive gaming! Embark on a journey through a digital realm where imagination and excitement know no bounds.")
            st.write("🎨 Immerse yourself in a universe where every pixel shines with AI-generated brilliance. Experience a vibrant symphony of colors, shapes, and textures, all crafted by the endless creativity of artificial intelligence.")
            st.write("🌟 Test your eye for art in our thrilling game of visual mastery. Your mission? Select the true masterpieces from an array of AI-generated images. Earn points, climb the ranks, and become a digital art connoisseur.")
            st.write("🏆 Conquer the game and join the elite on our leaderboard. Flaunt your achievements, enjoy your victory, and inspire others.")
            st.write("🔥 So, what are you waiting for? Step into the future of gaming where innovation thrives and creativity reigns supreme. Join us now and unleash your inner visionary!")


        
        st.sidebar.subheader("Acknowledgements")
        st.sidebar.write("This project was developed by the dedicated students of Becode Ghent:")
        st.sidebar.write("Bear, Caroline, Nathalie, Niels")

        st.sidebar.write("We extend our heartfelt thanks to the entire #Arai6 team for their invaluable contribution in generating the images.")
        st.sidebar.subheader("Special Thanks")
        st.sidebar.write("We are grateful to all our colleagues and mentors for their guidance and inspiration.")
        st.sidebar.subheader("Copyright")
        st.sidebar.write("© 2024 Becode Ghent. All rights reserved")


