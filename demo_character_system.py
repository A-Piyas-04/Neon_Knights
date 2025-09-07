#!/usr/bin/env python3
"""
Demonstration script for the Neon Knights Character Data Loader System.
This script shows how to:
1. Load hero data from JSON
2. Spawn heroes with gender-specific sprites
3. Display hero information
4. Add new heroes programmatically
"""

import pygame
import sys
from character_loader import CharacterDataLoader, load_and_spawn_hero
from character_data import HeroData

def demo_character_system():
    """Demonstrate the character data loader system."""
    
    print("=== Neon Knights Character Data Loader Demo ===")
    print()
    
    # Initialize the character loader
    print("1. Loading character data...")
    loader = CharacterDataLoader()
    
    if not loader.heroes_data:
        print("No heroes loaded! Make sure heroes.json exists.")
        return
    
    # Display available heroes
    print(f"\n2. Available Heroes ({len(loader.heroes_data)}):")
    for i, name in enumerate(loader.get_hero_names(), 1):
        hero_data = loader.get_hero_data(name)
        print(f"   {i}. {name} ({hero_data.gender})")
    
    # Show heroes by gender
    print("\n3. Heroes by Gender:")
    male_heroes = loader.get_heroes_by_gender("male")
    female_heroes = loader.get_heroes_by_gender("female")
    
    print(f"   Male Heroes ({len(male_heroes)}): {[h.name for h in male_heroes]}")
    print(f"   Female Heroes ({len(female_heroes)}): {[h.name for h in female_heroes]}")
    
    # Display detailed hero information
    print("\n4. Detailed Hero Information:")
    for hero_name in ["Stormbearer", "Aetheria", "Neon Centurion"]:
        hero_data = loader.get_hero_data(hero_name)
        if hero_data:
            print(f"\n   --- {hero_name} ({hero_data.gender}) ---")
            print(f"   Backstory: {hero_data.backstory}")
            print(f"   Stats: HP={hero_data.stats.hp}, Speed={hero_data.stats.speed}, "
                  f"Strength={hero_data.stats.strength}, Energy={hero_data.stats.energy}")
            print(f"   Short Attack: {hero_data.attacks.short_attack}")
            print(f"   Special: {hero_data.attacks.special}")
            print(f"   Sprite Path: {hero_data.sprite_path}")
    
    # Show stats summary
    print("\n5. Hero Stats Summary:")
    stats_summary = loader.get_hero_stats_summary()
    print(f"   {'Name':<15} {'Gender':<8} {'HP':<4} {'Speed':<6} {'Str':<4} {'Energy':<7} {'Total':<6}")
    print("   " + "-" * 60)
    
    for name, stats in stats_summary.items():
        print(f"   {name:<15} {stats['gender']:<8} {stats['hp']:<4} "
              f"{stats['speed']:<6} {stats['strength']:<4} {stats['energy']:<7} {stats['total_stats']:<6}")
    
    # Demonstrate adding a new hero
    print("\n6. Adding a New Hero:")
    new_hero_data = loader.create_hero_from_template(
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
    
    loader.add_hero(new_hero_data)
    print(f"   Added new hero: {new_hero_data.name}")
    print(f"   Total heroes now: {len(loader.heroes_data)}")
    
    return loader

def demo_pygame_integration():
    """Demonstrate pygame integration with hero spawning."""
    
    print("\n=== Pygame Integration Demo ===")
    
    # Initialize pygame (minimal setup for demo)
    pygame.init()
    
    try:
        # Create a small display for demo
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Neon Knights - Hero Demo")
        clock = pygame.time.Clock()
        
        # Load and spawn heroes
        print("\n7. Spawning Heroes in Pygame:")
        
        # Spawn different heroes
        heroes = []
        hero_names = ["Stormbearer", "Aetheria", "Webshade"]
        
        for i, name in enumerate(hero_names):
            hero = load_and_spawn_hero(name, x=50 + i * 100, y=150)
            if hero:
                heroes.append(hero)
                print(f"   Spawned {name} at position ({hero.x}, {hero.y})")
                print(f"     - Gender: {hero.gender}")
                print(f"     - HP: {hero.current_hp}/{hero.max_hp}")
                print(f"     - Sprite size: {hero.image.get_size()}")
        
        # Simple demo loop
        print("\n   Running pygame demo (press ESC to exit)...")
        running = True
        dt = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        # Make heroes attack
                        for hero in heroes:
                            hero.attack()
            
            # Update heroes
            for hero in heroes:
                hero.update(dt)
            
            # Draw everything
            screen.fill((20, 20, 40))  # Dark background
            
            for hero in heroes:
                screen.blit(hero.image, hero.rect)
                
                # Draw hero name
                font = pygame.font.Font(None, 24)
                text = font.render(hero.name, True, (255, 255, 255))
                screen.blit(text, (hero.rect.x, hero.rect.y - 25))
            
            # Draw instructions
            font = pygame.font.Font(None, 36)
            text = font.render("Press SPACE to attack, ESC to exit", True, (255, 255, 255))
            screen.blit(text, (10, 10))
            
            pygame.display.flip()
            dt = clock.tick(60) / 1000.0  # 60 FPS, dt in seconds
        
        print("   Demo completed!")
        
    except Exception as e:
        print(f"   Pygame demo error: {e}")
        print("   (This is normal if pygame is not properly installed)")
    
    finally:
        pygame.quit()

def main():
    """Main demo function."""
    try:
        # Run character system demo
        loader = demo_character_system()
        
        # Ask user if they want to run pygame demo
        print("\n" + "="*50)
        response = input("Run pygame integration demo? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            demo_pygame_integration()
        
        print("\n=== Demo Complete ===")
        print("\nTo add new heroes:")
        print("1. Edit assets/heroes.json directly, or")
        print("2. Use CharacterDataLoader.create_hero_from_template() and save_heroes_data()")
        print("\nTo use in your game:")
        print("1. from character_loader import CharacterDataLoader")
        print("2. loader = CharacterDataLoader()")
        print("3. hero = loader.spawn_hero('Hero Name', x, y)")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()