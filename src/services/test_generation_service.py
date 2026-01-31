import uuid
import asyncio
from typing import List, Dict, Any, Optional
from .file_storage_service import FileStorageService
from workflow.test_generation_workflow import TestGenerationWorkflow

class TestGenerationService:
    """Service for managing test generation."""
    def __init__(self):
        self.file_storage = FileStorageService()
        self.test_generation_workflow = TestGenerationWorkflow()

    def generate_test(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate test based on the provided parameters using the test generation workflow only."""
        technology = params.get('technology', 'Python')
        difficulty = params.get('difficulty', 'intermediate')
        num_questions = params.get('num_questions', 5)
        try:
            result = self.test_generation_workflow.generate_test_sync(technology, difficulty, num_questions)
            questions = result.get('questions', [])
            errors = result.get('errors', [])
            if errors:
                print(f"Errors during test generation: {errors}")
            tests = []
            for i, q in enumerate(questions, 1):
                test = {
                    'id': str(uuid.uuid4()),
                    'question_number': i,
                    'question': q['question'],
                    'options': q['options'],
                    'answer': q['answer'],
                    'technology': technology,
                    'difficulty': difficulty
                }
                tests.append(test)
            return tests
        except Exception as e:
            print(f"Error in test generation: {str(e)}")
            raise

    def generate_test_async(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Async version of test generation using only the test generation workflow."""
        technology = params.get('technology', 'Python')
        difficulty = params.get('difficulty', 'intermediate')
        num_questions = params.get('num_questions', 5)
        try:
            result = asyncio.run(self.test_generation_workflow.generate_test(technology, difficulty, num_questions))
            questions = result.get('questions', [])
            errors = result.get('errors', [])
            if errors:
                print(f"Errors during test generation: {errors}")
            tests = []
            for i, q in enumerate(questions, 1):
                test = {
                    'id': str(uuid.uuid4()),
                    'question_number': i,
                    'question': q['question'],
                    'options': q['options'],
                    'answer': q['answer'],
                    'technology': technology,
                    'difficulty': difficulty
                }
                tests.append(test)
            return tests
        except Exception as e:
            print(f"Error in async test generation: {str(e)}")
            raise

    def save_test(self, tests: List[Dict[str, Any]], test_name: str) -> str:
        """Save a set of test to storage."""
        return self.file_storage.save_tests(tests, test_name)

    def get_all_tests(self) -> List[Dict[str, Any]]:
        """Get all test sets."""
        return self.file_storage.load_tests()

    def get_test_set(self, test_set_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific test set by ID."""
        return self.file_storage.get_test_set(test_set_id)

    def search_tests(self, search_term: str = None, technology: str = None, difficulty: str = None) -> List[Dict[str, Any]]:
        """Search tests based on criteria."""
        all_tests = self.file_storage.load_tests()
        filtered_tests = []
        for test_set in all_tests:
            for test in test_set.get('tests', []):
                if technology and test.get('technology') != technology:
                    continue
                if difficulty and test.get('difficulty') != difficulty:
                    continue
                if search_term:
                    search_lower = search_term.lower()
                    test_text = test.get('question', '').lower()
                    if search_lower not in test_text:
                        continue
                filtered_tests.append(test)
        return filtered_tests

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data about tests."""
        all_tests = self.file_storage.load_tests()
        total_tests = 0
        total_sets = len(all_tests)
        technologies = set()
        difficulties = {}
        technology_distribution = {}
        for test_set in all_tests:
            tests = test_set.get('tests', [])
            total_tests += len(tests)
            for test in tests:
                technology = test.get('technology', 'Unknown')
                technologies.add(technology)
                technology_distribution[technology] = technology_distribution.get(technology, 0) + 1
                difficulty = test.get('difficulty', 'Unknown')
                difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
        return {
            'total_tests': total_tests,
            'total_sets': total_sets,
            'total_technologies': len(technologies),
            'avg_tests_per_set': round(total_tests / total_sets, 2) if total_sets > 0 else 0,
            'difficulty_distribution': difficulties,
            'technology_distribution': technology_distribution
        }

    def delete_test_set(self, test_set_id: str) -> bool:
        """Delete a test set."""
        return self.file_storage.delete_test_set(test_set_id)

    def update_test_set(self, test_set_id: str, updated_data: Dict[str, Any]) -> bool:
        """Update a test set."""
        return self.file_storage.update_test_set(test_set_id, updated_data)

    def export_tests(self, test_set_id: str, format: str = "json") -> Optional[str]:
        """Export tests to a file."""
        return self.file_storage.export_tests(test_set_id, format)

    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        return self.file_storage.get_storage_stats()

    def get_supported_technologies(self) -> List[str]:
        """Get list of supported technologies."""
        return [
            "Python", "JavaScript", "Java", "C++", "Ruby", "PHP",
            "TypeScript", "Go", "Rust", "Swift", "Kotlin", "C#",
            "React", "Angular", "Vue.js", "Node.js", "Django", "Flask",
            "Spring Boot", "Express.js", "MongoDB", "PostgreSQL", "MySQL"
        ]

    def get_difficulty_levels(self) -> List[str]:
        """Get list of supported difficulty levels."""
        return ["beginner", "intermediate", "advanced"] 