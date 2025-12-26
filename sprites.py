"""
Sprite rendering utilities for 16-bit pixel art style
"""

import pygame
from settings import *


def create_pixel_surface(width, height, scale=PIXEL_SCALE):
    """Create a surface for pixel art that will be scaled up"""
    return pygame.Surface((width, height), pygame.SRCALPHA)


def create_chain_up_attack_sprite(facing_right=True):
    """Create Chain's up-slash attack sprite"""
    size = 24
    surface = create_pixel_surface(size, size)
    
    offset_x = 4
    
    # Body
    body_color = TEAL
    pygame.draw.rect(surface, body_color, (offset_x + 4, 10, 8, 7))
    
    # Head (looking up slightly)
    skin_color = BEIGE
    pygame.draw.rect(surface, skin_color, (offset_x + 5, 6, 6, 5))
    
    # Hair
    hair_color = NAVY
    pygame.draw.rect(surface, hair_color, (offset_x + 5, 5, 6, 2))
    
    # Eyes (looking up)
    eye_color = DARK_BLUE
    pygame.draw.rect(surface, eye_color, (offset_x + 6, 7, 1, 1))
    pygame.draw.rect(surface, eye_color, (offset_x + 9, 7, 1, 1))
    
    # Legs
    leg_color = BROWN
    pygame.draw.rect(surface, leg_color, (offset_x + 5, 17, 2, 3))
    pygame.draw.rect(surface, leg_color, (offset_x + 9, 17, 2, 3))
    
    # Arms raised up
    pygame.draw.rect(surface, skin_color, (offset_x + 3, 8, 2, 4))
    pygame.draw.rect(surface, skin_color, (offset_x + 11, 8, 2, 4))
    
    # Sword pointing up
    sword_color = LIGHT_SLATE
    sword_handle = BROWN
    pygame.draw.rect(surface, sword_handle, (offset_x + 6, 4, 4, 3))
    pygame.draw.rect(surface, sword_color, (offset_x + 7, 0, 2, 5))
    pygame.draw.rect(surface, YELLOW, (offset_x + 5, 3, 6, 1))  # Guard
    
    # Slash effect
    pygame.draw.rect(surface, WHITE, (offset_x + 4, 0, 1, 4))
    pygame.draw.rect(surface, WHITE, (offset_x + 11, 0, 1, 4))
    
    return scale_surface(surface)


def create_chain_down_attack_sprite(facing_right=True):
    """Create Chain's downward stab attack sprite"""
    size = 24
    surface = create_pixel_surface(size, size)
    
    offset_x = 4
    
    # Body (crouched/diving position)
    body_color = TEAL
    pygame.draw.rect(surface, body_color, (offset_x + 4, 2, 8, 7))
    
    # Head (looking down)
    skin_color = BEIGE
    pygame.draw.rect(surface, skin_color, (offset_x + 5, 0, 6, 4))
    
    # Hair
    hair_color = NAVY
    pygame.draw.rect(surface, hair_color, (offset_x + 5, 0, 6, 2))
    
    # Legs tucked
    leg_color = BROWN
    pygame.draw.rect(surface, leg_color, (offset_x + 4, 9, 3, 3))
    pygame.draw.rect(surface, leg_color, (offset_x + 9, 9, 3, 3))
    
    # Arms pointing down
    pygame.draw.rect(surface, skin_color, (offset_x + 6, 8, 2, 3))
    pygame.draw.rect(surface, skin_color, (offset_x + 8, 8, 2, 3))
    
    # Sword pointing down
    sword_color = LIGHT_SLATE
    sword_handle = BROWN
    pygame.draw.rect(surface, sword_handle, (offset_x + 6, 11, 4, 2))
    pygame.draw.rect(surface, sword_color, (offset_x + 7, 13, 2, 8))
    pygame.draw.rect(surface, YELLOW, (offset_x + 5, 12, 6, 1))  # Guard
    
    # Stab effect
    pygame.draw.rect(surface, WHITE, (offset_x + 6, 18, 1, 3))
    pygame.draw.rect(surface, WHITE, (offset_x + 9, 18, 1, 3))
    pygame.draw.rect(surface, YELLOW, (offset_x + 7, 20, 2, 2))
    
    return scale_surface(surface)


def scale_surface(surface, scale=PIXEL_SCALE):
    """Scale a surface up for that chunky 16-bit look"""
    w, h = surface.get_size()
    return pygame.transform.scale(surface, (w * scale, h * scale))


