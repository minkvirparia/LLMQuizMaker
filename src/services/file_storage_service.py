import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid

class FileStorageService:
    """Service for managing file-based storage operations."""
    
    def __init__(self):
        self.base_dir = Path("data")
        self.tests_dir = self.base_dir / "tests"
        self.settings_dir = self.base_dir / "settings"
        self.exports_dir = self.base_dir / "exports"
        self.logs_dir = self.base_dir / "logs"
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories."""
        for directory in [self.tests_dir, self.settings_dir, self.exports_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _get_tests_file(self) -> Path:
        """Get the tests storage file path."""
        return self.tests_dir / "tests.json"
    
    def _get_settings_file(self) -> Path:
        """Get the settings storage file path."""
        return self.settings_dir / "app_settings.json"
    
    def _get_user_settings_file(self, user_id: str = "default") -> Path:
        """Get user-specific settings file path."""
        return self.settings_dir / f"user_{user_id}_settings.json"
    
    def _get_test_set_file(self, test_set_id: str) -> Path:
        """Get individual test set file path."""
        return self.tests_dir / f"test_set_{test_set_id}.json"
    
    def _get_export_file(self, filename: str) -> Path:
        """Get export file path."""
        return self.exports_dir / filename
    
    def _get_log_file(self) -> Path:
        """Get log file path."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        return self.logs_dir / f"app_log_{timestamp}.json"
    
    def save_tests(self, tests: List[Dict[str, Any]], test_name: str) -> str:
        """Save tests to file system."""
        try:
            # Validate input
            if not tests:
                raise ValueError("No tests provided to save")
            
            if not test_name or not test_name.strip():
                test_name = "Untitled Test"
            
            # Generate unique ID for the test set
            test_set_id = str(uuid.uuid4())
            
            # Create test set data
            test_set = {
                'id': test_set_id,
                'title': test_name,
                'tests': tests,
                'created_date': datetime.now().isoformat(),
                'total_tests': len(tests),
                'metadata': {
                    'technology': tests[0].get('technology', 'Unknown') if tests else 'Unknown',
                    'test_name': tests[0].get('test_name', 'Unknown') if tests else 'Unknown',
                    'difficulty': tests[0].get('difficulty', 'Unknown') if tests else 'Unknown'
                }
            }
            
            # Ensure tests directory exists
            self.tests_dir.mkdir(parents=True, exist_ok=True)
            
            # Save to individual file
            test_set_file = self._get_test_set_file(test_set_id)
            with open(test_set_file, 'w', encoding='utf-8') as f:
                json.dump(test_set, f, indent=2, ensure_ascii=False)
            
            # Update main tests index
            self._update_tests_index(test_set)
            
            # Log the operation
            self._log_operation("save_tests", {
                "test_set_id": test_set_id,
                "test_name": test_name,
                "test_count": len(tests),
                "file_path": str(test_set_file)
            })
            
            return test_set_id
            
        except Exception as e:
            error_msg = f"Error saving tests: {str(e)}"
            self._log_error("save_tests", error_msg)
            raise Exception(error_msg)
    
    def load_tests(self) -> List[Dict[str, Any]]:
        """Load all tests from file system."""
        try:
            tests_file = self._get_tests_file()
            if tests_file.exists():
                with open(tests_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self._log_error("load_tests", str(e))
            return []
    
    def get_test_set(self, test_set_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific test set by ID."""
        try:
            test_set_file = self._get_test_set_file(test_set_id)
            if test_set_file.exists():
                with open(test_set_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            self._log_error("get_test_set", str(e))
            return None
    
    def delete_test_set(self, test_set_id: str) -> bool:
        """Delete a test set."""
        try:
            # Remove individual file
            test_set_file = self._get_test_set_file(test_set_id)
            if test_set_file.exists():
                test_set_file.unlink()
            
            # Update main index
            tests = self.load_tests()
            tests = [ts for ts in tests if ts.get('id') != test_set_id]
            self._save_tests_index(tests)
            
            # Log the operation
            self._log_operation("delete_test_set", {
                "test_set_id": test_set_id
            })
            
            return True
        except Exception as e:
            self._log_error("delete_test_set", str(e))
            return False
    
    def update_test_set(self, test_set_id: str, updated_data: Dict[str, Any]) -> bool:
        """Update a test set."""
        try:
            test_set_file = self._get_test_set_file(test_set_id)
            if test_set_file.exists():
                with open(test_set_file, 'r', encoding='utf-8') as f:
                    test_set = json.load(f)
                
                # Update the data
                test_set.update(updated_data)
                
                # Save back to file
                with open(test_set_file, 'w', encoding='utf-8') as f:
                    json.dump(test_set, f, indent=2, ensure_ascii=False)
                
                # Update main index
                self._update_tests_index(test_set)
                
                # Log the operation
                self._log_operation("update_test_set", {
                    "test_set_id": test_set_id
                })
                
                return True
            return False
        except Exception as e:
            self._log_error("update_test_set", str(e))
            return False
    
    def save_settings(self, settings: Dict[str, Any], user_id: str = "default") -> bool:
        """Save user settings."""
        try:
            settings_file = self._get_user_settings_file(user_id)
            
            # Ensure directory exists
            settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            # Log the operation
            self._log_operation("save_settings", {
                "user_id": user_id,
                "settings_keys": list(settings.keys())
            })
            
            return True
        except Exception as e:
            self._log_error("save_settings", str(e))
            return False
    
    def load_settings(self, user_id: str = "default") -> Dict[str, Any]:
        """Load user settings."""
        try:
            settings_file = self._get_user_settings_file(user_id)
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self._log_error("load_settings", str(e))
            return {}
    
    def export_tests(self, test_set_id: str, format: str = "json") -> Optional[Path]:
        """Export tests to a file."""
        try:
            test_set = self.get_test_set(test_set_id)
            if not test_set:
                return None
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = test_set.get('title', 'test').replace(' ', '_')
            filename = f"{test_name}_{timestamp}.{format}"
            export_file = self._get_export_file(filename)
            
            if format == "json":
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(test_set, f, indent=2, ensure_ascii=False)
            elif format == "txt":
                self._export_to_txt(test_set, export_file)
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            # Log the operation
            self._log_operation("export_tests", {
                "test_set_id": test_set_id,
                "format": format,
                "export_file": str(export_file)
            })
            
            return export_file
        except Exception as e:
            self._log_error("export_tests", str(e))
            return None
    
    def _export_to_txt(self, test_set: Dict[str, Any], file_path: Path):
        """Export tests to text format."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Test: {test_set.get('title', 'Untitled')}\n")
            f.write(f"Created: {test_set.get('created_date', 'Unknown')}\n")
            f.write(f"Total Tests: {test_set.get('total_tests', 0)}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, test in enumerate(test_set.get('tests', []), 1):
                f.write(f"Test {i}:\n")
                f.write(f"{test.get('test', '')}\n\n")
                
                options = test.get('options', [])
                for j, option in enumerate(options):
                    f.write(f"{chr(65+j)}. {option}\n")
                
                f.write(f"\nCorrect Answer: {test.get('correct_answer', '')}\n")
                f.write(f"Explanation: {test.get('explanation', '')}\n")
                f.write("-" * 30 + "\n\n")
    
    def _update_tests_index(self, test_set: Dict[str, Any]):
        """Update the main tests index."""
        try:
            tests = self.load_tests()
            
            # Remove existing entry if it exists
            tests = [ts for ts in tests if ts.get('id') != test_set.get('id')]
            
            # Add new/updated entry
            tests.append(test_set)
            
            # Save updated index
            self._save_tests_index(tests)
            
        except Exception as e:
            error_msg = f"Error updating tests index: {str(e)}"
            self._log_error("_update_tests_index", error_msg)
            raise Exception(error_msg)
    
    def _save_tests_index(self, tests: List[Dict[str, Any]]):
        """Save the tests index."""
        try:
            tests_file = self._get_tests_file()
            
            # Ensure directory exists
            tests_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(tests_file, 'w', encoding='utf-8') as f:
                json.dump(tests, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            error_msg = f"Error saving tests index: {str(e)}"
            self._log_error("_save_tests_index", error_msg)
            raise Exception(error_msg)
    
    def _log_operation(self, operation: str, data: Dict[str, Any]):
        """Log an operation."""
        try:
            log_file = self._get_log_file()
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'operation': operation,
                'data': data
            }
            
            logs = []
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception:
            # Silently fail if logging fails
            pass
    
    def _log_error(self, operation: str, error_message: str):
        """Log an error."""
        self._log_operation(f"{operation}_error", {"error": error_message})
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        try:
            tests = self.load_tests()
            settings_files = list(self.settings_dir.glob("*.json"))
            export_files = list(self.exports_dir.glob("*"))
            
            return {
                'total_test_sets': len(tests),
                'total_tests': sum(len(ts.get('tests', [])) for ts in tests),
                'settings_files': len(settings_files),
                'export_files': len(export_files),
                'storage_size': self._get_directory_size(self.base_dir)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _get_directory_size(self, directory: Path) -> int:
        """Get directory size in bytes."""
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        return total_size
    
    def cleanup_old_files(self, days: int = 30):
        """Clean up old files."""
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            # Clean up old log files
            for log_file in self.logs_dir.glob("*.json"):
                if log_file.stat().st_mtime < cutoff_date:
                    log_file.unlink()
            
            # Clean up old export files
            for export_file in self.exports_dir.glob("*"):
                if export_file.stat().st_mtime < cutoff_date:
                    export_file.unlink()
                    
        except Exception as e:
            self._log_error("cleanup_old_files", str(e)) 