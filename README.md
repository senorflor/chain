# Chain - A Fully Introspectable 16-bit Adventure Game

> **Cmd+Click any element in the game to open its source code in Cursor.**

This is a pygame side-scroller where every visual element is traceable back to its implementation. The game serves as both a playable adventure and a live, explorable codebase—perfect for learning game development or debugging rendering issues.

---

## 🔍 Introspection: The Main Feature

### How It Works

Every sprite, tile, UI element, and effect drawn to the screen is tracked with its source location. When you **Cmd+Click** (macOS) on anything in the game window, Cursor opens directly to the line of code that renders it.

### Usage

| Action | Result |
|--------|--------|
| **Cmd+Click** | Opens Cursor at the source code rendering the clicked element |
| **Cmd+Shift+I** | Toggles debug overlay showing element boundaries and info |

### What's Introspectable

- **Player (Chain)** — sprite states, animations, movement
- **Enemies** — slimes, bats, knights, boss (Cannon), projectiles
- **UI Elements** — health bar, magic bar, spell selector, score, menus
- **Tiles** — grass, brick, stone, water, platforms
- **Items** — food, potions, heart containers, coins
- **Spell Effects** — shield aura, fireballs, thunder strikes
- **World Map** — terrain tiles, level markers

### Example Output

When you Cmd+click on Chain (the player), you'll see:

```
============================================================
🔍 INTROSPECTION: Clicked on 'player_chain'
============================================================

📚 Element stack at this position (3 elements):
  1. player_chain [z=45]
      metadata: {'state': 'idle', 'mode': 'level', 'health': 4}
  2. tile_grass [z=12]
  3. level_background_forest [z=0]

📍 Source stack for 'player_chain':
  → player.py:369 (Player.draw)
    game.py:383 (Game.draw_level)
    game.py:306 (Game.draw)

🚀 Opening in Cursor: cursor://file/.../player.py:369
============================================================
```

### Debug Overlay (Cmd+Shift+I)

The overlay visualizes:
- **Element boundaries** — colored rectangles around all tracked elements
- **Hover info** — element name, z-index, source file:line
- **Element stack** — all overlapping elements at cursor position

---

## 🎮 The Game: Chain's Quest

### Story
Chain is on a quest to rescue the lost princess, kidnapped by the archenemy **Cannon**. Navigate through dangerous lands, defeat enemies, and master magical spells to save her!

### Controls
| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move |
| Space | Jump (in levels) |
| Z | Attack |
| X | Cast spell |
| 1-5 | Select spell |
| Enter | Interact |
| ESC | Pause |
| I | Toggle invincibility (cheat) |
| C | Complete level (cheat) |

### Spells
1. **Shield** — Reduces incoming damage
2. **Swift** — Increases speed and jump height  
3. **Fireball** — Ranged projectile
4. **Thunder** — Area damage
5. **Thunder 2** — Powerful downward strike

### Enemies
- **Slimes** — Hop toward you
- **Bats** — Fly erratically, swoop when close
- **Knights** — Shielded, charge attacks
- **Cannon** — The boss with three phases

---

## 🛠 Installation

```bash
pip install -r requirements.txt
python main.py
```

## 📁 Project Structure

```
chain/
├── main.py           # Entry point
├── game.py           # Main loop, state management
├── player.py         # Chain (the hero)
├── enemies.py        # Slime, Bat, Knight, Cannon
├── items.py          # Collectibles
├── spells.py         # Magic system
├── level.py          # Side-scroller levels
├── world_map.py      # Overworld navigation
├── sprites.py        # Procedural pixel art
├── ui.py             # HUD and menus
├── settings.py       # Constants
├── sounds.py         # Audio (placeholder)
└── introspection.py  # ⭐ The introspection system
```

## 🎨 16-bit Aesthetic

All sprites are procedurally generated pixel art in a classic 16-bit style—no external assets required. The palette and chunky pixels evoke SNES/Genesis era games.
