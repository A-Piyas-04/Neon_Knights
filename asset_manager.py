import pygame
import os
from typing import Dict, Any

class AssetManager:
    """Manages loading and accessing of game assets"""
    
    def __init__(self):
        self.assets: Dict[str, Any] = {}
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.assets_path = os.path.join(self.base_path, "assets")
        
        # Neon color palette
        self.NEON_COLORS = {
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'purple': (128, 0, 255),
            'green': (0, 255, 0),
            'yellow': (255, 255, 0),
            'orange': (255, 128, 0),
            'pink': (255, 20, 147),
            'blue': (0, 191, 255),
            'white': (255, 255, 255),
            'black': (0, 0, 0)
        }
        
        self._load_default_assets()
    
    def _load_default_assets(self):
        """Load default fonts and create placeholder assets"""
        # Load default fonts
        try:
            self.assets['font_small'] = pygame.font.Font(None, 24)
            self.assets['font_medium'] = pygame.font.Font(None, 36)
            self.assets['font_large'] = pygame.font.Font(None, 48)
            self.assets['font_title'] = pygame.font.Font(None, 72)
        except:
            # Fallback to system font if custom fonts fail
            self.assets['font_small'] = pygame.font.SysFont('arial', 24)
            self.assets['font_medium'] = pygame.font.SysFont('arial', 36)
            self.assets['font_large'] = pygame.font.SysFont('arial', 48)
            self.assets['font_title'] = pygame.font.SysFont('arial', 72)
        
        # Create placeholder sprites
        self._create_placeholder_sprites()
    
    def _create_placeholder_sprites(self):
        """Create placeholder sprites with neon outlines"""
        # Player placeholder
        player_surface = pygame.Surface((32, 48), pygame.SRCALPHA)
        pygame.draw.rect(player_surface, self.NEON_COLORS['cyan'], (0, 0, 32, 48), 2)
        pygame.draw.circle(player_surface, self.NEON_COLORS['cyan'], (16, 12), 8, 2)
        self.assets['player_idle'] = player_surface
        
        # Enemy placeholder
        enemy_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(enemy_surface, self.NEON_COLORS['magenta'], (0, 0, 32, 32), 2)
        pygame.draw.polygon(enemy_surface, self.NEON_COLORS['magenta'], 
                          [(16, 8), (24, 24), (8, 24)], 2)
        self.assets['enemy_basic'] = enemy_surface
        
        # Projectile placeholder
        projectile_surface = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(projectile_surface, self.NEON_COLORS['yellow'], (4, 4), 4)
        pygame.draw.circle(projectile_surface, self.NEON_COLORS['white'], (4, 4), 2)
        self.assets['projectile_basic'] = projectile_surface
        
        # Power-up placeholder
        powerup_surface = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.rect(powerup_surface, self.NEON_COLORS['green'], (0, 0, 24, 24), 2)
        pygame.draw.polygon(powerup_surface, self.NEON_COLORS['green'],
                          [(12, 4), (20, 12), (12, 20), (4, 12)], 2)
        self.assets['powerup_health'] = powerup_surface
        
        # Background elements
        tile_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(tile_surface, self.NEON_COLORS['purple'], (0, 0, 32, 32), 1)
        self.assets['tile_floor'] = tile_surface
        
        wall_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.rect(wall_surface, self.NEON_COLORS['cyan'], (0, 0, 32, 32), 3)
        pygame.draw.lines(wall_surface, self.NEON_COLORS['cyan'], False, 
                         [(0, 0), (32, 32)], 1)
        pygame.draw.lines(wall_surface, self.NEON_COLORS['cyan'], False, 
                         [(32, 0), (0, 32)], 1)
        self.assets['tile_wall'] = wall_surface
    
    def load_image(self, name: str, filepath: str, scale: tuple = None) -> bool:
        """Load an image asset"""
        try:
            full_path = os.path.join(self.assets_path, filepath)
            image = pygame.image.load(full_path).convert_alpha()
            
            if scale:
                image = pygame.transform.scale(image, scale)
            
            self.assets[name] = image
            return True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Failed to load image {filepath}: {e}")
            return False
    
    def load_sound(self, name: str, filepath: str, volume: float = 1.0) -> bool:
        """Load a sound asset"""
        try:
            full_path = os.path.join(self.assets_path, filepath)
            sound = pygame.mixer.Sound(full_path)
            sound.set_volume(volume)
            self.assets[name] = sound
            return True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Failed to load sound {filepath}: {e}")
            return False
    
    def load_music(self, name: str, filepath: str) -> bool:
        """Load background music"""
        try:
            full_path = os.path.join(self.assets_path, filepath)
            self.assets[name] = full_path  # Store path for pygame.mixer.music
            return True
        except Exception as e:
            print(f"Failed to load music {filepath}: {e}")
            return False
    
    def load_font(self, name: str, filepath: str, size: int) -> bool:
        """Load a custom font"""
        try:
            full_path = os.path.join(self.assets_path, filepath)
            font = pygame.font.Font(full_path, size)
            self.assets[name] = font
            return True
        except (pygame.error, FileNotFoundError) as e:
            print(f"Failed to load font {filepath}: {e}")
            return False
    
    def get_asset(self, name: str) -> Any:
        """Get an asset by name"""
        return self.assets.get(name)
    
    def get_sprite(self, name: str) -> pygame.Surface:
        """Get a sprite asset"""
        asset = self.assets.get(name)
        if isinstance(asset, pygame.Surface):
            return asset
        return None
    
    def get_sound(self, name: str) -> pygame.mixer.Sound:
        """Get a sound asset"""
        asset = self.assets.get(name)
        if isinstance(asset, pygame.mixer.Sound):
            return asset
        return None
    
    def get_font(self, name: str) -> pygame.font.Font:
        """Get a font asset"""
        asset = self.assets.get(name)
        if isinstance(asset, pygame.font.Font):
            return asset
        return None
    
    def play_music(self, name: str, loops: int = -1, volume: float = 0.7):
        """Play background music"""
        music_path = self.assets.get(name)
        if music_path and os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(loops)
            except pygame.error as e:
                print(f"Failed to play music {name}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
    
    def get_color(self, color_name: str) -> tuple:
        """Get a neon color by name"""
        return self.NEON_COLORS.get(color_name, self.NEON_COLORS['white'])
    
    def create_text_surface(self, text: str, font_name: str, color_name: str, 
                           outline_color: str = None, outline_width: int = 1) -> pygame.Surface:
        """Create a text surface with optional neon outline effect"""
        font = self.get_font(font_name)
        if not font:
            font = self.assets['font_medium']
        
        color = self.get_color(color_name)
        text_surface = font.render(text, True, color)
        
        if outline_color:
            outline_col = self.get_color(outline_color)
            # Create outline effect
            outline_surface = pygame.Surface(
                (text_surface.get_width() + outline_width * 2,
                 text_surface.get_height() + outline_width * 2),
                pygame.SRCALPHA
            )
            
            # Draw outline in multiple directions
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        outline_text = font.render(text, True, outline_col)
                        outline_surface.blit(outline_text, 
                                           (dx + outline_width, dy + outline_width))
            
            # Draw main text on top
            outline_surface.blit(text_surface, (outline_width, outline_width))
            return outline_surface
        
        return text_surface
    
    def list_assets(self) -> list:
        """List all loaded assets"""
        return list(self.assets.keys())