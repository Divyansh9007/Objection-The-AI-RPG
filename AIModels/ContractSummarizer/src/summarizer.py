from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from typing import Dict, List

class ContractSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 30) -> str:
        """Generate a summary for the given text."""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        
        summary_ids = self.model.generate(
            inputs["input_ids"],
            max_length=max_length,
            min_length=min_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )
        
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    def summarize_contract(self, full_text: str, important_clauses: List[Dict]) -> Dict:
        """Generate summaries for the full contract and important clauses."""
        # Generate executive summary
        executive_summary = self.summarize_text(full_text, max_length=200)
        
        # Summarize each important clause
        clause_summaries = []
        for clause in important_clauses:
            summary = self.summarize_text(clause["content"], max_length=100)
            clause_summaries.append({
                "type": clause["type"],
                "heading": clause["heading"],
                "summary": summary,
                "confidence": clause["confidence"]
            })
        
        return {
            "executive_summary": executive_summary,
            "clause_summaries": clause_summaries
        }
