import streamlit as st
import pandas as pd
from collections import namedtuple
import altair as alt
import math
from sqlalchemy import create_engine

# Authenticate the user based on a predefined list of valid users and passwords.
def authenticate(username, password):
    return username in ['user1', 'user2'] and password in ['password1', 'password2']

# Handle user login and session state.
def login():
    st.title('Login')
    username, password = st.text_input('Username'), st.text_input('Password', type='password')
    if st.button('Login') and authenticate(username, password):
        st.session_state.authenticated = True
        st.experimental_rerun()
    elif st.button('Login'):
        st.error('Invalid username or password')

# Handle user sign out and session state.
def sign_out():
    if st.empty().button('Sign Out'):
        st.session_state.authenticated = False
        st.write("Signed out successfully.")
        st.experimental_rerun()

# Upload a file and save its content to an SQLite database.
def upload_and_save_file():
    st.subheader("Upload a File")
    file = st.file_uploader("Choose a file", type=['csv', 'txt', 'xlsx'])
    if file:
        file_content = pd.read_csv(file)
        st.write("File content:", file_content)
        engine = create_engine(f'sqlite:///uploaded_files.db')
        file_content.to_sql('uploaded_files', engine, if_exists='append', index=False)
        st.success("File saved to database 'uploaded_files.db' in table 'uploaded_files'.")

# Generate spiral data based on the given parameters.
def generate_spiral_data(total_points, num_turns):
    Point, data = namedtuple('Point', 'x y'), []
    points_per_turn = total_points / num_turns
    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x, y = radius * math.cos(angle), radius * math.sin(angle)
        data.append(Point(x, y))
    return data

# Render an Altair chart based on the given spiral data.
def render_spiral_chart(data):
    chart = alt.Chart(pd.DataFrame(data), height=500, width=500).mark_circle(color='#0068c9', opacity=0.5).encode(x='x:Q', y='y:Q')
    st.altair_chart(chart)

# Show previously uploaded files
def show_uploaded_files():
    engine = create_engine(f'sqlite:///uploaded_files.db')
    try:
        uploaded_files = pd.read_sql('uploaded_files', engine)
        if not uploaded_files.empty:
            st.subheader("Previously Uploaded Files")
            st.write(uploaded_files)
    except:
        st.write("No files uploaded yet.")
    
# Main application function to render the UI and handle user interactions.
def main_app():
    # Show previously uploaded files
    show_uploaded_files()
    
    render_spiral_chart(generate_spiral_data(st.slider("Number of points in spiral", 1, 5000, 2000), st.slider("Number of turns in spiral", 1, 100, 9)))
    upload_and_save_file()
    sign_out()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Show main app if authenticated, otherwise show login screen
if st.session_state.authenticated:
    main_app()
else:
    login()
