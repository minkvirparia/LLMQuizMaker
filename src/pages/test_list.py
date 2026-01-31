import streamlit as st
from services.test_generation_service import TestGenerationService
from components.question_list_view import QuestionListView

def show_test_list_page():
    """Display the test list page."""
    st.title("📋 List of Tests")
    st.markdown("---")
    
    # Initialize test service and list view
    test_service = TestGenerationService()
    list_view = QuestionListView()
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 All Tests", "🔍 Search & Filter", "📈 Analytics"])
    
    with tab1:
        show_all_tests(test_service, list_view)
    
    with tab2:
        show_search_filter(test_service, list_view)
    
    with tab3:
        show_analytics(test_service, list_view)
        st.markdown("---")

def show_all_tests(test_service, list_view):
    """Display all test sets in a list view."""
    st.subheader("📊 All Tests")

    # Get all test sets
    test_sets = test_service.get_all_tests()

    if not test_sets:
        st.info("No tests found. Generate some tests first!")
        return

    selected_test_id = st.session_state.get('selected_test_id', None)
    if selected_test_id:
        # Find the selected test set
        test_set = next((t for t in test_sets if t.get('id', '') == selected_test_id), None)
        if test_set:
            list_view.render_interactive_test_page(test_set)
        else:
            st.error("Selected test not found.")
        return

    # Display test sets using the list view component
    for test_set in test_sets:
        list_view.render_question_set(test_set)

def show_search_filter(test_service, list_view):
    """Display search and filter interface for tests."""
    st.subheader("🔍 Search & Filter")
    
    # Search and filter controls
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search questions", placeholder="Enter keywords...")
        tech_options = ["All"] + test_service.get_supported_technologies()
        technology_filter = st.selectbox("Filter by Technology", tech_options)
    
    with col2:
        diff_options = ["All"] + [d.capitalize() for d in ["Easy", "Medium", "Hard"]]
        difficulty_filter = st.selectbox("Filter by Difficulty", diff_options)
    
    # Apply filters button
    if st.button("🔍 Apply Filters", use_container_width=True):
        filtered_questions = test_service.search_tests(
            search_term=search_term,
            technology=technology_filter if technology_filter != "All" else None,
            difficulty=difficulty_filter.lower() if difficulty_filter != "All" else None
        )
        # Display filtered results
        list_view.render_search_results(filtered_questions)

def show_analytics(test_service, list_view):
    """Display analytics and statistics for tests."""
    st.subheader("📈 Analytics")
    analytics = test_service.get_analytics()
    list_view.render_analytics(analytics)

# For backward compatibility with app.py
show_question_list_page = show_test_list_page 