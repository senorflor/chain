"""
Item system for Chain - pickups, power-ups, and collectibles
"""

import pygame
from settings import *
from sprites import (
    create_food_sprite, create_magic_vial_sprite,
    create_heart_sprite, create_magic_sprite
)
from introspection import introspect


class Item(pygame.sprite.Sprite):
    """Base item class"""
    
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.frame = 0
        
        # Bobbing animation
        self.base_y = y
        self.bob_offset = 0
        
        # Create sprite
        self.update_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update_sprite(self):
        """Override in subclasses"""
        pass
    
    def update(self):
        """Update item animation"""
        self.frame += 1
        
        # Bobbing effect
        import math
        self.bob_offset = int(math.sin(self.frame * 0.1) * 3)
        self.rect.y = self.base_y + self.bob_offset
        
        self.update_sprite()
    
    def collect(self, player):
        """Called when player collects this item - override in subclasses"""
        self.kill()
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Draw item"""
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]
        introspect.draw(surface, self.image, (draw_x, draw_y), f"item_{self.item_type}",
                       {"item_type": self.item_type, "world_x": self.rect.x, "world_y": self.rect.y})


class Food(Item):
    """Food item - restores health"""
    
    def __init__(self, x, y, food_type='food'):
        self.food_type = food_type
        super().__init__(x, y, food_type)
        
        if food_type == 'feast':
            self.heal_amount = ITEM_TYPES['feast']['heal']
        else:
            self.heal_amount = ITEM_TYPES['food']['heal']
    
    def update_sprite(self):
        self.image = create_food_sprite(self.food_type)
    
    def collect(self, player):
        player.heal(self.heal_amount)
        super().collect(player)


class MagicVial(Item):
    """Magic vial - restores magic points"""
    
    def __init__(self, x, y, vial_type='magic_vial'):
        self.vial_type = vial_type
        super().__init__(x, y, vial_type)
        
        if vial_type == 'magic_potion':
            self.restore_amount = ITEM_TYPES['magic_potion']['restore']
        else:
            self.restore_amount = ITEM_TYPES['magic_vial']['restore']
    
    def update_sprite(self):
        self.image = create_magic_vial_sprite(self.vial_type)
    
    def collect(self, player):
        player.restore_magic(self.restore_amount)
        super().collect(player)


class HeartContainer(Item):
    """Heart container - increases max health"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'heart_container')
        self.increase_amount = ITEM_TYPES['heart_container']['max_health_increase']
    
    def update_sprite(self):
        self.image = create_heart_sprite(is_container=True)
    
    def collect(self, player):
        player.increase_max_health(self.increase_amount)
        super().collect(player)


