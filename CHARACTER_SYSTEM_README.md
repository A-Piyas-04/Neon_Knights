# Neon Knights Character Data Loader System

A comprehensive character data management system for the Neon Knights game that supports loading hero data from JSON files, spawning heroes with gender-specific sprites, and easy addition of new characters.

## Features

- **JSON-based Data Storage**: Easy-to-edit JSON format for hero data
- **Gender-specific Sprites**: Automatic sprite path generation for male/female characters
- **Comprehensive Stats System**: HP, Speed, Strength, and Energy attributes
- **Attack System**: Short attack, long attack, special, and super power abilities
- **Pygame Integration**: Ready-to-use Hero entities with sprite support
- **Easy Extensibility**: Simple API for adding new heroes

## Files Overview

- `character_data.py` - Core data classes (HeroData, HeroStats, HeroAttacks)
- `character_loader.py` - Main loader class for JSON data management
- `hero_entity.py` - Pygame-compatible Hero entity class
- `convert_heroes_data.py` - Utility to convert text data to JSON
- `demo_character_system.py` - Complete demonstration script
- `assets/heroes.json` - JSON data file containing all hero information

## Quick Start

### 1. Load and Spawn a Hero

```python
from character_loader import CharacterDataLoader

# Initialize the loader
loader = CharacterDataLoader()

# Spawn a hero at position (100, 200)
hero = loader.spawn_hero("Stormbearer", x=100, y=200)

# Use in pygame
all_sprites = pygame.sprite.Group()
all_sprites.add(hero)
```

### 2. Get Hero Information

```python
# Get available heroes
hero_names = loader.get_hero_names()
print(f"Available heroes: {hero_names}")

# Get heroes by gender
female_heroes = loader.get_heroes_by_gender("female")
male_heroes = loader.get_heroes_by_gender("male")

# Get detailed hero data
hero_data = loader.get_hero_data("Aetheria")
print(f"Backstory: {hero_data.backstory}")
print(f"HP: {hero_data.stats.hp}")
```

### 3. Add New Heroes

#### Method 1: Edit JSON directly

Edit `assets/heroes.json` and add a new hero entry:

```json
{
  "name": "New Hero",
  "backstory": "Hero description here",
  "attacks": {
    "short_attack": "Basic attack description",
    "long_attack": "Ranged attack description", 
    "special": "Special ability description",
    "super_power": "Ultimate ability description"
  },
  "stats": {
    "hp": 100,
    "speed": 60,
    "strength": 70,
    "energy": 90
  },
  "gender": "female",
  "sprite_path": "assets/sprites/new_hero_female.png"
}
```

#### Method 2: Programmatically

```python
# Create new hero
new_hero = loader.create_hero_from_template(
    name="Cyber Ninja",
    backstory="A stealthy warrior enhanced with cybernetic implants.",
    attacks={
        "short_attack": "Katana slashes and throwing stars.",
        "long_attack": "Cyber shuriken barrage.",
        "special": "Shadow clone technique.",
        "super_power": "Digital phantom mode - becomes untouchable."
    },
    stats={"hp": 85, "speed": 95, "strength": 65, "energy": 90},
    gender="male"
)

# Add to loader
loader.add_hero(new_hero)

# Save to file
loader.save_heroes_data()
```

## Hero Data Structure

### HeroData Class
- `name`: Hero's display name
- `backstory`: Character background story
- `attacks`: HeroAttacks object with 4 attack types
- `stats`: HeroStats object with combat statistics
- `gender`: "male" or "female" for sprite selection
- `sprite_path`: Path to character sprite file

### HeroStats Class
- `hp`: Health Points (default: 100)
- `speed`: Movement and attack speed (default: 50)
- `strength`: Physical damage modifier (default: 50)
- `energy`: Special ability resource (default: 100)

### HeroAttacks Class
- `short_attack`: Close-range combat ability
- `long_attack`: Ranged combat ability
- `special`: Special technique or ability
- `super_power`: Ultimate/finishing move

## Sprite System

The system automatically generates sprite paths based on hero name and gender:

```
assets/sprites/{hero_name}_{gender}_{animation}.png
```

Example paths:
- `assets/sprites/stormbearer_male_idle.png`
- `assets/sprites/aetheria_female_attack.png`
- `assets/sprites/nightclaw_female_walk.png`

Supported animations: `idle`, `walk`, `attack`, `special`, `hurt`, `death`

## Current Heroes

### Male Heroes (5)
1. **Stormbearer** - Thor-inspired hammer wielder
2. **Neon Centurion** - Iron Man-inspired tech hero
3. **Webshade** - Spider-Man-inspired agile fighter
4. **Hellrider** - Ghost Rider-inspired flame warrior
5. **Phantom Shard** - Ermac-inspired soul manipulator

### Female Heroes (5)
1. **Aetheria** - Wonder Woman-inspired warrior princess
2. **Solaris** - Power Girl-inspired solar-powered hero
3. **Nightclaw** - Catwoman-inspired agile thief
4. **Titaness** - She-Hulk-inspired powerhouse
5. **Crimson Veil** - Skarlet-inspired blood manipulator

## Running the Demo

```bash
python demo_character_system.py
```

This will demonstrate:
- Loading hero data from JSON
- Displaying hero information and stats
- Adding new heroes programmatically
- Pygame integration with sprite rendering

## Integration with Main Game

To integrate with your main game loop:

```python
import pygame
from character_loader import CharacterDataLoader

# Initialize
loader = CharacterDataLoader()
all_sprites = pygame.sprite.Group()

# Spawn heroes
player_hero = loader.spawn_hero("Stormbearer", x=100, y=300)
enemy_hero = loader.spawn_hero("Crimson Veil", x=500, y=300)

all_sprites.add(player_hero, enemy_hero)

# Game loop
while running:
    dt = clock.tick(60) / 1000.0
    
    # Update
    all_sprites.update(dt)
    
    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
```

## Tips for Adding New Heroes

1. **Balanced Stats**: Keep total stats around 300-350 for balance
2. **Unique Abilities**: Make each hero's attacks distinctive
3. **Gender Distribution**: Maintain roughly equal male/female ratio
4. **Sprite Consistency**: Use consistent sprite dimensions (64x64 recommended)
5. **Compelling Backstories**: Create engaging character narratives

## File Locations

- Hero data: `assets/heroes.json`
- Sprites: `assets/sprites/`
- Original text data: `assets/metahumans.txt`

The system is designed to be easily extensible - just edit the JSON file or use the programmatic API to add new heroes!