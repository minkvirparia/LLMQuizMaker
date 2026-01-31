# Test Generation Service Integration

This document describes the integration of the test generation workflow into the `test_generation_service.py`.

## Overview

The integration uses the test generation workflow to create a robust, feature-rich test generation service with technology-specific question generation and difficulty level support.

## Key Features

### 1. Technology and Difficulty Support
- **Technology-specific questions**: Questions are tailored to specific technologies (Python, JavaScript, Java, etc.)
- **Difficulty levels**: Support for beginner, intermediate, and advanced difficulty levels
- **Context-aware prompts**: LLM prompts include technology and difficulty context

### 2. Test Generation Workflow Architecture
- **State management**: Proper state tracking throughout the workflow
- **Error handling**: Comprehensive error handling with validation mechanisms
- **Validation**: Question validation to ensure quality and format consistency
- **Duplicate detection**: Prevents duplicate questions in the same test

### 3. Improved Data Structure
- **Consistent format**: Standardized question format across the workflow
- **Metadata support**: Technology, difficulty, and other metadata included
- **Unique IDs**: Each question gets a unique identifier

## File Structure

```
src/services/
├── test_generation_service.py    # Main service (updated)
├── file_storage_service.py       # Storage service (unchanged)
└── workflow_graph.png            # Workflow visualization

src/workflow/
├── test_generation_workflow.py   # Test generation workflow (uses Gemini)
```

## Integration Details

### Test Generation Workflow (`test_generation_workflow.py`)

The test generation workflow uses **Google Gemini** (via `google-generativeai`) for question generation:

```python
class TestGenerationWorkflow:
    def __init__(self):
        # Uses Gemini API (google-generativeai)
        ...
    async def generate_test(self, technology: str, difficulty: str, num_questions: int):
        # Generate technology-specific questions with difficulty levels
        ...
```

### Updated Service (`test_generation_service.py`)

The service now supports:

```python
class TestGenerationService:
    def __init__(self):
        self.test_generation_workflow = TestGenerationWorkflow()
    
    def generate_test(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Extract technology, difficulty, and num_questions from params
        # Use test generation workflow
        ...
    
    def generate_test_async(self, params: Dict[str, Any]):
        # Async version for better performance
        ...
```

## Usage Examples

### Basic Usage

```python
from src.services.test_generation_service import TestGenerationService

service = TestGenerationService()

# Generate Python intermediate questions
params = {
    'technology': 'Python',
    'difficulty': 'intermediate',
    'num_questions': 5
}

tests = service.generate_test(params)
```

### Advanced Usage

```python
# Generate JavaScript advanced questions
params = {
    'technology': 'JavaScript',
    'difficulty': 'advanced',
    'num_questions': 10
}

# Async generation
tests = service.generate_test_async(params)

# Save the test
test_id = service.save_test(tests, "JavaScript Advanced Test")
```

### Exporting the Workflow Graph as PNG

You can export the test generation workflow graph as a PNG image using the provided CLI tool:

```bash
python -m src.utils.export_workflow -o path/to/output.png
```
- The `-o` or `--output` argument is optional. If omitted, it defaults to `src/services/workflow_graph.png`.
- Example (default location):
  ```bash
  python -m src.utils.export_workflow
  ```
- Example (custom location):
  ```bash
  python -m src.utils.export_workflow -o my_workflow.png
  ```

No extra dependencies like `pygraphviz` are required for this export; the workflow object supports direct PNG export via its built-in `draw_png` method.

### Supported Technologies

```python
technologies = service.get_supported_technologies()
# Returns: ["Python", "JavaScript", "Java", "C++", "Ruby", "PHP", ...]

difficulties = service.get_difficulty_levels()
# Returns: ["beginner", "intermediate", "advanced"]
```

## Configuration

### Environment Variables

```bash
# Required for the test generation workflow
export GEMINI_API_KEY="your-gemini-api-key"
export GEMINI_MODEL_NAME="gemini-2.5-flash-lite"  # Optional, default is gemini-2.5-flash-lite
```

### Dependencies

The test generation workflow requires:

```toml
[dependencies]
dotenv>=0.9.9
google-generativeai>=0.8.5
langgraph>=0.5.3
pathlib2>=2.3.7.post1
streamlit>=1.46.1
typing-extensions>=4.14.1
```

**Note:** For exporting the workflow graph as PNG, no additional dependencies like `pygraphviz` are needed, as the workflow object provides a native `draw_png` method.

## Error Handling

The integration includes robust error handling:

1. **Primary**: Test generation workflow with technology/difficulty support (using Gemini)
2. **Error logging**: Comprehensive error logging and reporting
3. **Validation**: Question validation to ensure quality and format consistency
4. **Graceful error handling**: Service provides clear error messages when generation fails

## Testing

Run the integration test:

```bash
python test_integration.py
```

This will test:
- Test generation workflow functionality
- Test storage and retrieval
- Analytics and metadata

## Migration Guide

### From Original Service

If you're using the original service, the changes are backward compatible:

```python
# Old way (still works)
params = {'num_questions': 5}
tests = service.generate_test(params)

# New way (recommended)
params = {
    'technology': 'Python',
    'difficulty': 'intermediate',
    'num_questions': 5
}
tests = service.generate_test(params)
```

### API Changes

The main API remains the same, but new parameters are supported:

- `technology`: Specify the technology for questions
- `difficulty`: Set the difficulty level
- `num_questions`: Number of questions to generate

## Performance Considerations

- **Async support**: Use `generate_test_async()` for better performance
- **Caching**: Consider implementing caching for frequently requested technologies
- **Rate limiting**: Be aware of API rate limits for Gemini

## Troubleshooting

### API Key Issues

The most common issue is an invalid or missing Gemini API key. Here's how to fix it:

1. **Get a valid API key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key or use an existing one
   - Copy the API key (it should start with `AIza...`)

2. **Set the API key in your `.env` file**:
   ```bash
   # In your .env file
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL_NAME=gemini-2.0-flash
   ```

3. **Verify the API key is loaded**:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(f"API Key loaded: {os.getenv('GEMINI_API_KEY')[:10]}...")
   ```

4. **Common API key errors**:
   - `API_KEY_INVALID`: The API key is incorrect or expired
   - `API_KEY_NOT_FOUND`: The API key doesn't exist
   - `QUOTA_EXCEEDED`: You've exceeded your API quota

### Common Issues

1. **API Key Errors**: Ensure `GEMINI_API_KEY` is set correctly and is valid
2. **Import Errors**: Check that all dependencies are installed
3. **Workflow Failures**: Check logs for detailed error messages
4. **Generation Issues**: If the workflow fails to generate questions, check the error logs for specific issues

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When contributing to the integration:

1. Test the test generation workflow thoroughly
2. Update the test script with new features
3. Document any API changes
4. Ensure backward compatibility

## Conclusion

The integration successfully provides:

- ✅ Technology-specific question generation
- ✅ Difficulty level support
- ✅ Robust error handling and validation
- ✅ Backward compatibility
- ✅ Enhanced data structure and metadata
- ✅ Comprehensive testing and documentation

This creates a powerful and flexible test generation service that can handle a wide variety of use cases with reliable question generation. 