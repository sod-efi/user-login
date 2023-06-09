import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect
import os
import sqlite3
import uuid

# Set the database file path in the app's working directory
db_path = os.path.join(os.getcwd(), "uploaded_files.db")

# Authenticate the user based on a predefined list of valid users and passwords.
def authenticate(username, password):
    return username in ['user1', 'user2'] and password in ['password1', 'password2']

# Handle user login and session state.
def login():
    """Handle user login and session state."""
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login', key='login_button'):  # Add a unique key for the Login button
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.current_username = username  # Store the current username in the session state
            st.experimental_rerun()
        else:
            st.error('Invalid username or password')

def sign_out():
    """Handle user sign out and session state."""
    sign_out_button = st.empty()
    if sign_out_button.button('Sign Out', key='sign_out_button'):  # Add a unique key for the Sign Out button
        st.session_state.authenticated = False
        sign_out_button.write("Signed out successfully.")
        st.experimental_rerun()

def upload_and_save_file(username):
    st.subheader("Upload a File")
    file = st.file_uploader("Choose a file", type=['csv', 'txt', 'xlsx'])
    table_name = f'uploaded_files_{username}'  # Move this line outside the if statement
    if file:
        file_content = pd.read_csv(file)
        st.write("File content:", file_content)
        engine = create_engine(f'sqlite:///uploaded_files.db')
        file_content.to_sql(table_name, engine, if_exists='append', index=False)
        st.success(f"File saved to database 'uploaded_files.db' in table '{table_name}'.")
    
# Show previously uploaded files
def show_uploaded_files(username):
    engine = create_engine(f'sqlite:///uploaded_files.db')
    table_name = f'uploaded_files_{username}'
    try:
        uploaded_files = pd.read_sql(table_name, engine)
        if not uploaded_files.empty:
            st.subheader("Previously Uploaded Files")
            st.write(uploaded_files)
        else:
            st.write("No files uploaded yet.")
    except Exception as e:
        st.write("No files uploaded yet.")

def display_database_content():
    st.subheader("Database Content")
    engine = create_engine(f'sqlite:///uploaded_files.db')
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    if table_names:
        selected_table = st.selectbox("Select a table to view:", table_names)
        with engine.connect() as connection:
            result = connection.execute(f"SELECT * FROM {selected_table}")
            table_data = pd.DataFrame(result.fetchall(), columns=result.keys())
        st.write("Table content:", table_data)
    else:
        st.write("No tables found in the database.")


        
        
        

def main_app(current_username):
    sign_out()
    st.title("Welcome to the Streamlit App")
    upload_and_save_file(current_username)
    show_uploaded_files(current_username)
    display_database_content()

if __name__ == '__main__':
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        main_app(st.session_state.current_username)
    else:
        login()
