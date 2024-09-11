import streamlit as st
from HW1 import HW1  # Assuming HW1() is correctly defined in the HW1.py file
from hw2 import hw2  # Assuming hw2() is correctly defined in the hw2.py file

# Creating a Streamlit app that navigates like a multi-page application.
# Make sure each function 'HW1' and 'hw2' is defined in their respective modules 
# and contains the Streamlit code to run each app page.

# Create a sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ("HW 1", "HW 2"))  # Ensured consistent capitalization

# Conditional rendering based on the sidebar choice
if choice == "HW 1":
    HW1()  # Corrected to match the imported function
elif choice == "HW 2":
    hw2()  # Ensure hw2() is correctly defined and imported
