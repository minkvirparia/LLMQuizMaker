import streamlit as st

def create_sidebar():
    """Create the sidebar with navigation options."""
    # Initialize session state for page selection
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "welcome"
    
    # Sidebar header
    st.sidebar.title("📚 Test Generation")
    st.sidebar.markdown("---")
    
    # Sidebar menu items
    new_test_selected = st.sidebar.button(
        "🆕 New Test", 
        use_container_width=True,
        key="new_test_btn"
    )
    
    list_tests_selected = st.sidebar.button(
        "📋 List of Tests", 
        use_container_width=True,
        key="list_tests_btn"
    )
    
    # Update session state based on button clicks
    if new_test_selected:
        st.session_state.selected_page = "new_test"
        st.query_params["page"] = "new_test"
    elif list_tests_selected:
        st.session_state.selected_page = "list_tests"
        st.query_params["page"] = "list_tests"

    # Add some space before the help button
    st.sidebar.markdown("<div style='height: 8rem;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    help_selected = st.sidebar.button(
        "❓ Help / Welcome", 
        use_container_width=True,
        key="help_btn"
    )
    if help_selected:
        st.session_state.selected_page = "welcome"
        st.query_params["page"] = "welcome"

    # Return selected page from session state
    return st.session_state.selected_page 