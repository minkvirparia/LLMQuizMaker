import streamlit as st
from src.pages.test_generation import show_test_generation_page
from src.pages.test_list import show_question_list_page
from components.sidebar import create_sidebar
from components.welcome import show_welcome_page


def main():
    """Main Streamlit application entry point."""
    # Set page configuration
    st.set_page_config(
        page_title="Test Generation",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Read query params and set selected_page if present
    query_params = st.query_params
    page_from_url = query_params.get("page", [None])[0] if isinstance(query_params.get("page", None), list) else query_params.get("page", None)
    if page_from_url and "selected_page" not in st.session_state:
        st.session_state.selected_page = page_from_url

    # Create sidebar and get selected page
    selected_page = create_sidebar()

    # Route to appropriate page
    if selected_page == "new_test":
        show_test_generation_page()
    elif selected_page == "list_tests":
        show_question_list_page()
    else:
        show_welcome_page()

if __name__ == "__main__":
    main() 