import streamlit as st
import pandas as pd
from collections import namedtuple
import altair as alt
import math
import io
import sqlite3
from sqlalchemy import create_engine

# Authentication Functions

def authenticate(username, password):
    """Authenticate the user based on a predefined list of valid users and passwords."""
    valid_usernames = ['user1', 'user2']
    valid_passwords = ['password1', 'password2']

    if username in valid_usernames and password in valid_passwords:
        return True
    return False

def login():
    """Handle user login and session state."""
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error('Invalid username or password')

def sign_out():
    """Handle user sign out and session state."""
    sign_out_button = st.empty()
    if sign_out_button.button('Sign Out'):
        st.session_state.authenticated = False
        sign_out_button.write("Signed out successfully.")
        st.experimental_rerun()

# File Handling Functions

def upload_and_save_file():
    """Upload a file and save its content to an SQLite database."""
    st.subheader("Upload a File")
    file = st.file_uploader("Choose a file", type=['csv', 'txt', 'xlsx'])

    if file is not None:
        file_content = pd.read_csv(file)
        st.write("File content:")
        st.write(file_content)

        database_name = 'uploaded_files.db'
        table_name = 'uploaded_files'
        engine = create_engine(f'sqlite:///{database_name}')

        file_content.to_sql(table_name, engine, if_exists='append', index=False)
        st.success(f"File saved to database '{database_name}' in table '{table_name}'.")

# Spiral Data and Chart Functions

def generate_spiral_data(total_points, num_turns):
    """Generate spiral data based on the given parameters."""
    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    return data

def render_spiral_chart(data):
    """Render an Altair chart based on the given spiral data."""
    chart = alt.Chart(pd.DataFrame(data), height=500, width=500).mark_circle(color='#0068c9', opacity=0.5).encode(x='x:Q', y='y:Q')
    st.altair_chart(chart)

# Main App Function

def main_app():
    """Main application function to render the UI and handle user interactions."""
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    # Generate and render the spiral chart
    data = generate_spiral_data(total_points, num_turns)
    render_spiral_chart(data)

    # Call the function to upload and save a file
    upload_and_save_file()

    # Call the function to handle user sign out
    sign_out()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Show main app if authenticated, otherwise show login screen
if st.session_state.authenticated:
    main_app()
else:
    login()
