# Neon Knights

A cyberpunk-themed action game built with Python and Pygame.

## Features

- **Neon-themed graphics** with cyan, magenta, and purple color scheme
- **Modular architecture** with organized code structure
- **Asset management system** for sprites, sounds, music, and fonts
- **Splash screen** with neon glow effects
- **Extensible game framework** ready for gameplay implementation

## Project Structure

```
Neon Knights/
├── main.py              # Game entry point
├── asset_manager.py     # Asset loading and management
├── requirements.txt     # Python dependencies
├── player/              # Player logic, abilities, animations
├── enemy/               # Enemy AI and behavior
├── combat/              # Attack systems, collisions, damage
├── ui/                  # HUD, score, menus
├── levels/              # Level maps and transitions
└── assets/              # Game assets
    ├── sprites/         # Character and object sprites
    ├── sounds/          # Sound effects
    ├── music/           # Background music
    └── fonts/           # Custom fonts
```

## Installation

1. **Install Python 3.8+** if not already installed
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## Controls

- **ESC** - Exit game
- **Any key** - Skip splash screen

## Development

### Asset Manager

The `AssetManager` class provides:
- **Image loading** with optional scaling
- **Sound and music management** with volume control
- **Font loading** with multiple sizes
- **Neon color palette** for consistent theming
- **Placeholder sprites** for rapid prototyping
- **Text rendering** with glow effects

### Neon Color Palette

- **Cyan:** `#00FFFF` - Primary UI elements
- **Magenta:** `#FF00FF` - Enemy elements
- **Purple:** `#8000FF` - Secondary UI, outlines
- **Green:** `#00FF00` - Power-ups, health
- **Yellow:** `#FFFF00` - Projectiles, warnings
- **Orange:** `#FF8000` - Explosions, effects
- **Pink:** `#FF1493` - Special effects
- **Blue:** `#00BFFF` - Water, ice effects

### Game States

- **Splash** - Initial loading screen with title
- **Menu** - Main menu (placeholder)
- **Playing** - Active gameplay (to be implemented)
- **Paused** - Game pause state (to be implemented)

## Next Steps

1. **Implement player character** with movement and animations
2. **Add enemy AI** with basic behavior patterns
3. **Create combat system** with projectiles and collisions
4. **Design level layouts** with obstacles and objectives
5. **Add sound effects** and background music
6. **Implement UI elements** like health bars and score

## Technical Details

- **Resolution:** 1280x720 (16:9 aspect ratio)
- **Frame Rate:** 60 FPS
- **Engine:** Pygame 2.5+
- **Architecture:** Component-based with modular design

## Contributing

This project uses a modular structure to make adding new features straightforward:

1. **Player features** → `player/` directory
2. **Enemy types** → `enemy/` directory  
3. **Combat mechanics** → `combat/` directory
4. **UI components** → `ui/` directory
5. **Level content** → `levels/` directory

Each module should be self-contained with clear interfaces to other systems.