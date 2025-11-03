import json
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re
import pickle
import os
from datetime import datetime
from collections import Counter, defaultdict
import logging
from typing import List, Dict, Tuple, Any
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    logger.warning("Could not download NLTK data. Using basic preprocessing.")

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

# Advanced text preprocessing with legal-specific enhancements
class LegalTextPreprocessor:
    def __init__(self):
        try:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        except:
            self.lemmatizer = None
            self.stop_words = set(['the', 'is', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        
        # Legal-specific stop words to preserve
        self.legal_preserve = {
            'shall', 'may', 'must', 'liable', 'guilty', 'offence', 'punishment', 
            'imprisonment', 'fine', 'death', 'life', 'years', 'months', 'days',
            'section', 'chapter', 'act', 'code', 'law', 'court', 'judge'
        }
        
        # Remove common stop words but preserve legal terms
        self.stop_words = self.stop_words - self.legal_preserve
        
        # Legal synonyms for better matching
        self.legal_synonyms = {
            'kill': ['murder', 'homicide', 'slay', 'eliminate'],
            'steal': ['theft', 'rob', 'burgle', 'pilfer', 'embezzle'],
            'hit': ['assault', 'attack', 'strike', 'beat'],
            'hurt': ['harm', 'injure', 'wound', 'damage'],
            'cheat': ['fraud', 'deceive', 'swindle', 'con'],
            'lie': ['falsehood', 'perjury', 'fabricate', 'mislead'],
            'threaten': ['intimidate', 'menace', 'coerce', 'blackmail'],
            'take': ['seize', 'confiscate', 'appropriate', 'misappropriate']
        }
    
    def clean_text(self, text: str, preserve_legal_numbers: bool = False) -> str:
        """Enhanced text cleaning with legal context preservation"""
        if not text or isinstance(text, float):
            return ""
        
        text = str(text).lower()
        
        # Preserve legal section numbers if specified
        if preserve_legal_numbers:
            # Protect section numbers like "section 302", "302", "ipc 302"
            text = re.sub(r'\b(section\s+)?(\d{1,3}[a-z]?)\b', r'sec_\2', text)
        
        # Remove excessive punctuation but keep legal abbreviations
        text = re.sub(r'[^\w\s\-\.]', ' ', text)
        
        # Tokenize
        try:
            tokens = word_tokenize(text) if 'word_tokenize' in globals() else text.split()
        except:
            tokens = text.split()
        
        # Process tokens
        processed_tokens = []
        for token in tokens:
            # Skip very short tokens unless they're legal abbreviations
            if len(token) < 2 and token not in ['a', 'i']:
                continue
            
            # Skip stop words but preserve legal terms
            if token in self.stop_words:
                continue
            
            # Lemmatize if available
            if self.lemmatizer:
                try:
                    token = self.lemmatizer.lemmatize(token)
                except:
                    pass
            
            processed_tokens.append(token)
        
        # Restore section numbers
        text = ' '.join(processed_tokens)
        if preserve_legal_numbers:
            text = re.sub(r'sec_(\d+[a-z]?)', r'section \1', text)
        
        return ' '.join(text.split())  # Remove extra spaces
    
    def expand_with_synonyms(self, text: str) -> str:
        """Expand text with legal synonyms"""
        words = text.split()
        expanded_words = list(words)  # Start with original words
        
        for word in words:
            if word in self.legal_synonyms:
                expanded_words.extend(self.legal_synonyms[word][:2])  # Add top 2 synonyms
        
        return ' '.join(expanded_words)

# Initialize global preprocessor
text_processor = LegalTextPreprocessor()

# Enhanced data preparation with multiple text representations
def prepare_data(data):
    texts = []
    tfidf_texts = []
    valid_sections = []
    section_metadata = []
    
    for item in data:
        desc_lower = item.get('section_desc', '').lower()
        if 'repealed' in desc_lower:
            continue
        
        # Get raw text components
        title = item.get('section_title', '')
        desc = item.get('section_desc', '')
        section_num = item.get('Section', '')
        chapter = item.get('chapter_title', '')
        
        # Clean text for embeddings (preserve legal context)
        title_clean = text_processor.clean_text(title, preserve_legal_numbers=True)
        desc_clean = text_processor.clean_text(desc, preserve_legal_numbers=True)
        
        # Create enhanced text for embeddings
        text_for_embedding = f"{title_clean} {desc_clean}".strip()
        if chapter:
            chapter_clean = text_processor.clean_text(chapter)
            text_for_embedding = f"{chapter_clean} {text_for_embedding}"
        
        # Create text with synonyms for TF-IDF
        text_with_synonyms = text_processor.expand_with_synonyms(text_for_embedding)
        
        # Truncate if too long
        if len(text_for_embedding) > 512:
            text_for_embedding = text_for_embedding[:512]
        if len(text_with_synonyms) > 1024:
            text_with_synonyms = text_with_synonyms[:1024]
        
        if text_for_embedding:
            texts.append(text_for_embedding)
            tfidf_texts.append(text_with_synonyms)
            valid_sections.append(item)
            
            # Store metadata for weighted scoring
            metadata = {
                'section_number': section_num,
                'title_length': len(title_clean.split()),
                'desc_length': len(desc_clean.split()),
                'has_punishment': any(word in desc_lower for word in ['imprisonment', 'fine', 'death', 'punishment']),
                'is_definition': 'definition' in desc_lower or 'denotes' in desc_lower,
                'chapter': chapter
            }
            section_metadata.append(metadata)
    
    return texts, tfidf_texts, valid_sections, section_metadata

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

# Comprehensive and intelligent keyword mapping system
class EnhancedKeywordMapper:
    def __init__(self):
        # Core criminal acts with contextual variations
        self.keyword_map = {
            # Theft and Property Offenses
            r'theft|stole|steal|snatch|rob|take|pilfer|embezzle|misappropriat': {
                'terms': 'theft robbery dacoity dishonest misappropriation property movable immovable without consent criminal breach trust',
                'sections': [378, 379, 380, 381, 382, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409],
                'weight': 1.0
            },
            
            # Violence and Assault
            r'hurt|injure|assault|attack|hit|beat|wound|harm|violence|fight': {
                'terms': 'hurt grievous hurt simple hurt voluntarily causing assault criminal force bodily injury physical harm violence',
                'sections': [319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 351, 352, 353, 354, 355, 356, 357, 358],
                'weight': 1.2
            },
            
            # Murder and Homicide
            r'kill|murder|death|die|fatal|homicide|slay|eliminate': {
                'terms': 'murder culpable homicide intention knowledge death fatal cause dowry death attempt murder conspiracy murder',
                'sections': [299, 300, 301, 302, 303, 304, 304, 305, 306, 307, 308, 309],
                'weight': 1.5
            },
            
            # Traffic and Vehicular Offenses
            r'vehicle|driving|accident|crash|hit.and.run|rash|negligent|traffic': {
                'terms': 'rash negligent driving endangering life personal safety public way vehicle accident crash negligence',
                'sections': [279, 280, 304, 337, 338],
                'weight': 0.8
            },
            
            # Weapons and Firearms
            r'gun|shoot|firearm|weapon|knife|sword|dangerous.weapon|armed': {
                'terms': 'dangerous weapons firearm arms ammunition grievous hurt murder attempt culpable homicide weapon',
                'sections': [299, 300, 302, 304, 307, 324, 325, 326, 327],
                'weight': 1.3
            },
            
            # Fraud and Cheating
            r'cheat|fraud|scam|deceive|lie|swindle|con|trick|mislead': {
                'terms': 'cheating dishonest inducement delivery property fraud deception misrepresentation false promise',
                'sections': [415, 416, 417, 418, 419, 420],
                'weight': 1.0
            },
            
            # Forgery and Document Fraud
            r'forge|forgery|counterfeit|fake.document|falsify|false.document': {
                'terms': 'forgery forged document counterfeit false document electronic record signature seal fraud document',
                'sections': [463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477],
                'weight': 1.1
            },
            
            # Trespass and Breaking
            r'trespass|break.in|breaking|enter.illegally|intrude|burglary': {
                'terms': 'criminal trespass house trespass lurking house breaking burglary unlawful entry property',
                'sections': [441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460],
                'weight': 1.0
            },
            
            # Property Damage
            r'damage|destroy|vandalize|burn|arson|fire|mischief': {
                'terms': 'mischief destruction property fire arson wrongful loss damage burn public private property',
                'sections': [425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438],
                'weight': 1.0
            },
            
            # Sexual Offenses
            r'rape|sexual.assault|molest|harassment|outrage.modesty|sexual': {
                'terms': 'rape sexual assault outrage modesty sexual harassment indecent assault sexual offense women',
                'sections': [354, 375, 376, 509],
                'weight': 1.4
            },
            
            # Kidnapping and Abduction
            r'kidnap|abduct|confine|detention|wrongful.confinement': {
                'terms': 'kidnapping abduction wrongful confinement wrongful restraint detention unlawful confinement',
                'sections': [339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374],
                'weight': 1.3
            },
            
            # Dowry and Domestic Violence
            r'dowry|cruelty|domestic.violence|husband|wife|harassment': {
                'terms': 'cruelty husband relatives dowry death domestic violence harassment women protection',
                'sections': [304, 498],
                'weight': 1.2
            },
            
            # Poisoning and Drugging
            r'poison|drug|administer|noxious|substance|intoxicat': {
                'terms': 'administer poison noxious substance drug stupefying intoxicating hurt grievous hurt',
                'sections': [284, 285, 286, 287, 328],
                'weight': 1.1
            },
            
            # Corruption and Bribery
            r'bribe|corruption|corrupt|public.servant|misconduct': {
                'terms': 'criminal misconduct public servant bribery corruption dishonest illegal gratification',
                'sections': [403, 409, 420],
                'weight': 1.0
            },
            
            # Defamation
            r'defame|defamation|slander|libel|reputation|insult': {
                'terms': 'defamation publication harm reputation imputation insult criminal defame',
                'sections': [499, 500],
                'weight': 0.8
            },
            
            # Criminal Intimidation
            r'threat|threaten|blackmail|intimidate|coerce|menace': {
                'terms': 'criminal intimidation threat alarm injury reputation property person blackmail coercion',
                'sections': [503, 504, 505, 506, 507, 508],
                'weight': 1.0
            },
            
            # Public Nuisance
            r'nuisance|disturb|annoy|public.place|drunk|intoxicat': {
                'terms': 'public nuisance annoyance common injury public drunkenness public place disturbance',
                'sections': [268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 510],
                'weight': 0.7
            },
            
            # Cyber Crimes
            r'cyber|hack|computer|electronic|digital|online|internet|data': {
                'terms': 'electronic record computer cyber crime digital fraud hacking data theft online cheating',
                'sections': [420, 463, 465, 468],
                'weight': 1.0
            },
            
            # Rioting and Unlawful Assembly
            r'riot|mob|unlawful.assembly|fight|group.violence|affray': {
                'terms': 'rioting unlawful assembly affray public order disturbance mob violence group crime',
                'sections': [141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160],
                'weight': 1.1
            }
        }
        
        # Scenario type detection patterns
        self.scenario_types = {
            'violent_crime': r'kill|murder|attack|assault|fight|beat|stab|shoot|violence',
            'property_crime': r'theft|steal|rob|burglary|break.in|damage|destroy|arson',
            'fraud_crime': r'cheat|fraud|scam|deceive|forge|counterfeit|fake',
            'sexual_crime': r'rape|molest|sexual|harassment|assault.on.women',
            'traffic_crime': r'accident|driving|vehicle|crash|hit.and.run|rash|negligent',
            'cyber_crime': r'cyber|hack|computer|online|electronic|digital|internet',
            'domestic_crime': r'dowry|domestic|husband|wife|family|home|cruelty',
            'public_order': r'riot|mob|disturb|nuisance|public|gathering|protest'
        }
    
    def detect_scenario_type(self, text: str) -> List[str]:
        """Detect the type of criminal scenario"""
        text_lower = text.lower()
        detected_types = []
        
        for scenario_type, pattern in self.scenario_types.items():
            if re.search(pattern, text_lower):
                detected_types.append(scenario_type)
        
        return detected_types if detected_types else ['general_crime']
    
    def get_enhanced_terms(self, text: str) -> Tuple[str, List[int], float]:
        """Get enhanced legal terms and relevant sections with confidence weight"""
        text_lower = text.lower()
        matched_terms = []
        relevant_sections = []
        total_weight = 0.0
        match_count = 0
        
        for pattern, info in self.keyword_map.items():
            if re.search(pattern, text_lower):
                matched_terms.append(info['terms'])
                relevant_sections.extend(info['sections'])
                total_weight += info['weight']
                match_count += 1
        
        # Calculate average weight
        avg_weight = total_weight / match_count if match_count > 0 else 0.5
        
        # Add scenario-specific terms
        scenario_types = self.detect_scenario_type(text)
        for s_type in scenario_types:
            matched_terms.append(f"{s_type.replace('_', ' ')} criminal offense ipc")
        
        # Remove duplicates from sections
        relevant_sections = list(set(relevant_sections))
        
        enhanced_terms = ' '.join(matched_terms)
        if not enhanced_terms:
            enhanced_terms = "criminal offense ipc section law"
        
        return enhanced_terms, relevant_sections, avg_weight

# Initialize the enhanced keyword mapper
keyword_mapper = EnhancedKeywordMapper()

# Intelligent query augmentation and expansion
def augment_input(scenario):
    """Enhanced input augmentation with legal terminology and context"""
    # Clean the scenario
    scenario_clean = text_processor.clean_text(scenario, preserve_legal_numbers=True)
    
    # Get enhanced terms from keyword mapper
    enhanced_terms, relevant_sections, weight = keyword_mapper.get_enhanced_terms(scenario)
    
    # Detect scenario types
    scenario_types = keyword_mapper.detect_scenario_type(scenario)
    
    # Build augmented query
    augmented_parts = [scenario_clean]
    
    # Add enhanced legal terms
    if enhanced_terms:
        augmented_parts.append(enhanced_terms)
    
    # Add scenario type specific terms
    type_terms = ' '.join([t.replace('_', ' ') for t in scenario_types])
    augmented_parts.append(type_terms)
    
    # Add specific section numbers if highly relevant
    if relevant_sections and weight > 1.0:
        section_terms = ' '.join([f"section {s}" for s in relevant_sections[:5]])
        augmented_parts.append(section_terms)
    
    # Expand with synonyms
    base_text = ' '.join(augmented_parts)
    expanded_text = text_processor.expand_with_synonyms(base_text)
    
    # Ensure reasonable length
    if len(expanded_text) > 512:
        expanded_text = expanded_text[:512]
    
    return expanded_text.strip()

# Multi-model ensemble for better accuracy
class MultiModelProcessor:
    def __init__(self):
        self.models = []
        self.model_weights = []
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        
    def initialize_models(self):
        """Initialize multiple models for ensemble processing"""
        models_to_try = [
            ('all-mpnet-base-v2', 1.0),
            ('paraphrase-mpnet-base-v2', 0.8),
            ('all-MiniLM-L6-v2', 0.6)
        ]
        
        for model_name, weight in models_to_try:
            try:
                model = SentenceTransformer(model_name)
                self.models.append(model)
                self.model_weights.append(weight)
                logger.info(f"Loaded model: {model_name}")
                break  # Use first available model for now (can be extended to use multiple)
            except Exception as e:
                logger.warning(f"Failed to load model {model_name}: {e}")
                continue
        
        if not self.models:
            raise Exception("No embedding models could be loaded")
    
    def setup_tfidf(self, texts):
        """Setup TF-IDF vectorizer as complementary scoring method"""
        try:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words=None,  # We've already preprocessed
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            logger.info("TF-IDF vectorizer initialized")
        except Exception as e:
            logger.warning(f"TF-IDF setup failed: {e}")
    
    def get_embeddings(self, texts, cache_file='embeddings.pkl'):
        """Get embeddings with caching"""
        timestamp_cache = f"{cache_file}_{datetime.now().strftime('%Y%m%d')}"
        
        if os.path.exists(timestamp_cache):
            try:
                with open(timestamp_cache, 'rb') as f:
                    return pickle.load(f)
            except:
                logger.warning("Failed to load cached embeddings")
        
        if not self.models:
            self.initialize_models()
        
        embeddings = self.models[0].encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        try:
            with open(timestamp_cache, 'wb') as f:
                pickle.dump(embeddings, f)
        except:
            logger.warning("Failed to cache embeddings")
        
        return embeddings
    
    def compute_hybrid_similarity(self, query, texts, embeddings, section_metadata):
        """Compute hybrid similarity using both embeddings and TF-IDF"""
        # Embedding similarity
        query_embedding = self.models[0].encode([query], convert_to_numpy=True)
        embedding_similarities = cosine_similarity(query_embedding, embeddings)[0]
        
        # TF-IDF similarity
        tfidf_similarities = np.zeros(len(texts))
        if self.tfidf_vectorizer and self.tfidf_matrix is not None:
            try:
                query_tfidf = self.tfidf_vectorizer.transform([query])
                tfidf_similarities = linear_kernel(query_tfidf, self.tfidf_matrix)[0]
            except:
                logger.warning("TF-IDF similarity computation failed")
        
        # Combine similarities with weights
        combined_similarities = 0.7 * embedding_similarities + 0.3 * tfidf_similarities
        
        # Apply metadata-based boosting
        for i, metadata in enumerate(section_metadata):
            boost = 1.0
            
            # Boost sections with punishments (more actionable)
            if metadata['has_punishment']:
                boost += 0.1
            
            # Slightly reduce weight for pure definitions
            if metadata['is_definition']:
                boost -= 0.05
            
            # Boost sections with reasonable content length
            if 10 <= metadata['desc_length'] <= 100:
                boost += 0.05
            
            combined_similarities[i] *= boost
        
        return combined_similarities

# Initialize multi-model processor
multi_processor = MultiModelProcessor()

# Process a single scenario and return top k matches
def process_scenario(scenario, texts, valid_sections, model, embeddings, top_k=3, low_score_threshold=0.3):
    """Enhanced scenario processing with multi-model approach and intelligent ranking"""
    if not scenario or len(scenario.strip()) < 5:
        return {"error": "Please provide a scenario (at least 5 characters)."}
    
    # Get augmented query
    augmented_scenario = augment_input(scenario)
    
    # Use multi-model processor for hybrid similarity
    similarities = multi_processor.compute_hybrid_similarity(
        augmented_scenario, texts, embeddings, 
        getattr(multi_processor, 'section_metadata', [])
    )
    
    # Get top matches
    top_indices = np.argsort(similarities)[-top_k * 2:][::-1]  # Get more candidates
    
    # Advanced filtering and ranking
    matches = []
    seen_sections = set()
    
    for idx in top_indices:
        if len(matches) >= top_k:
            break
            
        section_num = valid_sections[idx].get('Section', 'N/A')
        
        # Skip duplicate sections (keep highest scoring)
        if section_num in seen_sections:
            continue
        seen_sections.add(section_num)
        
        score = similarities[idx]
        
        # Enhanced match information
        match = {
            'section': section_num,
            'chapter': valid_sections[idx].get('chapter_title', 'N/A').title(),
            'title': valid_sections[idx].get('section_title', 'N/A'),
            'description': valid_sections[idx].get('section_desc', 'N/A'),
            'score': float(score),
            'confidence': 'High' if score > 0.6 else 'Medium' if score > 0.4 else 'Low',
            'relevance_factors': []
        }
        
        # Add relevance factors for explanation
        if hasattr(multi_processor, 'section_metadata') and idx < len(multi_processor.section_metadata):
            metadata = multi_processor.section_metadata[idx]
            if metadata['has_punishment']:
                match['relevance_factors'].append('Contains punishment details')
            if not metadata['is_definition']:
                match['relevance_factors'].append('Actionable offense')
        
        matches.append(match)
    
    # Generate intelligent warnings and suggestions
    warnings = []
    suggestions = []
    
    if not matches or matches[0]['score'] < low_score_threshold:
        warnings.append("Low confidence match. Consider providing more specific details.")
        
        # Detect scenario type for suggestions
        scenario_types = keyword_mapper.detect_scenario_type(scenario)
        if scenario_types and scenario_types[0] != 'general_crime':
            suggestions.append(f"Detected as {scenario_types[0].replace('_', ' ')} - try including specific terms like location, intent, or method.")
    
    # Check for very high confidence
    if matches and matches[0]['score'] > 0.8:
        matches[0]['confidence'] = 'Very High'
    
    return {
        "matches": matches,
        "warnings": warnings,
        "suggestions": suggestions,
        "scenario_types": keyword_mapper.detect_scenario_type(scenario),
        "query_enhanced": augmented_scenario
    }

# Main function to process a scenario
def find_ipc_section(scenario, top_k=3):
    """Main function with enhanced processing pipeline"""
    try:
        # Load and prepare data
        data = load_ipc_data()
        texts, tfidf_texts, valid_sections, section_metadata = prepare_data(data)
        
        if not texts:
            return {"error": "No valid data found in JSON."}
        
        # Initialize multi-model processor
        multi_processor.initialize_models()
        multi_processor.section_metadata = section_metadata
        
        # Setup TF-IDF for hybrid approach
        multi_processor.setup_tfidf(tfidf_texts)
        
        # Get embeddings
        embeddings = multi_processor.get_embeddings(texts)
        
        # Process scenario
        result = process_scenario(scenario, texts, valid_sections, 
                                multi_processor.models[0], embeddings, top_k)
        
        if "error" in result:
            return result
        
        return {
            "scenario": scenario,
            "top_matches": result["matches"],
            "warnings": result.get("warnings", []),
            "suggestions": result.get("suggestions", []),
            "scenario_types": result.get("scenario_types", []),
            "processing_info": {
                "models_used": len(multi_processor.models),
                "total_sections_analyzed": len(valid_sections),
                "query_enhancement": "enabled"
            }
        }
        
    except Exception as e:
        logger.error(f"Error in find_ipc_section: {e}")
        return {"error": f"Processing failed: {str(e)}"}

# Legacy get_embeddings function for backward compatibility
def get_embeddings(texts, model, cache_file='embeddings.pkl'):
    return multi_processor.get_embeddings(texts, cache_file)

# Formatted print function
def print_results(result):
    """Enhanced results display with detailed information"""
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    
    print("\n" + "="*80)
    print(f"Scenario Analyzed: {result['scenario']}")
    print("="*80)
    
    # Display scenario types detected
    if result.get('scenario_types'):
        types_str = ', '.join([t.replace('_', ' ').title() for t in result['scenario_types']])
        print(f"Detected Crime Types: {types_str}")
    
    # Display warnings
    if result.get('warnings'):
        for warning in result['warnings']:
            print(f"Warning: {warning}")
    
    # Display suggestions
    if result.get('suggestions'):
        for suggestion in result['suggestions']:
            print(f"Suggestion: {suggestion}")
    
    print(f"\nTop {len(result['top_matches'])} Matching IPC Sections:")
    print("-" * 80)
    
    for i, match in enumerate(result['top_matches'], 1):
        score_pct = match['score'] * 100
        confidence = match.get('confidence', 'Medium')
        
        # Confidence indicator
        conf_indicator = {
            'Very High': '',
            'High': '', 
            'Medium': '',
            'Low': ''
        }.get(confidence, '')
        
        print(f"\n{i}. {conf_indicator} Section {match['section']} - {match['chapter']}")
        print(f"   Title: {match['title']}")
        
        # Truncate long descriptions
        desc = match['description']
        if len(desc) > 300:
            desc = desc[:300] + "..."
        print(f"   Description: {desc}")
        
        print(f"   Confidence: {confidence} ({score_pct:.1f}%)")
        
        # Show relevance factors if available
        if match.get('relevance_factors'):
            factors = ', '.join(match['relevance_factors'])
            print(f"   Relevance: {factors}")
    
    # Processing information
    if result.get('processing_info'):
        info = result['processing_info']
        print(f"\nProcessing Info:")
        print(f"   Models: {info.get('models_used', 'N/A')}, "
              f"Sections: {info.get('total_sections_analyzed', 'N/A')}, "
              f"Enhancement: {info.get('query_enhancement', 'N/A')}")
    
    print("\n" + "="*80)

# Interactive input with enhanced interface
if __name__ == "__main__":
    print("\nEnhanced IPC Laws Assistant")
    print("="*50)
    print("For full interactive experience, run: python interactive_assistant.py")
    print("="*50)
    
   
    while True:
        user_scenario = input("\nScenario: ").strip()
        
        if not user_scenario:
            print("\nThank you for using IPC Laws Assistant!")
            break
            
        if len(user_scenario) < 5:
            print("Please provide a more detailed scenario (at least 5 characters).")
            continue
        
        try:
            print("\nAnalyzing scenario with enhanced AI...")
            result = find_ipc_section(user_scenario)
            print_results(result)
            
            # Quick suggestions
            if result.get('top_matches') and len(result['top_matches']) > 0:
                top_score = result['top_matches'][0]['score']
                if top_score < 0.4:
                    print("\nTip: Try adding more details like location, intent, or method used.")
                elif top_score > 0.8:
                    print(f"\nHigh confidence match! Section {result['top_matches'][0]['section']} is very relevant.")
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try rephrasing your scenario.")
        
        print("\n" + "-"*50)
