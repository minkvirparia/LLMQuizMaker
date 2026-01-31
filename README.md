# LLMQuizMaker
LLMQuizMaker - AI-powered MCQ generation platform using Google Gemini API and LangGraph workflows. Generate high-quality technical questions across 30+ domains with a modern Streamlit interface.

# Test Generation App

A modular Streamlit-based application for generating and managing multiple choice questions (MCQs) with advanced AI-powered features and clean architecture.

## 🏗️ Project Structure

```
LLMQuizMaker/
├── src/                          # Source code directory
│   ├── app.py                    # Main Streamlit application entry point
│   ├── components/               # Reusable UI components
│   │   ├── sidebar.py           # Sidebar navigation with page routing
│   │   ├── welcome.py           # Welcome page component with help content
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
│   ├── tests/                   # Test data storage (JSON files)
│   ├── logs/                    # Application logs
│   ├── settings/                # Application settings
│   │   └── user_default_settings.json # User settings
│   └── README.md               # Data directory documentation
├── main.py                      # Application entry point
dependencies
├── .env.example                # Environment variables template
├── requirements.txt            # Requirements file
├── LICENSE                     # MIT License
├── INTEGRATION_README.md       # Integration documentation
└── README.md                   # This file
```

## ✨ Features

### 🆕 New Test Generation
- **AI-powered test generation** using Google Gemini API and LangGraph workflow
- **Advanced form interface** with comprehensive options
- **Real-time preview** of generated tests
- **Multiple difficulty levels**: Easy, Medium, Hard
- **Technology-specific questions**: Python, JavaScript, Java, React, Node.js, Machine Learning
- **Customizable parameters**: Number of questions, difficulty, technology
- **Workflow visualization** with diagram
- **Quality validation** with automatic question checking

### 📋 List of Tests
- **Comprehensive test management** with search and filter capabilities
- **Analytics dashboard** with detailed statistics
- **Multiple view options**: All Questions, Search & Filter, Analytics
- **Test set organization** with metadata

### ⚙️ Advanced Features
- **LangGraph workflow** for robust AI question generation
- **Modular architecture** for easy maintenance and extension
- **Persistent storage** with JSON file-based system
- **Session state management** for user preferences and temporary data
- **Responsive design** with modern UI components
- **Error handling** and user feedback
- **Workflow visualization** with diagram

## 🚀 Installation

1. Clone the repository:
```bash
$ git clone <repository-url>
$ cd LLMQuizMaker
```

2. Create and activate a virtual environment:
```bash
$ python -m venv venv
$ venv\Scripts\activate   # On Ubuntu: source venv/bin/activate
```

3. Install requirements.txt:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```bash
# Replace the API key below with your valid Gemini API key
GEMINI_API_KEY=your_valid_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-2.5-flash-lite
```

## 🏃‍♂️ Running the Application

To run the Streamlit application:

```bash
$ streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 📖 Usage

### New Test Generation
1. Click "🆕 New Test" in the sidebar
2. Fill in the test details:
   - **Test Name**: Enter a descriptive name for your test
   - **Number of Questions**: Choose how many questions to generate
   - **Difficulty**: Select Easy, Medium, or Hard
   - **Technology**: Choose the technology domain (Python, JavaScript, Java, React, Node.js, Machine Learning)
3. Click "🚀 Generate Test" to create your test using AI
4. Preview the generated questions with correct answers and explanations
5. Save the test or generate a new one

### List of Tests
1. Click "📋 List of Questions" in the sidebar
2. Use the tabs to navigate between different views:
   - **📊 All Questions**: View all generated test sets
   - **🔍 Search & Filter**: Find specific questions using filters
   - **📈 Analytics**: View statistics and distributions
3. Use action button "View" to view tests

## 🔧 Technical Architecture

### AI Integration
- **Google Gemini API**: Powers the question generation with advanced language models
- **LangGraph Workflow**: Ensures robust, validated question generation
- **Question Validation**: Automatic validation of generated questions for quality assurance

### Data Management
- **File Storage Service**: JSON-based persistent storage for tests and metadata
- **Session Management**: Streamlit session state for user preferences and temporary data

### Workflow System
The application uses a sophisticated LangGraph workflow for question generation:

1. **Question Generator**: Creates unique technical questions using Gemini API
2. **Validator**: Ensures question quality, format, and uniqueness
3. **State Management**: Tracks progress and maintains question history

## 🛠️ Development

### Code Organization
- **Components**: Reusable UI elements with clear interfaces
- **Pages**: Main application views with business logic
- **Services**: Data access and business logic layer
- **Workflow**: AI-powered question generation pipeline

### Key Dependencies
- **Streamlit**: Web application framework
- **LangGraph**: Workflow orchestration
- **Google Generative AI**: Question generation API
- **Python-dotenv**: Environment variable management

### Environment Setup
- **Python 3.12+**: Required for modern features
- **pip**: Python package manager
- **Google Gemini API Key**: Required for AI question generation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Requirements

- Python 3.12 or higher is required.

## 🛠️ Troubleshooting

- If you see errors about missing API keys, ensure your `.env` file is set up as described.
- If you have dependency issues, create a new virtual environement and run `pip install -r requirements.txt` again.