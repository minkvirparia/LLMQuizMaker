import streamlit as st
from typing import List, Dict, Any

class QuestionListView:
    """Component for displaying tests in list format."""
    
    def __init__(self):
        pass
    
    def render_question_set(self, test_set: Dict[str, Any]):
        """Render a single test set."""
        test_id = test_set.get('id', '')
        # If this test is selected, show the dedicated interactive page
        if st.session_state.get('selected_test_id', None) == test_id:
            self.render_interactive_test_page(test_set)
            return
        with st.expander(f"📄 {test_set.get('title', 'Untitled')} - {test_set.get('created_date', 'N/A')}"):
            # Metadata
            metadata = test_set.get('metadata', {})
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Technology:** {metadata.get('technology', 'N/A')}")
            with col2:
                st.markdown(f"**Test Name:** {test_set.get('title', 'Test Details')}")
            with col3:
                st.markdown(f"**Difficulty:** {metadata.get('difficulty', 'N/A')}")
            st.markdown(f"**Total Questions:** {test_set.get('total_tests', len(test_set.get('tests', [])))}")
            # Action buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👁️ View", key=f"view_{test_id}"):
                    st.session_state['selected_test_id'] = test_id
                    st.rerun()
            with col2:
                pass
            with col3:
                pass
            with col4:
                pass
    
    def show_test_details(self, test_set: Dict[str, Any]):
        """Show detailed view of a test set."""
        st.subheader(f"📄 {test_set.get('title', 'Test Details')}")
        metadata = test_set.get('metadata', {})
        st.markdown(f"**Technology:** {metadata.get('technology', 'N/A')}")
        st.markdown(f"**Test Name:** {test_set.get('title', 'Test Details')}")
        st.markdown(f"**Difficulty:** {metadata.get('difficulty', 'N/A')}")
        st.markdown(f"**Total Questions:** {test_set.get('total_tests', len(test_set.get('tests', [])))}")
        
        tests = test_set.get('tests', [])
        for i, test in enumerate(tests, 1):
            with st.expander(f"Question {i}: {test.get('question', 'No question text')[:50]}..."):
                self.render_single_test(test)
    
    def render_single_test(self, test: Dict[str, Any]):
        """Render a single test with all details."""
        st.markdown(f"**Question:** {test.get('question', '')}")
        
        # Options (dict)
        options = test.get('options', {})
        answer = test.get('answer', {})
        correct_key = answer.get('answer', '')
        st.markdown("**Options:**")
        for key, option in options.items():
            if key == correct_key:
                st.markdown(f"✅ **{option}")
            else:
                st.markdown(f"{option}")
        
        # Explanation
        explanation = answer.get('explanation', '')
        if explanation:
            st.markdown(f"**Explanation:** {explanation}")
        
        # Difficulty
        st.markdown(f"**Difficulty:** {test.get('difficulty', 'N/A')}")
        st.markdown(f"**Technology:** {test.get('technology', 'N/A')}")
    
    def download_tests(self, test_set: Dict[str, Any]):
        st.success(f"Downloading {test_set.get('title', 'tests')}...")
        # Implementation for download functionality would go here
    
    def edit_tests(self, test_set: Dict[str, Any]):
        st.info(f"Editing {test_set.get('title', 'tests')}...")
        # Implementation for edit functionality would go here
    
    def delete_tests(self, test_set: Dict[str, Any]):
        if st.button("Confirm Delete", key=f"confirm_delete_{test_set.get('id', '')}"):
            st.success(f"Deleted {test_set.get('title', 'tests')}")
            # Implementation for delete functionality would go here
    
    def render_search_results(self, questions: List[Dict[str, Any]]):
        if not questions:
            st.info("No questions match your search criteria.")
            return
        st.subheader(f"🔍 Found {len(questions)} questions")
        for question in questions:
            with st.expander(f"Question: {question.get('question', '')[:50]}..."):
                self.render_single_test(question)
    
    def render_analytics(self, analytics: Dict[str, Any]):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Questions", analytics.get('total_tests', 0))
        with col2:
            st.metric("Test Sets", analytics.get('total_sets', 0))
        with col3:
            st.metric("Technologies", analytics.get('total_technologies', 0))
        with col4:
            st.metric("Avg Questions/Set", analytics.get('avg_tests_per_set', 0))
        st.subheader("📊 Difficulty Distribution")
        difficulty_data = analytics.get('difficulty_distribution', {})
        if difficulty_data:
            max_count = max(difficulty_data.values()) if difficulty_data else 1
            for difficulty, count in difficulty_data.items():
                st.progress(count / max_count if max_count > 0 else 0)
                st.markdown(f"**{difficulty}:** {count} questions")
        st.subheader("📚 Technology Distribution")
        technology_data = analytics.get('technology_distribution', {})
        if technology_data:
            max_count = max(technology_data.values()) if technology_data else 1
            for technology, count in technology_data.items():
                st.progress(count / max_count if max_count > 0 else 0)
                st.markdown(f"**{technology}:** {count} questions") 

    def render_interactive_test_page(self, test_set: Dict[str, Any]):
        """Show a dedicated interactive Q&A page for a test set."""
        st.subheader(f"📄 {test_set.get('title', 'Test Details')}")
        metadata = test_set.get('metadata', {})
        st.markdown(f"**Technology:** {metadata.get('technology', 'N/A')}")
        st.markdown(f"**Test Name:** {test_set.get('title', 'Test Details')}")
        st.markdown(f"**Difficulty:** {metadata.get('difficulty', 'N/A')}")
        st.markdown(f"**Total Questions:** {test_set.get('total_tests', len(test_set.get('tests', [])))}")
        st.markdown("---")
        tests = test_set.get('tests', [])
        for i, test in enumerate(tests, 1):
            with st.expander(f"Question {i}: {test.get('question', 'No question text')[:50]}..."):
                self.render_interactive_single_test(test, i, test_set.get('id', ''))
        if st.button("⬅️ Back to List", key="back_to_list_btn"):
            st.session_state['selected_test_id'] = None
            st.rerun()

    def render_interactive_single_test(self, test: Dict[str, Any], idx: int, test_id: str):
        """Render a single test as interactive Q&A (radio, highlight, explanation)."""
        st.markdown(f"**Question:** {test.get('question', '')}")
        options = test.get('options', {})
        answer = test.get('answer', {})
        correct_key = answer.get('answer', '')
        explanation = answer.get('explanation', '')
        radio_key = f"selected_{test_id}_{idx}"
        version_key = f"{radio_key}_version"
        if version_key not in st.session_state:
            st.session_state[version_key] = 0
        radio_version = st.session_state[version_key]
        radio_widget_key = f"{radio_key}_v{radio_version}"
        selected = st.session_state.get(radio_key, None)

        # Always define placeholders at the top
        feedback_placeholder = st.empty()
        explanation_placeholder = st.empty()

        if selected is None:
            selected_val = st.radio(
                "Select your answer:",
                options=[(k, options.get(k, '')) for k in ['a', 'b', 'c', 'd']],
                format_func=lambda x: f"{x[0]}. {x[1]}",
                key=radio_widget_key,
                index=None,  # No default selection
                disabled=False
            )
            # If the user made a selection, store it in session_state and rerun
            radio_val = st.session_state.get(radio_widget_key, None)
            if radio_val is not None:
                # Only store the letter if it's a tuple
                if isinstance(radio_val, tuple):
                    st.session_state[radio_key] = radio_val[0]
                else:
                    st.session_state[radio_key] = radio_val
                st.rerun()
            # Render feedback and explanation placeholders directly below options
            feedback_placeholder.markdown("<div style='min-height:32px'></div>", unsafe_allow_html=True)
            explanation_placeholder.markdown("<div style='min-height:32px'></div>", unsafe_allow_html=True)
        else:
            # If value is a tuple (from previous run), extract the letter
            if isinstance(selected, tuple):
                selected_letter = selected[0]
            else:
                selected_letter = selected
            # Only show colored markdown options, not the radio button
            for k in ['a', 'b', 'c', 'd']:
                opt_text = options.get(k, '')
                if k == correct_key:
                    # Light green background for correct answer
                    st.markdown(f"<span style='color: #256029; background-color: #C8E6C9; padding: 4px 8px; border-radius: 4px; display: inline-block;'><b>{k}. {opt_text}</b></span>", unsafe_allow_html=True)
                elif k == selected_letter:
                    # Light red background for incorrect selection
                    st.markdown(f"<span style='color: #B71C1C; background-color: #FFCDD2; padding: 4px 8px; border-radius: 4px; display: inline-block;'><b>{k}. {opt_text}</b></span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"{k}. {opt_text}")
            if selected_letter == correct_key:
                feedback_placeholder.success("Correct! 🎉")
            else:
                feedback_placeholder.error(f"Incorrect. The correct answer is **{correct_key}**.")
            if explanation:
                explanation_placeholder.info(f"**Explanation:** {explanation}")
            else:
                explanation_placeholder.markdown("<div style='min-height:32px'></div>", unsafe_allow_html=True)
            # Add Reset Answer button
            if st.button("Reset Answer", key=f"reset_{test_id}_{idx}"):
                st.session_state.pop(radio_key, None)
                st.session_state[version_key] += 1
                st.rerun() 