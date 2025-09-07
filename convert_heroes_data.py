#!/usr/bin/env python3
"""
Script to convert metahumans.txt to heroes.json format.
Run this script to generate the JSON data file from the text file.
"""

import json
import os
from character_data import CharacterDataParser

def convert_heroes_to_json():
    """Convert metahumans.txt to heroes.json format."""
    
    # Initialize parser
    parser = CharacterDataParser()
    
    # Parse the metahumans.txt file
    metahumans_path = os.path.join("assets", "metahumans.txt")
    
    if not os.path.exists(metahumans_path):
        print(f"Error: {metahumans_path} not found!")
        return
    
    print(f"Parsing {metahumans_path}...")
    heroes = parser.parse_metahumans_file(metahumans_path)
    
    if not heroes:
        print("No heroes found in the file!")
        return
    
    # Convert to dictionary format
    heroes_data = {
        "heroes": [hero.to_dict() for hero in heroes],
        "metadata": {
            "version": "1.0",
            "total_heroes": len(heroes),
            "description": "Neon Knights Hero Data - Generated from metahumans.txt"
        }
    }
    
    # Save to JSON file
    output_path = os.path.join("assets", "heroes.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(heroes_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {len(heroes)} heroes to {output_path}")
    
    # Print summary
    print("\nHeroes converted:")
    for hero in heroes:
        print(f"  - {hero.name} ({hero.gender})")
    
    return heroes_data

if __name__ == "__main__":
    convert_heroes_to_json()