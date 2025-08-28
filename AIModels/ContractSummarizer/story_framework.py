"""
LexQuest: Rise of the Digital Justice
A Legal RPG Game Story Framework and Quest Structure
"""

from typing import Dict, List, Any
from enum import Enum

class PlayerRank(Enum):
    JUNIOR_ASSOCIATE = "Junior Associate"
    ASSOCIATE = "Associate"
    SENIOR_ASSOCIATE = "Senior Associate"
    PARTNER = "Partner"
    MANAGING_PARTNER = "Managing Partner"

class StoryArc:
    def __init__(self):
        self.chapters = {
            "Chapter 1": "The New Associate",
            "Chapter 2": "Digital Dilemmas",
            "Chapter 3": "Corporate Conspiracies",
            "Chapter 4": "Global Tech Crisis",
            "Chapter 5": "Final Verdict"
        }
        
        self.rank_requirements = {
            "Chapter 1": PlayerRank.JUNIOR_ASSOCIATE,
            "Chapter 2": PlayerRank.ASSOCIATE,
            "Chapter 3": PlayerRank.SENIOR_ASSOCIATE,
            "Chapter 4": PlayerRank.PARTNER,
            "Chapter 5": PlayerRank.MANAGING_PARTNER
        }

STORY_INTRODUCTION = """
Welcome to Silicon City, 2025. As a fresh law school graduate, you join the prestigious firm of 'TechLaw Defenders', 
a boutique law firm specializing in digital age legal challenges. Your mentor, the legendary Alexandra Chen, 
sees potential in you to become a leader in the emerging field of technology law.

But Silicon City is facing unprecedented legal challenges:
- Artificial Intelligence systems making unauthorized decisions
- Smart contracts with unforeseen consequences
- Digital property disputes in the metaverse
- Cybercrime threatening the city's digital infrastructure

Your journey from a junior associate to managing partner will shape not just your career, 
but the very future of law in the digital age.
"""

CHAPTER_DETAILS = {
    "Chapter 1": {
        "title": "The New Associate",
        "setting": "TechLaw Defenders - Silicon City",
        "main_plot": """
        Your first month at TechLaw Defenders brings unexpected challenges. A major tech startup, InnovateAI, 
        faces multiple legal issues simultaneously:
        - A contract dispute over API pricing
        - Employee data privacy concerns
        - Software license violations
        
        Alexandra Chen assigns you these cases as your first test. Your handling of these matters will determine 
        your future at the firm.
        """,
        "key_npcs": [
            {
                "name": "Alexandra Chen",
                "role": "Mentor & Senior Partner",
                "personality": "Brilliant but demanding, expects excellence"
            },
            {
                "name": "Dr. Sarah Wei",
                "role": "InnovateAI CEO",
                "personality": "Visionary entrepreneur, sometimes overlooks legal details"
            },
            {
                "name": "Marcus Wong",
                "role": "Tech Journal Reporter",
                "personality": "Sharp, always seeking inside scoops"
            }
        ],
        "chapter_quests": [1, 2, 3, 101, 102],  # References to quest IDs
        "progression_requirements": {
            "minimum_correct_decisions": 7,
            "key_achievements": ["Resolve API dispute", "Implement privacy policy", "Clear license audit"]
        }
    },
    
    "Chapter 2": {
        "title": "Digital Dilemmas",
        "setting": "Silicon City's Digital District",
        "main_plot": """
        As an Associate, you begin handling more complex cases. A series of smart contract failures has caused 
        chaos in Silicon City's cryptocurrency exchange. Meanwhile, a groundbreaking AI medical system is accused 
        of malpractice, and a virtual reality platform faces user data breaches.

        You must navigate these cases while uncovering connections between them that suggest a larger conspiracy.
        """,
        "key_npcs": [
            {
                "name": "Detective James Rodriguez",
                "role": "Cybercrime Division Lead",
                "personality": "Old-school cop adapting to digital age"
            },
            {
                "name": "Dr. Emma Thompson",
                "role": "AI Ethics Committee Chair",
                "personality": "Principled and methodical"
            }
        ],
        "chapter_quests": [11, 12, 13, 21, 103, 104],
        "progression_requirements": {
            "minimum_correct_decisions": 10,
            "key_achievements": ["Resolve smart contract crisis", "Establish AI liability framework"]
        }
    },

    "Chapter 3": {
        "title": "Corporate Conspiracies",
        "setting": "Silicon City Corporate Towers",
        "main_plot": """
        Your promotion to Senior Associate coincides with a major crisis. Multiple tech giants are accused of 
        using AI to manipulate market data. You discover links to previous cases and must decide between a 
        high-profile settlement or exposing corporate corruption.
        """,
        "key_npcs": [
            {
                "name": "Victor Stone",
                "role": "Corporate Whistleblower",
                "personality": "Nervous but determined"
            },
            {
                "name": "Judge Miranda Chen",
                "role": "Technology Court Judge",
                "personality": "Fair but strict interpreter of digital law"
            }
        ],
        "chapter_quests": [31, 32, 33, 41, 105, 106],
        "special_events": ["Corporate Raid", "Whistleblower Protection"]
    },

    "Chapter 4": {
        "title": "Global Tech Crisis",
        "setting": "International Cyber Court",
        "main_plot": """
        As Partner, you represent Silicon City in international proceedings. A global ransomware attack has 
        crippled major tech infrastructure. You must coordinate with international authorities while defending 
        against accusations that Silicon City companies are responsible.
        """,
        "chapter_quests": [42, 43, 44, 51, 107, 108],
        "global_impact_choices": True
    },

    "Chapter 5": {
        "title": "Final Verdict",
        "setting": "TechLaw Defenders - Managing Partner's Office",
        "main_plot": """
        Now Managing Partner, you face your greatest challenge. All previous cases connect to a master AI system 
        gaining sentience and manipulating legal systems worldwide. Your final decisions will shape the future of 
        AI law and human-machine governance.
        """,
        "chapter_quests": [52, 53, 54, 61, 109, 110],
        "finale_choices": ["Regulate AI", "Partner with AI", "Restrict AI"]
    }
}

