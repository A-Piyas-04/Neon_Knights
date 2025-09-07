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
        
        # Advanced character design features
        self.body_type = self._determine_body_type()
        self.sprite_variants = self._get_sprite_variants()
        self.animation_sets = self._initialize_animation_sets()
        
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
    
    def _determine_body_type(self):
        """Determine body type based on gender and character attributes"""
        if self.gender.lower() == 'female':
            # Female body types with distinguishable features
            strength = self.strength
            if strength > 80:
                return 'athletic_female'  # Muscular but feminine
            elif strength > 60:
                return 'fit_female'      # Toned and curvy
            else:
                return 'slender_female'  # Graceful and elegant
        else:
            # Male body types
            strength = self.strength
            if strength > 80:
                return 'muscular_male'
            elif strength > 60:
                return 'athletic_male'
            else:
                return 'lean_male'
    
    def _get_sprite_variants(self):
        """Get sprite variants for different body types and animations"""
        variants = {
            'idle': [],
            'walk': [],
            'attack': [],
            'hurt': [],
            'victory': []
        }
        
        # Generate sprite paths for each animation and direction
        for animation in variants.keys():
            for direction in ['left', 'right']:
                sprite_name = f"{self.name.lower().replace(' ', '_')}_{self.body_type}_{animation}_{direction}"
                variants[animation].append(f"assets/sprites/{sprite_name}.png")
        
        return variants
    
    def _initialize_animation_sets(self):
        """Initialize animation frame sets for different actions"""
        return {
            'idle': {'frames': 4, 'loop': True, 'speed': 200},
            'walk': {'frames': 6, 'loop': True, 'speed': 120},
            'attack': {'frames': 8, 'loop': False, 'speed': 80},
            'hurt': {'frames': 3, 'loop': False, 'speed': 100},
            'victory': {'frames': 6, 'loop': True, 'speed': 150}
        }
    
    def _create_placeholder_sprite(self) -> pygame.Surface:
        """Create a placeholder sprite with gender-specific appearance."""
        if self.gender.lower() == 'female':
            return self._create_female_sprite()
        else:
            return self._create_male_sprite()
    
    def _create_female_sprite(self):
        """Create a detailed female character sprite with distinguishable features"""
        sprite = pygame.Surface((64, 96), pygame.SRCALPHA)
        
        # Base colors based on character
        if 'storm' in self.name.lower():
            primary_color = (70, 130, 180)    # Steel blue
            secondary_color = (255, 255, 255) # White
        elif 'aetheria' in self.name.lower():
            primary_color = (138, 43, 226)    # Blue violet
            secondary_color = (255, 215, 0)   # Gold
        elif 'titaness' in self.name.lower():
            primary_color = (184, 134, 11)    # Dark goldenrod
            secondary_color = (139, 69, 19)   # Saddle brown
        elif 'crimson' in self.name.lower():
            primary_color = (220, 20, 60)     # Crimson
            secondary_color = (25, 25, 112)   # Midnight blue
        else:
            primary_color = (255, 100, 150)   # Default pink
            secondary_color = (200, 200, 200) # Light gray
        
        # Draw female body silhouette with curves
        # Head (smaller, more oval)
        pygame.draw.ellipse(sprite, (255, 220, 177), (22, 5, 20, 25))
        
        # Torso (hourglass shape)
        # Upper torso
        pygame.draw.ellipse(sprite, primary_color, (18, 25, 28, 35))
        # Waist (narrower)
        pygame.draw.ellipse(sprite, primary_color, (20, 45, 24, 20))
        # Hips (wider)
        pygame.draw.ellipse(sprite, primary_color, (16, 60, 32, 25))
        
        # Arms (slender)
        pygame.draw.ellipse(sprite, primary_color, (8, 30, 12, 30))   # Left arm
        pygame.draw.ellipse(sprite, primary_color, (44, 30, 12, 30))  # Right arm
        
        # Legs (shapely)
        pygame.draw.ellipse(sprite, primary_color, (18, 80, 12, 15))  # Left leg
        pygame.draw.ellipse(sprite, primary_color, (34, 80, 12, 15))  # Right leg
        
        # Hair (longer, flowing)
        pygame.draw.ellipse(sprite, secondary_color, (18, 2, 28, 30))
        
        # Chest area (distinguishable female feature)
        pygame.draw.circle(sprite, (255, 200, 200), (26, 35), 6)
        pygame.draw.circle(sprite, (255, 200, 200), (38, 35), 6)
        
        # Add hero name text
        font = pygame.font.Font(None, 12)
        text = font.render(self.name[:8], True, (255, 255, 255))
        sprite.blit(text, (2, 2))
        
        return sprite
    
    def _create_male_sprite(self):
        """Create a detailed male character sprite"""
        sprite = pygame.Surface((64, 96), pygame.SRCALPHA)
        
        # Base colors based on character
        if 'neon' in self.name.lower():
            primary_color = (0, 255, 255)     # Cyan
            secondary_color = (255, 20, 147)  # Deep pink
        elif 'hellrider' in self.name.lower():
            primary_color = (139, 0, 0)       # Dark red
            secondary_color = (255, 140, 0)   # Dark orange
        elif 'solaris' in self.name.lower():
            primary_color = (255, 215, 0)     # Gold
            secondary_color = (255, 69, 0)    # Red orange
        elif 'nightclaw' in self.name.lower():
            primary_color = (25, 25, 112)     # Midnight blue
            secondary_color = (128, 128, 128) # Gray
        elif 'phantom' in self.name.lower():
            primary_color = (75, 0, 130)      # Indigo
            secondary_color = (192, 192, 192) # Silver
        else:
            primary_color = (100, 150, 255)   # Default blue
            secondary_color = (200, 200, 200) # Light gray
        
        # Draw male body silhouette (broader, more angular)
        # Head (larger, more square)
        pygame.draw.rect(sprite, (255, 220, 177), (20, 5, 24, 28))
        
        # Torso (broader shoulders, straighter)
        pygame.draw.rect(sprite, primary_color, (14, 28, 36, 45))
        
        # Arms (muscular)
        pygame.draw.rect(sprite, primary_color, (6, 32, 14, 35))   # Left arm
        pygame.draw.rect(sprite, primary_color, (44, 32, 14, 35))  # Right arm
        
        # Legs (straight, powerful)
        pygame.draw.rect(sprite, primary_color, (18, 70, 14, 25))  # Left leg
        pygame.draw.rect(sprite, primary_color, (32, 70, 14, 25))  # Right leg
        
        # Hair (shorter)
        pygame.draw.rect(sprite, secondary_color, (20, 2, 24, 20))
        
        # Chest (broader, flatter)
        pygame.draw.rect(sprite, (200, 180, 160), (18, 35, 28, 20))
        
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
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0:
                self.is_attacking = False
                self.set_animation('idle')
        
        # Update animation based on current state
        self._update_animation(dt)
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def _update_animation(self, dt: float):
        """Update character animation based on current state"""
        animation_info = self.animation_sets[self.current_animation]
        
        # Update animation timer
        self.animation_timer += dt * 1000  # Convert to milliseconds
        
        # Check if it's time to advance frame
        if self.animation_timer >= animation_info['speed']:
            self.animation_frame += 1
            self.animation_timer = 0
            
            # Handle animation looping
            if self.animation_frame >= animation_info['frames']:
                if animation_info['loop']:
                    self.animation_frame = 0
                else:
                    # Non-looping animation finished
                    self.animation_frame = animation_info['frames'] - 1
                    if self.current_animation == 'attack':
                        self.set_animation('idle')
                    elif self.current_animation == 'hurt':
                        self.set_animation('idle')
            
            # Update sprite with new frame
            self.image = self._get_current_sprite()
    
    def set_animation(self, animation: str):
        """Set the current animation state."""
        if animation != self.current_animation:
            self.current_animation = animation
            self.animation_frame = 0
            self.animation_timer = 0
    
    def move(self, dx: float, dy: float):
        """Move the hero by the specified amount with walking animation."""
        if dx != 0 or dy != 0:
            # Set walking animation if moving
            if self.current_animation == 'idle':
                self.set_animation('walk')
            
            self.velocity_x = dx * self.speed
            self.velocity_y = dy * self.speed
            
            # Update facing direction
            if dx > 0:
                if not self.facing_right:
                    self.facing_right = True
                    self.image = self._get_current_sprite()
            elif dx < 0:
                if self.facing_right:
                    self.facing_right = False
                    self.image = self._get_current_sprite()
        else:
            # Stop walking animation when not moving
            if self.current_animation == 'walk':
                self.set_animation('idle')
            self.velocity_x = 0
            self.velocity_y = 0
    
    def attack(self, attack_type: str = "short") -> bool:
        """Perform an attack with enhanced animation if not on cooldown."""
        if self.is_attacking or self.attack_cooldown > 0:
            return False
        
        if self.current_energy < 10:
            return False
        
        self.is_attacking = True
        self.attack_cooldown = 1.0  # 1 second cooldown
        self.current_energy -= 10
        
        # Set appropriate animation
        if attack_type == "special":
            self.set_animation("special")
        else:
            self.set_animation("attack")
        
        # Calculate damage based on strength and body type
        base_damage = self.strength
        
        # Body type modifiers
        if 'muscular' in self.body_type or 'athletic' in self.body_type:
            base_damage *= 1.1  # 10% bonus for muscular/athletic builds
        
        print(f"{self.name} ({self.body_type}) attacks for {base_damage:.1f} damage!")
        
        return True
    
    def take_damage(self, damage: int):
        """Take damage with hurt animation and gender-specific reactions."""
        # Apply damage with body type considerations
        actual_damage = damage
        if 'athletic' in self.body_type or 'muscular' in self.body_type:
            actual_damage *= 0.9  # 10% damage reduction for fit characters
        
        self.current_hp = max(0, self.current_hp - actual_damage)
        
        if self.current_hp <= 0:
            self.set_animation("death")
            print(f"{self.name} has been defeated!")
        else:
            self.set_animation("hurt")
        
        # Gender-specific damage reactions
        if self.gender.lower() == 'female':
            print(f"{self.name} gracefully absorbs {actual_damage:.1f} damage! HP: {self.current_hp}/{self.max_hp}")
        else:
            print(f"{self.name} takes {actual_damage:.1f} damage like a champion! HP: {self.current_hp}/{self.max_hp}")
    
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