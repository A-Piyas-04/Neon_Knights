import pygame
import json
import os
from typing import Dict, List, Optional, Tuple
from character_data import HeroData, HeroStats, HeroAttacks

class Hero(pygame.sprite.Sprite):
    """Hero entity class for spawning and managing heroes in the game."""
    
    def __init__(self, hero_data: HeroData, x: int = 0, y: int = 0):
        super().__init__()
        
        # Store hero data
        self.hero_data = hero_data
        self.name = hero_data.name
        self.backstory = hero_data.backstory
        self.attacks = hero_data.attacks
        self.gender = hero_data.gender
        
        # Current stats (can be modified during gameplay)
        self.current_hp = hero_data.stats.hp
        self.max_hp = hero_data.stats.hp
        self.speed = hero_data.stats.speed
        self.strength = hero_data.stats.strength
        self.current_energy = hero_data.stats.energy
        self.max_energy = hero_data.stats.energy
        
        # Position and movement
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Animation and sprite handling
        self.sprite_sheets = {}
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # milliseconds per frame
        
        # Load sprites based on gender
        self._load_sprites()
        
        # Combat state
        self.is_attacking = False
        self.attack_cooldown = 0
        self.facing_right = True
        
        # Set initial sprite (after facing_right is initialized)
        self.image = self._get_current_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def _load_sprites(self):
        """Load gender-specific sprites and animations."""
        # Define sprite paths based on gender
        base_path = f"assets/sprites/{self.name.lower().replace(' ', '_')}_{self.gender}"
        
        # Animation states to load
        animations = ["idle", "walk", "attack", "special", "hurt", "death"]
        
        for animation in animations:
            sprite_path = f"{base_path}_{animation}.png"
            
            # Check if sprite file exists, otherwise use placeholder
            if os.path.exists(sprite_path):
                try:
                    sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                    self.sprite_sheets[animation] = self._load_sprite_frames(sprite_sheet)
                except pygame.error:
                    self.sprite_sheets[animation] = [self._create_placeholder_sprite()]
            else:
                # Create placeholder sprite with gender-specific color
                self.sprite_sheets[animation] = [self._create_placeholder_sprite()]
    
    def _load_sprite_frames(self, sprite_sheet: pygame.Surface) -> List[pygame.Surface]:
        """Load individual frames from a sprite sheet."""
        # For now, assume single frame sprites
        # This can be extended to handle multi-frame animations
        return [sprite_sheet]
    
    def _create_placeholder_sprite(self) -> pygame.Surface:
        """Create a placeholder sprite with gender-specific appearance."""
        # Create a simple colored rectangle as placeholder
        width, height = 64, 64
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Gender-specific colors
        if self.gender == "female":
            color = (255, 100, 150, 255)  # Pink-ish
        else:
            color = (100, 150, 255, 255)  # Blue-ish
        
        # Draw simple character representation
        pygame.draw.rect(sprite, color, (16, 8, 32, 48))  # Body
        pygame.draw.circle(sprite, (255, 220, 177), (32, 16), 8)  # Head
        
        # Add hero name text
        font = pygame.font.Font(None, 12)
        text = font.render(self.name[:8], True, (255, 255, 255))
        sprite.blit(text, (2, 2))
        
        return sprite
    
    def _get_current_sprite(self) -> pygame.Surface:
        """Get the current sprite based on animation state."""
        if self.current_animation in self.sprite_sheets:
            frames = self.sprite_sheets[self.current_animation]
            if frames:
                frame_index = self.animation_frame % len(frames)
                sprite = frames[frame_index]
                
                # Flip sprite if facing left
                if not self.facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                
                return sprite
        
        # Fallback to idle animation
        return self.sprite_sheets.get("idle", [self._create_placeholder_sprite()])[0]
    
    def update(self, dt: float):
        """Update hero state, animations, and position."""
        # Update animation
        self.animation_timer += dt * 1000  # Convert to milliseconds
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame += 1
        
        # Update sprite
        self.image = self._get_current_sprite()
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0:
                self.is_attacking = False
                self.set_animation("idle")
    
    def set_animation(self, animation: str):
        """Set the current animation state."""
        if animation != self.current_animation:
            self.current_animation = animation
            self.animation_frame = 0
            self.animation_timer = 0
    
    def move(self, dx: float, dy: float):
        """Move the hero by the specified amount."""
        self.velocity_x = dx * self.speed
        self.velocity_y = dy * self.speed
        
        # Update facing direction
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
        
        # Set walking animation if moving
        if dx != 0 or dy != 0:
            self.set_animation("walk")
        else:
            self.set_animation("idle")
    
    def attack(self, attack_type: str = "short") -> bool:
        """Perform an attack if not on cooldown."""
        if self.is_attacking or self.attack_cooldown > 0:
            return False
        
        self.is_attacking = True
        self.attack_cooldown = 1.0  # 1 second cooldown
        
        # Set appropriate animation
        if attack_type == "special":
            self.set_animation("special")
        else:
            self.set_animation("attack")
        
        return True
    
    def take_damage(self, damage: int):
        """Apply damage to the hero."""
        self.current_hp = max(0, self.current_hp - damage)
        
        if self.current_hp <= 0:
            self.set_animation("death")
        else:
            self.set_animation("hurt")
    
    def heal(self, amount: int):
        """Heal the hero."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def use_energy(self, amount: int) -> bool:
        """Use energy for special abilities."""
        if self.current_energy >= amount:
            self.current_energy -= amount
            return True
        return False
    
    def restore_energy(self, amount: int):
        """Restore energy."""
        self.current_energy = min(self.max_energy, self.current_energy + amount)
    
    def is_alive(self) -> bool:
        """Check if the hero is still alive."""
        return self.current_hp > 0
    
    def get_info(self) -> Dict:
        """Get hero information for UI display."""
        return {
            "name": self.name,
            "hp": f"{self.current_hp}/{self.max_hp}",
            "energy": f"{self.current_energy}/{self.max_energy}",
            "gender": self.gender,
            "backstory": self.backstory,
            "attacks": {
                "short_attack": self.attacks.short_attack,
                "long_attack": self.attacks.long_attack,
                "special": self.attacks.special,
                "super_power": self.attacks.super_power
            }
        }