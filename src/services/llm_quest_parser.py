"""LLM-powered quest parser using Ollama."""

import json
import requests
from typing import Optional, Dict, Any


class LLMQuestParser:
    """Parse natural language quest descriptions using Ollama."""

    def __init__(self, ollama_host: str = "http://loki.local:11434", model: str = "qwen2.5:7b"):
        """Initialize LLM quest parser.

        Args:
            ollama_host: Ollama server URL
            model: Model to use for parsing
        """
        self.ollama_host = ollama_host
        self.model = model

    def parse_quest(self, user_input: str, user_context: str = "") -> Optional[Dict[str, Any]]:
        """Parse a natural language quest description into structured data.

        Args:
            user_input: Natural language quest description
            user_context: User context (location, memberships, etc.)

        Returns:
            Dictionary with quest parameters, or None if parsing failed
        """
        context_section = f"\n\nUser context (for reference only, don't adjust XP): {user_context}" if user_context else ""

        prompt = f"""Parse this quest description into JSON format. Extract:
- title: short quest title
- description: what to do
- category: one of "social", "constitutional", "creative", "experiential"
- xp_reward: base difficulty XP for the activity itself (easy=10, medium=20, hard=30, extreme=45)
  * Simple daily activities (walk, journal): 10 XP
  * Social meetups, short outings: 15-20 XP
  * Museum visits, attractions, events: 25-30 XP
  * Complex multi-step activities: 35-45 XP
- renewal_type: "daily", "weekly", "monthly", "seasonal", or null. Use your knowledge: museums/attractions are often repeatable monthly/seasonal, daily activities are "daily", etc.
- constraint_type: "day_of_week", "day_of_month", "time_of_day", or null
- constraint_note: constraint details (e.g., "Friday", "first_friday", "10:00-16:30")
- time_note: operating hours if relevant (e.g., "10am-4:30pm")

Use your knowledge of SF attractions to fill in operating hours and suggest reasonable renewal patterns.
Set XP based on the ACTIVITY ITSELF, not user circumstances - the system will adjust for user memberships/location later.

Examples:

Input: "First Friday Poetry at Coit Tower - go hear some spoken word in North Beach"
Output: {{"title": "First Friday Poetry at Coit Tower", "description": "go hear some spoken word in North Beach for free", "category": "experiential", "xp_reward": 20, "renewal_type": "monthly", "constraint_type": "day_of_month", "constraint_note": "first_friday", "time_note": null}}

Input: "Visit the California Academy of Sciences"
Output: {{"title": "Visit the California Academy of Sciences", "description": "Go to the California Academy of Sciences in Golden Gate Park", "category": "experiential", "xp_reward": 25, "renewal_type": "seasonal", "constraint_type": "time_of_day", "constraint_note": "10:00-17:00", "time_note": "Opens 10am, closes 5pm"}}

Input: "Daily morning walk around the block"
Output: {{"title": "Morning walk", "description": "Walk around the block", "category": "constitutional", "xp_reward": 10, "renewal_type": "daily", "constraint_type": null, "constraint_note": null, "time_note": null}}

Input: "Weekly game night on Fridays"
Output: {{"title": "Weekly game night", "description": "Play board games with friends", "category": "social", "xp_reward": 15, "renewal_type": "weekly", "constraint_type": "day_of_week", "constraint_note": "Friday", "time_note": null}}

Input: "Visit SFMOMA"
Output: {{"title": "Visit SFMOMA", "description": "Go to the SF Museum of Modern Art", "category": "experiential", "xp_reward": 25, "renewal_type": "seasonal", "constraint_type": "time_of_day", "constraint_note": "10:00-17:00", "time_note": "Open 10am-5pm, closed Wednesdays"}}

Now parse this quest:
Input: "{user_input}"
Output:"""

        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                },
                timeout=30
            )

            if response.status_code != 200:
                return None

            result = response.json()
            quest_data = json.loads(result.get("response", "{}"))

            # Validate required fields
            required = ["title", "category", "xp_reward"]
            if not all(k in quest_data for k in required):
                return None

            # Set defaults
            quest_data.setdefault("description", "")
            quest_data.setdefault("renewal_type", None)
            quest_data.setdefault("constraint_type", None)
            quest_data.setdefault("constraint_note", None)
            quest_data.setdefault("time_note", None)

            return quest_data

        except Exception:
            return None

    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
