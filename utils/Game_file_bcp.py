# import streamlit as st
# import random
# from .Database_file import Database
# from .Leaderboard_file import Leaderboard


# class GameTinder:
#     def __init__(self, db):
#         """Initialize the Game class with a database instance."""
#         self.db = db

#     def display_play_page(self):
#         """Display the game play page."""
#         player_name = st.text_input("Enter your name to start playing:", "")
#         if player_name:
#             if "player_id" not in st.session_state:
#                 st.session_state.player_id = self.db.add_player(player_name)
#             self.start_game()

#     def start_game(self):
#         """Start the game and handle game logic."""
#         if "level" not in st.session_state:
#             st.session_state.level = 1
#             st.session_state.score = 0
#             st.session_state.timer = 30

#         real_image, genai_image = self.db.get_random_images()
#         images = [(real_image, 1), (genai_image, 0)]
#         random.shuffle(images)

#         col1, col2 = st.columns(2)
#         # with col1:
#         #     if st.button("Select Left Image", key="left"):
#         #         self.check_selection(images[0][1] == 1)
#         #     st.image(images[0][0][4], use_column_width=True)
#         # with col2:
#         #     if st.button("Select Right Image", key="right"):
#         #         self.check_selection(images[1][1] == 1)
#         #     st.image(images[1][0][4], use_column_width=True)

#         with col1:
#             if st.button("Select Left Image", key=f"left_{st.session_state.level}"):
#                 self.check_selection(images[0][1] == 1)
#             st.image(images[0][0][4], use_column_width=True)
#         with col2:
#             if st.button("Select Right Image", key=f"right_{st.session_state.level}"):
#                 self.check_selection(images[1][1] == 1)
#             st.image(images[1][0][4], use_column_width=True)  

#     def check_selection(self, is_real_image):
#         """Check the user's selection and update the game state."""
#         if is_real_image:
#             st.session_state.score += 1
#             st.session_state.level += 1
#             st.session_state.timer *= 0.9
#             st.write(f"Correct! Your current score: {st.session_state.score}")
#             self.start_game()
#         else:
#             st.write("Wrong! Game Over!")
#             st.write(f"Your final score: {st.session_state.score}")
#             st.session_state.page = "home"
  
# class GameFacemash:
#     """Class to handle the game functionality."""
    
#     def __init__(self):
#         self.db = Database()
#         self.db.refresh_active_status()  # Refresh the database status
#         self.images = self.db.get_active_images()
#         self.current_image_pair = random.sample(self.images, 2)
#         self.player_name = ""
        
#     @staticmethod
#     def display_game_page():
#         """Displays the game page."""
#         st.title("Game Page")
#         player_name = st.text_input("Enter your name to start playing:", key="player_name")
        
#         if player_name:
#             game = GameFacemash()
#             game.player_name = player_name
#             GameFacemash.play_game(game)
    
#     @staticmethod
#     def play_game(game):
#         """Main game loop to display images and capture player choices."""
#         st.write("Click the image you like better:")
#         col1, col2 = st.columns(2)

#         if 'current_image_pair' not in st.session_state:
#             st.session_state.current_image_pair = game.current_image_pair
        
#         with col1:
#             if st.button("Choose Image 1"):
#                 game.process_choice(st.session_state.current_image_pair[0], st.session_state.current_image_pair[1])
#         with col2:
#             if st.button("Choose Image 2"):
#                 game.process_choice(st.session_state.current_image_pair[1], st.session_state.current_image_pair[0])

#         col1.image(st.session_state.current_image_pair[0]['filepath'])
#         col2.image(st.session_state.current_image_pair[1]['filepath'])

#     def process_choice(self, winner, loser):
#         """Process the chosen image and update the next pair."""
#         self.update_image_score(winner, loser)
#         # Keep the chosen image and replace the other one
#         if winner == st.session_state.current_image_pair[0]:
#             st.session_state.current_image_pair[1] = self.get_new_image()
#         else:
#             st.session_state.current_image_pair[0] = self.get_new_image()
        
#         if len(self.images) < 2:
#             self.images = self.db.get_active_images()  # Reset images when run out

#     def get_new_image(self):
#         """Get a new image that is not currently displayed."""
#         remaining_images = [img for img in self.images if img not in st.session_state.current_image_pair]
#         if not remaining_images:
#             remaining_images = self.db.get_active_images()
#             remaining_images = [img for img in remaining_images if img not in st.session_state.current_image_pair]
#         return random.choice(remaining_images)

#     def update_image_score(self, winner, loser):
#         """Update the ELO score of the chosen image."""
#         Leaderboard.update_elo(winner['image_id'], loser['image_id'])

    