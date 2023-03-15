import streamlit as st
import pandas as pd
from collections import namedtuple
import altair as alt
import math


def authenticate(username, password):
    # Replace the following lines with your own authentication logic
    valid_usernames = ['user1', 'user2']
    valid_passwords = ['password1', 'password2']

    if username in valid_usernames and password in valid_passwords:
        return True
    return False

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

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

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
    

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    main()
else:
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if authenticate(username, password):
            st.session_state.authenticated = True
            main()
        else:
            st.error('Invalid username or password')
            


