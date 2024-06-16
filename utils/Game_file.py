import streamlit as st
import random
from .Database_file import Database
from .Leaderboard_file import Leaderboard

class GameTinder:
    def __init__(self):
        """Initialize the Game class with a database instance."""
        self.db = Database()
        self.db.refresh_active_status()
        self.images = self.db.get_active_images()
        self.current_image_pair = []
        self.player_name = ""
        self.score = 0
        self.level = 1
        self.lives = 3
        if 'reviewed_images' not in st.session_state:
            st.session_state.reviewed_images = set()
        if 'displayed_image_ids' not in st.session_state:
            st.session_state.displayed_image_ids = set()

    def display_play_page(self):
        """Display the game play page."""
        st.title("Welcome to the Tinder GAME")
        st.subheader("Let's get started")

        player_name = st.text_input("Enter your name to start playing:", key="player_name")
        if player_name:
            self.player_name = player_name
            self.start_game()

    def start_game(self):
        """Start the game and handle game logic."""
        if "level" not in st.session_state:
            st.session_state.score = 0
            st.session_state.level = 1
            st.session_state.lives = 3
            st.session_state.page = "play"

        self.display_images()

    def display_images(self):
        """Display image selection interface."""
        real_image, genai_image = self.db.get_random_images()
        self.current_image_pair = [(real_image, 1), (genai_image, 0)]
        random.shuffle(self.current_image_pair)

        left_button_key = f"left_{st.session_state.level}"
        right_button_key = f"right_{st.session_state.level}"

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select Left Image", key=left_button_key):
                st.session_state.selected_image = self.current_image_pair[0]
                st.session_state.last_clicked = "left"
        with col2:
            if st.button("Select Right Image", key=right_button_key):
                st.session_state.selected_image = self.current_image_pair[1]
                st.session_state.last_clicked = "right"

        if "selected_image" in st.session_state:
            self.check_selection(st.session_state.selected_image)

    def check_selection(self, selected_image):
        """Check the user's selection and update the game state."""
        is_real_image = selected_image[1] == 1
        if is_real_image:
            st.session_state.score += 1
            st.session_state.level += 1
            st.write(f"Correct! Your current score: {st.session_state.score}")
            del st.session_state.selected_image  # Reset selection
            self.display_images()
        else:
            st.session_state.lives -= 1
            if st.session_state.lives > 0:
                st.write("Wrong! This image was real. Try again!")
                del st.session_state.selected_image  # Reset selection
                self.display_images()
            else:
                st.write("Game Over!")
                st.write(f"Your final score: {st.session_state.score}")
                self.update_leaderboard()
                st.session_state.page = "home"

    # def update_leaderboard(self):
    #     """Update the leaderboard with the player's score."""
    #     st.write("Updating leaderboard...")
    #     # Update leaderboard logic goes here, you can use your Database methods

    #     # Example:
    #     leaderboard = Leaderboard()  # Initialize your Leaderboard class
    #     leaderboard.add_score(self.player_name, st.session_state.score)

    #     # Display leaderboard
    #     st.write("Leaderboard:")
    #     leaderboard_data = leaderboard.get_leaderboard()
    #     for idx, entry in enumerate(leaderboard_data, start=1):
    #         st.write(f"{idx}. {entry['player_name']}: {entry['score']}")

    #     # Reset game state
    #     st.session_state.score = 0
    #     st.session_state.level = 1
    #     st.session_state.lives = 3
    #     st.session_state.page = "home"



# class GameTinder:
#     def __init__(self):
#         """Initialize the Game class with a database instance."""
#         #self.db = db
#         self.db = Database()
#         self.db.refresh_active_status()
#         self.images = self.db.get_active_images()
#         self.current_image_pair = random.sample(self.images, 2)
#         self.player_name = ""
#         self.match_count = 0
#         if 'reviewed_images' not in st.session_state:
#             st.session_state.reviewed_images = set()
#         if 'displayed_image_ids' not in st.session_state:
#             st.session_state.displayed_image_ids = set()

#     def display_play_page(self):
#         """Display the game play page."""
#         st.title("Welcom to the Tinder GAME")
#         st.subheader("Let's get started")