def draw_pixel_rect(surface, color, rect, scale=1):
    """Draw a rectangle with pixel-perfect edges"""
    pygame.draw.rect(surface, color, rect)


def create_chain_sprite(facing_right=True, frame=0):
    """Create Chain's sprite - the hero"""
    size = 16
    surface = create_pixel_surface(size, size)
    
    # Body (tunic)
    body_color = TEAL
    pygame.draw.rect(surface, body_color, (4, 6, 8, 7))
    
    # Head
    skin_color = BEIGE
    pygame.draw.rect(surface, skin_color, (5, 2, 6, 5))
    
    # Hair (blue-ish)
    hair_color = NAVY
    pygame.draw.rect(surface, hair_color, (5, 1, 6, 2))
    pygame.draw.rect(surface, hair_color, (4, 2, 1, 2))
    if facing_right:
        pygame.draw.rect(surface, hair_color, (11, 2, 1, 3))
    else:
        pygame.draw.rect(surface, hair_color, (4, 2, 1, 3))
    
    # Eyes
    eye_color = DARK_BLUE
    if facing_right:
        pygame.draw.rect(surface, eye_color, (9, 4, 1, 1))
    else:
        pygame.draw.rect(surface, eye_color, (6, 4, 1, 1))
    
    # Legs (animated)
    leg_color = BROWN
    if frame % 2 == 0:
        pygame.draw.rect(surface, leg_color, (5, 13, 2, 3))
        pygame.draw.rect(surface, leg_color, (9, 13, 2, 3))
    else:
        pygame.draw.rect(surface, leg_color, (4, 13, 2, 3))
        pygame.draw.rect(surface, leg_color, (10, 13, 2, 3))
    
    # Boots
    boot_color = DARK_BROWN
    if frame % 2 == 0:
        pygame.draw.rect(surface, boot_color, (5, 15, 2, 1))
        pygame.draw.rect(surface, boot_color, (9, 15, 2, 1))
    else:
        pygame.draw.rect(surface, boot_color, (4, 15, 2, 1))
        pygame.draw.rect(surface, boot_color, (10, 15, 2, 1))
    
    # Belt
    belt_color = BROWN
    pygame.draw.rect(surface, belt_color, (4, 10, 8, 1))
    
    # Belt buckle (chain link symbol)
    pygame.draw.rect(surface, YELLOW, (7, 10, 2, 1))
    
    if not facing_right:
        surface = pygame.transform.flip(surface, True, False)
    
    return scale_surface(surface)


def create_chain_attack_sprite(facing_right=True):
    """Create Chain's attack sprite with sword"""
    size = 24
    surface = create_pixel_surface(size, size)
    
    # Base character (offset to make room for sword)
    offset_x = 4 if facing_right else 4
    
    # Body
    body_color = TEAL
    pygame.draw.rect(surface, body_color, (offset_x + 4, 6, 8, 7))
    
    # Head
    skin_color = BEIGE
    pygame.draw.rect(surface, skin_color, (offset_x + 5, 2, 6, 5))
    
    # Hair
    hair_color = NAVY
    pygame.draw.rect(surface, hair_color, (offset_x + 5, 1, 6, 2))
    
    # Eyes
    eye_color = DARK_BLUE
    if facing_right:
        pygame.draw.rect(surface, eye_color, (offset_x + 9, 4, 1, 1))
    else:
        pygame.draw.rect(surface, eye_color, (offset_x + 6, 4, 1, 1))
    
    # Legs
    leg_color = BROWN
    pygame.draw.rect(surface, leg_color, (offset_x + 5, 13, 2, 3))
    pygame.draw.rect(surface, leg_color, (offset_x + 9, 13, 2, 3))
    
    # Sword
    sword_color = LIGHT_SLATE
    sword_handle = BROWN
    if facing_right:
        pygame.draw.rect(surface, sword_handle, (offset_x + 12, 6, 2, 3))
        pygame.draw.rect(surface, sword_color, (offset_x + 14, 4, 6, 2))
        pygame.draw.rect(surface, YELLOW, (offset_x + 12, 5, 3, 1))  # Guard
    else:
        pygame.draw.rect(surface, sword_handle, (offset_x - 2, 6, 2, 3))
        pygame.draw.rect(surface, sword_color, (offset_x - 8, 4, 6, 2))
        pygame.draw.rect(surface, YELLOW, (offset_x - 3, 5, 3, 1))  # Guard
    
    if not facing_right:
        surface = pygame.transform.flip(surface, True, False)
    
    return scale_surface(surface)


