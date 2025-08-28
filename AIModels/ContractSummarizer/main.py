from src.preprocessor import DocumentPreprocessor
from src.classifier import ClauseClassifier
from src.summarizer import ContractSummarizer
from src.output_generator import OutputGenerator
import argparse
import os

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Contract Summarization Tool')
    parser.add_argument('input_file', help='Path to the contract file (PDF/TXT)')
    parser.add_argument('--output-dir', default='output', help='Output directory for results')
    args = parser.parse_args()
    
    # Initialize components
    preprocessor = DocumentPreprocessor()
    classifier = ClauseClassifier()
    summarizer = ContractSummarizer()
    output_gen = OutputGenerator(args.output_dir)
    
    # Process document
    print("Reading and preprocessing document...")
    full_text, clauses = preprocessor.process_document(args.input_file)
    
    # Identify important clauses
    print("Identifying important clauses...")
    important_clauses = classifier.identify_important_clauses(clauses)
    
    # Generate summaries
    print("Generating summaries...")
    summary_data = summarizer.summarize_contract(full_text, important_clauses)
    
    # Save outputs
    print("Saving results...")
    base_filename = os.path.splitext(os.path.basename(args.input_file))[0]
    output_gen.save_json(summary_data, f"{base_filename}_summary.json")
    output_gen.create_word_report(summary_data, f"{base_filename}_report.docx")
    
    print("Done! Results saved in:", args.output_dir)

if __name__ == "__main__":
    main()
