import streamlit as st
from hw1 import hw1
from hw2 import hw2

# Creating a Streamlit app that navigates like a multi-page application.
# Each function 'lab1' and 'lab2' should be defined in their respective modules and should contain the Streamlit code to run each app page.

# Create a sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ("hw 1", "hw 2"))

# Conditional rendering based on the sidebar choice
if choice == "Lab 1":
    hw1()  
elif choice == "Lab 2":
    hw2()  