class MagicBottle(Item):
    """Magic bottle - increases max magic"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'magic_bottle')
        self.increase_amount = ITEM_TYPES['magic_bottle']['max_magic_increase']
    
    def update_sprite(self):
        self.image = create_magic_sprite(is_bottle=True)
    
    def collect(self, player):
        player.increase_max_magic(self.increase_amount)
        super().collect(player)


class Coin(Item):
    """Coin - adds to score"""
    
    def __init__(self, x, y, value=10):
        self.value = value
        super().__init__(x, y, 'coin')
    
    def update_sprite(self):
        # Create coin sprite
        size = 10
        surface = pygame.Surface((size * PIXEL_SCALE, size * PIXEL_SCALE), pygame.SRCALPHA)
        
        # Animated rotation effect
        frame_mod = self.frame % 20
        if frame_mod < 5:
            width = 8
        elif frame_mod < 10:
            width = 6
        elif frame_mod < 15:
            width = 4
        else:
            width = 6
        
        x_offset = (10 - width) // 2
        
        # Draw coin
        scaled_width = width * PIXEL_SCALE
        scaled_x = x_offset * PIXEL_SCALE
        
        pygame.draw.rect(surface, YELLOW, 
                        (scaled_x, 2 * PIXEL_SCALE, scaled_width, 6 * PIXEL_SCALE))
        pygame.draw.rect(surface, ORANGE, 
                        (scaled_x, 6 * PIXEL_SCALE, scaled_width, 2 * PIXEL_SCALE))
        
        self.image = surface
    
    def collect(self, player):
        player.add_score(self.value)
        super().collect(player)


class Key(Item):
    """Key - unlocks doors/chests"""
    
    def __init__(self, x, y, key_id='default'):
        self.key_id = key_id
        super().__init__(x, y, 'key')
    
    def update_sprite(self):
        # Create key sprite
        size = 12
        surface = pygame.Surface((size * PIXEL_SCALE, size * PIXEL_SCALE), pygame.SRCALPHA)
        
        # Key shape
        pygame.draw.rect(surface, YELLOW, 
                        (2 * PIXEL_SCALE, 2 * PIXEL_SCALE, 4 * PIXEL_SCALE, 4 * PIXEL_SCALE))
        pygame.draw.rect(surface, YELLOW, 
                        (4 * PIXEL_SCALE, 5 * PIXEL_SCALE, 2 * PIXEL_SCALE, 6 * PIXEL_SCALE))
        pygame.draw.rect(surface, YELLOW, 
                        (2 * PIXEL_SCALE, 8 * PIXEL_SCALE, 2 * PIXEL_SCALE, 2 * PIXEL_SCALE))
        pygame.draw.rect(surface, ORANGE, 
                        (3 * PIXEL_SCALE, 3 * PIXEL_SCALE, 2 * PIXEL_SCALE, 2 * PIXEL_SCALE))
        
        self.image = surface
    
    def collect(self, player):
        # Add key to player inventory (would need to implement inventory)
        player.add_score(100)  # For now, just add score
        super().collect(player)


class ItemManager:
    """Manages all items in a level"""
    
    def __init__(self):
        self.items = pygame.sprite.Group()
    
    def add_item(self, item):
        """Add an item to the manager"""
        self.items.add(item)
    
    def spawn_food(self, x, y, feast=False):
        """Spawn a food item"""
        food_type = 'feast' if feast else 'food'
        self.items.add(Food(x, y, food_type))
    
    def spawn_magic_vial(self, x, y, potion=False):
        """Spawn a magic vial"""
        vial_type = 'magic_potion' if potion else 'magic_vial'
        self.items.add(MagicVial(x, y, vial_type))
    
    def spawn_heart_container(self, x, y):
        """Spawn a heart container"""
        self.items.add(HeartContainer(x, y))
    
    def spawn_magic_bottle(self, x, y):
        """Spawn a magic bottle"""
        self.items.add(MagicBottle(x, y))
    
    def spawn_coin(self, x, y, value=10):
        """Spawn a coin"""
        self.items.add(Coin(x, y, value))
    
    def spawn_key(self, x, y, key_id='default'):
        """Spawn a key"""
        self.items.add(Key(x, y, key_id))
    
    def update(self):
        """Update all items"""
        self.items.update()
    
    def check_collection(self, player):
        """Check if player collected any items"""
        for item in self.items:
            if player.rect.colliderect(item.rect):
                item.collect(player)
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Draw all items"""
        for item in self.items:
            item.draw(surface, camera_offset)
    
    def clear(self):
        """Clear all items"""
        self.items.empty()


def create_item(item_type, x, y):
    """Factory function to create items"""
    if item_type == 'food':
        return Food(x, y, 'food')
    elif item_type == 'feast':
        return Food(x, y, 'feast')
    elif item_type == 'magic_vial':
        return MagicVial(x, y, 'magic_vial')
    elif item_type == 'magic_potion':
        return MagicVial(x, y, 'magic_potion')
    elif item_type == 'heart_container':
        return HeartContainer(x, y)
    elif item_type == 'magic_bottle':
        return MagicBottle(x, y)
    elif item_type == 'coin':
        return Coin(x, y)
    elif item_type == 'key':
        return Key(x, y)
    else:
        return Coin(x, y)  # Default
