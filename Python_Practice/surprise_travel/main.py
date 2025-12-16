"""
Main module for the surprise_travel package.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional

class SurpriseTravel:
    """Main class for surprise travel planning."""
    
    def __init__(self):
        self.preferences: Dict = {}
        self.destinations: List[Dict] = []
        self.load_destinations()
    
    def load_destinations(self) -> None:
        """Load destinations from a JSON file."""
        try:
            data_path = Path(__file__).parent / 'data' / 'destinations.json'
            with open(data_path, 'r', encoding='utf-8') as f:
                self.destinations = json.load(f)
        except FileNotFoundError:
            self.destinations = []
    
    def set_preferences(self, **preferences) -> None:
        """Set travel preferences."""
        self.preferences.update(preferences)
    
    def get_suggestions(self) -> List[Dict]:
        """Get travel suggestions based on preferences."""
        if not self.destinations:
            return [{"error": "No destinations available. Please train the model first."}]
        
        # Simple matching based on preferences
        suggestions = []
        for dest in self.destinations:
            match_score = 0
            for key, value in self.preferences.items():
                if key in dest and dest[key] == value:
                    match_score += 1
            
            if match_score > 0:
                suggestions.append({
                    **dest,
                    'match_score': match_score
                })
        
        return sorted(suggestions, key=lambda x: x.get('match_score', 0), reverse=True)

def run():
    """Run the surprise travel CLI."""
    print("🌍 Welcome to Surprise Travel! 🚀")
    print("Let's find your perfect surprise destination!\n")
    
    travel_planner = SurpriseTravel()
    
    # Example preferences
    print("Setting up some example preferences...")
    travel_planner.set_preferences(
        climate="warm",
        budget="medium",
        activity_type="adventure"
    )
    
    print("\nHere are some travel suggestions for you:")
    suggestions = travel_planner.get_suggestions()
    
    for i, suggestion in enumerate(suggestions[:3], 1):
        print(f"\n{i}. {suggestion.get('name', 'Unknown Destination')}")
        print(f"   🌡️  Climate: {suggestion.get('climate', 'N/A')}")
        print(f"   💰 Budget: {suggestion.get('budget', 'N/A')}")
        print(f"   🎯 Activities: {', '.join(suggestion.get('activities', []))}")

def train():
    """Train the surprise travel model with sample data."""
    print("🚂 Training the surprise travel model...")
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Sample destinations data
    destinations = [
        {
            "name": "Bali, Indonesia",
            "climate": "tropical",
            "budget": "medium",
            "activities": ["beach", "surfing", "yoga", "culture"],
            "description": "A tropical paradise with beautiful beaches and rich culture."
        },
        {
            "name": "Swiss Alps, Switzerland",
            "climate": "cold",
            "budget": "high",
            "activities": ["skiing", "hiking", "sightseeing"],
            "description": "Breathtaking mountain views and world-class ski resorts."
        },
        {
            "name": "Cape Town, South Africa",
            "climate": "warm",
            "budget": "medium",
            "activities": ["safari", "hiking", "wine tasting"],
            "description": "Stunning landscapes, wildlife, and world-famous vineyards."
        }
    ]
    
    # Save destinations to file
    with open(data_dir / 'destinations.json', 'w', encoding='utf-8') as f:
        json.dump(destinations, f, indent=2)
    
    print(f"✅ Trained with {len(destinations)} destinations!")

if __name__ == "__main__":
    run()
