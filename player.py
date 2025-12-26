"""
Player (Chain) class for the game
"""

import pygame
from settings import *
from sprites import (create_chain_sprite, create_chain_attack_sprite, 
                     create_chain_up_attack_sprite, create_chain_down_attack_sprite,
                     create_chain_world_sprite)
from spells import SpellManager


class Player(pygame.sprite.Sprite):
    """The main character - Chain"""
    
    def __init__(self, x, y, mode='level'):
        super().__init__()
        self.mode = mode  # 'level' for side-scroller, 'world' for top-down
        
        # Animation
        self.frame = 0
        self.facing_right = True
        self.facing = 'down'  # For world map
        self.is_attacking = False
        self.attack_frame = 0
        
        # Create sprite
        self.update_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Physics (for side-scroller)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # Last safe position (for pit respawn)
        self.last_safe_x = x
        self.last_safe_y = y
        
        # Stats
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.max_magic = PLAYER_MAX_MAGIC
        self.magic = self.max_magic
        
        # Combat
        self.attack_cooldown = 0
        self.invincibility = 0
        self.is_hurt = False
        self.is_up_attack = False  # For upward slash
        self.is_down_attack = False  # For downward stab
        
        # Spells
        self.spell_manager = SpellManager()
        
        # Score
        self.score = 0
        
        # Invincible mode (cheat)
        self.invincible_mode = False
        self.invincible_frame = 0
    
    def update_sprite(self):
        """Update the current sprite based on state"""
        if self.mode == 'world':
            self.image = create_chain_world_sprite(self.facing, self.frame)
        elif self.is_attacking:
            if self.is_up_attack:
                self.image = create_chain_up_attack_sprite(self.facing_right)
            elif self.is_down_attack:
                self.image = create_chain_down_attack_sprite(self.facing_right)
            else:
                self.image = create_chain_attack_sprite(self.facing_right)
        else:
            self.image = create_chain_sprite(self.facing_right, self.frame)
    
    def handle_input(self, keys, events):
        """Handle player input"""
        if self.mode == 'level':
            self.handle_level_input(keys, events)
        else:
            self.handle_world_input(keys, events)
    
    def handle_level_input(self, keys, events):
        """Handle input for side-scroller mode"""
        # Get speed multiplier from swift spell
        speed_mult = self.spell_manager.get_speed_multiplier()
        jump_mult = self.spell_manager.get_jump_multiplier()
        
        # Horizontal movement
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED * speed_mult
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED * speed_mult
            self.facing_right = True
        
        # Check for key events
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Jump
                if event.key == pygame.K_SPACE and self.on_ground:
                    self.velocity_y = PLAYER_JUMP_SPEED * jump_mult
                    self.on_ground = False
                
                # Attack (check if holding up/down for directional attacks)
                if event.key == pygame.K_z and self.attack_cooldown <= 0:
                    self.is_attacking = True
                    self.attack_frame = 15
                    self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
                    # Check if up is held for up-slash
                    self.is_up_attack = keys[pygame.K_UP] or keys[pygame.K_w]
                    # Check if down is held for down-stab (only in air)
                    self.is_down_attack = (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not self.on_ground
                
                # Cast spell
                if event.key == pygame.K_x:
                    cost = self.spell_manager.cast_current_spell(
                        self, self.magic, self.facing_right
                    )
                    self.magic -= cost
                
                # Select spell (1-5)
                if event.key == pygame.K_1:
                    self.spell_manager.select_spell(0)
                if event.key == pygame.K_2:
                    self.spell_manager.select_spell(1)
                if event.key == pygame.K_3:
                    self.spell_manager.select_spell(2)
                if event.key == pygame.K_4:
                    self.spell_manager.select_spell(3)
                if event.key == pygame.K_5:
                    self.spell_manager.select_spell(4)
                
                # Toggle invincible mode
                if event.key == pygame.K_i:
                    self.invincible_mode = not self.invincible_mode
    
    def handle_world_input(self, keys, events):
        """Handle input for world map mode"""
        speed = WORLD_PLAYER_SPEED
        
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -speed
            self.facing = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = speed
            self.facing = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -speed
            self.facing = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = speed
            self.facing = 'down'
    
    def update(self, tiles=None):
        """Update player state"""
        self.frame += 1
        
        # Update cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.invincibility > 0:
            self.invincibility -= 1
            self.is_hurt = self.invincibility % 10 < 5  # Flashing effect
        else:
            self.is_hurt = False
        
        # Update attack animation
        if self.is_attacking:
            self.attack_frame -= 1
            if self.attack_frame <= 0:
                self.is_attacking = False
                self.is_up_attack = False
                self.is_down_attack = False
        
        # Update spells
        self.spell_manager.update()
        
        if self.mode == 'level':
            self.update_level_physics(tiles)
        else:
            self.update_world_movement(tiles)
        
        self.update_sprite()
    
    def update_level_physics(self, tiles):
        """Update physics for side-scroller mode"""
        # Apply gravity
        self.velocity_y += PLAYER_GRAVITY
        if self.velocity_y > 15:  # Terminal velocity
            self.velocity_y = 15
        
        # Move horizontally
        self.rect.x += self.velocity_x
        
        # Check horizontal collisions
        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    if self.velocity_x > 0:
                        self.rect.right = tile.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = tile.rect.right
        
        # Move vertically
        self.rect.y += self.velocity_y
        
        # Check vertical collisions
        self.on_ground = False
        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    if self.velocity_y > 0:
                        self.rect.bottom = tile.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                        # Save safe position when landing
                        self.last_safe_x = self.rect.x
                        self.last_safe_y = self.rect.y
                    elif self.velocity_y < 0:
                        self.rect.top = tile.rect.bottom
                        self.velocity_y = 0
    
    def update_world_movement(self, tiles):
        """Update movement for world map mode"""
        # Move and check collisions
        old_x, old_y = self.rect.x, self.rect.y
        
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check tile collisions
        if tiles:
            for tile in tiles:
                if not tile.walkable and self.rect.colliderect(tile.rect):
                    self.rect.x = old_x
                    self.rect.y = old_y
                    break
    
    def take_damage(self, amount):
        """Take damage from an enemy or hazard"""
        # Invincible mode blocks all damage
        if self.invincible_mode:
            return False
        
        if self.invincibility > 0:
            return False
        
        # Apply shield damage reduction
        damage_mult = self.spell_manager.get_damage_multiplier()
        actual_damage = max(1, int(amount * damage_mult))
        
        self.health -= actual_damage
        self.invincibility = PLAYER_INVINCIBILITY_FRAMES
        
        if self.health <= 0:
            self.health = 0
            return True  # Player died
        return False
    
    def heal(self, amount):
        """Restore health"""
        self.health = min(self.max_health, self.health + amount)
    
    def restore_magic(self, amount):
        """Restore magic points"""
        self.magic = min(self.max_magic, self.magic + amount)
    
    def increase_max_health(self, amount=1):
        """Increase maximum health"""
        self.max_health += amount
        self.health += amount  # Also heal by the same amount
    
    def increase_max_magic(self, amount=1):
        """Increase maximum magic"""
        self.max_magic += amount
        self.magic += amount  # Also restore by the same amount
    
    def add_score(self, points):
        """Add to score"""
        self.score += points
    
    def get_attack_rect(self):
        """Get the attack hitbox"""
        if not self.is_attacking:
            return None
        
        # Up slash attack
        if self.is_up_attack:
            return pygame.Rect(
                self.rect.centerx - 15,
                self.rect.top - 35,
                30,
                40
            )
        
        # Down stab attack
        if self.is_down_attack:
            return pygame.Rect(
                self.rect.centerx - 12,
                self.rect.bottom,
                24,
                40
            )
        
        # Normal horizontal attack
        if self.facing_right:
            return pygame.Rect(
                self.rect.right,
                self.rect.centery - 10,
                30,
                20
            )
        else:
            return pygame.Rect(
                self.rect.left - 30,
                self.rect.centery - 10,
                30,
                20
            )
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Draw the player"""
        # Calculate draw position with camera offset
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]
        
        # Flash when hurt
        if self.is_hurt and self.frame % 4 < 2:
            return  # Don't draw (flashing effect)
        
        # Rainbow shimmer effect when in invincible mode
        if self.invincible_mode:
            self.invincible_frame += 1
            # Create rainbow-tinted copy of sprite
            rainbow_img = self.image.copy()
            
            # Cycle through rainbow colors
            hue = (self.invincible_frame * 8) % 360
            # Convert hue to RGB (simplified rainbow)
            if hue < 60:
                r, g, b = 255, int(hue * 4.25), 0
            elif hue < 120:
                r, g, b = int((120 - hue) * 4.25), 255, 0
            elif hue < 180:
                r, g, b = 0, 255, int((hue - 120) * 4.25)
            elif hue < 240:
                r, g, b = 0, int((240 - hue) * 4.25), 255
            elif hue < 300:
                r, g, b = int((hue - 240) * 4.25), 0, 255
            else:
                r, g, b = 255, 0, int((360 - hue) * 4.25)
            
            # Apply rainbow tint
            rainbow_img.fill((r, g, b, 100), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Draw with glow effect
            glow_surface = pygame.Surface((rainbow_img.get_width() + 8, rainbow_img.get_height() + 8), pygame.SRCALPHA)
            glow_surface.fill((r, g, b, 50))
            surface.blit(glow_surface, (draw_x - 4, draw_y - 4))
            surface.blit(rainbow_img, (draw_x, draw_y))
        else:
            surface.blit(self.image, (draw_x, draw_y))
        
        # Draw spell effects
        player_center = (
            self.rect.centerx - camera_offset[0],
            self.rect.centery - camera_offset[1]
        )
        self.spell_manager.draw(surface, player_center)
    
    def set_mode(self, mode):
        """Switch between level and world mode"""
        self.mode = mode
        self.velocity_x = 0
        self.velocity_y = 0
        self.update_sprite()
    
    def reset_position(self, x, y):
        """Reset player position"""
        self.rect.topleft = (x, y)
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_safe_x = x
        self.last_safe_y = y
    
    def respawn_at_safe_position(self):
        """Respawn at last safe position after falling in pit"""
        self.rect.x = self.last_safe_x
        self.rect.y = self.last_safe_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True
    
    def fell_in_pit(self, level_height):
        """Check if player fell below the level"""
        return self.rect.top > level_height + 100