#         player_name = st.text_input("Enter your name to start playing:", key="player_name")
#         if player_name:
#             game_t = GameTinder()
#             game_t.player_name = player_name
#             if 'match_count' not in st.session_state:
#                 st.session_state.match_count = 0
#             if 'current_image_pair' not in st.session_state:
#                 st.session_state.current_image_pair = game_t.current_image_pair
#             GameTinder.start_game(game_t)


#     def start_game(self):
#         """Start the game and handle game logic."""
#         if "level" not in st.session_state:
#             st.session_state.level = 1
#             st.session_state.score = 0
#             st.session_state.timer = 30

#         real_image, genai_image = self.db.get_random_images()
#         images = [(real_image, 1), (genai_image, 0)]
#         random.shuffle(images)

#         #unique keys:
#         left_button_key = f"left_{st.session_state.level}"
#         right_button_key = f"right_{st.session_state.level}"

#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("Select Left Image", key=left_button_key):
#                 self.check_selection(images[0][1] == 1)
#             st.image(images[0][0][4], use_column_width=True)
#         with col2:
#             if st.button("Select Right Image", key=right_button_key):
#                 self.check_selection(images[1][1] == 1)
#             st.image(images[1][0][4], use_column_width=True)

#     def check_selection(self, is_real_image):
#         if is_real_image:
#             st.session_state.score += 1
#             st.session_state.level += 1
#             st.session_state.timer *= 0.9
#             st.write(f"Correct! Your current score: {st.session_state.score}")
#         else:
#             st.write("Wrong! Game Over!")
#             st.write(f"Your final score: {st.session_state.score}")
#             st.session_state.page = "home"
        
#         if st.session_state.page != "home":
#             self.start_game()


#     # def check_selection(self, is_real_image):
#     #     """Check the user's selection and update the game state."""
#     #     if is_real_image:
#     #         st.session_state.score += 1
#     #         st.session_state.level += 1
#     #         st.session_state.timer *= 0.9
#     #         st.write(f"Correct! Your current score: {st.session_state.score}")
#     #         self.start_game()
#     #     else:
#     #         st.write("Wrong! Game Over!")
#     #         st.write(f"Your final score: {st.session_state.score}")
#     #         st.session_state.page = "home"
  
