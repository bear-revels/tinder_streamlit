import streamlit as st
import pandas as pd
import os
import time

# Define the path to the images folder and mapping file
images_folder = "images/"
mapping_file = "files/mapping.csv"

# Function to update mapping.csv with current contents of images folder
def update_mapping(images_folder, mapping_file):
    # Read existing mapping file
    if os.path.exists(mapping_file):
        mapping = pd.read_csv(mapping_file)
    else:
        mapping = pd.DataFrame(columns=['image_id', 'image_path', 'creator', 'team', 'prompt', 'parameters', 'real', 'present'])
    
    # Get the list of current image filenames
    current_images = set(os.listdir(images_folder))

    # Update mapping file with current images
    mapping['present'] = mapping['image_path'].apply(lambda x: 1 if os.path.basename(x) in current_images else 0)
    
    # Add new images to the mapping
    existing_images = set(mapping['image_path'].apply(os.path.basename))
    new_images = current_images - existing_images

    for image in new_images:
        new_entry = pd.DataFrame({
            'image_id': [len(mapping) + 1],
            'image_path': [os.path.join(images_folder, image)],
            'creator': ['unknown'],
            'team': ['unknown'],
            'prompt': [''],
            'parameters': [''],
            'real': [0],
            'present': [1]
        })
        mapping = pd.concat([mapping, new_entry], ignore_index=True)

    # Save updated mapping file
    mapping.to_csv(mapping_file, index=False)
    return mapping

# Update the mapping.csv file
mapping = update_mapping(images_folder, mapping_file)

# Load data
mapping['image_path'] = 'images/' + mapping['image_path'].apply(os.path.basename)  # Ensure correct paths
if os.path.exists("files/scores.csv"):
    scores = pd.read_csv("files/scores.csv")
else:
    scores = pd.DataFrame(columns=['player', 'image_id', 'time_to_respond', 'response'])

# Initialize session state
if 'current_photo' not in st.session_state:
    st.session_state.current_photo = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'responses' not in st.session_state:
    st.session_state.responses = []
if 'player' not in st.session_state:
    st.session_state.player = None
if 'photos' not in st.session_state:
    st.session_state.photos = pd.DataFrame()
if 'seen_images' not in st.session_state:
    st.session_state.seen_images = set()

# Helper function to calculate stats
def calculate_stats(player):
    responses = [r for r in st.session_state.responses if r['player'] == player]
    if responses:
        total_correct = sum(r['response'] == mapping[mapping['image_id'] == r['image_id']]['real'].values[0] for r in responses)
        avg_speed = sum(r['time_to_respond'] for r in responses) / len(responses)
        accuracy = total_correct / len(responses)
        score = round((accuracy * 100) / avg_speed)
        return accuracy * 100, avg_speed, score
    return 0, 0, 0

