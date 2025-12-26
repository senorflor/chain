# Chain - A 16-bit Adventure Side-Scroller

## Story
Chain is on a quest to rescue the lost princess, kidnapped by the archenemy **Cannon**. 
Navigate through dangerous lands, defeat enemies, and master magical spells to save her!

## Gameplay

### Controls
- **Arrow Keys / WASD**: Move Chain
- **Space**: Jump (in side-scroller mode)
- **Z**: Attack
- **X**: Cast selected spell
- **1-4**: Select spell slot
- **Enter**: Interact / Confirm
- **ESC**: Pause / Back

### Points System
- **Health (❤️)**: Starts at 4 max. Depleted when hit by enemies.
- **Magic (✨)**: Starts at 4 max. Depleted when casting spells.

### Collectibles
- **Food**: Restores health points
- **Magic Vials**: Restores magic points
- **Heart Containers**: Permanently increases max health
- **Magic Bottles**: Permanently increases max magic

### Spells
1. **Shield**: Reduces incoming damage (buff)
2. **Swift**: Increases movement and jump speed (buff)
3. **Fireball**: Ranged offensive spell
4. **Thunder**: Area-of-effect damage spell

### Enemies
Various enemies with different behaviors and difficulty levels:
- **Slimes**: Easy, slow-moving
- **Bats**: Medium, flying erratic patterns
- **Knights**: Hard, shielded and aggressive
- **Cannon** (Boss): The archenemy!

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure
```
chain/
├── main.py           # Game entry point
├── settings.py       # Game constants and configuration
├── game.py           # Main game class and loop
├── player.py         # Chain player class
├── enemies.py        # Enemy classes
├── items.py          # Collectible items
├── spells.py         # Spell system
├── world_map.py      # Top-view world map
├── level.py          # Side-scroller level
├── sprites.py        # Sprite rendering utilities
├── ui.py             # User interface elements
└── assets/           # Game assets (generated procedurally)
```

## 16-bit Aesthetic
The game features procedurally generated pixel art in a classic 16-bit style,
with vibrant colors and chunky sprites reminiscent of SNES/Genesis era games.
