import json
import re
from typing import Dict, List, Tuple
from datetime import datetime

class EntityExtractor:
    """Extracts named entities from user input."""
    
    def __init__(self, entities_file: str = "data/entities.json"):
        """Initialize EntityExtractor with entity patterns."""
        self.entities = self._load_entities(entities_file)
        self.extracted_entities = {}
    
    def _load_entities(self, file_path: str) -> Dict:
        """Load entity patterns from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get('entities', {})
        except FileNotFoundError:
            print(f"Warning: Entities file '{file_path}' not found.")
            return {}
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text."""
        text_lower = text.lower()
        extracted = {}
        
        for entity_type, entity_data in self.entities.items():
            patterns = entity_data.get('patterns', [])
            matches = []
            
            for pattern in patterns:
                # Exact match
                if pattern in text_lower:
                    matches.append(pattern)
                # Partial match with word boundaries
                elif re.search(r'\b' + pattern + r'\b', text_lower):
                    matches.append(pattern)
            
            if matches:
                extracted[entity_type] = list(set(matches))
        
        # Extract numbers
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            extracted['NUMBER'] = numbers
        
        # Extract dates
        dates = self._extract_dates(text)
        if dates:
            extracted['DATE'] = dates
        
        self.extracted_entities = extracted
        return extracted
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract date patterns from text."""
        dates = []
        
        # Pattern for dates like "2024-01-15" or "01/15/2024"
        date_pattern = r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}'
        dates.extend(re.findall(date_pattern, text))
        
        # Pattern for named dates
        named_dates = ['today', 'tomorrow', 'yesterday', 'monday', 'tuesday', 'wednesday', 
                       'thursday', 'friday', 'saturday', 'sunday', 'january', 'february',
                       'march', 'april', 'may', 'june', 'july', 'august', 'september',
                       'october', 'november', 'december']
        
        text_lower = text.lower()
        for date_name in named_dates:
            if date_name in text_lower:
                dates.append(date_name)
        
        return dates
    
    def get_entities(self) -> Dict[str, List[str]]:
        """Return extracted entities."""
        return self.extracted_entities
    
    def get_entity_by_type(self, entity_type: str) -> List[str]:
        """Get entities of a specific type."""
        return self.extracted_entities.get(entity_type, [])
