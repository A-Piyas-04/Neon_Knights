import json
import os
from typing import Dict, List, Optional
from character_data import HeroData, HeroStats, HeroAttacks
from hero_entity import Hero

class CharacterDataLoader:
    """Loads character data from JSON files and manages hero creation."""
    
    def __init__(self, heroes_json_path: str = "assets/heroes.json"):
        self.heroes_json_path = heroes_json_path
        self.heroes_data: Dict[str, HeroData] = {}
        self.load_heroes_data()
    
    def load_heroes_data(self) -> bool:
        """Load heroes data from JSON file."""
        try:
            if not os.path.exists(self.heroes_json_path):
                print(f"Warning: Heroes data file not found at {self.heroes_json_path}")
                return False
            
            with open(self.heroes_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clear existing data
            self.heroes_data.clear()
            
            # Load each hero
            for hero_dict in data.get("heroes", []):
                hero_data = HeroData.from_dict(hero_dict)
                self.heroes_data[hero_data.name] = hero_data
            
            print(f"Loaded {len(self.heroes_data)} heroes from {self.heroes_json_path}")
            return True
            
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"Error loading heroes data: {e}")
            return False
    
    def get_hero_names(self) -> List[str]:
        """Get list of available hero names."""
        return list(self.heroes_data.keys())
    
    def get_hero_data(self, hero_name: str) -> Optional[HeroData]:
        """Get hero data by name."""
        return self.heroes_data.get(hero_name)
    
    def get_heroes_by_gender(self, gender: str) -> List[HeroData]:
        """Get all heroes of a specific gender."""
        return [hero for hero in self.heroes_data.values() if hero.gender == gender]
    
    def spawn_hero(self, hero_name: str, x: int = 0, y: int = 0) -> Optional[Hero]:
        """Spawn a hero entity from the loaded data."""
        hero_data = self.get_hero_data(hero_name)
        if hero_data:
            return Hero(hero_data, x, y)
        else:
            print(f"Hero '{hero_name}' not found in loaded data")
            return None
    
    def spawn_random_hero(self, x: int = 0, y: int = 0, gender: Optional[str] = None) -> Optional[Hero]:
        """Spawn a random hero, optionally filtered by gender."""
        import random
        
        if gender:
            available_heroes = self.get_heroes_by_gender(gender)
        else:
            available_heroes = list(self.heroes_data.values())
        
        if available_heroes:
            hero_data = random.choice(available_heroes)
            return Hero(hero_data, x, y)
        else:
            print(f"No heroes available{' for gender ' + gender if gender else ''}")
            return None
    
    def add_hero(self, hero_data: HeroData) -> bool:
        """Add a new hero to the loaded data (runtime only, doesn't save to file)."""
        self.heroes_data[hero_data.name] = hero_data
        return True
    
    def save_heroes_data(self, output_path: Optional[str] = None) -> bool:
        """Save current heroes data to JSON file."""
        if output_path is None:
            output_path = self.heroes_json_path
        
        try:
            heroes_data = {
                "heroes": [hero.to_dict() for hero in self.heroes_data.values()],
                "metadata": {
                    "version": "1.0",
                    "total_heroes": len(self.heroes_data),
                    "description": "Neon Knights Hero Data"
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(heroes_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved {len(self.heroes_data)} heroes to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving heroes data: {e}")
            return False
    
    def create_hero_from_template(self, name: str, backstory: str, 
                                attacks: Dict[str, str], stats: Dict[str, int],
                                gender: str = "male") -> HeroData:
        """Create a new hero from individual components."""
        hero_attacks = HeroAttacks(
            short_attack=attacks.get("short_attack", ""),
            long_attack=attacks.get("long_attack", ""),
            special=attacks.get("special", ""),
            super_power=attacks.get("super_power", "")
        )
        
        hero_stats = HeroStats(
            hp=stats.get("hp", 100),
            speed=stats.get("speed", 50),
            strength=stats.get("strength", 50),
            energy=stats.get("energy", 100)
        )
        
        sprite_path = f"assets/sprites/{name.lower().replace(' ', '_')}_{gender}.png"
        
        return HeroData(
            name=name,
            backstory=backstory,
            attacks=hero_attacks,
            stats=hero_stats,
            gender=gender,
            sprite_path=sprite_path
        )
    
    def get_hero_stats_summary(self) -> Dict[str, Dict]:
        """Get a summary of all heroes' stats for balancing purposes."""
        summary = {}
        
        for name, hero in self.heroes_data.items():
            summary[name] = {
                "gender": hero.gender,
                "hp": hero.stats.hp,
                "speed": hero.stats.speed,
                "strength": hero.stats.strength,
                "energy": hero.stats.energy,
                "total_stats": (hero.stats.hp + hero.stats.speed + 
                               hero.stats.strength + hero.stats.energy)
            }
        
        return summary
    
    def reload_data(self) -> bool:
        """Reload heroes data from the JSON file."""
        return self.load_heroes_data()

# Convenience function for easy hero spawning
def load_and_spawn_hero(hero_name: str, x: int = 0, y: int = 0, 
                       heroes_json_path: str = "assets/heroes.json") -> Optional[Hero]:
    """Convenience function to load data and spawn a hero in one call."""
    loader = CharacterDataLoader(heroes_json_path)
    return loader.spawn_hero(hero_name, x, y)