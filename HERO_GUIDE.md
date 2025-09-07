# Neon Knights - Hero Addition Guide

This guide explains how to easily add new heroes to the Neon Knights game using the JSON-based character system.

## Quick Start

### Method 1: Edit JSON Directly (Recommended)

1. Open `assets/heroes.json`
2. Add your hero to the `heroes` array following the schema
3. Update the `total_heroes` count in metadata
4. Save and restart the game

### Method 2: Use Text File + Converter

1. Add hero data to `assets/metahumans.txt`
2. Run `python convert_heroes_data.py` to regenerate JSON
3. Restart the game

## Hero JSON Structure

```json
{
  "name": "Hero Name",
  "backstory": "Hero's background story (10-1000 characters)",
  "attacks": {
    "short_attack": "Quick attack description",
    "long_attack": "Ranged attack description", 
    "special": "Special ability description",
    "super_power": "Ultimate power description"
  },
  "stats": {
    "hp": 120,        // Health: 50-200
    "speed": 7,       // Speed: 1-10
    "strength": 8,    // Strength: 1-10
    "energy": 150     // Energy: 50-200
  },
  "gender": "male",  // "male" or "female"
  "sprite_path": "assets/sprites/male/hero_name.png"
}
```

## Example: Adding a New Hero

### Step 1: Create Hero Data

```json
{
  "name": "Cyber Phantom",
  "backstory": "A former hacker who merged with an AI system, gaining the ability to phase between digital and physical realms.",
  "attacks": {
    "short_attack": "Data Spike - Quick digital energy burst",
    "long_attack": "Virus Beam - Corrupting energy projectile",
    "special": "Phase Shift - Temporarily become intangible",
    "super_power": "System Override - Complete digital domination"
  },
  "stats": {
    "hp": 100,
    "speed": 9,
    "strength": 6,
    "energy": 180
  },
  "gender": "female",
  "sprite_path": "assets/sprites/female/cyber_phantom.png"
}
```

### Step 2: Add to heroes.json

1. Open `assets/heroes.json`
2. Find the `heroes` array
3. Add your hero object to the array (don't forget the comma!)
4. Update `metadata.total_heroes` count

### Step 3: Add Sprite Assets

- Place sprite files in appropriate gender folders:
  - Male: `assets/sprites/male/`
  - Female: `assets/sprites/female/`
- Supported formats: PNG, JPG, JPEG
- Recommended size: 64x64 pixels

## Stat Guidelines

### HP (Health Points)
- **Tank Heroes**: 150-200 HP
- **Balanced Heroes**: 100-149 HP  
- **Glass Cannon Heroes**: 50-99 HP

### Speed (Movement)
- **1-3**: Slow, heavy hitters
- **4-6**: Average mobility
- **7-10**: Fast, agile fighters

### Strength (Attack Power)
- **1-3**: Support/utility focused
- **4-6**: Balanced damage
- **7-10**: High damage dealers

### Energy (Special Abilities)
- **50-99**: Limited special usage
- **100-149**: Moderate special usage
- **150-200**: Frequent special abilities

## Attack Descriptions

### Short Attack
- Quick, basic melee attack
- Low energy cost
- Example: "Lightning Jab", "Plasma Punch"

### Long Attack  
- Ranged projectile attack
- Medium energy cost
- Example: "Energy Beam", "Ice Shard"

### Special
- Unique defensive or utility ability
- High energy cost
- Example: "Force Shield", "Teleport"

### Super Power
- Ultimate devastating attack
- Highest energy cost
- Example: "Nuclear Blast", "Time Stop"

## Gender-Specific Features

### Male Heroes
- Sprite folder: `assets/sprites/male/`
- Default color theme: Cyan/Blue
- Animation set: "male_animations"

### Female Heroes
- Sprite folder: `assets/sprites/female/`
- Default color theme: Magenta/Pink
- Animation set: "female_animations"

## Validation

The system includes automatic validation:

- **Name**: 1-50 characters, unique
- **Backstory**: 10-1000 characters
- **Stats**: Within specified ranges
- **Gender**: Must be "male" or "female"
- **Sprite Path**: Must exist and be valid image format

## Testing Your Hero

1. **Run Demo**: `python demo_character_system.py`
2. **Use Arrow Keys**: Navigate to your new hero
3. **Check Stats**: Verify all data displays correctly
4. **Test Sprites**: Ensure gender-specific sprites load

## Troubleshooting

### Hero Not Appearing
- Check JSON syntax (use JSON validator)
- Verify all required fields are present
- Ensure sprite file exists at specified path

### Invalid Stats
- HP: Must be 50-200
- Speed/Strength: Must be 1-10  
- Energy: Must be 50-200

### Sprite Issues
- Check file path matches exactly
- Verify image format (PNG/JPG/JPEG)
- Ensure file exists in correct gender folder

## Advanced Features

### Batch Adding Heroes

```python
# Use the character loader for bulk operations
from character_loader import CharacterDataLoader

loader = CharacterDataLoader()

# Add multiple heroes from a list
heroes_data = [
    {"name": "Hero1", ...},
    {"name": "Hero2", ...}
]

for hero_data in heroes_data:
    loader.add_hero(hero_data)

loader.save_heroes_data()
```

### Custom Sprite Variants

```json
{
  "sprite_path": "assets/sprites/male/hero_name.png",
  "sprite_variants": {
    "idle": "assets/sprites/male/hero_name_idle.png",
    "attack": "assets/sprites/male/hero_name_attack.png",
    "special": "assets/sprites/male/hero_name_special.png"
  }
}
```

## Schema Validation

Use `hero_schema.json` to validate your hero data:

```python
import json
import jsonschema

# Load schema
with open('hero_schema.json', 'r') as f:
    schema = json.load(f)

# Validate hero data
with open('assets/heroes.json', 'r') as f:
    heroes_data = json.load(f)

jsonschema.validate(heroes_data, schema)
print("Hero data is valid!")
```

## Tips for Great Heroes

1. **Unique Names**: Avoid duplicates
2. **Balanced Stats**: Don't make heroes too overpowered
3. **Compelling Backstory**: Make heroes interesting
4. **Thematic Attacks**: Match abilities to character concept
5. **Quality Sprites**: Use consistent art style
6. **Test Thoroughly**: Verify everything works in-game

---

**Happy Hero Creating!** 🦸‍♂️🦸‍♀️

For more help, check the source code in `character_loader.py` and `hero_entity.py`.