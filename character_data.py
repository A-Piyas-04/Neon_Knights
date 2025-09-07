from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import re

@dataclass
class HeroStats:
    """Represents a hero's combat statistics."""
    hp: int = 100
    speed: int = 50
    strength: int = 50
    energy: int = 100

@dataclass
class HeroAttacks:
    """Represents a hero's attack abilities."""
    short_attack: str = ""
    long_attack: str = ""
    special: str = ""
    super_power: str = ""

@dataclass
class HeroData:
    """Represents complete hero data including stats, attacks, and metadata."""
    name: str
    backstory: str
    attacks: HeroAttacks
    stats: HeroStats
    gender: str = "male"  # "male" or "female"
    sprite_path: str = ""
    
    def to_dict(self) -> Dict:
        """Convert HeroData to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "backstory": self.backstory,
            "attacks": {
                "short_attack": self.attacks.short_attack,
                "long_attack": self.attacks.long_attack,
                "special": self.attacks.special,
                "super_power": self.attacks.super_power
            },
            "stats": {
                "hp": self.stats.hp,
                "speed": self.stats.speed,
                "strength": self.stats.strength,
                "energy": self.stats.energy
            },
            "gender": self.gender,
            "sprite_path": self.sprite_path
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HeroData':
        """Create HeroData from dictionary (for JSON deserialization)."""
        attacks = HeroAttacks(
            short_attack=data["attacks"]["short_attack"],
            long_attack=data["attacks"]["long_attack"],
            special=data["attacks"]["special"],
            super_power=data["attacks"]["super_power"]
        )
        
        stats = HeroStats(
            hp=data["stats"]["hp"],
            speed=data["stats"]["speed"],
            strength=data["stats"]["strength"],
            energy=data["stats"]["energy"]
        )
        
        return cls(
            name=data["name"],
            backstory=data["backstory"],
            attacks=attacks,
            stats=stats,
            gender=data.get("gender", "male"),
            sprite_path=data.get("sprite_path", "")
        )

class CharacterDataParser:
    """Parses hero data from text files and converts to structured format."""
    
    def __init__(self):
        # Define default stats for different hero types
        self.default_stats = {
            "Stormbearer": HeroStats(hp=120, speed=45, strength=80, energy=90),
            "Neon Centurion": HeroStats(hp=100, speed=60, strength=70, energy=100),
            "Webshade": HeroStats(hp=80, speed=90, strength=50, energy=85),
            "Hellrider": HeroStats(hp=110, speed=70, strength=75, energy=95),
            "Aetheria": HeroStats(hp=95, speed=65, strength=70, energy=80),
            "Solaris": HeroStats(hp=105, speed=75, strength=85, energy=90),
            "Nightclaw": HeroStats(hp=75, speed=95, strength=55, energy=75),
            "Titaness": HeroStats(hp=140, speed=35, strength=95, energy=70),
            "Crimson Veil": HeroStats(hp=85, speed=80, strength=60, energy=85),
            "Phantom Shard": HeroStats(hp=90, speed=55, strength=65, energy=100)
        }
        
        # Define genders for heroes
        self.hero_genders = {
            "Stormbearer": "male",
            "Neon Centurion": "male",
            "Webshade": "male",
            "Hellrider": "male",
            "Aetheria": "female",
            "Solaris": "female",
            "Nightclaw": "female",
            "Titaness": "female",
            "Crimson Veil": "female",
            "Phantom Shard": "male"
        }
    
    def parse_metahumans_file(self, file_path: str) -> List[HeroData]:
        """Parse the metahumans.txt file and extract hero data."""
        heroes = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split content by hero sections (looking for emoji patterns)
        hero_sections = re.split(r'[⚡🤖🕷️🔥🛡️🌟🐾💪🩸☠️]\s*', content)
        
        for section in hero_sections[1:]:  # Skip the first empty section
            if section.strip():
                hero_data = self._parse_hero_section(section.strip())
                if hero_data:
                    heroes.append(hero_data)
        
        return heroes
    
    def _parse_hero_section(self, section: str) -> Optional[HeroData]:
        """Parse individual hero section and extract data."""
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        
        if not lines:
            return None
        
        # Extract hero name (first line, remove inspiration part)
        name_line = lines[0]
        name = re.sub(r'\s*\([^)]*\)', '', name_line).strip()
        
        # Initialize data
        backstory = ""
        attacks = HeroAttacks()
        
        # Parse each line
        for line in lines[1:]:
            if line.startswith("Backstory:"):
                backstory = line.replace("Backstory:", "").strip()
            elif line.startswith("Short Attack:"):
                attacks.short_attack = line.replace("Short Attack:", "").strip()
            elif line.startswith("Long Attack:"):
                attacks.long_attack = line.replace("Long Attack:", "").strip()
            elif line.startswith("Special:"):
                attacks.special = line.replace("Special:", "").strip()
            elif line.startswith("Super Power:"):
                attacks.super_power = line.replace("Super Power:", "").strip()
        
        # Get stats and gender
        stats = self.default_stats.get(name, HeroStats())
        gender = self.hero_genders.get(name, "male")
        
        # Set sprite path based on gender
        sprite_path = f"assets/sprites/{name.lower().replace(' ', '_')}_{gender}.png"
        
        return HeroData(
            name=name,
            backstory=backstory,
            attacks=attacks,
            stats=stats,
            gender=gender,
            sprite_path=sprite_path
        )