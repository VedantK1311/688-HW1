import streamlit as st
from HW1 import HW1  
from hw2 import hw2

# Creating a Streamlit app that navigates like a multi-page application.
# Each function 'HW1' and 'hw2' should be defined in their respective modules and should contain the Streamlit code to run each app page.

# Create a sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Go to", ("HW 1", "HW 2"))  # Ensured consistent capitalization

# Conditional rendering based on the sidebar choice
if choice == "HW 1":
    HW1()  # Corrected to match the imported function
elif choice == "HW 2":
    hw2()  
