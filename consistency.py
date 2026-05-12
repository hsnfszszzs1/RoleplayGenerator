"""
RoleplayGenerator v1.0 - Character Consistency System
"""

from typing import List, Dict

class CharacterConsistency:
    def __init__(self, character_name: str):
        self.character_name = character_name
        self.traits = []                    # List of defined personality traits
        self.violations = []                # List of detected inconsistencies
        self.score = 100                    # 0-100

    def add_trait(self, trait: str):
        self.traits.append(trait.lower())

    def check_response(self, response: str) -> float:
        """
        Simple consistency check.
        Returns new consistency score (0-100).
        """
        violations_found = 0

        # Check if response contradicts known traits
        response_lower = response.lower()
        for trait in self.traits:
            # Very basic contradiction detection
            if trait in ["shy", "timid"] and any(word in response_lower for word in ["confident", "bold", "loud"]):
                violations_found += 1
            if trait in ["dominant"] and any(word in response_lower for word in ["submissive", "shy", "hesitant"]):
                violations_found += 1

        # Update score
        penalty = violations_found * 15
        self.score = max(0, self.score - penalty)

        if violations_found > 0:
            self.violations.append(f"Possible inconsistency detected in response")

        return self.score

    def get_consistency_report(self) -> Dict:
        return {
            "character": self.character_name,
            "current_score": self.score,
            "traits_defined": len(self.traits),
            "violations_count": len(self.violations),
            "status": "Excellent" if self.score >= 90 else "Good" if self.score >= 70 else "Needs Attention"
        }