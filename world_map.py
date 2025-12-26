"""
World Map for traversing between adventures
"""

import pygame
from settings import *
from sprites import create_world_map_tile


class WorldMapTile:
    """A tile on the world map"""
    
    def __init__(self, x, y, tile_type, walkable=True, level_id=None):
        self.tile_type = tile_type
        self.walkable = walkable
        self.level_id = level_id  # If this tile leads to a level
        
        self.image = create_world_map_tile(tile_type)
        # Use actual image size for positioning (16 * PIXEL_SCALE = 32)
        tile_size = self.image.get_width()
        self.rect = pygame.Rect(
            x * tile_size,
            y * tile_size,
            tile_size,
            tile_size
        )
        self.grid_x = x
        self.grid_y = y
    
    def draw(self, surface, camera_offset=(0, 0)):
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]
        surface.blit(self.image, (draw_x, draw_y))


class LevelMarker:
    """Marker for a level entrance on the world map"""
    
    def __init__(self, grid_x, grid_y, level_id, level_name, level_type):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.level_id = level_id
        self.level_name = level_name
        self.level_type = level_type
        self.completed = False
        self.unlocked = False
        
        self.image = create_world_map_tile('level_marker')
        # Use actual image size for positioning (16 * PIXEL_SCALE = 32)
        tile_size = self.image.get_width()
        self.rect = pygame.Rect(
            grid_x * tile_size,
            grid_y * tile_size,
            tile_size,
            tile_size
        )
        
        # Animation
        self.frame = 0
    
    def update(self):
        self.frame += 1
    
    def draw(self, surface, camera_offset=(0, 0)):
        if not self.unlocked:
            return
        
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]
        
        # Pulsing effect
        import math
        pulse = int(math.sin(self.frame * 0.1) * 3)
        
        # Draw marker
        if self.completed:
            # Completed levels show as green
            completed_img = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            completed_img.blit(self.image, (0, 0))
            completed_img.fill((*LIME[:3], 100), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(completed_img, (draw_x, draw_y + pulse))
        else:
            surface.blit(self.image, (draw_x, draw_y + pulse))


class WorldMap:
    """The overworld map for traversing between levels"""
    
    def __init__(self):
        self.tiles = []
        self.level_markers = []
        self.map_width = WORLD_MAP_WIDTH
        self.map_height = WORLD_MAP_HEIGHT
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Current level selection
        self.current_marker_index = 0
        
        self.generate_map()
    
    def generate_map(self):
        """Generate the world map"""
        # Define the map layout
        # Legend: G=grass, F=forest, M=mountain, W=water, P=path, C=castle, V=cave, B=boss, R=fortress
        map_data = [
            "MMMMMMMMMWWWWWWWWWWWMMMMMM",
            "MMMMMMMMWWWWWWWWWWWWMMMMMM",
            "MMMMFFFFFGGGGGGGFFFMMMMMM",
            "MMMFFFFFFGGGGGGGGFFMMMMMM",
            "MMFFFFFFFGGCGGGGGFFFMMMMM",
            "MFFFFFFFGGPPGGGGFFFFMMMMM",
            "FFFFFFFFGGPPGGGGFFFFFMMMM",
            "FFFFFFFGGGPPGGGGFFFFFFMMM",
            "FFFFFFGGGGPPPPGGGFFFFFMMM",
            "FFFFFGGGGGGGPPGGGFFFFFFMM",
            "FFFFGGGGGVGGPPGGGFFFFFFMM",
            "FFFGGGGGGGGPPPPPPPRFFFMMM",
            "FFFGGGGGGGPPGGGGGPPFFFMMM",
            "FFGGGGGGGGPPGGGGGGPPPFMMM",
            "FGGGGGGGGGPPGGGGGGGPBFMMM",
            "GGGGGGGGGPPPPGGGGGGGGFMMM",
            "GGGGGGGGGGGPPGGGGGGGFFMMM",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        
        tile_map = {
            'G': ('grass', True),
            'F': ('forest', False),
            'M': ('mountain', False),
            'W': ('water', False),
            'P': ('path', True),
            'C': ('castle', True),
            'V': ('cave', True),
            'R': ('fortress', True),
            'B': ('boss', True),
        }
        
        # Create tiles
        for y, row in enumerate(map_data):
            for x, char in enumerate(row):
                if char in tile_map:
                    tile_type, walkable = tile_map[char]
                    tile = WorldMapTile(x, y, tile_type, walkable)
                    self.tiles.append(tile)
        
        # Create level markers - progression through the world
        self.level_markers = [
            LevelMarker(10, 4, 'castle', "Castle Entrance", LEVEL_CASTLE),
            LevelMarker(9, 10, 'cave', "Dark Cave", LEVEL_CAVE),
            LevelMarker(17, 11, 'fortress', "Cannon's Domain", LEVEL_CASTLE),
            LevelMarker(19, 14, 'boss', "Cannon's Throne", LEVEL_BOSS),
        ]
        
        # Start with first level unlocked
        self.level_markers[0].unlocked = True
    
    def get_walkable_tiles(self):
        """Get list of walkable tiles for collision"""
        return [tile for tile in self.tiles if not tile.walkable]
    
    def get_current_level_marker(self, player_rect):
        """Check if player is on a level marker"""
        for marker in self.level_markers:
            if marker.unlocked and player_rect.colliderect(marker.rect):
                return marker
        return None
    
    def complete_level(self, level_id):
        """Mark a level as completed and unlock next"""
        for i, marker in enumerate(self.level_markers):
            if marker.level_id == level_id:
                marker.completed = True
                # Unlock next level
                if i + 1 < len(self.level_markers):
                    self.level_markers[i + 1].unlocked = True
                break
    
    def get_start_position(self):
        """Get the starting position for the player"""
        # Start near the first level marker
        first_marker = self.level_markers[0]
        return (
            first_marker.rect.x,
            first_marker.rect.y + TILE_SIZE * PIXEL_SCALE
        )
    
    def update_camera(self, player):
        """Update camera to follow player"""
        # Center camera on player
        target_x = player.rect.centerx - SCREEN_WIDTH // 2
        target_y = player.rect.centery - SCREEN_HEIGHT // 2
        
        # Smooth camera movement
        self.camera_x += (target_x - self.camera_x) * 0.1
        self.camera_y += (target_y - self.camera_y) * 0.1
        
        # Clamp to map bounds (tile size is 16 * PIXEL_SCALE = 32)
        actual_tile_size = 16 * PIXEL_SCALE
        max_x = self.map_width * actual_tile_size - SCREEN_WIDTH
        max_y = self.map_height * actual_tile_size - SCREEN_HEIGHT
        
        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))
    
    def update(self, player):
        """Update world map state"""
        self.update_camera(player)
        
        for marker in self.level_markers:
            marker.update()
    
    def draw(self, surface):
        """Draw the world map"""
        camera_offset = (int(self.camera_x), int(self.camera_y))
        
        # Draw tiles
        for tile in self.tiles:
            # Only draw visible tiles
            if (tile.rect.x - camera_offset[0] > -TILE_SIZE * PIXEL_SCALE and
                tile.rect.x - camera_offset[0] < SCREEN_WIDTH + TILE_SIZE * PIXEL_SCALE and
                tile.rect.y - camera_offset[1] > -TILE_SIZE * PIXEL_SCALE and
                tile.rect.y - camera_offset[1] < SCREEN_HEIGHT + TILE_SIZE * PIXEL_SCALE):
                tile.draw(surface, camera_offset)
        
        # Draw level markers
        for marker in self.level_markers:
            marker.draw(surface, camera_offset)
    
    def get_camera_offset(self):
        """Get current camera offset"""
        return (int(self.camera_x), int(self.camera_y))
    
    def get_location_name(self, player_rect):
        """Get the name of current location"""
        marker = self.get_current_level_marker(player_rect)
        if marker:
            status = " (Completed)" if marker.completed else " (Press ENTER)"
            return marker.level_name + status
        
        # Check tile type
        for tile in self.tiles:
            if player_rect.colliderect(tile.rect):
                names = {
                    'grass': 'Grasslands',
                    'forest': 'Dense Forest',
                    'mountain': 'Mountains',
                    'water': 'Ocean',
                    'path': 'The Road',
                    'castle': 'Castle',
                    'cave': 'Cave Entrance',
                    'boss': "Cannon's Domain"
                }
                return names.get(tile.tile_type, '')
        
        return ''
