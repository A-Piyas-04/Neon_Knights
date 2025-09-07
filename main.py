import pygame
import sys
from asset_manager import AssetManager

class NeonKnights:
    def __init__(self):
        pygame.init()
        
        # Game constants
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.FPS = 60
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Neon Knights")
        
        # Game clock
        self.clock = pygame.time.Clock()
        
        # Game state
        self.running = True
        self.game_state = "splash"  # splash, menu, playing, paused
        
        # Initialize asset manager
        self.asset_manager = AssetManager()
        
        # Neon colors
        self.NEON_CYAN = (0, 255, 255)
        self.NEON_MAGENTA = (255, 0, 255)
        self.NEON_PURPLE = (128, 0, 255)
        self.BLACK = (0, 0, 0)
        
        # Splash screen timer
        self.splash_timer = 0
        self.splash_duration = 3000  # 3 seconds
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.game_state == "splash":
                    # Skip splash screen on any key press
                    self.game_state = "menu"
    
    def update(self, dt):
        """Update game logic"""
        if self.game_state == "splash":
            self.splash_timer += dt
            if self.splash_timer >= self.splash_duration:
                self.game_state = "menu"
    
    def draw_splash_screen(self):
        """Draw the splash screen"""
        self.screen.fill(self.BLACK)
        
        # Game title
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        title_text = font_large.render("NEON KNIGHTS", True, self.NEON_CYAN)
        subtitle_text = font_small.render("Press any key to continue", True, self.NEON_MAGENTA)
        
        # Center the text
        title_rect = title_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        subtitle_rect = subtitle_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 50))
        
        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Add a glowing effect (simple outline)
        outline_title = font_large.render("NEON KNIGHTS", True, self.NEON_PURPLE)
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            outline_rect = title_rect.copy()
            outline_rect.x += dx
            outline_rect.y += dy
            self.screen.blit(outline_title, outline_rect)
        
        self.screen.blit(title_text, title_rect)
    
    def draw_menu_screen(self):
        """Draw the main menu"""
        self.screen.fill(self.BLACK)
        
        font = pygame.font.Font(None, 48)
        menu_text = font.render("MAIN MENU - Coming Soon!", True, self.NEON_CYAN)
        menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        
        self.screen.blit(menu_text, menu_rect)
    
    def render(self):
        """Render the current game state"""
        if self.game_state == "splash":
            self.draw_splash_screen()
        elif self.game_state == "menu":
            self.draw_menu_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.FPS)
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = NeonKnights()
    game.run()