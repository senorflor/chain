"""
Enemy classes for Chain
"""

import pygame
import math
import random
from settings import *
from sprites import create_slime_sprite, create_bat_sprite, create_knight_sprite, create_cannon_sprite


class Enemy(pygame.sprite.Sprite):
    """Base enemy class"""
    
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        self.stats = ENEMY_TYPES[enemy_type]
        
        self.max_health = self.stats['health']
        self.health = self.max_health
        self.damage = self.stats['damage']
        self.speed = self.stats['speed']
        self.score = self.stats['score']
        
        self.frame = 0
        self.facing_right = True
        
        # AI state
        self.state = 'patrol'
        self.patrol_distance = 100
        self.start_x = x
        self.direction = 1
        
        # Physics
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Combat
        self.hurt_timer = 0
        self.attack_cooldown = 0
        
        # Create initial sprite
        self.update_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update_sprite(self):
        """Override in subclasses"""
        pass
    
    def update(self, player=None, tiles=None):
        """Update enemy state"""
        self.frame += 1
        
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        self.ai_update(player)
        self.physics_update(tiles)
        self.update_sprite()
    
    def ai_update(self, player):
        """AI behavior - override in subclasses"""
        pass
    
    def physics_update(self, tiles):
        """Apply physics"""
        # Apply gravity
        self.velocity_y += PLAYER_GRAVITY
        if self.velocity_y > 15:
            self.velocity_y = 15
        
        # Move
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check tile collisions
        if tiles:
            for tile in tiles:
                if self.rect.colliderect(tile.rect):
                    if self.velocity_y > 0:
                        self.rect.bottom = tile.rect.top
                        self.velocity_y = 0
                    elif self.velocity_y < 0:
                        self.rect.top = tile.rect.bottom
                        self.velocity_y = 0
    
    def take_damage(self, amount):
        """Take damage"""
        self.health -= amount
        self.hurt_timer = 10
        
        if self.health <= 0:
            self.kill()
            return True  # Enemy died
        return False
    
    def draw(self, surface, camera_offset=(0, 0)):
        """Draw enemy"""
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]
        
        # Flash when hurt
        if self.hurt_timer > 0 and self.frame % 4 < 2:
            return
        
        surface.blit(self.image, (draw_x, draw_y))
        
        # Draw health bar for tough enemies
        if self.max_health > 2:
            self.draw_health_bar(surface, camera_offset)
    
    def draw_health_bar(self, surface, camera_offset):
        """Draw health bar above enemy"""
        bar_width = 30
        bar_height = 4
        
        x = self.rect.centerx - camera_offset[0] - bar_width // 2
        y = self.rect.top - camera_offset[1] - 8
        
        # Background
        pygame.draw.rect(surface, DARK_RED, (x, y, bar_width, bar_height))
        
        # Health
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(surface, RED, (x, y, health_width, bar_height))


class Slime(Enemy):
    """Slime enemy - easy, hops around"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'slime')
        self.hop_timer = 0
    
    def update_sprite(self):
        self.image = create_slime_sprite(self.frame)
    
    def ai_update(self, player):
        self.velocity_x = 0
        
        # Hop periodically
        self.hop_timer += 1
        if self.hop_timer >= 60:
            self.hop_timer = 0
            self.velocity_y = -6
            
            # Move toward player if nearby, otherwise patrol
            if player and abs(player.rect.centerx - self.rect.centerx) < 200:
                if player.rect.centerx < self.rect.centerx:
                    self.velocity_x = -self.speed * 2
                else:
                    self.velocity_x = self.speed * 2
            else:
                # Patrol
                if self.rect.x > self.start_x + self.patrol_distance:
                    self.direction = -1
                elif self.rect.x < self.start_x - self.patrol_distance:
                    self.direction = 1
                self.velocity_x = self.speed * self.direction


class Bat(Enemy):
    """Bat enemy - flying, erratic movement"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'bat')
        self.start_y = y
        self.angle = 0
        self.swoop_target = None
    
    def update_sprite(self):
        self.image = create_bat_sprite(self.frame)
    
    def ai_update(self, player):
        # Erratic flying pattern
        self.angle += 0.05
        
        if player and abs(player.rect.centerx - self.rect.centerx) < 150:
            # Swoop toward player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist > 0:
                self.velocity_x = (dx / dist) * self.speed * 1.5
                self.velocity_y = (dy / dist) * self.speed * 1.5
        else:
            # Patrol pattern
            self.velocity_x = math.sin(self.angle) * self.speed
            self.velocity_y = math.cos(self.angle * 2) * self.speed * 0.5
        
        self.facing_right = self.velocity_x > 0
    
    def physics_update(self, tiles):
        # Bats don't use gravity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Keep within bounds
        if self.rect.y < self.start_y - 100:
            self.rect.y = self.start_y - 100
        if self.rect.y > self.start_y + 100:
            self.rect.y = self.start_y + 100


