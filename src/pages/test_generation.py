import streamlit as st
from components.test_form import TestForm
from services.test_generation_service import TestGenerationService
import os

def show_test_generation_page():
    """Display the test generation page with a 2x2 grid layout."""
    st.title("🆕 New Test")
    st.markdown("---")

    # Initialize question service
    question_service = TestGenerationService()

    # Initialize session state for generated test and progress
    if 'generated_test' not in st.session_state:
        st.session_state.generated_test = None
    if 'current_form_data' not in st.session_state:
        st.session_state.current_form_data = None
    if 'is_generating_test' not in st.session_state:
        st.session_state.is_generating_test = False

    # Create two main columns: left (form+diagram), right (question paper)
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        # First row: Test Form
        with st.container():
            test_form = TestForm()
            form_data = test_form.render()

            # Generate questions button (disabled if form is not valid)
            generate_btn_disabled = form_data is None or st.session_state.is_generating_test
            if st.button("🚀 Generate Test", type="primary", use_container_width=True, key="generate_test_btn", disabled=generate_btn_disabled):
                if form_data:
                    # Merge form data with settings
                    generation_params = {
                        'test_name': form_data['test_name'],
                        'num_questions': form_data['num_questions'],
                        'difficulty': form_data['difficulty'],
                        'technology': form_data['technology'],
                    }
                    st.session_state.current_form_data = form_data
                    st.session_state.is_generating_test = True

                    # Show loading state
                    with st.spinner("Generating test..."):
                        try:
                            # Generate questions using the service
                            test = question_service.generate_test(generation_params)
                            print(test)

                            # Store in session state
                            st.session_state.generated_test = test
                            st.session_state.current_form_data = form_data  # Save form data for later use

                            # Automatically save the test
                            test_name = form_data.get('test_name', 'Untitled')
                            question_set_id = question_service.save_test(test, test_name)
                            
                            # Show success toast message
                            st.success(f"✅ Test generated and saved successfully!")
                            st.info(f"📁 Saved as: {test_name} (ID: {question_set_id})")
                            st.info("💡 You can view your saved test in the 'List of Tests' page.")

                            st.session_state.is_generating_test = False
                            st.rerun()

                        except Exception as e:
                            st.session_state.is_generating_test = False
                            st.error(f"Error generating test: {str(e)}")

            # Generate new test button (only if a test is generated)
            if st.session_state.generated_test:
                st.markdown("---")
                if st.button("🔄 Generate New Test", use_container_width=True, key="generate_new_btn"):
                    st.session_state.generated_test = None
                    st.session_state.current_form_data = None
                    st.rerun()

        # Second row: Diagram
        with st.container():
            st.subheader("🗺️ Workflow Diagram")
            png_path = os.path.join(os.path.dirname(__file__), "../services/workflow_graph.png")
            if os.path.exists(png_path):
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: center; align-items: center; width: 100%;'>
                        <img src='data:image/png;base64,{get_base64_image(png_path)}' style='max-height: 500px; height: auto; display: block; margin: 0 auto;'/>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.info("Workflow PNG diagram not found. Please generate it first using the export-graph-png command.")

    with col_right:
        # This column spans both rows: Question Paper Preview
        if st.session_state.is_generating_test:
            st.subheader("📋 Generated Test Preview")
            st.markdown(
                """
                <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px;'>
                    <div style='font-size: 3em;'>⏳</div>
                    <div style='font-size: 1.2em; margin-top: 1em;'>Generating your test... Please wait!</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif st.session_state.generated_test:
            display_generated_test(st.session_state.generated_test)
        else:
            st.subheader("📋 Generated Test Preview")
            st.info("No test generated yet. Fill the form and click 'Generate Test' to preview your test here.")

def display_generated_test(test):
    """Display the generated test in a clean preview format without answers, using full width and improved visibility."""
    st.subheader("📋 Generated Test Preview")

    # Improved CSS for card-like appearance and full width
    st.markdown(
        """
        <style>
        .question-card {
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.07);
            border: 1.5px solid #e0e0e0;
            padding: 2em 2em 1.5em 2em;
            margin-bottom: 2em;
            width: 100%;
            min-width: 0;
            max-width: 100%;
            box-sizing: border-box;
        }
        .question-title {
            font-weight: bold;
            font-size: 1.15em;
            margin-bottom: 0.7em;
        }
        .option-list {
            margin-left: 1.2em;
            margin-bottom: 0.7em;
        }
        .meta {
            color: #888;
            font-size: 0.98em;
            margin-top: 0.7em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    for i, question in enumerate(test, 1):
        options = question.get('options', {})
        with st.container():
            st.markdown(
                f"""
                <div class="question-card">
                    <div class="question-title">Question {i}: {question.get('question', 'No question text')}</div>
                    <div><b>Options:</b></div>
                    <div class="option-list">
                        <div>a. {options.get('a', '')}</div>
                        <div>b. {options.get('b', '')}</div>
                        <div>c. {options.get('c', '')}</div>
                        <div>d. {options.get('d', '')}</div>
                    </div>
                    <div class="meta"><b>Difficulty:</b> {question.get('difficulty', 'N/A')} &nbsp; | &nbsp; <b>Technology:</b> {question.get('technology', 'N/A')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def get_base64_image(image_path):
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode() 