import streamlit as st
import pandas as pd
import random
import time
import os

# Load data
mapping = pd.read_csv("files/mapping.csv")
mapping['image_path'] = 'images/' + mapping['image_path']  # Prepend the images folder to the image_path
if os.path.exists("files/scores.csv"):
    scores = pd.read_csv("files/scores.csv")
else:
    scores = pd.DataFrame(columns=['player', 'image_id', 'time_to_respond', 'response'])

# Initialize session state
if 'current_level' not in st.session_state:
    st.session_state.current_level = 1
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
        score = accuracy / avg_speed
        return accuracy * 100, avg_speed, round(score)
    return 0, 0, 0

# User input
if st.session_state.player is None:
    st.session_state.player = st.text_input("Enter your name to start:", value="")
    if st.session_state.player:
        st.session_state.start_time = time.time()
else:
    player = st.session_state.player

    if st.session_state.current_level <= 10:
        if st.session_state.photos.empty:
            st.session_state.photos = mapping[~mapping['image_id'].isin(st.session_state.seen_images)].sample(n=5).reset_index(drop=True)
            st.session_state.start_time = time.time()
        
        current_photo = st.session_state.photos.loc[st.session_state.current_photo, 'image_path']
        st.image(current_photo)
        
        response = None
        
        if st.button("Real", key=f"real_{st.session_state.current_level}_{st.session_state.current_photo}"):
            response = 1
        if st.button("Fake", key=f"fake_{st.session_state.current_level}_{st.session_state.current_photo}"):
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

            if st.session_state.current_photo >= len(st.session_state.photos):
                st.session_state.current_level += 1
                st.session_state.current_photo = 0
                st.session_state.photos = pd.DataFrame()
                accuracy, avg_speed, score = calculate_stats(player)
                st.write(f"Level {st.session_state.current_level - 1} stats: Accuracy: {accuracy:.1f}%, Avg. Speed: {avg_speed:.2f} seconds, Score: {score}")

    else:
        st.write("Game Over")
        accuracy, avg_speed, score = calculate_stats(player)
        st.write(f"Final stats: Accuracy: {accuracy:.1f}%, Avg. Speed: {avg_speed:.2f} seconds, Score: {score}")
        
        # Add player scores to scores.csv
        new_scores = pd.DataFrame(st.session_state.responses)
        scores = pd.concat([scores, new_scores], ignore_index=True)
        scores.to_csv("files/scores.csv", index=False)

        # Calculate and display rankings
        player_scores = scores.groupby('player').agg({'response': 'mean', 'time_to_respond': 'mean'}).reset_index()
        player_scores['score'] = player_scores['response'] / player_scores['time_to_respond']
        player_scores['rank'] = player_scores['score'].rank(ascending=False)
        player_scores['accuracy'] = player_scores['response'] * 100
        player_scores = player_scores[['player', 'accuracy', 'time_to_respond', 'score', 'rank']]
        player_scores['accuracy'] = player_scores['accuracy'].map('{:.1f}%'.format)
        player_scores['time_to_respond'] = player_scores['time_to_respond'].map('{:.2f} seconds'.format)
        player_scores['score'] = player_scores['score'].map('{:.0f}'.format)
        
        image_scores = scores.groupby('image_id').agg({'response': 'mean', 'time_to_respond': 'mean'}).reset_index()
        image_scores['score'] = image_scores['response'] / image_scores['time_to_respond']
        image_scores['rank'] = image_scores['score'].rank(ascending=False)
        image_scores['accuracy'] = image_scores['response'] * 100
        image_scores = image_scores[['image_id', 'accuracy', 'time_to_respond', 'score', 'rank']]
        image_scores['accuracy'] = image_scores['accuracy'].map('{:.1f}%'.format)
        image_scores['time_to_respond'] = image_scores['time_to_respond'].map('{:.2f} seconds'.format)
        image_scores['score'] = image_scores['score'].map('{:.0f}'.format)
        
        creator_scores = scores.merge(mapping, on='image_id').groupby('creator').agg({'response': 'mean', 'time_to_respond': 'mean'}).reset_index()
        creator_scores['score'] = creator_scores['response'] / creator_scores['time_to_respond']
        creator_scores['rank'] = creator_scores['score'].rank(ascending=False)
        creator_scores['accuracy'] = creator_scores['response'] * 100
        creator_scores = creator_scores[['creator', 'accuracy', 'time_to_respond', 'score', 'rank']]
        creator_scores['accuracy'] = creator_scores['accuracy'].map('{:.1f}%'.format)
        creator_scores['time_to_respond'] = creator_scores['time_to_respond'].map('{:.2f} seconds'.format)
        creator_scores['score'] = creator_scores['score'].map('{:.0f}'.format)

        st.write("Player Rankings")
        st.dataframe(player_scores.sort_values(by='rank'))

        st.write("Image Rankings")
        st.dataframe(image_scores.sort_values(by='rank'))

        st.write("Creator Rankings")
        st.dataframe(creator_scores.sort_values(by='rank'))

        st.write("Thank you for playing!")