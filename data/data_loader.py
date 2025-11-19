import json
from typing import List, Dict, Any

class DataLoader:
    def __init__(self, file_path: str = None):
        from config import DEFAULT_DATA_FILE
        self.file_path = file_path or DEFAULT_DATA_FILE
    
    def load_data(self) -> List[Dict[str, Any]]:
        data = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        data.append(json.loads(line))
            print(f"Loaded {len(data)} records from {self.file_path}")
            return data
        except FileNotFoundError:
            print(f"Error: Data file not found at {self.file_path}")
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
