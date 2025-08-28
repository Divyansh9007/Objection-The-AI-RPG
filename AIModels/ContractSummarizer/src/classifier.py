from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List
import numpy as np

class ClauseClassifier:
    def __init__(self, model_name: str = "nlpaueb/legal-bert-base-uncased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.clause_types = [
            "jurisdiction",
            "indemnity",
            "termination",
            "confidentiality",
            "arbitration",
            "liability",
            "payment"
        ]
        
    def classify_clause(self, text: str) -> Dict[str, float]:
        """Classify a clause into predefined categories."""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            
        # Convert probabilities to dictionary
        clause_scores = {
            clause_type: float(prob)
            for clause_type, prob in zip(self.clause_types, probs[0])
        }
        
        return clause_scores
    
    def identify_important_clauses(self, clauses: List[Dict[str, str]], threshold: float = 0.5) -> List[Dict]:
        """Identify and categorize important clauses."""
        important_clauses = []
        
        for clause in clauses:
            scores = self.classify_clause(clause["content"])
            
            # Get the highest scoring category
            max_category = max(scores.items(), key=lambda x: x[1])
            
            if max_category[1] > threshold:
                important_clauses.append({
                    "heading": clause["heading"],
                    "content": clause["content"],
                    "type": max_category[0],
                    "confidence": max_category[1]
                })
                
        return important_clauses
