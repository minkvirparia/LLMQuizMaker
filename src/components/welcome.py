import streamlit as st


def show_welcome_page():
    """Display the welcome page with app details and usage instructions."""
    st.title("🎓 Welcome to Test Generation")
    st.markdown("---")

    # Friendly intro
    st.markdown("""
    ### Your all-in-one assistant for generating and managing test questions!
    
    This application helps you create, preview, and manage multiple choice questions (MCQs) with advanced AI-powered features using Google Gemini API and LangGraph workflow.
    """)

    st.subheader("🚀 Quick Start")
    st.markdown("""
    1. **Generate Tests**: Click **🆕 New Test** in the sidebar to create a new test with AI-generated questions.
    2. **Manage Tests**: Click **📋 List of Tests** to view, search, filter, and manage your test sets.
    3. **View Analytics**: Use the analytics tab to review statistics and distributions of your questions.
    """)

    st.subheader("📖 How to Use")
    st.markdown("""
    **New Test Generation**
    1. Click **🆕 New Test** in the sidebar
    2. Fill in the test details:
       - **Test Name**: Enter a descriptive name for your test
       - **Number of Questions**: Choose how many questions to generate (1-10)
       - **Difficulty**: Select Easy, Medium, or Hard
       - **Technology**: Choose from 30+ technologies including Python, JavaScript, Java, React, Node.js, Machine Learning, and more
    3. Click **🚀 Generate Test** to create your test using AI
    4. Preview the generated questions with correct answers and explanations
    5. The test is automatically saved to your local storage in the data/tests directory
    6. Repeat the process to generate more tests

    **List of Tests**
    1. Click **📋 List of Tests** in the sidebar
    2. Use the tabs to navigate between different views:
       - **📊 All Tests**: View all generated test sets with interactive preview
       - **🔍 Search & Filter**: Find specific questions using keywords, technology, and difficulty filters
       - **📈 Analytics**: View comprehensive statistics and distributions
    3. Use action buttons to manage tests (View, Edit, Delete)
    """)

    st.subheader("✨ Features")
    st.markdown("""
    - **AI-powered test generation** using Google Gemini API and LangGraph workflow
    - **Advanced form interface** with comprehensive options and validation
    - **Real-time preview** of generated tests with clean, card-like display
    - **Multiple difficulty levels**: Easy, Medium, Hard
    - **30+ Technology domains**: Python, JavaScript, Java, C++, React, Angular, Node.js, Machine Learning, Data Science, DevOps, and more
    - **Quality validation** with automatic question checking
    - **Comprehensive test management** with search, filter, and analytics
    - **Persistent storage** with JSON file-based system
    - **Session state management** for user preferences and temporary data
    - **Modern, responsive UI** with workflow visualization
    - **Workflow diagram** showing the AI generation process
    - **Error handling** and user feedback with loading states
    """)

    with st.expander("📁 Project Structure (for Developers)"):
        st.code('''
test-generation/
├── src/                          # Source code directory
│   ├── app.py                    # Main Streamlit application entry point
│   ├── components/               # Reusable UI components
│   │   ├── sidebar.py           # Sidebar navigation with page routing
│   │   ├── welcome.py           # Welcome page component (this file)
│   │   ├── test_form.py         # Test generation form with validation
│   │   └── question_list_view.py # Question display and management components
│   ├── pages/                   # Page components
│   │   ├── test_generation.py   # New test generation page with 2x2 layout
│   │   └── test_list.py         # Test list and management page with tabs
│   ├── services/                # Business logic services
│   │   ├── test_generation_service.py # Test management and generation service
│   │   ├── file_storage_service.py # Data persistence service
│   │   └── workflow_graph.png   # Workflow visualization
│   ├── workflow/                # AI workflow components
│   │   └── test_generation_workflow.py # LangGraph workflow for AI generation
│   └── utils/                   # Utility functions
│       └── export_workflow.py   # Workflow export utilities
├── data/                        # Data storage
│   ├── tests/                   # Test data storage
│   ├── logs/                    # Application logs
│   ├── exports/                 # Exported data
│   ├── settings/                # Application settings
│   └── README.md               # Data directory documentation
├── main.py                      # Application entry point
├── pyproject.toml              # Project configuration and dependencies
├── .env                        # Environment variables (GEMINI_API_KEY)
├── .python-version             # Python version specification (3.12+)
└── README.md                   # Project documentation
''', language='text')
        st.markdown("See the README for more details on customization and development.")

    st.subheader("💡 Tips")
    st.markdown("""
    - **Select the appropriate technology** for your test from 30+ available options
    - **Adjust difficulty levels** based on your audience (Easy, Medium, Hard)
    - **Use the analytics tab** to review your question sets and statistics
    - **The AI workflow automatically validates** and retries failed question generation
    - **All tests are automatically saved** to local JSON storage in the data/tests directory
    - **Workflow diagram** shows the AI generation process in real-time
    - **Search and filter** functionality helps you find specific questions quickly
    - **Session state** preserves your form data and preferences during the session
    """)

    st.subheader("🔧 Technical Details")
    st.markdown("""
    - **Built with Streamlit** for modern web interface
    - **Powered by Google Gemini API** for intelligent question generation
    - **LangGraph workflow** ensures robust, validated question generation
    - **Python 3.12+** required for modern features
    - **Modular architecture** for easy maintenance and extension
    - **JSON-based storage** for data persistence
    - **Environment variables** for secure API key management
    """) 