class GameFacemash:
    """Class to handle the game functionality."""
    
    def __init__(self):
        self.db = Database()
        self.db.refresh_active_status()
        self.images = self.db.get_active_images()
        self.current_image_pair = random.sample(self.images, 2)
        self.player_name = ""
        self.match_count = 0
        if 'reviewed_images' not in st.session_state:
            st.session_state.reviewed_images = set()
        if 'displayed_image_ids' not in st.session_state:
            st.session_state.displayed_image_ids = set()
        
    @staticmethod
    def display_game_page():
        """Displays the game page."""
        st.title("Welcom to the FaceMash GAME")
        st.subheader("Let's get started")

        #video from youtube: why facemash?
        st.text("This game is based on the film The Social Network. ")
        video_url = "https://www.youtube.com/embed/kKqu1PgpjY4?start=54&end=81"
        video_html = f"""
        <iframe width="560" height="315" src="{video_url}" frameborder="0" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """
        st.markdown(video_html, unsafe_allow_html=True)

        player_name = st.text_input("Enter your name to start playing:", key="player_name")
        
        # if player_name:
        #     game = GameFacemash()
        #     game.player_name = player_name
        #     GameFacemash.play_game(game)
        if player_name:
            game = GameFacemash()
            game.player_name = player_name
            if 'match_count' not in st.session_state:
                st.session_state.match_count = 0
            if 'current_image_pair' not in st.session_state:
                st.session_state.current_image_pair = game.current_image_pair
            GameFacemash.play_game(game)
    
    @staticmethod
    def play_game(game):
        # """Main game loop to display images and capture player choices."""
        # st.write("Click the image you like better:")
        # col1, col2 = st.columns(2)

        # if 'current_image_pair' not in st.session_state:
        #     st.session_state.current_image_pair = game.current_image_pair
        
        # with col1:
        #     if st.button("Choose Image 1"):
        #         game.process_choice(st.session_state.current_image_pair[0], st.session_state.current_image_pair[1])
        # with col2:
        #     if st.button("Choose Image 2"):
        #         game.process_choice(st.session_state.current_image_pair[1], st.session_state.current_image_pair[0])

        # col1.image(st.session_state.current_image_pair[0]['filepath'])
        # col2.image(st.session_state.current_image_pair[1]['filepath'])
        """Main game loop to display images and capture player choices."""
        if st.session_state.match_count >= 9:
            GameFacemash.display_pause_screen(game)
        else:
            GameFacemash.display_progress_bar(st.session_state.match_count, 9)
            st.write("Click the image you like better:")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👇 Choose 👇"):
                    game.process_choice(st.session_state.current_image_pair[0], st.session_state.current_image_pair[1])
            with col2:
                if st.button(" 👇 Choose 👇"):
                    game.process_choice(st.session_state.current_image_pair[1], st.session_state.current_image_pair[0])

            col1.image(st.session_state.current_image_pair[0]['filepath'], use_column_width=True)
            col2.image(st.session_state.current_image_pair[1]['filepath'], use_column_width=True)
    
    @staticmethod
    def display_progress_bar(current, total):
        """Displays a progress bar using Streamlit's built-in method."""
        progress_percent = ((current) / total)
        st.progress(progress_percent)

    @staticmethod
    def display_pause_screen(game):
        """Displays the pause screen with leaderboard and options to continue or view leaderboard."""
        st.write("Level complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎮  Continue playing"):
                st.session_state.match_count = 0
                st.session_state.reviewed_images = set()
                st.rerun()
        with col2:
            if st.button("🏆  View full leaderboard"):
                st.switch_page("./pages/3_🏆_Leaderboard.py")

        st.write("Top 5 Images You Reviewed:")
        GameFacemash.display_reviewed_leaderboard()

    @staticmethod
    def display_reviewed_leaderboard():
        """Displays the leaderboard of reviewed images."""
        db = Database()
        reviewed_images = list(st.session_state.reviewed_images)
        if not reviewed_images:
            st.write("No images reviewed yet.")
            return
        
        placeholders = ', '.join('?' for _ in reviewed_images)
        query = f"""
            SELECT image_id, filepath, score, (SELECT creator_name FROM creators WHERE creator_id = images.creator_id)
            FROM images
            WHERE image_id IN ({placeholders})
            ORDER BY score DESC
            LIMIT 5
        """
        scores = db.conn.execute(query, reviewed_images).fetchall()
        
        for index, entry in enumerate(scores):
            st.write(f"Rank {index + 1}")
            col1, col2, col3 = st.columns([1, 3, 2])
            col1.image(entry[1], width=50)
            col2.write(f"Score: {entry[2]}")
            col3.write(f"Creator: {entry[3]}")
            st.write("---")

    def process_choice(self, winner, loser):
        """Process the chosen image and update the next pair."""
        self.update_image_score(winner, loser)

        # Keep track of reviewed images
        st.session_state.reviewed_images.add(winner['image_id'])
        st.session_state.reviewed_images.add(loser['image_id'])

        # Keep the chosen image and replace the other one
        if winner == st.session_state.current_image_pair[0]:
            st.session_state.current_image_pair[1] = self.get_new_image(winner['image_id'])
        else:
            st.session_state.current_image_pair[0] = self.get_new_image(loser['image_id'])
        
        if len(self.images) < 2:
            self.images = self.db.get_active_images()

        st.session_state.match_count += 1

    def get_new_image(self, exclude_image_id):
        """Get a new image that is not currently displayed and not the same as the excluded image."""
        remaining_images = [img for img in self.images if img['image_id'] not in st.session_state.displayed_image_ids and img['image_id'] != exclude_image_id]
        if not remaining_images:
            st.session_state.displayed_image_ids = set()  # Reset the displayed images set
            remaining_images = [img for img in self.images if img['image_id'] != exclude_image_id]
        new_image = random.choice(remaining_images)
        st.session_state.displayed_image_ids.add(new_image['image_id'])
        return new_image

    def update_image_score(self, winner, loser):
        """Update the ELO score of the chosen image."""
        Leaderboard.update_elo(winner['image_id'], loser['image_id'])
    