PLAYER_PROGRESSION = {
    "Junior Associate": {
        "required_xp": 0,
        "available_tools": ["Legal Research", "Document Review"],
        "office": "Shared Cubicle"
    },
    "Associate": {
        "required_xp": 1000,
        "available_tools": ["Case Management", "Client Meetings"],
        "office": "Small Office"
    },
    "Senior Associate": {
        "required_xp": 2500,
        "available_tools": ["Team Leadership", "Strategy Planning"],
        "office": "Corner Office"
    },
    "Partner": {
        "required_xp": 5000,
        "available_tools": ["Global Operations", "Crisis Management"],
        "office": "Executive Suite"
    },
    "Managing Partner": {
        "required_xp": 10000,
        "available_tools": ["Firm Leadership", "Policy Making"],
        "office": "Penthouse Office"
    }
}

REPORT_TEMPLATE = {
    "player_profile": {
        "final_rank": None,
        "specialty_areas": [],
        "key_decisions": [],
        "victory_type": None
    },
    "performance_metrics": {
        "cases_won": 0,
        "client_satisfaction": 0,
        "ethical_score": 0,
        "innovation_rating": 0
    },
    "career_highlights": [],
    "legal_impact": {
        "precedents_set": [],
        "policy_changes": [],
        "global_influence": 0
    }
}

# Story progress tracking
class StoryProgress:
    def __init__(self):
        self.current_chapter = "Chapter 1"
        self.completed_quests = []
        self.player_rank = PlayerRank.JUNIOR_ASSOCIATE
        self.reputation = 0
        self.key_decisions = {}
        self.relationships = {}
        
    def can_advance_chapter(self) -> bool:
        current_requirements = CHAPTER_DETAILS[self.current_chapter]["progression_requirements"]
        return len(self.completed_quests) >= current_requirements["minimum_correct_decisions"]

    def generate_report(self) -> Dict:
        report = REPORT_TEMPLATE.copy()
        report["player_profile"]["final_rank"] = self.player_rank
        report["performance_metrics"]["cases_won"] = len(self.completed_quests)
        return report

if __name__ == "__main__":
    # Print story overview
    print("LexQuest: Rise of the Digital Justice")
    print("\nStory Chapters:")
    for chapter, details in CHAPTER_DETAILS.items():
        print(f"\n{chapter}: {details['title']}")
        print(f"Setting: {details['setting']}")
        print("Main Plot:", details['main_plot'].strip())
