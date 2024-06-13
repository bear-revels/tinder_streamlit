import streamlit as st

class Home:
    def __init__(self, db):
        """Initialize the Home class with a database instance."""
        self.db = db

    def display_home_page(self):
        """Display the home page with navigation tiles."""
        st.write("Welcome to the Arcade!")
        st.write("🚀 Welcome to the cutting-edge intersection of AI creativity and interactive gaming! Get ready to embark on an electrifying journey through a digital realm where imagination knows no bounds and excitement knows no limits.")
        st.write("🎨 Dive into a mesmerizing universe where every pixel pulsates with the brilliance of AI-generated imagery. Immerse yourself in a symphony of colors, shapes, and textures, each crafted by the boundless creativity of artificial intelligence.")
        st.write("🌟 But wait, there's more! Prepare to put your discerning eye to the test in our exhilarating game of visual mastery. Your mission? To sift through a stunning array of AI-generated images and select the true masterpieces from the crowd. With each astute choice, you'll earn points, climb the ranks, and solidify your status as a connoisseur of digital art.")
        st.write("🏆 And that's not all – once you've conquered the game, take your place among the elite on our prestigious leaderboard. Flaunt your achievements, bask in the glory of victory, and inspire others to follow in your footsteps.")
        st.write("🔥 So, what are you waiting for? Step into the future of gaming, where innovation thrives, creativity reigns supreme, and every click brings you closer to greatness. Join us now and unleash your inner visionary on an adventure like no other!")

        #display animation at specific place via COLUMNS
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("Play")
            st.page_link("./pages/1_🎮_Facesmash_GAME.py", label="Facesmash",icon="🎮")
        
        with col2:
            st.write("Play")
            st.page_link("./pages/1_🎮_Tinder_GAME.py", label="Tinder",icon="🎮")

        with col3:
            st.write("Contribute")
            st.page_link("./pages/2_⬆️_Contribute.py", label="upload",icon="⬆️")
        with col4:
            st.write("Leaderboard")
            st.page_link("./pages/3_🏆_Leaderboard.py", label="board",icon="🏆")
        
        st.sidebar.write("Made by students @BecodeGhent:")
        st.sidebar.write("Bear, Caroline, Nathalie, Niels")
        st.sidebar.write("Shout out to the other collegues for generating the images:")
        st.sidebar.write("??")
        st.sidebar.write("©️copyrights")