def create_slime_sprite(frame=0):
    """Create slime enemy sprite"""
    size = 12
    surface = create_pixel_surface(size, size)
    
    color = LIME
    dark = DARK_GREEN
    
    # Body (bouncy animation)
    if frame % 20 < 10:
        pygame.draw.rect(surface, dark, (1, 6, 10, 6))
        pygame.draw.rect(surface, color, (2, 4, 8, 6))
        pygame.draw.rect(surface, color, (3, 3, 6, 2))
    else:
        pygame.draw.rect(surface, dark, (0, 8, 12, 4))
        pygame.draw.rect(surface, color, (1, 6, 10, 4))
        pygame.draw.rect(surface, color, (2, 5, 8, 2))
    
    # Eyes
    pygame.draw.rect(surface, WHITE, (3, 5, 2, 2))
    pygame.draw.rect(surface, WHITE, (7, 5, 2, 2))
    pygame.draw.rect(surface, BLACK, (4, 6, 1, 1))
    pygame.draw.rect(surface, BLACK, (8, 6, 1, 1))
    
    return scale_surface(surface)


def create_bat_sprite(frame=0):
    """Create bat enemy sprite"""
    size = 14
    surface = create_pixel_surface(size, size)
    
    color = PURPLE
    dark = DARK_BLUE
    
    # Body
    pygame.draw.rect(surface, color, (5, 5, 4, 5))
    pygame.draw.rect(surface, dark, (6, 4, 2, 2))
    
    # Wings (animated)
    if frame % 10 < 5:
        # Wings up
        pygame.draw.rect(surface, color, (0, 3, 5, 3))
        pygame.draw.rect(surface, color, (9, 3, 5, 3))
        pygame.draw.rect(surface, color, (1, 2, 3, 2))
        pygame.draw.rect(surface, color, (10, 2, 3, 2))
    else:
        # Wings down
        pygame.draw.rect(surface, color, (0, 6, 5, 3))
        pygame.draw.rect(surface, color, (9, 6, 5, 3))
        pygame.draw.rect(surface, color, (1, 8, 3, 2))
        pygame.draw.rect(surface, color, (10, 8, 3, 2))
    
    # Eyes (red, menacing)
    pygame.draw.rect(surface, RED, (5, 5, 1, 1))
    pygame.draw.rect(surface, RED, (8, 5, 1, 1))
    
    # Ears
    pygame.draw.rect(surface, color, (5, 3, 1, 2))
    pygame.draw.rect(surface, color, (8, 3, 1, 2))
    
    return scale_surface(surface)


def create_knight_sprite(facing_right=True, frame=0):
    """Create knight enemy sprite - armored and tough"""
    size = 16
    surface = create_pixel_surface(size, size)
    
    armor_color = SLATE
    armor_dark = GRAY
    visor_color = DARK_BLUE
    
    # Body (armor)
    pygame.draw.rect(surface, armor_dark, (4, 6, 8, 7))
    pygame.draw.rect(surface, armor_color, (5, 5, 6, 6))
    
    # Helmet
    pygame.draw.rect(surface, armor_dark, (4, 1, 8, 5))
    pygame.draw.rect(surface, armor_color, (5, 2, 6, 3))
    
    # Visor
    pygame.draw.rect(surface, visor_color, (6, 3, 4, 2))
    pygame.draw.rect(surface, RED, (7, 3, 1, 1))  # Glowing eye
    pygame.draw.rect(surface, RED, (9, 3, 1, 1))  # Glowing eye
    
    # Shield
    if facing_right:
        pygame.draw.rect(surface, armor_dark, (2, 6, 3, 5))
        pygame.draw.rect(surface, armor_color, (2, 7, 2, 3))
    else:
        pygame.draw.rect(surface, armor_dark, (11, 6, 3, 5))
        pygame.draw.rect(surface, armor_color, (12, 7, 2, 3))
    
    # Sword
    sword_color = LIGHT_SLATE
    if facing_right:
        pygame.draw.rect(surface, sword_color, (12, 4, 2, 6))
        pygame.draw.rect(surface, sword_color, (13, 2, 1, 3))
    else:
        pygame.draw.rect(surface, sword_color, (2, 4, 2, 6))
        pygame.draw.rect(surface, sword_color, (2, 2, 1, 3))
    
    # Legs (armored)
    if frame % 2 == 0:
        pygame.draw.rect(surface, armor_dark, (5, 13, 2, 3))
        pygame.draw.rect(surface, armor_dark, (9, 13, 2, 3))
    else:
        pygame.draw.rect(surface, armor_dark, (4, 13, 2, 3))
        pygame.draw.rect(surface, armor_dark, (10, 13, 2, 3))
    
    if not facing_right:
        surface = pygame.transform.flip(surface, True, False)
    
    return scale_surface(surface)


