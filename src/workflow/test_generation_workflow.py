"""
Test Generation Workflow
Combines the best features of both the original langgraph workflow and the test_generation workflow
"""

import os
import json
import logging
from typing import TypedDict, List, Dict, Optional, Any
from langgraph.graph import StateGraph, END

# --- Load environment variables from .env if present ---
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

import google.generativeai as genai

# --- Logging Setup ---
logging.basicConfig(level=logging.WARNING, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("test_generation_workflow")


# --- Data Structures ---
class Question(TypedDict):
    question: str
    options: Dict[
        str, str
    ]  # {'a': 'option a', 'b': 'option b', 'c': 'option c', 'd': 'option d'}
    answer: Dict[str, str]  # {'answer': 'a', 'explanation': 'explanation text'}


class WorkflowState(TypedDict):
    technology: str
    difficulty: str
    questions: List[Question]
    errors: List[str]
    num_questions: int
    current_question: Optional[Dict[str, Any]]


class TestGenerationWorkflow:
    """Test generation workflow with technology and difficulty support."""

    def __init__(self):
        # Initialize Google Generative AI
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "GEMINI_API_KEY environment variable is not set. Gemini API calls will fail."
            )

        self.model_name = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash")
        genai.configure(api_key=self.api_key)

        # Create the question generation prompt template
        self.prompt_template = (
            "You are an expert technical interviewer specializing in {technology}. "
            "Generate a multiple choice question at {difficulty} level difficulty.\n\n"
            "Requirements:\n"
            "- Question should be clear, concise, and end with a question mark\n"
            '- Provide exactly 4 options, as a dictionary with keys a, b, c, d (e.g., {{"a": "option a", ...}})\n'
            "- The question should be challenging but appropriate for {difficulty} level\n"
            "- Include a brief explanation for the correct answer\n"
            "IMPORTANT: Respond ONLY with a single valid JSON object, with no markdown, no explanation, and no extra text. Your response MUST start with '{{' and end with '}}'. Do not include any introductory or trailing text.\n"
            "Format the response as JSON:\n"
            "{{\n"
            '    "question": "Your question here?",\n'
            '    "options": {{"a": "option a", "b": "option b", "c": "option c", "d": "option d"}},\n'
            '    "correct_answer": "a",\n'
            '    "explanation": "Brief explanation of why this is correct"\n'
            "}}\n\n"
            "Focus on {technology} concepts, best practices, and common scenarios.\n"
            "Use one of the following difficulty levels: Easy, Medium, Hard."
        )

    def generate_single_question(self, state: WorkflowState) -> WorkflowState:
        """Generate a single question using the LLM."""
        try:
            print(
                f"[DEBUG] Generating question for {state['technology']} at {state['difficulty']} difficulty"
            )
            # Get previous questions to avoid repetition
            # previous_questions = "; ".join([q["question"] for q in state["questions"]]) if state["questions"] else "None"

            # Create the prompt
            try:
                prompt = self.prompt_template.format(
                    technology=state["technology"],
                    difficulty=state["difficulty"],
                    # previous_questions=""
                )
                print(f"[DEBUG] Prompt: {prompt}")
            except Exception as e:
                print(f"[ERROR] Error formatting prompt: {e}")
                return state
            # Get response from Gemini LLM
            model = genai.GenerativeModel(self.model_name)

            # Generate content from the model
            response = model.generate_content(prompt)
            print(f"[DEBUG] Raw LLM response: {response.text}")
            text = response.text.strip()

            # --- Robust JSON extraction from the response ---
            # Some times the LLM response is not a valid JSON object. So we need to extract it manually.
            # This function will try to extract the JSON object from the text and we will not need any LLM calls for this validation
            def extract_json(text):
                import re, json

                # Remove code block markers if present
                text = re.sub(r"^```[a-zA-Z]*", "", text).strip()
                text = re.sub(r"```$", "", text).strip()

                # Find the first JSON object in the text. the re.DOTALL is used to match across multiple lines.
                json_match = re.search(r"\{.*\}", text, re.DOTALL)
                # If the text contains a JSON object, return it.
                if json_match:
                    json_str = json_match.group()
                    return json.loads(json_str)
                
                # Fallback: if the text contains '"question"' but no braces, try wrapping in {}
                if '"question"' in text and not text.strip().startswith("{"):
                    try_str = "{" + text.strip().strip(",") + "}"
                    print(f"[DEBUG] Attempting fallback parse: {try_str}")
                    try:
                        return json.loads(try_str)
                    except Exception as e:
                        logger.error(
                            f"Failed fallback parse. Attempted string: {try_str}\nRaw response: {text}"
                        )
                        print(
                            f"[ERROR] Failed fallback parse. Attempted string: {try_str}\nRaw response: {text}"
                        )
                        raise
                
                # Failsafe: try to extract fields line by line. This is a fallback mechanism to handle cases where the JSON object is not properly formatted.
                fields = ["question", "options", "correct_answer", "explanation"]
                result = {}
                for field in fields:
                    # This regex will match the field name and the value.
                    field_match = re.search(rf'"{field}"\s*:\s*(.*)', text)
                    # If the field is found, extract the value.
                    if field_match:
                        value = field_match.group(1).strip().rstrip(",")
                        # Remove quotes for non-list fields.
                        if field == "options":
                            try:
                                result[field] = json.loads(value)
                            except Exception:
                                result[field] = {"a": "", "b": "", "c": "", "d": ""}
                        else:
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            result[field] = value
                # If the result has all the fields, return it.
                if set(result.keys()) == set(fields):
                    print(f"[DEBUG] Failsafe extraction result: {result}")
                    return result
                # Final attempt: try to parse the whole text
                print(f"[DEBUG] Final attempt, trying to parse whole text: {text}")
                try:
                    return json.loads(text)
                except Exception as e:
                    # All parsing attempts failed - raise a proper error
                    error_msg = f"Failed to parse LLM response after all attempts. Raw response: {text[:200]}..."
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            # Parse the JSON response
            try:
                question_data = extract_json(text)
                # Validate the response structure
                if self._validate_question_data(question_data):
                    # No need to convert options, already a dict
                    formatted_question = {
                        "question": question_data["question"],
                        "options": question_data["options"],
                        "answer": {
                            "answer": question_data["correct_answer"],
                            "explanation": question_data["explanation"],
                        },
                    }
                    state["current_question"] = formatted_question
                    state["errors"] = []
                else:
                    state["errors"].append("Invalid question format received from LLM")
                    state["current_question"] = None
            except json.JSONDecodeError as e:
                logger.error(
                    f"Failed to parse LLM response as JSON: {str(e)}\nRaw response: {text}"
                )
                state["errors"].append(
                    f"Failed to parse LLM response as JSON: {str(e)}. Raw response: {text}"
                )
                state["current_question"] = None
            except Exception as e:
                logger.error(
                    f"Unexpected error during JSON extraction: {str(e)}\nRaw response: {text}"
                )
                state["errors"].append(
                    f"Unexpected error during JSON extraction: {str(e)}. Raw response: {text}"
                )
                state["current_question"] = None
        except Exception as e:
            state["errors"].append(f"Error generating question: {str(e)}")
            state["current_question"] = None
        return state

    def _validate_question_data(self, data: Dict[str, Any]) -> bool:
        """Validate the question data structure."""
        required_fields = ["question", "options", "correct_answer", "explanation"]

        # Check if all required fields exist
        if not all(field in data for field in required_fields):
            return False

        # Check if question is not empty and ends with question mark
        if not data["question"] or not data["question"].strip().endswith("?"):
            return False

        # Check if options is a dict with exactly 4 keys a, b, c, d
        if not isinstance(data["options"], dict) or set(data["options"].keys()) != {
            "a",
            "b",
            "c",
            "d",
        }:
            return False

        # Check if correct_answer is valid
        if data["correct_answer"] not in ["a", "b", "c", "d"]:
            return False

        # Check if explanation is not empty
        if not data["explanation"] or len(data["explanation"].strip()) < 10:
            return False

        # Check if difficulty is valid (if present)
        if "difficulty" in data and data["difficulty"] not in [
            "Easy",
            "Medium",
            "Hard",
        ]:
            return False

        return True

    def validate_and_add_question(self, state: WorkflowState) -> WorkflowState:
        """Validate the current question and add it to the list if valid."""
        current_question = state.get("current_question")

        if current_question:
            # Check for duplicates
            is_duplicate = any(
                q["question"].lower() == current_question["question"].lower()
                for q in state["questions"]
            )

            if is_duplicate:
                state["errors"].append("Duplicate question detected")
                state["current_question"] = None
            else:
                # Add the question to the list
                state["questions"].append(current_question)
                state["current_question"] = None
                logger.info(
                    f"Added question {len(state['questions'])}/{state['num_questions']}"
                )
        else:
            state["errors"].append("No valid question to add")

        return state

    def should_continue(self, state: WorkflowState) -> str:
        """Determine if the workflow should continue or end."""
        if len(state["questions"]) >= state["num_questions"]:
            logger.info(
                f"Workflow complete. Generated {len(state['questions'])} questions."
            )
            return END

        # If we have errors, we can continue a few times
        if state.get("errors") and len(state["errors"]) > 5:
            logger.warning("Too many errors, ending workflow")
            return END

        return "generate"

    def create_workflow(self) -> StateGraph:
        """Create the workflow graph."""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("generate", self.generate_single_question)
        workflow.add_node("validate", self.validate_and_add_question)

        # Add edges
        # This is the main Edge and it will always go from generating a question to validating it.
        workflow.add_edge("generate", "validate")

        # This is the conditional edge and it will go from validating a question to generating a new question if the question is valid.
        workflow.add_conditional_edges(
            "validate", self.should_continue, {"generate": "generate", END: END}
        )

        # Set entry point
        workflow.set_entry_point("generate")

        return workflow.compile()

    async def generate_test(
        self, technology: str, difficulty: str = "Medium", num_questions: int = 5
    ) -> Dict[str, Any]:
        """
        Generate a test with the specified parameters.

        Args:
            technology (str): The technology to generate questions for
            difficulty (str): The difficulty level ("Easy", "Medium", "Hard")
            num_questions (int): Number of questions to generate

        Returns:
            Dict[str, Any]: A dictionary containing the test questions and any errors
        """
        # Initialize the state
        state: WorkflowState = {
            "technology": technology,
            "difficulty": difficulty,
            "questions": [],
            "errors": [],
            "num_questions": num_questions,
            "current_question": None,
        }

        # Create and run the workflow
        workflow = self.create_workflow()

        try:
            await workflow.ainvoke(state)
        except Exception as e:
            state["errors"].append(f"Workflow execution error: {str(e)}")

        # Return the result
        return {
            "questions": state["questions"],
            "errors": state["errors"],
            "technology": technology,
            "difficulty": difficulty,
            "total_questions": len(state["questions"]),
        }

    def generate_test_sync(
        self, technology: str, difficulty: str = "Medium", num_questions: int = 5
    ) -> Dict[str, Any]:
        """Synchronous version of generate_test."""
        import asyncio

        return asyncio.run(self.generate_test(technology, difficulty, num_questions))


# If we directly want to execute the workflow, we can use this function independently
# This function will just generate list of questions and return it.
def run_test_generation_workflow(
    technology: str = "Python", difficulty: str = "Medium", num_questions: int = 5
) -> List[Dict[str, Any]]:
    """Run the test generation workflow and return questions."""
    workflow = TestGenerationWorkflow()
    result = workflow.generate_test_sync(technology, difficulty, num_questions)
    return result["questions"]


def export_workflow_png(output_path="src/services/workflow_graph.png"):
    """
    Export the workflow graph as a PNG image using its built-in method.

    Args:
        output_path (str): The path to save the workflow graph as a PNG image
    """
    workflow = TestGenerationWorkflow().create_workflow()
    graph = workflow.get_graph()
    graph.draw_png(output_path)
    print(f"Workflow graph exported to {output_path}")
