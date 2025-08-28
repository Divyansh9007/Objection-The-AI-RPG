# Contract Summarizer

A Python-based tool that uses state-of-the-art NLP models to analyze and summarize legal contracts. The tool extracts key clauses, provides summaries in layman's terms, and generates structured reports.

## Features

- Document preprocessing for PDF and TXT files
- Automatic clause detection and classification
- Important clause highlighting (Jurisdiction, Indemnity, Termination, etc.)
- Contract summarization in simple language
- Export to JSON and Word formats

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool from the command line:

```bash
python main.py path/to/contract.pdf --output-dir output
```

The tool will:

1. Process the contract document
2. Identify and classify important clauses
3. Generate summaries
4. Save results as JSON and Word documents in the output directory

## Architecture

The project uses a hybrid approach combining:

- LegalBERT for clause classification
- PEGASUS for text summarization
- Custom preprocessing pipeline for document handling

Components:

- `preprocessor.py`: Document reading and text preprocessing
- `classifier.py`: Clause classification using LegalBERT
- `summarizer.py`: Text summarization using PEGASUS
- `output_generator.py`: Report generation in various formats

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- Sufficient disk space for model downloads

## Output Format

The tool generates two types of output files:

1. JSON file with structured data
2. Word document with formatted report

## License

MIT License
