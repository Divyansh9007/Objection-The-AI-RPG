import pdfplumber
import re
from typing import List, Dict, Union, Tuple
import nltk
from nltk.tokenize import sent_tokenize

class DocumentPreprocessor:
    def __init__(self):
        nltk.download('punkt')
        
    def read_document(self, file_path: str) -> str:
        """Read document content from PDF or TXT file."""
        if file_path.lower().endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                text = '\n'.join(page.extract_text() for page in pdf.pages)
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        return text
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove page numbers and headers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n', text)
        # Remove special characters but keep periods
        text = re.sub(r'[^\w\s\.\-,:]', ' ', text)
        return text.strip()
    
    def split_into_clauses(self, text: str) -> List[Dict[str, str]]:
        """Split contract into clauses based on section headings."""
        # Common section heading patterns
        section_pattern = r'(?i)(?:\d+\.?\s+)?(?:ARTICLE|SECTION|CLAUSE)\s+[IVXLCDM\d]+\.?\s*([^.\n]+)'
        sections = re.split(section_pattern, text)
        
        clauses = []
        for i in range(1, len(sections), 2):
            if i < len(sections):
                heading = sections[i].strip()
                content = sections[i+1].strip() if i+1 < len(sections) else ""
                clauses.append({
                    "heading": heading,
                    "content": content
                })
        
        return clauses
    
    def process_document(self, file_path: str) -> Tuple[str, List[Dict[str, str]]]:
        """Main processing pipeline."""
        # Read document
        text = self.read_document(file_path)
        
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Split into clauses
        clauses = self.split_into_clauses(cleaned_text)
        
        return cleaned_text, clauses