def create_cannon_sprite(frame=0):
    """Create Cannon (boss) sprite - the archenemy"""
    size = 24
    surface = create_pixel_surface(size, size)
    
    # Cape
    cape_color = DARK_RED
    pygame.draw.rect(surface, cape_color, (2, 6, 20, 14))
    pygame.draw.rect(surface, RED, (4, 8, 16, 10))
    
    # Body (dark armor)
    armor_color = DARK_BLUE
    armor_accent = NAVY
    pygame.draw.rect(surface, armor_color, (7, 6, 10, 10))
    pygame.draw.rect(surface, armor_accent, (8, 7, 8, 8))
    
    # Head (helmet with crown)
    pygame.draw.rect(surface, armor_color, (8, 1, 8, 6))
    pygame.draw.rect(surface, DARK_RED, (9, 3, 6, 3))  # Visor
    
    # Crown spikes
    pygame.draw.rect(surface, YELLOW, (8, 0, 2, 2))
    pygame.draw.rect(surface, YELLOW, (11, 0, 2, 1))
    pygame.draw.rect(surface, YELLOW, (14, 0, 2, 2))
    
    # Evil eyes
    pygame.draw.rect(surface, YELLOW, (10, 3, 1, 1))
    pygame.draw.rect(surface, YELLOW, (13, 3, 1, 1))
    
    # Cannon arm (signature weapon)
    cannon_color = GRAY
    if frame % 30 < 15:
        pygame.draw.rect(surface, cannon_color, (17, 8, 6, 4))
        pygame.draw.rect(surface, DARK_BROWN, (16, 9, 2, 2))
        pygame.draw.rect(surface, ORANGE, (22, 9, 2, 2))  # Charging
    else:
        pygame.draw.rect(surface, cannon_color, (17, 8, 6, 4))
        pygame.draw.rect(surface, DARK_BROWN, (16, 9, 2, 2))
    
    # Legs
    pygame.draw.rect(surface, armor_color, (8, 16, 3, 6))
    pygame.draw.rect(surface, armor_color, (13, 16, 3, 6))
    pygame.draw.rect(surface, DARK_BROWN, (8, 21, 3, 2))
    pygame.draw.rect(surface, DARK_BROWN, (13, 21, 3, 2))
    
    return scale_surface(surface)


def create_heart_sprite(full=True, is_container=False):
    """Create heart sprite for health display"""
    size = 10
    surface = create_pixel_surface(size, size)
    
    if is_container:
        color = YELLOW
        outline = ORANGE
    elif full:
        color = RED
        outline = DARK_RED
    else:
        color = GRAY
        outline = DARK_BROWN
    
    # Heart shape
    pygame.draw.rect(surface, outline, (1, 2, 3, 3))
    pygame.draw.rect(surface, outline, (6, 2, 3, 3))
    pygame.draw.rect(surface, outline, (0, 3, 2, 3))
    pygame.draw.rect(surface, outline, (8, 3, 2, 3))
    pygame.draw.rect(surface, outline, (2, 5, 6, 3))
    pygame.draw.rect(surface, outline, (3, 8, 4, 1))
    pygame.draw.rect(surface, outline, (4, 9, 2, 1))
    
    # Fill
    pygame.draw.rect(surface, color, (2, 3, 2, 2))
    pygame.draw.rect(surface, color, (6, 3, 2, 2))
    pygame.draw.rect(surface, color, (1, 4, 2, 2))
    pygame.draw.rect(surface, color, (7, 4, 2, 2))
    pygame.draw.rect(surface, color, (3, 5, 4, 2))
    pygame.draw.rect(surface, color, (4, 7, 2, 1))
    
    # Highlight
    if full or is_container:
        pygame.draw.rect(surface, WHITE, (2, 3, 1, 1))
    
    return scale_surface(surface)