class Knight(Enemy):
    """Knight enemy - tough, shielded, aggressive"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'knight')
        self.shield_active = True
        self.charge_timer = 0
        self.charging = False
    
    def update_sprite(self):
        self.image = create_knight_sprite(self.facing_right, self.frame)
    
    def ai_update(self, player):
        self.velocity_x = 0
        
        if player:
            dx = player.rect.centerx - self.rect.centerx
            
            # Face player
            self.facing_right = dx > 0
            
            if abs(dx) < 250:
                # Aggressive pursuit
                self.charge_timer += 1
                
                if self.charge_timer >= 90:
                    # Charge attack
                    self.charging = True
                    self.charge_timer = 0
                
                if self.charging:
                    self.velocity_x = self.speed * 3 * (1 if self.facing_right else -1)
                    if abs(dx) < 30 or abs(dx) > 200:
                        self.charging = False
                else:
                    # Walk toward player
                    if abs(dx) > 40:
                        self.velocity_x = self.speed * (1 if dx > 0 else -1)
            else:
                # Patrol
                self.charge_timer = 0
                self.charging = False
                if self.rect.x > self.start_x + self.patrol_distance:
                    self.direction = -1
                    self.facing_right = False
                elif self.rect.x < self.start_x - self.patrol_distance:
                    self.direction = 1
                    self.facing_right = True
                self.velocity_x = self.speed * self.direction
    
    def take_damage(self, amount):
        """Knights take reduced damage from front when shield is up"""
        if self.shield_active:
            # Shield blocks some damage
            amount = max(1, amount - 1)
        return super().take_damage(amount)


class Cannon(Enemy):
    """Boss enemy - the archenemy"""
    
    def __init__(self, x, y):
        super().__init__(x, y, 'cannon')
        self.phase = 1
        self.attack_pattern = 0
        self.pattern_timer = 0
        self.projectiles = pygame.sprite.Group()
        self.arena_bounds = (x - 200, x + 200)
        
        # Intro animation
        self.intro_active = True
        self.intro_timer = 0
        self.intro_duration = 180  # 3 seconds at 60fps
        self.intro_y_offset = -200  # Start above screen
        self.original_y = y
        
        # Phase transition
        self.phase_transition = False
        self.phase_transition_timer = 0
        self.last_phase = 1
    
    def update_sprite(self):
        # Flash during phase transition (guard against early call during __init__)
        if getattr(self, 'phase_transition', False) and self.frame % 4 < 2:
            self.image = pygame.Surface((48, 48), pygame.SRCALPHA)
            self.image.fill((*YELLOW[:3], 200))
        else:
            self.image = create_cannon_sprite(self.frame)
    
    def ai_update(self, player):
        self.velocity_x = 0
        
        # Handle intro animation
        if self.intro_active:
            self.intro_timer += 1
            # Descend from above
            progress = min(1.0, self.intro_timer / (self.intro_duration * 0.6))
            # Ease out
            ease = 1 - (1 - progress) ** 3
            self.intro_y_offset = -200 * (1 - ease)
            self.rect.y = self.original_y + self.intro_y_offset
            
            if self.intro_timer >= self.intro_duration:
                self.intro_active = False
                self.intro_y_offset = 0
                self.rect.y = self.original_y
            return
        
        if not player:
            return
        
        # Handle phase transition animation
        if self.phase_transition:
            self.phase_transition_timer += 1
            if self.phase_transition_timer >= 60:
                self.phase_transition = False
                self.phase_transition_timer = 0
            return
        
        # Update phase based on health
        old_phase = self.phase
        if self.health <= self.max_health * 0.3:
            self.phase = 3
        elif self.health <= self.max_health * 0.5:
            self.phase = 2
        
        # Trigger phase transition animation
        if self.phase != old_phase:
            self.phase_transition = True
            self.phase_transition_timer = 0
            self.last_phase = self.phase
        
        dx = player.rect.centerx - self.rect.centerx
        self.facing_right = dx > 0
        
        self.pattern_timer += 1
        
        if self.phase == 1:
            self.phase1_ai(player)
        elif self.phase == 2:
            self.phase2_ai(player)
        else:
            self.phase3_ai(player)
    
    def phase1_ai(self, player):
        """Phase 1: Patrol and shoot"""
        # Move back and forth
        if self.rect.x > self.arena_bounds[1]:
            self.direction = -1
        elif self.rect.x < self.arena_bounds[0]:
            self.direction = 1
        
        self.velocity_x = self.speed * self.direction
        
        # Shoot periodically
        if self.pattern_timer >= 90:
            self.shoot_cannon_ball(player)
            self.pattern_timer = 0
    
    def phase2_ai(self, player):
        """Phase 2: Jump attacks and spread shot"""
        dx = player.rect.centerx - self.rect.centerx
        
        # Aggressive chase
        if abs(dx) > 80:
            self.velocity_x = self.speed * 2 * (1 if dx > 0 else -1)
        
        # Jump attack periodically
        if self.pattern_timer % 120 == 0 and self.pattern_timer > 0:
            self.velocity_y = -10  # Jump!
        
        # Spread shot - fires 3 cannon balls
        if self.pattern_timer >= 60:
            self.shoot_cannon_ball(player)
            # Shoot additional balls at angles
            self.shoot_spread_shot(player)
            self.pattern_timer = 0
    
    def shoot_spread_shot(self, player):
        """Fire spread of cannon balls"""
        # Upper shot
        ball1 = CannonBall(
            self.rect.centerx,
            self.rect.centery,
            player.rect.centerx,
            player.rect.centery - 100
        )
        # Lower shot
        ball2 = CannonBall(
            self.rect.centerx,
            self.rect.centery,
            player.rect.centerx,
            player.rect.centery + 100
        )
        self.projectiles.add(ball1)
        self.projectiles.add(ball2)
    
    def phase3_ai(self, player):
        """Phase 3: Enraged - fast and aggressive"""
        dx = player.rect.centerx - self.rect.centerx
        
        # Aggressive pursuit
        self.velocity_x = self.speed * 2 * (1 if dx > 0 else -1)
        
        # Very rapid fire
        if self.pattern_timer >= 30:
            self.shoot_cannon_ball(player)
            self.pattern_timer = 0
    
    def shoot_cannon_ball(self, player):
        """Fire a cannon ball at the player"""
        ball = CannonBall(
            self.rect.centerx,
            self.rect.centery,
            player.rect.centerx,
            player.rect.centery
        )
        self.projectiles.add(ball)
    
    def update(self, player=None, tiles=None):
        super().update(player, tiles)
        self.projectiles.update()
    
    def draw(self, surface, camera_offset=(0, 0)):
        super().draw(surface, camera_offset)
        
        # Draw projectiles
        for ball in self.projectiles:
            ball.draw(surface, camera_offset)
        
        # Draw boss health bar at top of screen
        self.draw_boss_health_bar(surface)
    
    def draw_boss_health_bar(self, surface):
        """Draw large boss health bar at top"""
        bar_width = 500
        bar_height = 35
        x = SCREEN_WIDTH // 2 - bar_width // 2
        y = 55
        
        pygame.font.init()
        title_font = pygame.font.Font(None, 48)
        phase_font = pygame.font.Font(None, 32)
        
        # Draw intro text if in intro
        if self.intro_active:
            # Dramatic intro text
            if self.intro_timer > 30:
                intro_texts = ["THE ARCHENEMY", "CANNON", "APPEARS!"]
                text_idx = min(2, (self.intro_timer - 30) // 40)
                intro_text = title_font.render(intro_texts[text_idx], True, RED)
                intro_rect = intro_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                
                # Flashing background
                if self.frame % 8 < 4:
                    pygame.draw.rect(surface, DARK_RED, 
                                   (intro_rect.x - 20, intro_rect.y - 10, 
                                    intro_rect.width + 40, intro_rect.height + 20))
                surface.blit(intro_text, intro_rect)
            return
        
        # Boss name header - large and prominent
        name_text = title_font.render("CANNON", True, YELLOW)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 28))
        
        # Name background panel
        panel_rect = pygame.Rect(name_rect.x - 25, name_rect.y - 8, 
                                name_rect.width + 50, name_rect.height + 16)
        pygame.draw.rect(surface, DARK_BLUE, panel_rect)
        pygame.draw.rect(surface, DARK_RED, panel_rect, 3)
        pygame.draw.rect(surface, YELLOW, panel_rect.inflate(-6, -6), 2)
        surface.blit(name_text, name_rect)
        
        # Skull decorations on sides
        skull_left = title_font.render("☠", True, RED)
        skull_right = title_font.render("☠", True, RED)
        surface.blit(skull_left, (panel_rect.left - 30, name_rect.y - 2))
        surface.blit(skull_right, (panel_rect.right + 10, name_rect.y - 2))
        
        # Health bar outer frame
        frame_rect = pygame.Rect(x - 10, y - 10, bar_width + 20, bar_height + 20)
        pygame.draw.rect(surface, DARK_BLUE, frame_rect)
        pygame.draw.rect(surface, DARK_BROWN, frame_rect, 4)
        
        # Health bar inner background
        pygame.draw.rect(surface, BLACK, (x - 2, y - 2, bar_width + 4, bar_height + 4))
        pygame.draw.rect(surface, DARK_RED, (x, y, bar_width, bar_height))
        
        # Health bar fill with gradient
        health_width = int(bar_width * (self.health / self.max_health))
        if health_width > 0:
            # Choose color based on phase
            if self.phase == 3:
                bar_color = MAGENTA
                highlight_color = PINK
            elif self.phase == 2:
                bar_color = ORANGE
                highlight_color = YELLOW
            else:
                bar_color = RED
                highlight_color = ORANGE
            
            # Main health bar
            pygame.draw.rect(surface, bar_color, (x, y, health_width, bar_height))
            # Top highlight
            pygame.draw.rect(surface, highlight_color, (x, y, health_width, bar_height // 4))
            # Bottom shadow
            pygame.draw.rect(surface, DARK_RED, (x, y + bar_height - 5, health_width, 5))
        
        # Golden border
        pygame.draw.rect(surface, YELLOW, (x - 4, y - 4, bar_width + 8, bar_height + 8), 3)
        
        # Phase indicator with dramatic styling
        if self.phase >= 2:
            phase_color = MAGENTA if self.phase == 3 else ORANGE
            phase_str = "⚡ PHASE 2 - ENRAGED ⚡" if self.phase == 2 else "💀 PHASE 3 - FINAL FORM 💀"
            phase_text = phase_font.render(phase_str, True, phase_color)
            phase_rect = phase_text.get_rect(center=(SCREEN_WIDTH // 2, y + bar_height + 18))
            
            # Flashing effect during transition
            if self.phase_transition and self.frame % 6 < 3:
                pygame.draw.rect(surface, phase_color, phase_rect.inflate(20, 10))
            surface.blit(phase_text, phase_rect)
        
        # Health percentage
        health_pct = int((self.health / self.max_health) * 100)
        pct_text = phase_font.render(f"{health_pct}%", True, WHITE)
        pct_rect = pct_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        surface.blit(pct_text, pct_rect)


class CannonBall(pygame.sprite.Sprite):
    """Projectile fired by Cannon boss"""
    
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        
        self.speed = 5
        if dist > 0:
            self.velocity_x = (dx / dist) * self.speed
            self.velocity_y = (dy / dist) * self.speed
        else:
            self.velocity_x = self.speed
            self.velocity_y = 0
        
        self.damage = 2
        self.lifetime = 180
        
        # Create sprite
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GRAY, (8, 8), 7)
        pygame.draw.circle(self.image, DARK_BROWN, (8, 8), 5)
        pygame.draw.circle(self.image, ORANGE, (6, 6), 2)
        
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        self.lifetime -= 1
        
        if self.lifetime <= 0:
            self.kill()
    
    def draw(self, surface, camera_offset=(0, 0)):
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1]
        surface.blit(self.image, (draw_x, draw_y))


def create_enemy(enemy_type, x, y):
    """Factory function to create enemies"""
    if enemy_type == 'slime':
        return Slime(x, y)
    elif enemy_type == 'bat':
        return Bat(x, y)
    elif enemy_type == 'knight':
        return Knight(x, y)
    elif enemy_type == 'cannon':
        return Cannon(x, y)
    else:
        return Slime(x, y)  # Default
