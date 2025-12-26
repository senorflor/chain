"""
Spell system for Chain
"""

import pygame
import math
from settings import *
from sprites import create_fireball_sprite, create_thunder_sprite, create_shield_effect_sprite


class Spell:
    """Base spell class"""
    
    def __init__(self, name, cost, spell_type):
        self.name = name
        self.cost = cost
        self.spell_type = spell_type  # 'buff' or 'offensive'
        self.active = False
        self.duration = 0
        self.frame = 0
    
    def can_cast(self, magic_points):
        return magic_points >= self.cost
    
    def cast(self, caster, target_pos=None, facing_right=True):
        """Override in subclasses"""
        pass
    
    def update(self):
        self.frame += 1
    
    def draw(self, surface, pos):
        pass


class ShieldSpell(Spell):
    """Shield buff - reduces incoming damage"""
    
    def __init__(self):
        super().__init__('Shield', SPELL_COSTS['shield'], 'buff')
        self.duration = SPELL_DURATIONS['shield']
        self.remaining_duration = 0
    
    def cast(self, caster, target_pos=None, facing_right=True):
        self.active = True
        self.remaining_duration = self.duration
        return True
    
    def update(self):
        super().update()
        if self.active:
            self.remaining_duration -= 1
            if self.remaining_duration <= 0:
                self.active = False
    
    def get_damage_multiplier(self):
        if self.active:
            return SHIELD_DAMAGE_REDUCTION
        return 1.0
    
    def draw(self, surface, pos):
        if self.active:
            sprite = create_shield_effect_sprite(self.frame)
            # Center on player
            x = pos[0] - sprite.get_width() // 2
            y = pos[1] - sprite.get_height() // 2
            surface.blit(sprite, (x, y))


class SwiftSpell(Spell):
    """Swift buff - increases movement and jump speed"""
    
    def __init__(self):
        super().__init__('Swift', SPELL_COSTS['swift'], 'buff')
        self.duration = SPELL_DURATIONS['swift']
        self.remaining_duration = 0
        self.trail_particles = []  # Store particle positions
        self.last_pos = None
    
    def cast(self, caster, target_pos=None, facing_right=True):
        self.active = True
        self.remaining_duration = self.duration
        self.trail_particles = []
        return True
    
    def update(self):
        super().update()
        if self.active:
            self.remaining_duration -= 1
            if self.remaining_duration <= 0:
                self.active = False
                self.trail_particles = []
    
    def get_speed_multiplier(self):
        if self.active:
            return SWIFT_SPEED_MULTIPLIER
        return 1.0
    
    def get_jump_multiplier(self):
        if self.active:
            return SWIFT_JUMP_MULTIPLIER
        return 1.0
    
    def update_trail(self, current_pos):
        """Update trail particles based on player position"""
        if self.active:
            # Add new particle at current position
            self.trail_particles.append({
                'x': current_pos[0],
                'y': current_pos[1],
                'life': 15,
                'size': 8
            })
            # Update existing particles
            for particle in self.trail_particles:
                particle['life'] -= 1
                particle['size'] = max(2, particle['size'] - 0.3)
            # Remove dead particles
            self.trail_particles = [p for p in self.trail_particles if p['life'] > 0]
            # Limit particle count
            if len(self.trail_particles) > 20:
                self.trail_particles = self.trail_particles[-20:]
    
    def draw(self, surface, pos):
        if self.active:
            # Update trail with current position
            self.update_trail(pos)
            
            # Draw trail particles behind player (oldest first)
            colors = [CYAN, TEAL, MINT, WHITE]
            for i, particle in enumerate(self.trail_particles):
                alpha = int((particle['life'] / 15) * 200)
                color_idx = i % len(colors)
                color = colors[color_idx]
                size = int(particle['size'])
                pygame.draw.rect(surface, color, 
                               (int(particle['x']) - size//2, 
                                int(particle['y']) - size//2, 
                                size, size))