# CSS styling for the game
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gotham+Rounded:wght@400;700&display=swap');

    .title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        font-family: 'Gotham Rounded', sans-serif;
    }
    .subtitle {
        font-size: 36px;
        text-align: center;
        color: #4A4A4A;
        font-family: 'Gotham Rounded', sans-serif;
    }
    .text-center {
        text-align: center;
    }
    .bold {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# User input
if st.session_state.player is None:
    st.markdown("<h1 class='title'>Welcome to the Image Game!</h1>", unsafe_allow_html=True)
    st.session_state.player = st.text_input("Enter your name to start:", value="")
    if st.session_state.player:
        st.session_state.start_time = time.time()
else:
    player = st.session_state.player

    if st.session_state.photos.empty:
        st.session_state.photos = mapping[mapping['present'] == 1].sample(frac=1).reset_index(drop=True)  # Shuffle images
        st.session_state.start_time = time.time()
    
    if st.session_state.current_photo < len(st.session_state.photos):
        current_photo = st.session_state.photos.loc[st.session_state.current_photo, 'image_path']
        st.image(current_photo)
        
        response = None
        
        if st.button("Real", key=f"real_{st.session_state.current_photo}"):
            response = 1
        if st.button("Fake", key=f"fake_{st.session_state.current_photo}"):
            response = 0

        if response is not None:
            time_to_respond = time.time() - st.session_state.start_time
            image_id = st.session_state.photos.loc[st.session_state.current_photo, 'image_id']
            # Record response
            st.session_state.responses.append({
                'player': player,
                'image_id': image_id,
                'time_to_respond': time_to_respond,
                'response': response
            })
            
            st.session_state.seen_images.add(image_id)
            st.session_state.current_photo += 1
            st.session_state.start_time = time.time()  # Reset start time for next image

    else:
        st.markdown("<h1 class='title'>Game Over</h1>", unsafe_allow_html=True)
        st.markdown("<h2 class='subtitle'>Thank you for playing!</h2>", unsafe_allow_html=True)
        accuracy, avg_speed, score = calculate_stats(player)
        
        # Add player scores to scores.csv
        new_scores = pd.DataFrame(st.session_state.responses)
        scores = pd.concat([scores, new_scores], ignore_index=True)
        scores.to_csv("files/scores.csv", index=False)

        # Calculate and display rankings
        player_scores = scores.groupby('player').agg({'response': 'mean', 'time_to_respond': 'mean'}).reset_index()
        player_scores['score'] = (player_scores['response'] * 100) / player_scores['time_to_respond']
        player_scores['rank'] = player_scores['score'].rank(ascending=False)
        player_scores['accuracy'] = player_scores['response'] * 100
        player_scores = player_scores[['player', 'accuracy', 'time_to_respond', 'score', 'rank']]
        player_scores['accuracy'] = player_scores['accuracy'].map('{:.1f}%'.format)
        player_scores['time_to_respond'] = player_scores['time_to_respond'].map('{:.2f} seconds'.format)
        player_scores['score'] = player_scores['score'].map('{:.0f}'.format)
        player_scores = player_scores.sort_values(by='rank')  # Sort by rank

        image_scores = scores.groupby('image_id').agg({'response': 'mean', 'time_to_respond': 'mean'}).reset_index()
        image_scores['score'] = (image_scores['response'] * 100) / image_scores['time_to_respond']
        image_scores['rank'] = image_scores['score'].rank(ascending=False)
        image_scores['accuracy'] = image_scores['response'] * 100
        image_scores = image_scores[['image_id', 'accuracy', 'time_to_respond', 'score', 'rank']]
        image_scores['accuracy'] = image_scores['accuracy'].map('{:.1f}%'.format)
        image_scores['time_to_respond'] = image_scores['time_to_respond'].map('{:.2f} seconds'.format)
        image_scores['score'] = image_scores['score'].map('{:.0f}'.format)
        image_scores = image_scores.sort_values(by='rank')  # Sort by rank

        creator_scores = scores.merge(mapping, on='image_id').groupby('creator').agg({'response': 'mean', 'time_to_respond': 'mean'}).reset_index()
        creator_scores['score'] = (creator_scores['response'] * 100) / creator_scores['time_to_respond']
        creator_scores['rank'] = creator_scores['score'].rank(ascending=False)
        creator_scores['accuracy'] = creator_scores['response'] * 100
        creator_scores = creator_scores[['creator', 'accuracy', 'time_to_respond', 'score', 'rank']]
        creator_scores['accuracy'] = creator_scores['accuracy'].map('{:.1f}%'.format)
        creator_scores['time_to_respond'] = creator_scores['time_to_respond'].map('{:.2f} seconds'.format)
        creator_scores['score'] = creator_scores['score'].map('{:.0f}'.format)
        creator_scores = creator_scores.sort_values(by='rank')  # Sort by rank


        # Find the player's rank
        player_rank = player_scores[player_scores['player'] == player]['rank'].values[0]

        # Check for new record
        highest_score = player_scores['score'].max()
        if score == highest_score:
            st.markdown("<h1 style='color: red; font-size: 72px; text-align: center;'>NEW RECORD!!!</h1>", unsafe_allow_html=True)

        st.write(f"Your Rank: {int(player_rank)}")
        st.write(f"Your Score: {score}")
        st.write(f"Accuracy: {accuracy:.1f}%")
        st.write(f"Avg. Speed: {avg_speed:.2f} seconds")

        tab1, tab2, tab3 = st.tabs(["Player Rankings", "Image Rankings", "Creator Rankings"])

        with tab1:
            st.dataframe(player_scores, height=300)

        with tab2:
            st.dataframe(image_scores, height=300)

        with tab3:
            st.dataframe(creator_scores, height=300)