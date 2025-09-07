import pygame
import sys
from character_loader import CharacterDataLoader

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

def main():
    """Main game function with character data loader integration."""
    
    # Initialize display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neon Knights - Character System Demo")
    clock = pygame.time.Clock()
    
    # Initialize character loader
    print("Loading character data...")
    loader = CharacterDataLoader()
    
    if not loader.heroes_data:
        print("Error: No hero data loaded!")
        return
    
    print(f"Loaded {len(loader.heroes_data)} heroes")
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    heroes = pygame.sprite.Group()
    
    # Spawn some heroes for demonstration
    hero_names = ["Stormbearer", "Aetheria", "Neon Centurion", "Nightclaw"]
    spawned_heroes = []
    
    for i, name in enumerate(hero_names):
        x = 150 + (i * 200)
        y = 400
        hero = loader.spawn_hero(name, x, y)
        if hero:
            all_sprites.add(hero)
            heroes.add(hero)
            spawned_heroes.append(hero)
            print(f"Spawned {name} at ({x}, {y})")
    
    # Game state
    selected_hero_index = 0
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    print("\nGame Controls:")
    print("- Arrow Keys: Select hero")
    print("- SPACE: Attack")
    print("- S: Special attack")
    print("- ESC: Exit")
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    selected_hero_index = (selected_hero_index - 1) % len(spawned_heroes)
                elif event.key == pygame.K_RIGHT:
                    selected_hero_index = (selected_hero_index + 1) % len(spawned_heroes)
                elif event.key == pygame.K_SPACE:
                    if spawned_heroes:
                        spawned_heroes[selected_hero_index].attack("short")
                elif event.key == pygame.K_s:
                    if spawned_heroes:
                        spawned_heroes[selected_hero_index].attack("special")
        
        # Update all sprites
        all_sprites.update(dt)
        
        # Draw everything
        screen.fill((20, 20, 40))  # Dark blue background
        
        # Draw title
        title_text = font.render("Neon Knights - Character System", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        # Draw heroes
        all_sprites.draw(screen)
        
        # Draw hero names and selection indicator
        for i, hero in enumerate(spawned_heroes):
            # Hero name
            name_text = small_font.render(hero.name, True, (255, 255, 255))
            text_x = hero.rect.centerx - name_text.get_width() // 2
            screen.blit(name_text, (text_x, hero.rect.y - 30))
            
            # Selection indicator
            if i == selected_hero_index:
                pygame.draw.rect(screen, (255, 255, 0), hero.rect, 3)
                
                # Show selected hero info
                info = hero.get_info()
                info_y = 150
                info_texts = [
                    f"Selected: {info['name']} ({info['gender']})",
                    f"HP: {info['hp']}",
                    f"Energy: {info['energy']}",
                    f"Short Attack: {info['attacks']['short_attack'][:50]}...",
                    f"Special: {info['attacks']['special'][:50]}..."
                ]
                
                for j, text in enumerate(info_texts):
                    rendered_text = small_font.render(text, True, (255, 255, 255))
                    screen.blit(rendered_text, (50, info_y + j * 25))
        
        # Draw controls
        controls = [
            "Controls: ← → Select Hero | SPACE Attack | S Special | ESC Exit"
        ]
        
        for i, control in enumerate(controls):
            control_text = small_font.render(control, True, (200, 200, 200))
            screen.blit(control_text, (50, SCREEN_HEIGHT - 50 + i * 25))
        
        pygame.display.flip()
    
    pygame.quit()
    print("Game ended.")

if __name__ == "__main__":
    main()