class Fireball(pygame.sprite.Sprite):
    """Fireball projectile"""
    
    def __init__(self, x, y, facing_right):
        super().__init__()
        self.frame = 0
        self.image = create_fireball_sprite(self.frame)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 1 if facing_right else -1
        self.speed = FIREBALL_SPEED
        self.damage = FIREBALL_DAMAGE
        self.lifetime = 120  # frames
    
    def update(self):
        self.frame += 1
        self.rect.x += self.speed * self.direction
        self.image = create_fireball_sprite(self.frame)
        self.lifetime -= 1
        
        if self.lifetime <= 0:
            self.kill()


class FireballSpell(Spell):
    """Fireball offensive spell"""
    
    def __init__(self):
        super().__init__('Fireball', SPELL_COSTS['fireball'], 'offensive')
        self.projectiles = pygame.sprite.Group()
    
    def cast(self, caster, target_pos=None, facing_right=True):
        # Create fireball projectile
        fireball = Fireball(caster.rect.centerx, caster.rect.centery, facing_right)
        self.projectiles.add(fireball)
        return fireball
    
    def update(self):
        super().update()
        self.projectiles.update()
    
    def draw(self, surface, pos):
        self.projectiles.draw(surface)
    
    def get_projectiles(self):
        return self.projectiles


class ThunderEffect(pygame.sprite.Sprite):
    """Thunder area effect"""
    
    def __init__(self, x, y):
        super().__init__()
        self.frame = 0
        self.image = create_thunder_sprite(self.frame)
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = THUNDER_DAMAGE
        self.radius = THUNDER_RADIUS
        self.lifetime = 30  # frames
        self.hit_enemies = set()  # Track which enemies have been hit
    
    def update(self):
        self.frame += 1
        self.image = create_thunder_sprite(self.frame)
        self.lifetime -= 1
        
        if self.lifetime <= 0:
            self.kill()
    
    def can_hit(self, enemy):
        """Check if enemy is in range and hasn't been hit yet"""
        if enemy in self.hit_enemies:
            return False
        
        # Calculate distance
        dx = enemy.rect.centerx - self.rect.centerx
        dy = enemy.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance <= self.radius:
            self.hit_enemies.add(enemy)
            return True
        return False


class ThunderSpell(Spell):
    """Thunder area-of-effect offensive spell"""
    
    def __init__(self):
        super().__init__('Thunder', SPELL_COSTS['thunder'], 'offensive')
        self.effects = pygame.sprite.Group()
    
    def cast(self, caster, target_pos=None, facing_right=True):
        # Create thunder effect at player position
        offset = 50 if facing_right else -50
        thunder = ThunderEffect(caster.rect.centerx + offset, caster.rect.centery)
        self.effects.add(thunder)
        return thunder
    
    def update(self):
        super().update()
        self.effects.update()
    
    def draw(self, surface, pos):
        self.effects.draw(surface)
    
    def get_effects(self):
        return self.effects