def create_magic_sprite(full=True, is_bottle=False):
    """Create magic point sprite (star/crystal)"""
    size = 10
    surface = create_pixel_surface(size, size)
    
    if is_bottle:
        color = MAGENTA
        outline = PURPLE
    elif full:
        color = CYAN
        outline = TEAL
    else:
        color = GRAY
        outline = DARK_BROWN
    
    # Crystal/star shape
    pygame.draw.rect(surface, outline, (4, 0, 2, 2))
    pygame.draw.rect(surface, outline, (3, 2, 4, 2))
    pygame.draw.rect(surface, outline, (0, 3, 10, 2))
    pygame.draw.rect(surface, outline, (2, 5, 6, 2))
    pygame.draw.rect(surface, outline, (3, 7, 4, 2))
    pygame.draw.rect(surface, outline, (4, 9, 2, 1))
    
    # Fill
    pygame.draw.rect(surface, color, (4, 1, 2, 1))
    pygame.draw.rect(surface, color, (3, 3, 4, 1))
    pygame.draw.rect(surface, color, (1, 4, 8, 1))
    pygame.draw.rect(surface, color, (3, 5, 4, 1))
    pygame.draw.rect(surface, color, (4, 6, 2, 2))
    
    # Highlight
    if full or is_bottle:
        pygame.draw.rect(surface, WHITE, (4, 3, 1, 1))
    
    return scale_surface(surface)


def create_food_sprite(food_type='food'):
    """Create food item sprite"""
    size = 10
    surface = create_pixel_surface(size, size)
    
    if food_type == 'feast':
        # Roasted chicken leg
        pygame.draw.rect(surface, TAN, (2, 2, 6, 5))
        pygame.draw.rect(surface, BEIGE, (3, 3, 4, 3))
        pygame.draw.rect(surface, BROWN, (1, 6, 2, 3))  # Bone
        pygame.draw.rect(surface, CREAM, (1, 8, 2, 1))
    else:
        # Apple
        pygame.draw.rect(surface, RED, (2, 3, 6, 5))
        pygame.draw.rect(surface, RED, (3, 2, 4, 1))
        pygame.draw.rect(surface, DARK_RED, (2, 6, 6, 2))
        pygame.draw.rect(surface, BROWN, (4, 0, 2, 3))  # Stem
        pygame.draw.rect(surface, GREEN, (5, 1, 2, 2))  # Leaf
        pygame.draw.rect(surface, WHITE, (3, 3, 1, 1))  # Highlight
    
    return scale_surface(surface)


def create_magic_vial_sprite(vial_type='magic_vial'):
    """Create magic vial sprite"""
    size = 10
    surface = create_pixel_surface(size, size)
    
    if vial_type == 'magic_potion':
        color = TEAL
        liquid = CYAN
    else:
        color = PURPLE
        liquid = MAGENTA
    
    # Bottle
    pygame.draw.rect(surface, LIGHT_GRAY, (3, 0, 4, 2))  # Cork
    pygame.draw.rect(surface, LIGHT_SLATE, (2, 2, 6, 2))  # Neck
    pygame.draw.rect(surface, LIGHT_SLATE, (1, 4, 8, 5))  # Body outline
    
    # Liquid
    pygame.draw.rect(surface, color, (2, 5, 6, 3))
    pygame.draw.rect(surface, liquid, (3, 6, 4, 2))
    
    # Highlight
    pygame.draw.rect(surface, WHITE, (2, 4, 1, 2))
    
    # Sparkle
    pygame.draw.rect(surface, WHITE, (5, 5, 1, 1))
    
    return scale_surface(surface)


