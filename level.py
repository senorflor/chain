"""
Side-scroller level system for Chain
"""

import pygame
import random
from settings import *
from sprites import create_tile_sprite
from enemies import create_enemy
from items import create_item, ItemManager
from introspection import introspect


class Tile(pygame.sprite.Sprite):
    """A platform/ground tile"""
    
    # Actual tile size in pixels (16 base * 2 scale)
    SIZE = 16 * PIXEL_SCALE
    
    def __init__(self, x, y, tile_type='grass', variant=0):
        super().__init__()
        self.tile_type = tile_type
        self.image = create_tile_sprite(tile_type, variant)
        self.rect = self.image.get_rect(topleft=(x, y))


class Level:
    """A side-scrolling level"""
    
    def __init__(self, level_id, level_type=LEVEL_FOREST):
        self.level_id = level_id
        self.level_type = level_type
        
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.item_manager = ItemManager()
        
        # Level dimensions
        self.width = 0
        self.height = 0
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Level state
        self.completed = False
        self.exit_rect = None
        
        # Player start position
        self.start_x = 100
        self.start_y = 400
        
        # Level name
        self.name = self.get_level_name()
        
        # Generate level
        self.generate()
    
    def get_level_name(self):
        """Get display name for level"""
        names = {
            'castle': 'Castle Entrance',
            'cave': 'Dark Cave',
            'fortress': "Cannon's Domain",
            'boss': "Cannon's Throne"
        }
        return names.get(self.level_id, 'Unknown Area')
    
    def generate(self):
        """Generate level based on type"""
        if self.level_id == 'castle':
            self.generate_castle_level()
        elif self.level_id == 'cave':
            self.generate_cave_level()
        elif self.level_id == 'fortress':
            self.generate_fortress_level()
        elif self.level_id == 'boss':
            self.generate_boss_level()
        else:
            self.generate_forest_level()
    
    def generate_forest_level(self):
        """Generate a forest-themed level"""
        ts = Tile.SIZE  # Actual tile size (32 pixels)
        
        # Level size
        self.width = 3000
        self.height = 600
        
        # Ground
        ground_y = self.height - ts * 2
        for x in range(0, self.width, ts):
            self.tiles.add(Tile(x, ground_y, 'grass', x // ts))
            self.tiles.add(Tile(x, ground_y + ts, 'dirt', x // ts))
        
        # Platforms
        platforms = [
            (200, ground_y - ts * 3, 3),
            (500, ground_y - ts * 2, 4),
            (800, ground_y - ts * 4, 2),
            (1000, ground_y - ts * 3, 5),
            (1400, ground_y - ts * 2, 3),
            (1700, ground_y - ts * 4, 4),
            (2000, ground_y - ts * 3, 3),
            (2300, ground_y - ts * 2, 5),
        ]
        
        for px, py, length in platforms:
            for i in range(length):
                self.tiles.add(Tile(px + i * ts, py, 'grass'))
        
        # Enemies
        self.enemies.add(create_enemy('slime', 400, ground_y - ts))
        self.enemies.add(create_enemy('slime', 900, ground_y - ts))
        self.enemies.add(create_enemy('bat', 600, ground_y - ts * 4))
        self.enemies.add(create_enemy('slime', 1200, ground_y - ts))
        self.enemies.add(create_enemy('bat', 1500, ground_y - ts * 3))
        self.enemies.add(create_enemy('knight', 2000, ground_y - ts))
        
        # Items
        self.item_manager.spawn_food(550, ground_y - ts * 3)
        self.item_manager.spawn_magic_vial(850, ground_y - ts * 5)
        self.item_manager.spawn_coin(1050, ground_y - ts * 4)
        self.item_manager.spawn_coin(1100, ground_y - ts * 4)
        self.item_manager.spawn_food(1750, ground_y - ts * 5, feast=True)
        self.item_manager.spawn_heart_container(2350, ground_y - ts * 3)
        
        # Exit
        self.exit_rect = pygame.Rect(self.width - 100, ground_y - ts * 2, 
                                     ts, ts * 2)
        
        self.start_y = ground_y - ts
    
    def generate_castle_level(self):
        """Generate castle-themed level"""
        ts = Tile.SIZE  # Actual tile size (32 pixels)
        
        self.width = 2500
        self.height = 600
        
        # Ground
        ground_y = self.height - ts * 2
        for x in range(0, self.width, ts):
            self.tiles.add(Tile(x, ground_y, 'brick', x // ts))
            self.tiles.add(Tile(x, ground_y + ts, 'stone', x // ts))
        
        # Castle platforms and structure
        platforms = [
            (150, ground_y - ts * 2, 4, 'brick'),
            (450, ground_y - ts * 4, 3, 'brick'),
            (700, ground_y - ts * 3, 5, 'brick'),
            (1000, ground_y - ts * 5, 3, 'stone'),
            (1250, ground_y - ts * 3, 4, 'brick'),
            (1550, ground_y - ts * 4, 3, 'brick'),
            (1800, ground_y - ts * 2, 6, 'brick'),
        ]
        
        for px, py, length, tile_type in platforms:
            for i in range(length):
                self.tiles.add(Tile(px + i * ts, py, tile_type))
        
        # Enemies - more knights in castle
        self.enemies.add(create_enemy('knight', 300, ground_y - ts))
        self.enemies.add(create_enemy('bat', 550, ground_y - ts * 5))
        self.enemies.add(create_enemy('knight', 800, ground_y - ts))
        self.enemies.add(create_enemy('bat', 1100, ground_y - ts * 6))
        self.enemies.add(create_enemy('knight', 1350, ground_y - ts))
        self.enemies.add(create_enemy('knight', 1900, ground_y - ts))
        
        # Items
        self.item_manager.spawn_food(200, ground_y - ts * 3)
        self.item_manager.spawn_magic_vial(500, ground_y - ts * 5)
        self.item_manager.spawn_magic_vial(750, ground_y - ts * 4, potion=True)
        self.item_manager.spawn_coin(1050, ground_y - ts * 6)
        self.item_manager.spawn_food(1600, ground_y - ts * 5, feast=True)
        self.item_manager.spawn_magic_bottle(2000, ground_y - ts * 3)
        
        # Exit
        self.exit_rect = pygame.Rect(self.width - 100, ground_y - ts * 2,
                                     ts, ts * 2)
        
        self.start_y = ground_y - ts
    
    def generate_cave_level(self):
        """Generate cave-themed level"""
        ts = Tile.SIZE  # Actual tile size (32 pixels)
        
        self.width = 2800
        self.height = 700
        
        # Cave floor and ceiling
        ground_y = self.height - ts * 2
        
        for x in range(0, self.width, ts):
            # Floor
            self.tiles.add(Tile(x, ground_y, 'stone', x // ts))
            self.tiles.add(Tile(x, ground_y + ts, 'stone', x // ts))
            # Ceiling
            self.tiles.add(Tile(x, 0, 'stone', x // ts))
            self.tiles.add(Tile(x, ts, 'stone', x // ts))
        
        # Cave platforms (more varied heights)
        platforms = [
            (200, ground_y - ts * 2, 3, 'stone'),
            (400, ground_y - ts * 4, 2, 'stone'),
            (550, ground_y - ts * 3, 4, 'stone'),
            (800, ground_y - ts * 5, 2, 'stone'),
            (950, ground_y - ts * 2, 3, 'stone'),
            (1150, ground_y - ts * 4, 3, 'stone'),
            (1400, ground_y - ts * 3, 2, 'stone'),
            (1550, ground_y - ts * 5, 4, 'stone'),
            (1850, ground_y - ts * 2, 3, 'stone'),
            (2050, ground_y - ts * 4, 2, 'stone'),
            (2250, ground_y - ts * 3, 5, 'stone'),
        ]
        
        for px, py, length, tile_type in platforms:
            for i in range(length):
                self.tiles.add(Tile(px + i * ts, py, tile_type))
        
        # Lots of bats in cave
        self.enemies.add(create_enemy('bat', 300, ground_y - ts * 4))
        self.enemies.add(create_enemy('slime', 500, ground_y - ts))
        self.enemies.add(create_enemy('bat', 700, ground_y - ts * 5))
        self.enemies.add(create_enemy('bat', 900, ground_y - ts * 3))
        self.enemies.add(create_enemy('slime', 1100, ground_y - ts))
        self.enemies.add(create_enemy('bat', 1300, ground_y - ts * 4))
        self.enemies.add(create_enemy('knight', 1600, ground_y - ts))
        self.enemies.add(create_enemy('bat', 1800, ground_y - ts * 5))
        self.enemies.add(create_enemy('bat', 2000, ground_y - ts * 3))
        self.enemies.add(create_enemy('knight', 2300, ground_y - ts))
        
        # Items - magic vials common in cave (magical place)
        self.item_manager.spawn_magic_vial(250, ground_y - ts * 3)
        self.item_manager.spawn_magic_vial(600, ground_y - ts * 4)
        self.item_manager.spawn_food(850, ground_y - ts * 6)
        self.item_manager.spawn_magic_vial(1000, ground_y - ts * 3, potion=True)
        self.item_manager.spawn_food(1200, ground_y - ts * 5)
        self.item_manager.spawn_magic_vial(1450, ground_y - ts * 4)
        self.item_manager.spawn_magic_bottle(1650, ground_y - ts * 6)
        self.item_manager.spawn_food(1900, ground_y - ts * 3, feast=True)
        self.item_manager.spawn_heart_container(2100, ground_y - ts * 5)
        
        # Exit
        self.exit_rect = pygame.Rect(self.width - 100, ground_y - ts * 2,
                                     ts, ts * 2)
        
        self.start_y = ground_y - ts
    
    def generate_fortress_level(self):
        """Generate Cannon's Domain - a difficult dungeon"""
        ts = Tile.SIZE  # Actual tile size (32 pixels)
        
        # Longer, more challenging level
        self.width = 4000
        self.height = 700
        
        # Fortress floor and walls
        ground_y = self.height - ts * 2
        
        # Ground with gaps (hazards!)
        gap_positions = [600, 1200, 1800, 2400, 3000, 3400]
        for x in range(0, self.width, ts):
            # Check if this is a gap
            is_gap = any(gap <= x < gap + ts * 3 for gap in gap_positions)
            if not is_gap:
                self.tiles.add(Tile(x, ground_y, 'brick', x // ts))
                self.tiles.add(Tile(x, ground_y + ts, 'stone', x // ts))
        
        # Ceiling
        for x in range(0, self.width, ts):
            self.tiles.add(Tile(x, 0, 'stone', x // ts))
            self.tiles.add(Tile(x, ts, 'stone', x // ts))
        
        # Complex platform layout - requires precise jumping
        platforms = [
            # Section 1: Introduction
            (150, ground_y - ts * 2, 3, 'brick'),
            (350, ground_y - ts * 4, 2, 'brick'),
            # Over first gap
            (550, ground_y - ts * 3, 2, 'brick'),
            (700, ground_y - ts * 2, 2, 'brick'),
            # Section 2: Vertical challenge
            (850, ground_y - ts * 3, 3, 'brick'),
            (950, ground_y - ts * 5, 2, 'stone'),
            (1050, ground_y - ts * 7, 2, 'stone'),
            # Over second gap
            (1150, ground_y - ts * 4, 2, 'brick'),
            (1300, ground_y - ts * 2, 2, 'brick'),
            # Section 3: Narrow platforms
            (1450, ground_y - ts * 3, 1, 'brick'),
            (1550, ground_y - ts * 4, 1, 'brick'),
            (1650, ground_y - ts * 5, 1, 'brick'),
            (1750, ground_y - ts * 4, 1, 'brick'),
            # Over third gap
            (1850, ground_y - ts * 3, 2, 'brick'),
            (2000, ground_y - ts * 2, 3, 'brick'),
            # Section 4: Knight gauntlet
            (2200, ground_y - ts * 3, 4, 'brick'),
            (2450, ground_y - ts * 2, 3, 'brick'),
            # Over fourth gap
            (2350, ground_y - ts * 5, 2, 'stone'),
            (2550, ground_y - ts * 3, 2, 'brick'),
            # Section 5: Final stretch
            (2700, ground_y - ts * 4, 3, 'brick'),
            (2900, ground_y - ts * 2, 2, 'brick'),
            # Over fifth gap
            (2950, ground_y - ts * 4, 2, 'brick'),
            (3100, ground_y - ts * 3, 3, 'brick'),
            # Section 6: Before exit
            (3300, ground_y - ts * 2, 2, 'brick'),
            # Over sixth gap
            (3350, ground_y - ts * 4, 2, 'brick'),
            (3500, ground_y - ts * 3, 3, 'brick'),
            (3700, ground_y - ts * 2, 5, 'brick'),
        ]
        
        for px, py, length, tile_type in platforms:
            for i in range(length):
                self.tiles.add(Tile(px + i * ts, py, tile_type))
        
        # MANY enemies - this is the hard level!
        # Section 1
        self.enemies.add(create_enemy('knight', 200, ground_y - ts))
        self.enemies.add(create_enemy('bat', 400, ground_y - ts * 5))
        self.enemies.add(create_enemy('slime', 500, ground_y - ts))
        
        # Section 2 - vertical challenge with bats
        self.enemies.add(create_enemy('bat', 900, ground_y - ts * 4))
        self.enemies.add(create_enemy('bat', 1000, ground_y - ts * 6))
        self.enemies.add(create_enemy('knight', 1100, ground_y - ts))
        
        # Section 3 - narrow platforms with bats harassing
        self.enemies.add(create_enemy('bat', 1500, ground_y - ts * 5))
        self.enemies.add(create_enemy('bat', 1600, ground_y - ts * 6))
        self.enemies.add(create_enemy('bat', 1700, ground_y - ts * 5))
        self.enemies.add(create_enemy('knight', 1900, ground_y - ts))
        
        # Section 4 - knight gauntlet!
        self.enemies.add(create_enemy('knight', 2250, ground_y - ts))
        self.enemies.add(create_enemy('knight', 2400, ground_y - ts))
        self.enemies.add(create_enemy('bat', 2300, ground_y - ts * 4))
        self.enemies.add(create_enemy('knight', 2600, ground_y - ts))
        
        # Section 5 - mixed assault
        self.enemies.add(create_enemy('bat', 2800, ground_y - ts * 5))
        self.enemies.add(create_enemy('knight', 2950, ground_y - ts))
        self.enemies.add(create_enemy('bat', 3050, ground_y - ts * 4))
        self.enemies.add(create_enemy('slime', 3150, ground_y - ts))
        
        # Section 6 - final defense
        self.enemies.add(create_enemy('knight', 3400, ground_y - ts))
        self.enemies.add(create_enemy('bat', 3500, ground_y - ts * 4))
        self.enemies.add(create_enemy('knight', 3600, ground_y - ts))
        self.enemies.add(create_enemy('knight', 3750, ground_y - ts))
        
        # Items - strategically placed to help but require skill to get
        self.item_manager.spawn_food(180, ground_y - ts * 3)
        self.item_manager.spawn_magic_vial(380, ground_y - ts * 5)
        self.item_manager.spawn_food(720, ground_y - ts * 3)
        self.item_manager.spawn_magic_vial(1000, ground_y - ts * 6, potion=True)
        self.item_manager.spawn_food(1350, ground_y - ts * 3, feast=True)
        self.item_manager.spawn_magic_vial(1600, ground_y - ts * 5)
        self.item_manager.spawn_food(2050, ground_y - ts * 3)
        self.item_manager.spawn_magic_vial(2280, ground_y - ts * 4, potion=True)
        self.item_manager.spawn_heart_container(2400, ground_y - ts * 6)
        self.item_manager.spawn_food(2750, ground_y - ts * 5, feast=True)
        self.item_manager.spawn_magic_vial(3050, ground_y - ts * 4)
        self.item_manager.spawn_magic_bottle(3150, ground_y - ts * 4)
        self.item_manager.spawn_food(3550, ground_y - ts * 4, feast=True)
        self.item_manager.spawn_magic_vial(3720, ground_y - ts * 3, potion=True)
        
        # Exit
        self.exit_rect = pygame.Rect(self.width - 100, ground_y - ts * 2,
                                     ts, ts * 2)
        
        self.start_y = ground_y - ts
    
    def generate_boss_level(self):
        """Generate boss arena"""
        ts = Tile.SIZE  # Actual tile size (32 pixels)
        
        self.width = 1000
        self.height = 600
        
        # Arena floor
        ground_y = self.height - ts * 2
        for x in range(0, self.width, ts):
            self.tiles.add(Tile(x, ground_y, 'brick', x // ts))
            self.tiles.add(Tile(x, ground_y + ts, 'stone', x // ts))
        
        # Arena walls
        for y in range(0, ground_y, ts):
            self.tiles.add(Tile(0, y, 'stone'))
            self.tiles.add(Tile(self.width - ts, y, 'stone'))
        
        # Some platforms for dodging
        platforms = [
            (200, ground_y - ts * 3, 2, 'brick'),
            (450, ground_y - ts * 4, 3, 'brick'),
            (750, ground_y - ts * 3, 2, 'brick'),
        ]
        
        for px, py, length, tile_type in platforms:
            for i in range(length):
                self.tiles.add(Tile(px + i * ts, py, tile_type))
        
        # THE BOSS - Cannon!
        self.enemies.add(create_enemy('cannon', 700, ground_y - ts * 2))
        
        # Items for the fight
        self.item_manager.spawn_food(100, ground_y - ts * 4, feast=True)
        self.item_manager.spawn_magic_vial(250, ground_y - ts * 4, potion=True)
        self.item_manager.spawn_food(500, ground_y - ts * 5)
        self.item_manager.spawn_magic_vial(800, ground_y - ts * 4, potion=True)
        
        # No exit - must defeat boss
        self.exit_rect = None
        
        self.start_x = 150
        self.start_y = ground_y - ts
    
    def get_tiles(self):
        """Get all tiles for collision"""
        return self.tiles.sprites()
    
    def update_camera(self, player):
        """Update camera to follow player"""
        # Center on player horizontally
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        target_y = player.rect.centery - SCREEN_HEIGHT // 2
        
        # Smooth follow
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.05
        
        # Clamp to level bounds
        self.camera_x = max(0, min(self.camera_x, self.width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.height - SCREEN_HEIGHT))
    
    def update(self, player):
        """Update level state"""
        self.update_camera(player)
        
        # Update enemies
        tiles = self.get_tiles()
        for enemy in self.enemies:
            enemy.update(player, tiles)
        
        # Update items
        self.item_manager.update()
        
        # Check if boss is defeated
        if self.level_id == 'boss' and len(self.enemies) == 0:
            self.completed = True
        
        # Check if player reached exit
        if self.exit_rect and player.rect.colliderect(self.exit_rect):
            self.completed = True
    
    def get_camera_offset(self):
        """Get current camera offset"""
        return (int(self.camera_x), int(self.camera_y))
    
    def draw(self, surface):
        """Draw the level"""
        camera_offset = self.get_camera_offset()
        
        # Draw background
        self.draw_background(surface)
        
        # Track background region
        introspect.track_region(
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            f"level_background_{self.level_type}",
            {"level_id": self.level_id, "level_type": self.level_type}
        )
        
        # Draw tiles
        for tile in self.tiles:
            draw_x = tile.rect.x - camera_offset[0]
            draw_y = tile.rect.y - camera_offset[1]
            
            # Only draw visible tiles
            if (-TILE_SIZE * PIXEL_SCALE < draw_x < SCREEN_WIDTH + TILE_SIZE * PIXEL_SCALE and
                -TILE_SIZE * PIXEL_SCALE < draw_y < SCREEN_HEIGHT + TILE_SIZE * PIXEL_SCALE):
                introspect.draw(surface, tile.image, (draw_x, draw_y), 
                               f"tile_{tile.tile_type}",
                               {"tile_type": tile.tile_type, "world_x": tile.rect.x, "world_y": tile.rect.y})
        
        # Draw exit
        if self.exit_rect:
            exit_x = self.exit_rect.x - camera_offset[0]
            exit_y = self.exit_rect.y - camera_offset[1]
            exit_screen_rect = pygame.Rect(exit_x, exit_y, self.exit_rect.width, self.exit_rect.height)
            pygame.draw.rect(surface, YELLOW, exit_screen_rect, 2)
            # Draw arrow
            pygame.draw.polygon(surface, YELLOW, [
                (exit_x + 16, exit_y + 10),
                (exit_x + 26, exit_y + 25),
                (exit_x + 6, exit_y + 25)
            ])
            introspect.track_region(exit_screen_rect, "level_exit",
                                   {"level_id": self.level_id})
        
        # Draw items
        self.item_manager.draw(surface, camera_offset)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(surface, camera_offset)
    
    def draw_background(self, surface):
        """Draw level background"""
        if self.level_type == LEVEL_CAVE:
            surface.fill(DARK_BROWN)
            # Cave atmosphere
            for i in range(20):
                x = (i * 157 - int(self.camera_x * 0.2)) % SCREEN_WIDTH
                y = (i * 89) % SCREEN_HEIGHT
                pygame.draw.circle(surface, BROWN, (x, y), 30)
        elif self.level_id == 'fortress':
            # Cannon's Domain - dark and foreboding
            surface.fill(DARK_BLUE)
            # Ominous red glow from below
            for i in range(SCREEN_WIDTH // 40):
                x = i * 40 - int(self.camera_x * 0.1) % 40
                glow_height = 100 + (i % 3) * 30
                pygame.draw.rect(surface, (*DARK_RED[:3], 50), 
                               (x, SCREEN_HEIGHT - glow_height, 35, glow_height))
            # Dark pillars
            for i in range(12):
                x = (i * 180 - int(self.camera_x * 0.15)) % (SCREEN_WIDTH + 150)
                pygame.draw.rect(surface, NAVY, (x, 0, 60, SCREEN_HEIGHT))
                pygame.draw.rect(surface, DARK_BROWN, (x + 10, 0, 40, SCREEN_HEIGHT))
            # Chains hanging from ceiling
            for i in range(8):
                x = (i * 250 - int(self.camera_x * 0.2)) % (SCREEN_WIDTH + 200)
                for j in range(6):
                    pygame.draw.rect(surface, GRAY, (x + 5, j * 25, 10, 20))
        elif self.level_type == LEVEL_CASTLE:
            surface.fill(NAVY)
            # Castle interior
            for i in range(10):
                x = (i * 200 - int(self.camera_x * 0.1)) % (SCREEN_WIDTH + 100)
                pygame.draw.rect(surface, DARK_BLUE, (x, 0, 80, SCREEN_HEIGHT))
        elif self.level_type == LEVEL_BOSS:
            surface.fill(DARK_RED)
            # Ominous atmosphere
            for i in range(5):
                x = SCREEN_WIDTH // 2 + (i - 2) * 150
                pygame.draw.rect(surface, RED, (x, 0, 20, SCREEN_HEIGHT), 1)
            # Pulsing glow effect
            import math
            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.002)) * 30)
            pygame.draw.rect(surface, (*RED[:3], pulse), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            # Forest background
            surface.fill(SKY_BLUE)
            # Clouds
            for i in range(8):
                x = (i * 200 - int(self.camera_x * 0.3)) % (SCREEN_WIDTH + 200)
                pygame.draw.ellipse(surface, WHITE, (x, 50 + i * 20, 100, 40))
            # Distant trees
            for i in range(15):
                x = (i * 150 - int(self.camera_x * 0.5)) % (SCREEN_WIDTH + 100)
                pygame.draw.rect(surface, DARK_GREEN, (x, 300, 40, 200))
                pygame.draw.polygon(surface, GREEN, [
                    (x - 20, 300), (x + 20, 200), (x + 60, 300)
                ])