class Thunder2Effect(pygame.sprite.Sprite):
    """Thunder 2.0 - strikes down from above"""
    
    def __init__(self, x, target_y):
        super().__init__()
        self.frame = 0
        self.x = x
        self.target_y = target_y
        self.current_y = target_y - 300  # Start from above
        self.damage = THUNDER2_DAMAGE
        self.width = 40
        self.height = 0
        self.lifetime = 45  # frames
        self.hit_enemies = set()
        self.striking = True
        
        # Create initial image
        self.update_image()
        self.rect = self.image.get_rect(midtop=(x, self.current_y))
    
    def update_image(self):
        """Create the lightning bolt image"""
        if self.striking:
            # Growing lightning bolt
            self.height = min(300, self.height + 25)
        
        self.image = pygame.Surface((self.width, max(10, self.height)), pygame.SRCALPHA)
        
        # Draw lightning bolt with zigzag pattern
        color = YELLOW if self.frame % 4 < 2 else WHITE
        core_color = WHITE if self.frame % 4 < 2 else YELLOW
        
        # Main bolt
        bolt_x = self.width // 2
        segments = max(1, self.height // 30)
        points = [(bolt_x, 0)]
        
        for i in range(segments):
            y = (i + 1) * (self.height // segments)
            x_offset = ((i % 2) * 2 - 1) * 8  # Zigzag
            points.append((bolt_x + x_offset, y))
        
        if len(points) >= 2:
            # Draw glow
            for offset in [-4, -2, 0, 2, 4]:
                glow_points = [(p[0] + offset, p[1]) for p in points]
                if len(glow_points) >= 2:
                    pygame.draw.lines(self.image, (*color[:3], 100), False, glow_points, 6)
            
            # Draw core
            pygame.draw.lines(self.image, core_color, False, points, 4)
            pygame.draw.lines(self.image, WHITE, False, points, 2)
    
    def update(self):
        self.frame += 1
        self.lifetime -= 1
        
        if self.striking and self.height >= 300:
            self.striking = False
        
        self.update_image()
        self.rect = self.image.get_rect(midtop=(self.x, self.target_y - self.height))
        
        if self.lifetime <= 0:
            self.kill()
    
    def can_hit(self, enemy):
        """Check if enemy is hit by the lightning"""
        if enemy in self.hit_enemies:
            return False
        
        # Check if enemy is within the bolt's path
        if (abs(enemy.rect.centerx - self.x) < 30 and
            enemy.rect.top < self.target_y and
            enemy.rect.bottom > self.target_y - self.height):
            self.hit_enemies.add(enemy)
            return True
        return False


class Thunder2Spell(Spell):
    """Thunder 2.0 - powerful downward strike"""
    
    def __init__(self):
        super().__init__('Thunder2', SPELL_COSTS['thunder2'], 'offensive')
        self.effects = pygame.sprite.Group()
    
    def cast(self, caster, target_pos=None, facing_right=True):
        # Create thunder strike in front of player
        offset = 60 if facing_right else -60
        thunder = Thunder2Effect(caster.rect.centerx + offset, caster.rect.bottom)
        self.effects.add(thunder)
        return thunder
    
    def update(self):
        super().update()
        self.effects.update()
    
    def draw(self, surface, pos):
        self.effects.draw(surface)
    
    def get_effects(self):
        return self.effects


class SpellManager:
    """Manages all spells for the player"""
    
    def __init__(self):
        self.spells = {
            'shield': ShieldSpell(),
            'swift': SwiftSpell(),
            'fireball': FireballSpell(),
            'thunder': ThunderSpell(),
            'thunder2': Thunder2Spell()
        }
        self.spell_order = ['shield', 'swift', 'fireball', 'thunder', 'thunder2']
        self.selected_spell = 0
    
    def get_current_spell(self):
        spell_name = self.spell_order[self.selected_spell]
        return self.spells[spell_name]
    
    def select_spell(self, index):
        if 0 <= index < len(self.spell_order):
            self.selected_spell = index
    
    def next_spell(self):
        self.selected_spell = (self.selected_spell + 1) % len(self.spell_order)
    
    def prev_spell(self):
        self.selected_spell = (self.selected_spell - 1) % len(self.spell_order)
    
    def cast_current_spell(self, caster, magic_points, facing_right=True):
        spell = self.get_current_spell()
        if spell.can_cast(magic_points):
            result = spell.cast(caster, facing_right=facing_right)
            if result:
                return spell.cost
        return 0
    
    def update(self):
        for spell in self.spells.values():
            spell.update()
    
    def draw(self, surface, player_pos):
        for spell in self.spells.values():
            spell.draw(surface, player_pos)
    
    def get_speed_multiplier(self):
        return self.spells['swift'].get_speed_multiplier()
    
    def get_jump_multiplier(self):
        return self.spells['swift'].get_jump_multiplier()
    
    def get_damage_multiplier(self):
        return self.spells['shield'].get_damage_multiplier()
    
    def get_active_buffs(self):
        """Return list of active buff names"""
        active = []
        if self.spells['shield'].active:
            active.append('shield')
        if self.spells['swift'].active:
            active.append('swift')
        return active
    
    def get_projectiles(self):
        """Return all active projectiles"""
        return self.spells['fireball'].get_projectiles()
    
    def get_effects(self):
        """Return all active effects (thunder and thunder2)"""
        # Combine effects from both thunder spells
        all_effects = pygame.sprite.Group()
        for effect in self.spells['thunder'].get_effects():
            all_effects.add(effect)
        for effect in self.spells['thunder2'].get_effects():
            all_effects.add(effect)
        return all_effects