def create_fireball_sprite(frame=0):
    """Create fireball projectile sprite"""
    size = 10
    surface = create_pixel_surface(size, size)
    
    # Core
    pygame.draw.rect(surface, YELLOW, (3, 3, 4, 4))
    pygame.draw.rect(surface, WHITE, (4, 4, 2, 2))
    
    # Flames (animated)
    if frame % 4 < 2:
        pygame.draw.rect(surface, ORANGE, (2, 2, 2, 2))
        pygame.draw.rect(surface, ORANGE, (6, 2, 2, 2))
        pygame.draw.rect(surface, ORANGE, (2, 6, 2, 2))
        pygame.draw.rect(surface, ORANGE, (6, 6, 2, 2))
        pygame.draw.rect(surface, RED, (1, 4, 2, 2))
    else:
        pygame.draw.rect(surface, ORANGE, (1, 3, 2, 2))
        pygame.draw.rect(surface, ORANGE, (7, 3, 2, 2))
        pygame.draw.rect(surface, ORANGE, (1, 5, 2, 2))
        pygame.draw.rect(surface, ORANGE, (7, 5, 2, 2))
        pygame.draw.rect(surface, RED, (0, 4, 2, 2))
    
    return scale_surface(surface)


def create_thunder_sprite(frame=0):
    """Create thunder effect sprite"""
    size = 16
    surface = create_pixel_surface(size, size)
    
    # Lightning bolt shape
    color = YELLOW if frame % 4 < 2 else WHITE
    
    pygame.draw.rect(surface, color, (8, 0, 3, 4))
    pygame.draw.rect(surface, color, (6, 3, 4, 3))
    pygame.draw.rect(surface, color, (4, 5, 6, 3))
    pygame.draw.rect(surface, color, (6, 7, 4, 3))
    pygame.draw.rect(surface, color, (8, 9, 3, 4))
    pygame.draw.rect(surface, color, (10, 12, 2, 4))
    
    return scale_surface(surface)


def create_shield_effect_sprite(frame=0):
    """Create shield buff visual effect"""
    size = 20
    surface = create_pixel_surface(size, size)
    
    # Shimmering shield
    alpha = 128 + int(64 * ((frame % 30) / 30))
    color = (*CYAN[:3], alpha)
    
    # Circular shield
    for i in range(8):
        angle_offset = (frame * 3 + i * 45) % 360
        x = int(10 + 7 * (1 if i % 2 == 0 else -1) * ((frame + i * 5) % 10) / 10)
        y = int(10 + 7 * (1 if i < 4 else -1) * ((frame + i * 5) % 10) / 10)
        pygame.draw.rect(surface, CYAN, (x, y, 2, 2))
    
    # Border
    pygame.draw.rect(surface, TEAL, (0, 8, 2, 4))
    pygame.draw.rect(surface, TEAL, (18, 8, 2, 4))
    pygame.draw.rect(surface, TEAL, (8, 0, 4, 2))
    pygame.draw.rect(surface, TEAL, (8, 18, 4, 2))
    
    return scale_surface(surface)


