import streamlit as st


class TestForm:
    """Component for test generation form."""

    def __init__(self):
        self.form_data = {}

    def render(self):
        """Render the simplified test generation form."""
        # Test name
        st.markdown("**📝 Test Details**")
        test_name = st.text_input(
            "Test Name", placeholder="e.g., Python Basics Test, JavaScript Fundamentals"
        )

        # Main parameters
        st.markdown("**🔢 Main Parameters**")
        col1, col2 = st.columns(2)

        with col1:
            num_questions = st.number_input(
                "Number of Questions", min_value=1, max_value=50, value=5
            )
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

        with col2:
            technology = st.selectbox(
                "Technology",
                [
                    "Python",
                    "JavaScript",
                    "Java",
                    "C++",
                    "C#",
                    "PHP",
                    "Ruby",
                    "Go",
                    "Rust",
                    "Swift",
                    "React",
                    "Angular",
                    "Vue.js",
                    "Node.js",
                    "Django",
                    "Flask",
                    "Spring Boot",
                    "Laravel",
                    "MySQL",
                    "PostgreSQL",
                    "MongoDB",
                    "Redis",
                    "Docker",
                    "Kubernetes",
                    "AWS",
                    "Azure",
                    "Machine Learning",
                    "Data Science",
                    "DevOps",
                    "Cybersecurity",
                    "Web Development",
                    "Mobile Development",
                    "Game Development",
                    "Blockchain",
                    "Cloud Computing",
                ],
            )

        # Return form data if required fields are filled
        if test_name and technology:
            return {
                "test_name": test_name,
                "num_questions": num_questions,
                "difficulty": difficulty,
                "technology": technology,
            }
        else:
            st.warning("Please fill in Test Name and select a Technology")
            return None
