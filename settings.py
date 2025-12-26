"""
Game settings and constants for Chain
"""

# Display settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32
PIXEL_SCALE = 2  # For that chunky 16-bit look

# Game title
TITLE = "Chain - Quest for the Lost Princess"

# Colors - 16-bit palette inspired
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (24, 20, 37)
NAVY = (38, 43, 68)
PURPLE = (58, 68, 102)
SLATE = (90, 105, 136)
LIGHT_SLATE = (139, 155, 180)
SKY_BLUE = (87, 114, 119)
TEAL = (62, 137, 137)
CYAN = (116, 196, 182)
MINT = (177, 220, 176)

RED = (172, 50, 50)
DARK_RED = (102, 46, 46)
ORANGE = (223, 113, 38)
YELLOW = (251, 191, 69)
CREAM = (247, 228, 182)

GREEN = (75, 105, 47)
DARK_GREEN = (55, 75, 37)
LIME = (106, 190, 48)

PINK = (215, 123, 186)
MAGENTA = (143, 77, 137)

BROWN = (102, 57, 49)
DARK_BROWN = (63, 40, 50)
TAN = (143, 86, 59)
BEIGE = (217, 160, 102)

GRAY = (89, 86, 82)
LIGHT_GRAY = (155, 156, 130)

# Player settings
PLAYER_SPEED = 4
PLAYER_JUMP_SPEED = -12
PLAYER_GRAVITY = 0.5
PLAYER_MAX_HEALTH = 4
PLAYER_MAX_MAGIC = 4
PLAYER_ATTACK_COOLDOWN = 30  # frames
PLAYER_INVINCIBILITY_FRAMES = 120  # 2 seconds at 60 FPS

# Spell costs
SPELL_COSTS = {
    'shield': 1,
    'swift': 1,
    'fireball': 2,
    'thunder': 3,
    'thunder2': 2
}

# Spell durations (in frames, for buffs)
SPELL_DURATIONS = {
    'shield': 300,  # 5 seconds
    'swift': 240,   # 4 seconds
}

# Buff effects
SHIELD_DAMAGE_REDUCTION = 0.5
SWIFT_SPEED_MULTIPLIER = 1.5
SWIFT_JUMP_MULTIPLIER = 1.3

# Projectile settings
FIREBALL_SPEED = 8
FIREBALL_DAMAGE = 2
THUNDER_RADIUS = 80
THUNDER_DAMAGE = 3
THUNDER2_DAMAGE = 4

# Enemy settings
ENEMY_TYPES = {
    'slime': {
        'health': 2,
        'damage': 1,
        'speed': 1,
        'score': 10,
        'color': LIME
    },
    'bat': {
        'health': 1,
        'damage': 1,
        'speed': 2.5,
        'score': 20,
        'color': PURPLE
    },
    'knight': {
        'health': 4,
        'damage': 2,
        'speed': 1.5,
        'score': 50,
        'color': SLATE
    },
    'cannon': {
        'health': 20,
        'damage': 3,
        'speed': 2,
        'score': 500,
        'color': DARK_RED
    }
}

# Item settings
ITEM_TYPES = {
    'food': {
        'heal': 1,
        'color': ORANGE
    },
    'feast': {
        'heal': 2,
        'color': YELLOW
    },
    'magic_vial': {
        'restore': 1,
        'color': CYAN
    },
    'magic_potion': {
        'restore': 2,
        'color': TEAL
    },
    'heart_container': {
        'max_health_increase': 1,
        'color': RED
    },
    'magic_bottle': {
        'max_magic_increase': 1,
        'color': MAGENTA
    }
}

# World map settings
WORLD_MAP_WIDTH = 25
WORLD_MAP_HEIGHT = 19
WORLD_PLAYER_SPEED = 3

# Level types
LEVEL_FOREST = 'forest'
LEVEL_CAVE = 'cave'
LEVEL_CASTLE = 'castle'
LEVEL_BOSS = 'boss'

# Game states
STATE_MENU = 'menu'
STATE_WORLD_MAP = 'world_map'
STATE_LEVEL = 'level'
STATE_PAUSE = 'pause'
STATE_GAME_OVER = 'game_over'
STATE_VICTORY = 'victory'
