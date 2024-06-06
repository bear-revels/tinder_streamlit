import streamlit as st
import pandas as pd
import os
import random
import time
import yagmail

# Initialize Yagmail for sending emails
yag = yagmail.SMTP('your_email@gmail.com', 'your_password')

# Placeholder for user responses
if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'current_level' not in st.session_state:
    st.session_state.current_level = 1

if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

if 'scoreboard' not in st.session_state:
    if os.path.exists('files/scoreboard.csv'):
        st.session_state.scoreboard = pd.read_csv('files/scoreboard.csv')
    else:
        st.session_state.scoreboard = pd.DataFrame(columns=['name', 'email', 'level', 'accuracy', 'speed', 'score', 'rank'])

# Load mapping.csv
mapping_df = pd.read_csv('files/mapping.csv')

# User login
st.title('AI vs Real Photo Identifier Game')
name = st.text_input("Enter your name:")
email = st.text_input("Enter your email:")

if name and email:
    st.session_state.name = name
    st.session_state.email = email
    st.success("Logged in as {}!".format(name))

    # Load images for the current level
    level_path = f"files/level_{st.session_state.current_level}"
    images = [{"id": i, "path": os.path.join(level_path, img)} for i, img in enumerate(os.listdir(level_path))]

    # Shuffle images
    random.shuffle(images)

    # Image display and user response
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0

    if st.session_state.current_index < len(images):
        image_info = images[st.session_state.current_index]
        st.image(image_info['path'])
        st.write("Do you think this image is real or fake?")
        if st.button("Real"):
            st.session_state.responses.append((image_info['path'], "real"))
            st.session_state.current_index += 1
        if st.button("Fake"):
            st.session_state.responses.append((image_info['path'], "fake"))
            st.session_state.current_index += 1
    else:
        st.write(f"You have completed level {st.session_state.current_level}!")

        # Calculate accuracy
        correct_responses = sum(
            1 for response in st.session_state.responses if
            response[1] == ("real" if mapping_df[mapping_df['image_path'] == response[0]]['real'].values[0] == 1 else "fake")
        )
        total_responses = len(st.session_state.responses)
        accuracy = correct_responses / total_responses

        # Calculate speed and score
        end_time = time.time()
        speed = end_time - st.session_state.start_time
        score = accuracy / speed

        # Update scoreboard
        st.session_state.scoreboard = st.session_state.scoreboard.append({
            'name': st.session_state.name,
            'email': st.session_state.email,
            'level': st.session_state.current_level,
            'accuracy': accuracy,
            'speed': speed,
            'score': score,
            'rank': 0  # Placeholder for rank, will update later
        }, ignore_index=True)

        # Update ranks
        st.session_state.scoreboard['rank'] = st.session_state.scoreboard.groupby('level')['score'].rank(ascending=False, method='min')

        # Save scoreboard
        st.session_state.scoreboard.to_csv('files/scoreboard.csv', index=False)

        # Display results
        st.write(f"Your accuracy: {accuracy:.2f}")
        st.write(f"Your speed: {speed:.2f} seconds")
        st.write(f"Your score: {score:.4f}")
        st.write("Leaderboard:")
        st.write(st.session_state.scoreboard[st.session_state.scoreboard['level'] == st.session_state.current_level].sort_values(by='rank'))

        # Email results
        yag.send(
            to=st.session_state.email,
            subject=f"Your Level {st.session_state.current_level} Results",
            contents=f"Hello {st.session_state.name},\n\nHere are your results for level {st.session_state.current_level}:\n\nAccuracy: {accuracy:.2f}\nSpeed: {speed:.2f} seconds\nScore: {score:.4f}\n\nLeaderboard:\n{st.session_state.scoreboard.to_string()}"
        )

        # Reset for next level
        st.session_state.responses = []
        st.session_state.current_index = 0
        st.session_state.start_time = time.time()
        st.session_state.current_level += 1

        if st.session_state.current_level > 10:  # Assuming 10 levels + FinalBoss
            st.write("Congratulations! You've completed all levels!")
            st.session_state.current_level = 1  # Reset to level 1 for replay