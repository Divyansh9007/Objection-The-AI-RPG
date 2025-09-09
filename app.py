import json
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
import pickle
import os
from datetime import datetime

# Function to load IPC data from JSON file
def load_ipc_data(filename='ipc.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Download from https://github.com/civictech-India/Indian-Law-Penal-Code-Json/blob/main/ipc.json")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in ipc.json.")
        sys.exit(1)

# Enhanced text cleaning for better embedding quality, handling diverse texts
def clean_text(text):
    if not text or isinstance(text, float):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    # General stop words for legal context
    stop_words = r'\b(a|an|the|and|or|but|in|on|at|to|for|of|with|by|as|is|are|was|were|be|been|have|has|had|do|does|did|will|would|shall|should|may|might|can|could)\b'
    text = re.sub(stop_words, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Preprocess and prepare data, excluding repealed sections
def prepare_data(data):
    texts = []
    valid_sections = []
    for item in data:
        desc_lower = item.get('section_desc', '').lower()
        if 'repealed' in desc_lower:
            continue
        title = clean_text(item.get('section_title', ''))
        desc = clean_text(item.get('section_desc', ''))
        text = f"{title} {desc}".strip()
        if len(text) > 512:  # Truncate for model compatibility
            text = text[:512]
        if text:
            texts.append(text)
            valid_sections.append(item)
    return texts, valid_sections

# Load or compute BERT embeddings with timestamped cache
def get_embeddings(texts, model, cache_file='embeddings.pkl'):
    timestamp_cache = f"{cache_file}_{datetime.now().strftime('%Y%m%d')}"
    if os.path.exists(timestamp_cache):
        with open(timestamp_cache, 'rb') as f:
            return pickle.load(f)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    with open(timestamp_cache, 'wb') as f:
        pickle.dump(embeddings, f)
    return embeddings

# Broad keyword map for diverse scenarios, avoiding overfitting
keyword_map = {
    r'theft|stole|steal|snatch|rob|take': 'theft dishonest misappropriation property without consent section 378 379 390 391',
    r'hurt|injure|assault|attack|hit|beat|wound': 'hurt grievous hurt criminal force bodily injury section 319 320 323 324 325 326 351 352',
    r'kill|murder|death|die|fatal': 'murder culpable homicide intention cause death section 299 300 302 304 304a',
    r'vehicle|driving|accident|crash|hit and run': 'rash negligent driving endangering life personal safety section 279 304a 337 338',
    r'gun|shoot|firearm|weapon': 'culpable homicide murder grievous hurt dangerous weapons section 299 300 302 304 324 326 307',
    r'cheat|fraud|scam|deceive|lie': 'cheating dishonest inducement fraud section 415 420',
    r'forge|counterfeit|fake document': 'forgery false document electronic record section 463 465 466 467 468',
    r'trespass|break in|enter illegally|intrude': 'criminal trespass house trespass lurking house breaking section 441 442 443 444 445 446',
    r'damage|destroy|vandalize|burn|arson': 'mischief destruction property wrongful loss section 425 426 427 435 436',
    r'rape|sexual assault|molest|harass': 'rape outrage modesty sexual offense section 375 376 354 509',
    r'kidnap|abduct|confine': 'kidnapping abduction wrongful confinement section 359 360 361 362 363 340',
    r'dowry|cruelty|harassment': 'cruelty husband relatives dowry death section 498a 304b',
    r'poison|drug': 'administer poison hurt grievous hurt section 324 326 328',
    r'bribe|corruption': 'criminal misconduct bribery public servant section 409 420',
    r'defame|slander|libel': 'defamation harm reputation section 499 500',
    r'threat|blackmail|intimidate': 'criminal intimidation threat injury section 503 506 507',
    r'drunk|intoxicate|public nuisance': 'public nuisance drunkenness annoyance section 268 510',
    r'cyber|hack|data': 'cheating electronic record breach trust section 403 406 420',
}

# Augment user input with legal keywords for better matching
def augment_input(scenario):
    scenario_clean = clean_text(scenario)
    augmented = scenario_clean
    matched = False
    for user_terms, legal_terms in keyword_map.items():
        if re.search(user_terms, scenario_clean, re.IGNORECASE):
            augmented += f" {legal_terms}"
            matched = True
    if not matched:
        augmented += " criminal offence ipc section"
    if len(augmented) > 512:
        augmented = augmented[:512]
    return augmented.strip()

# Process a single scenario and return top k matches
def process_scenario(scenario, texts, valid_sections, model, embeddings, top_k=3, low_score_threshold=0.3):
    if not scenario or len(scenario.strip()) < 5:
        return {"error": "Please provide a scenario (at least 5 characters)."}
    
    augmented_scenario = augment_input(scenario)
    scenario_vec = model.encode([augmented_scenario], convert_to_numpy=True)
    similarities = cosine_similarity(scenario_vec, embeddings)[0]
    
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    matches = []
    for idx in top_indices:
        score = similarities[idx]
        match = {
            'section': valid_sections[idx].get('Section', 'N/A'),
            'chapter': valid_sections[idx].get('chapter_title', 'N/A').title(),
            'title': valid_sections[idx].get('section_title', 'N/A'),
            'description': valid_sections[idx].get('section_desc', 'N/A'),
            'score': score
        }
        matches.append(match)
    
    warning = ""
    if matches[0]['score'] < low_score_threshold:
        warning = "Note: Low confidence. Try including specific details or legal terms (e.g., 'negligent', 'assault', 'theft') for better results."
    
    return {
        "matches": matches,
        "warning": warning
    }

# Main function to process a scenario
def find_ipc_section(scenario, top_k=3):
    data = load_ipc_data()
    texts, valid_sections = prepare_data(data)
    
    if not texts:
        return {"error": "No valid data found in JSON."}
    
    try:
        model = SentenceTransformer('all-mpnet-base-v2')
    except Exception as e:
        print(f"Warning: Failed to load primary model, falling back: {e}")
        try:
            model = SentenceTransformer('paraphrase-mpnet-base-v2')
        except:
            model = SentenceTransformer('all-MiniLM-L6-v2')
    
    embeddings = get_embeddings(texts, model)
    
    result = process_scenario(scenario, texts, valid_sections, model, embeddings, top_k)
    if "error" in result:
        return result
    
    return {
        "scenario": scenario,
        "top_matches": result["matches"],
        "warning": result["warning"]
    }

# Formatted print function
def print_results(result):
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print("\n" + "="*70)
    print(f"Scenario Analyzed: {result['scenario']}")
    print("="*70)
    
    if result['warning']:
        print(result['warning'])
    
    print("\nTop Matching IPC Sections:")
    for i, match in enumerate(result['top_matches'], 1):
        score_pct = match['score'] * 100
        print(f"\n{i}. Section {match['section']} - {match['chapter']}")
        print(f"   Title: {match['title']}")
        print(f"   Description: {match['description']}")
        print(f"   Confidence Score: {match['score']:.4f} ({score_pct:.2f}%)")

# Interactive input
if __name__ == "__main__":
    print("Enter a scenario to find matching IPC sections (or press Enter to exit):")
    user_scenario = input().strip()
    while user_scenario:
        result = find_ipc_section(user_scenario)
        print_results(result)
        print("\nEnter another scenario (or press Enter to exit):")
        user_scenario = input().strip()