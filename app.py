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
name = st.text_input("Enter your name (required):")
email = st.text_input("Enter your email (optional):")
st.markdown("*used to send your results only, not saved anywhere*")

if name:
    st.session_state.name = name
    st.session_state.email = email if email else None
    st.success("Logged in as {}!".format(name))

    # Load images for the current level
    if 'level' in mapping_df.columns:
        current_level_images = mapping_df[mapping_df['level'] == st.session_state.current_level]
        images = [{"id": i, "path": os.path.join('images', row['image_path']), "real": row['real']} for i, row in current_level_images.iterrows()]

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
                st.session_state.responses.append((image_info['path'], "real", image_info['real']))
                st.session_state.current_index += 1
            if st.button("Fake"):
                st.session_state.responses.append((image_info['path'], "fake", image_info['real']))
                st.session_state.current_index += 1
        else:
            st.write(f"You have completed level {st.session_state.current_level}!")

            # Calculate accuracy for the level
            level_responses = [r for r in st.session_state.responses if mapping_df[mapping_df['image_path'] == r[0]]['level'].values[0] == st.session_state.current_level]
            correct_responses = sum(
                1 for response in level_responses if
                response[1] == ("real" if response[2] == 1 else "fake")
            )
            total_responses = len(level_responses)
            accuracy = correct_responses / total_responses

            # Calculate speed and score for the level
            end_time = time.time()
            speed = end_time - st.session_state.start_time
            score = accuracy / speed

            # Update scoreboard for the level
            st.session_state.scoreboard = st.session_state.scoreboard.append({
                'name': st.session_state.name,
                'email': '',  # Do not save the email
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

            # Display results for the level
            st.write(f"Your accuracy for level {st.session_state.current_level}: {accuracy:.2f}")
            st.write(f"Your speed for level {st.session_state.current_level}: {speed:.2f} seconds")
            st.write(f"Your score for level {st.session_state.current_level}: {score:.4f}")
            st.write("Leaderboard for this level:")
            st.write(st.session_state.scoreboard[st.session_state.scoreboard['level'] == st.session_state.current_level].sort_values(by='rank'))

            # Reset for next level
            st.session_state.start_time = time.time()
            st.session_state.current_level += 1

            if st.session_state.current_level > 11:  # Assuming 11 levels including FinalBoss
                # Calculate overall results
                overall_responses = st.session_state.responses
                overall_correct_responses = sum(
                    1 for response in overall_responses if
                    response[1] == ("real" if response[2] == 1 else "fake")
                )
                overall_total_responses = len(overall_responses)
                overall_accuracy = overall_correct_responses / overall_total_responses

                overall_end_time = time.time()
                overall_speed = overall_end_time - st.session_state.start_time
                overall_score = overall_accuracy / overall_speed

                # Add overall results to the scoreboard
                st.session_state.scoreboard = st.session_state.scoreboard.append({
                    'name': st.session_state.name,
                    'email': '',  # Do not save the email
                    'level': 'Overall',
                    'accuracy': overall_accuracy,
                    'speed': overall_speed,
                    'score': overall_score,
                    'rank': 0  # Placeholder for rank, will update later
                }, ignore_index=True)

                # Update overall ranks
                st.session_state.scoreboard['rank'] = st.session_state.scoreboard.groupby('level')['score'].rank(ascending=False, method='min')

                # Save overall scoreboard
                st.session_state.scoreboard.to_csv('files/scoreboard.csv', index=False)

                # Display overall results
                st.write("Congratulations! You've completed all levels!")
                st.write(f"Your overall accuracy: {overall_accuracy:.2f}")
                st.write(f"Your overall speed: {overall_speed:.2f} seconds")
                st.write(f"Your overall score: {overall_score:.4f}")
                st.write("Overall Leaderboard:")
                st.write(st.session_state.scoreboard[st.session_state.scoreboard['level'] == 'Overall'].sort_values(by='rank'))

                # Email overall results if email is provided
                if st.session_state.email:
                    yag.send(
                        to=st.session_state.email,
                        subject="Your Overall Results",
                        contents=f"Hello {st.session_state.name},\n\nHere are your overall results:\n\nAccuracy: {overall_accuracy:.2f}\nSpeed: {overall_speed:.2f} seconds\nScore: {overall_score:.4f}\n\nOverall Leaderboard:\n{st.session_state.scoreboard[st.session_state.scoreboard['level'] == 'Overall'].to_string()}"
                    )

                # Reset for next user
                st.session_state.responses = []
                st.session_state.current_index = 0
                st.session_state.start_time = time.time()
                st.session_state.current_level = 1  # Reset to level 1 for replay
    else:
        st.error("The 'level' column is missing from the mapping file.")
else:
    st.warning("Please enter your name to start the game.")