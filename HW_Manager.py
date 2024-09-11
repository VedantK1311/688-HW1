import streamlit as st
try:
    from HW1 import HW1
except ImportError as e:
    st.error(f"Failed to import HW1: {str(e)}")

from hw2 import hw2

def main():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ("HW 1", "HW 2"))

    if choice == "HW 1":
        HW1()
    elif choice == "HW 2":
        hw2()

if __name__ == "__main__":
    main()
