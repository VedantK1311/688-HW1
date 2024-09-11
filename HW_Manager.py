import streamlit as st
from HW1 import HW1
from hw2 import hw2

# Creating a Streamlit app that navigates like a multi-page application.
# Each function 'lab1' and 'lab2' should be defined in their respective modules and should contain the Streamlit code to run each app page.

# Create a sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ("HW 1", "hw 2"))

# Conditional rendering based on the sidebar choice
if choice == "HW 1":
    hw1()  
elif choice == "hw 2":
    hw2()  