def create_tile_sprite(tile_type, variant=0):
    """Create tile sprites for levels"""
    size = 16
    surface = create_pixel_surface(size, size)
    
    if tile_type == 'grass':
        pygame.draw.rect(surface, GREEN, (0, 0, 16, 16))
        pygame.draw.rect(surface, LIME, (0, 0, 16, 4))
        # Grass detail
        for i in range(4):
            x = (i * 4 + variant) % 16
            pygame.draw.rect(surface, DARK_GREEN, (x, 4, 1, 2))
    
    elif tile_type == 'dirt':
        pygame.draw.rect(surface, BROWN, (0, 0, 16, 16))
        pygame.draw.rect(surface, TAN, (2, 2, 3, 2))
        pygame.draw.rect(surface, TAN, (10, 8, 4, 3))
        pygame.draw.rect(surface, DARK_BROWN, (6, 12, 2, 2))
    
    elif tile_type == 'stone':
        pygame.draw.rect(surface, GRAY, (0, 0, 16, 16))
        pygame.draw.rect(surface, LIGHT_GRAY, (1, 1, 6, 5))
        pygame.draw.rect(surface, LIGHT_GRAY, (9, 8, 5, 6))
        pygame.draw.rect(surface, DARK_BROWN, (0, 7, 16, 1))
        pygame.draw.rect(surface, DARK_BROWN, (7, 0, 1, 16))
    
    elif tile_type == 'brick':
        pygame.draw.rect(surface, DARK_RED, (0, 0, 16, 16))
        # Brick pattern
        pygame.draw.rect(surface, RED, (1, 1, 6, 6))
        pygame.draw.rect(surface, RED, (9, 1, 6, 6))
        pygame.draw.rect(surface, RED, (1, 9, 14, 6))
        pygame.draw.rect(surface, BROWN, (0, 7, 16, 2))
        pygame.draw.rect(surface, BROWN, (7, 0, 2, 8))
    
    elif tile_type == 'wood':
        pygame.draw.rect(surface, BROWN, (0, 0, 16, 16))
        # Wood grain
        for i in range(4):
            y = i * 4 + 1
            pygame.draw.rect(surface, TAN, (0, y, 16, 2))
        pygame.draw.rect(surface, DARK_BROWN, (4, 0, 1, 16))
        pygame.draw.rect(surface, DARK_BROWN, (11, 0, 1, 16))
    
    elif tile_type == 'water':
        base = TEAL if variant % 2 == 0 else SKY_BLUE
        pygame.draw.rect(surface, base, (0, 0, 16, 16))
        # Waves
        wave_color = CYAN
        for i in range(3):
            x = (i * 6 + variant * 2) % 16
            pygame.draw.rect(surface, wave_color, (x, 4, 4, 1))
            pygame.draw.rect(surface, wave_color, ((x + 3) % 16, 10, 4, 1))
    
    elif tile_type == 'lava':
        pygame.draw.rect(surface, DARK_RED, (0, 0, 16, 16))
        pygame.draw.rect(surface, RED, (2, 2, 5, 4))
        pygame.draw.rect(surface, RED, (9, 7, 5, 5))
        pygame.draw.rect(surface, ORANGE, (3, 3, 2, 2))
        pygame.draw.rect(surface, ORANGE, (10, 9, 3, 2))
        pygame.draw.rect(surface, YELLOW, (4, 3, 1, 1))
    
    elif tile_type == 'sky':
        pygame.draw.rect(surface, SKY_BLUE, (0, 0, 16, 16))
        if variant % 3 == 0:
            # Cloud
            pygame.draw.rect(surface, WHITE, (2, 4, 8, 4))
            pygame.draw.rect(surface, WHITE, (4, 2, 4, 2))
    
    return scale_surface(surface)


