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
    """Main game function with enhanced character design system showcase."""
    
    # Initialize display with larger resolution
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Neon Knights - Advanced Character Design Demo")
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
    
    # Spawn heroes with gender variety for demonstration
    hero_configs = [
        ("Stormbearer", 150, 350),    # Female
        ("Neon Centurion", 350, 350), # Male
        ("Aetheria", 550, 350),       # Female
        ("Hellrider", 750, 350),      # Male
        ("Titaness", 950, 350),       # Female
    ]
    spawned_heroes = []
    
    for name, x, y in hero_configs:
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
    tiny_font = pygame.font.Font(None, 16)
    show_stats = True
    animation_demo_timer = 0
    
    print("\nEnhanced Game Controls:")
    print("- Arrow Keys: Select hero")
    print("- SPACE: Attack animation")
    print("- H: Hurt animation (take damage)")
    print("- W/A/D: Walking animation")
    print("- S: Toggle stats display")
    print("- ESC: Exit")
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        animation_demo_timer += dt
        
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
                        spawned_heroes[selected_hero_index].attack()
                elif event.key == pygame.K_h:
                    if spawned_heroes:
                        spawned_heroes[selected_hero_index].take_damage(20)
                elif event.key == pygame.K_s:
                    show_stats = not show_stats
                elif event.key == pygame.K_w:
                    if spawned_heroes:
                        spawned_heroes[selected_hero_index].move(1, 0)
                elif event.key == pygame.K_a:
                    if spawned_heroes:
                        spawned_heroes[selected_hero_index].move(-1, 0)
                elif event.key == pygame.K_d:
                    if spawned_heroes:
                        spawned_heroes[selected_hero_index].move(1, 0)
        
        # Auto-demo animations every 5 seconds
        if animation_demo_timer > 5.0:
            if spawned_heroes:
                import random
                demo_hero = random.choice(spawned_heroes)
                actions = ['attack', 'walk', 'hurt']
                action = random.choice(actions)
                
                if action == 'attack':
                    demo_hero.attack()
                elif action == 'walk':
                    demo_hero.move(random.choice([-1, 1]), 0)
                elif action == 'hurt':
                    demo_hero.take_damage(10)
            
            animation_demo_timer = 0
        
        # Update all sprites
        all_sprites.update(dt)
        
        # Draw gradient background
        for y in range(800):
            color_intensity = int(20 + (y / 800) * 40)
            pygame.draw.line(screen, (color_intensity, color_intensity // 2, color_intensity), 
                           (0, y), (1200, y))
        
        # Draw title
        title_text = font.render("Neon Knights - Advanced Character Design", True, (255, 255, 255))
        screen.blit(title_text, (1200 // 2 - title_text.get_width() // 2, 30))
        
        # Draw subtitle
        subtitle_text = small_font.render("Realistic Character Bodies with Gender-Specific Features", True, (200, 200, 255))
        screen.blit(subtitle_text, (1200 // 2 - subtitle_text.get_width() // 2, 80))
        
        # Draw heroes
        all_sprites.draw(screen)
        
        # Draw hero information
        for i, hero in enumerate(spawned_heroes):
            # Hero name
            name_text = small_font.render(hero.name, True, (255, 255, 255))
            text_x = hero.rect.centerx - name_text.get_width() // 2
            screen.blit(name_text, (text_x, hero.rect.y - 35))
            
            # Gender and body type
            info_text = tiny_font.render(f"{hero.gender} - {hero.body_type}", True, (180, 180, 180))
            info_x = hero.rect.centerx - info_text.get_width() // 2
            screen.blit(info_text, (info_x, hero.rect.y - 20))
            
            # Animation state
            anim_text = tiny_font.render(f"Anim: {hero.current_animation}", True, (150, 255, 150))
            anim_x = hero.rect.centerx - anim_text.get_width() // 2
            screen.blit(anim_text, (anim_x, hero.rect.y + hero.rect.height + 5))
            
            # Selection indicator
            if i == selected_hero_index:
                pygame.draw.rect(screen, (255, 255, 0), 
                               (hero.rect.x - 8, hero.rect.y - 8, 
                                hero.rect.width + 16, hero.rect.height + 16), 4)
                
                # Selected hero stats
                if show_stats:
                    info = hero.get_info()
                    stats_y = 120
                    stats_texts = [
                        f"Selected: {info['name']}",
                        f"Gender: {info['gender']}",
                        f"Body Type: {hero.body_type}",
                        f"HP: {info['hp']}",
                        f"Energy: {info['energy']}",
                        f"Strength: {hero.strength}",
                        f"Speed: {hero.speed}",
                        f"Animation: {hero.current_animation} (Frame {hero.animation_frame})"
                    ]
                    
                    # Draw stats background
                    stats_bg = pygame.Surface((300, len(stats_texts) * 25 + 20))
                    stats_bg.set_alpha(180)
                    stats_bg.fill((0, 0, 0))
                    screen.blit(stats_bg, (50, stats_y - 10))
                    
                    for j, stat in enumerate(stats_texts):
                        color = (255, 255, 255) if j == 0 else (200, 200, 200)
                        stat_text = small_font.render(stat, True, color)
                        screen.blit(stat_text, (60, stats_y + j * 25))
        
        # Draw enhanced controls
        controls = [
            "Enhanced Controls:",
            "← → : Select Hero",
            "SPACE: Attack Animation",
            "H: Hurt Animation (Take Damage)",
            "W/A/D: Walking Animation",
            "S: Toggle Stats Display",
            "ESC: Exit",
            "",
            "Features Demonstrated:",
            "• Gender-specific body shapes",
            "• Distinguishable female features",
            "• Body type variations (athletic, fit, etc.)",
            "• Character-specific color schemes",
            "• Advanced animation system",
            "• Realistic character proportions"
        ]
        
        # Draw controls background
        controls_bg = pygame.Surface((400, len(controls) * 20 + 20))
        controls_bg.set_alpha(160)
        controls_bg.fill((0, 0, 0))
        screen.blit(controls_bg, (780, 800 - len(controls) * 20 - 40))
        
        for i, control in enumerate(controls):
            if control == "":
                continue
            color = (255, 255, 100) if control.endswith(":") else (200, 200, 200)
            if control.startswith("•"):
                color = (150, 255, 150)
            text = tiny_font.render(control, True, color)
            screen.blit(text, (790, 800 - len(controls) * 20 - 20 + i * 20))
        
        # Draw performance info
        fps_text = tiny_font.render(f"FPS: {int(clock.get_fps())}", True, (100, 255, 100))
        screen.blit(fps_text, (10, 10))
        
        pygame.display.flip()
    
    pygame.quit()
    print("Game ended.")

if __name__ == "__main__":
    main()