def create_world_map_tile(tile_type):
    """Create tiles for the world map"""
    size = 16
    surface = create_pixel_surface(size, size)
    
    if tile_type == 'grass':
        pygame.draw.rect(surface, GREEN, (0, 0, 16, 16))
        pygame.draw.rect(surface, LIME, (3, 3, 2, 2))
        pygame.draw.rect(surface, LIME, (10, 8, 2, 2))
        pygame.draw.rect(surface, DARK_GREEN, (7, 12, 2, 2))
    
    elif tile_type == 'forest':
        pygame.draw.rect(surface, DARK_GREEN, (0, 0, 16, 16))
        # Trees
        pygame.draw.rect(surface, GREEN, (2, 4, 4, 6))
        pygame.draw.rect(surface, GREEN, (10, 2, 4, 8))
        pygame.draw.rect(surface, BROWN, (3, 10, 2, 4))
        pygame.draw.rect(surface, BROWN, (11, 10, 2, 4))
    
    elif tile_type == 'mountain':
        pygame.draw.rect(surface, GRAY, (0, 0, 16, 16))
        # Mountain peak
        pygame.draw.rect(surface, SLATE, (6, 0, 4, 6))
        pygame.draw.rect(surface, SLATE, (4, 6, 8, 4))
        pygame.draw.rect(surface, SLATE, (2, 10, 12, 6))
        pygame.draw.rect(surface, WHITE, (7, 1, 2, 3))  # Snow cap
    
    elif tile_type == 'water':
        pygame.draw.rect(surface, NAVY, (0, 0, 16, 16))
        pygame.draw.rect(surface, TEAL, (2, 4, 6, 2))
        pygame.draw.rect(surface, TEAL, (8, 10, 6, 2))
    
    elif tile_type == 'path':
        # Full path tile that connects in all directions
        pygame.draw.rect(surface, TAN, (0, 0, 16, 16))
        # Add some texture/detail
        pygame.draw.rect(surface, BEIGE, (2, 2, 4, 4))
        pygame.draw.rect(surface, BEIGE, (10, 10, 4, 4))
        pygame.draw.rect(surface, BROWN, (7, 6, 2, 2))
        pygame.draw.rect(surface, BROWN, (1, 12, 2, 2))
        pygame.draw.rect(surface, BROWN, (12, 2, 2, 2))
    
    elif tile_type == 'castle':
        pygame.draw.rect(surface, GRAY, (0, 0, 16, 16))
        # Castle structure
        pygame.draw.rect(surface, SLATE, (2, 4, 12, 12))
        pygame.draw.rect(surface, SLATE, (0, 2, 4, 4))
        pygame.draw.rect(surface, SLATE, (12, 2, 4, 4))
        pygame.draw.rect(surface, DARK_BLUE, (6, 10, 4, 6))  # Door
        pygame.draw.rect(surface, RED, (2, 0, 2, 3))  # Flag
    
    elif tile_type == 'cave':
        pygame.draw.rect(surface, DARK_BROWN, (0, 0, 16, 16))
        pygame.draw.rect(surface, BLACK, (4, 6, 8, 10))
        pygame.draw.rect(surface, DARK_BROWN, (2, 4, 12, 4))
    
    elif tile_type == 'fortress':
        # Cannon's Domain entrance - dark fortress
        pygame.draw.rect(surface, DARK_BLUE, (0, 0, 16, 16))
        # Fortress walls
        pygame.draw.rect(surface, NAVY, (1, 2, 14, 14))
        pygame.draw.rect(surface, DARK_BROWN, (3, 4, 10, 10))
        # Gate
        pygame.draw.rect(surface, BLACK, (5, 8, 6, 8))
        # Spikes on top
        pygame.draw.rect(surface, GRAY, (2, 1, 2, 4))
        pygame.draw.rect(surface, GRAY, (7, 1, 2, 4))
        pygame.draw.rect(surface, GRAY, (12, 1, 2, 4))
        # Red glow
        pygame.draw.rect(surface, RED, (6, 9, 4, 2))
    
    elif tile_type == 'boss':
        pygame.draw.rect(surface, DARK_RED, (0, 0, 16, 16))
        # Evil castle
        pygame.draw.rect(surface, DARK_BLUE, (2, 4, 12, 12))
        pygame.draw.rect(surface, DARK_BLUE, (0, 2, 4, 4))
        pygame.draw.rect(surface, DARK_BLUE, (12, 2, 4, 4))
        pygame.draw.rect(surface, BLACK, (6, 10, 4, 6))
        pygame.draw.rect(surface, YELLOW, (4, 6, 2, 2))  # Evil eye
        pygame.draw.rect(surface, YELLOW, (10, 6, 2, 2))  # Evil eye
    
    elif tile_type == 'level_marker':
        pygame.draw.rect(surface, YELLOW, (4, 4, 8, 8))
        pygame.draw.rect(surface, ORANGE, (6, 6, 4, 4))
    
    return scale_surface(surface)


def create_chain_world_sprite(facing='down', frame=0):
    """Create Chain sprite for world map (top-down view)"""
    size = 12
    surface = create_pixel_surface(size, size)
    
    # Body
    pygame.draw.rect(surface, TEAL, (3, 3, 6, 6))
    
    # Head direction
    skin = BEIGE
    hair = NAVY
    
    if facing == 'down':
        pygame.draw.rect(surface, hair, (4, 2, 4, 2))
        pygame.draw.rect(surface, skin, (4, 4, 4, 3))
        pygame.draw.rect(surface, DARK_BLUE, (5, 5, 1, 1))
        pygame.draw.rect(surface, DARK_BLUE, (7, 5, 1, 1))
    elif facing == 'up':
        pygame.draw.rect(surface, hair, (4, 2, 4, 4))
        pygame.draw.rect(surface, skin, (5, 5, 2, 2))
    elif facing == 'left':
        pygame.draw.rect(surface, hair, (3, 2, 4, 3))
        pygame.draw.rect(surface, skin, (3, 4, 3, 3))
        pygame.draw.rect(surface, DARK_BLUE, (3, 5, 1, 1))
    elif facing == 'right':
        pygame.draw.rect(surface, hair, (5, 2, 4, 3))
        pygame.draw.rect(surface, skin, (6, 4, 3, 3))
        pygame.draw.rect(surface, DARK_BLUE, (8, 5, 1, 1))
    
    # Feet (animated)
    if frame % 20 < 10:
        pygame.draw.rect(surface, BROWN, (3, 9, 2, 2))
        pygame.draw.rect(surface, BROWN, (7, 9, 2, 2))
    else:
        pygame.draw.rect(surface, BROWN, (4, 9, 2, 2))
        pygame.draw.rect(surface, BROWN, (6, 9, 2, 2))
    
    return scale_surface(surface)
