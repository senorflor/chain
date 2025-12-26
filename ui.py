"""
User Interface elements for Chain
"""

import pygame
from settings import *
from sprites import create_heart_sprite, create_magic_sprite


class UI:
    """Handles all UI rendering"""
    
    def __init__(self):
        # Initialize font
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
        self.font_tiny = pygame.font.Font(None, 22)
        
        # Cache sprites and scale them up for prominence
        heart_full = create_heart_sprite(full=True)
        heart_empty = create_heart_sprite(full=False)
        magic_full = create_magic_sprite(full=True)
        magic_empty = create_magic_sprite(full=False)
        
        # Scale up HUD sprites by 1.5x for better visibility
        scale = 1.5
        self.heart_full = pygame.transform.scale(heart_full, 
            (int(heart_full.get_width() * scale), int(heart_full.get_height() * scale)))
        self.heart_empty = pygame.transform.scale(heart_empty, 
            (int(heart_empty.get_width() * scale), int(heart_empty.get_height() * scale)))
        self.magic_full = pygame.transform.scale(magic_full, 
            (int(magic_full.get_width() * scale), int(magic_full.get_height() * scale)))
        self.magic_empty = pygame.transform.scale(magic_empty, 
            (int(magic_empty.get_width() * scale), int(magic_empty.get_height() * scale)))
        
        # Spell icons
        self.spell_names = ['Shield', 'Swift', 'Fireball', 'Thunder', 'Thundr2']
        self.spell_colors = [CYAN, LIME, ORANGE, YELLOW, MAGENTA]
    
    def draw_health_bar(self, surface, current, maximum, x=16, y=16):
        """Draw health hearts with background panel"""
        # Calculate panel size
        heart_w = self.heart_full.get_width()
        heart_h = self.heart_full.get_height()
        panel_width = maximum * (heart_w + 6) + 20
        panel_height = heart_h + 16
        
        # Draw panel background
        pygame.draw.rect(surface, (*DARK_BLUE[:3], 200), (x - 8, y - 8, panel_width, panel_height))
        pygame.draw.rect(surface, RED, (x - 8, y - 8, panel_width, panel_height), 2)
        
        # Draw label
        label = self.font_tiny.render("HP", True, RED)
        surface.blit(label, (x - 4, y - 6))
        
        # Draw hearts
        for i in range(maximum):
            if i < current:
                sprite = self.heart_full
            else:
                sprite = self.heart_empty
            
            surface.blit(sprite, (x + 24 + i * (heart_w + 6), y))
    
    def draw_magic_bar(self, surface, current, maximum, x=16, y=60):
        """Draw magic crystals with background panel"""
        # Calculate panel size
        magic_w = self.magic_full.get_width()
        magic_h = self.magic_full.get_height()
        panel_width = maximum * (magic_w + 6) + 20
        panel_height = magic_h + 16
        
        # Draw panel background
        pygame.draw.rect(surface, (*DARK_BLUE[:3], 200), (x - 8, y - 8, panel_width, panel_height))
        pygame.draw.rect(surface, CYAN, (x - 8, y - 8, panel_width, panel_height), 2)
        
        # Draw label
        label = self.font_tiny.render("MP", True, CYAN)
        surface.blit(label, (x - 4, y - 6))
        
        # Draw crystals
        for i in range(maximum):
            if i < current:
                sprite = self.magic_full
            else:
                sprite = self.magic_empty
            
            surface.blit(sprite, (x + 24 + i * (magic_w + 6), y))
    
    def draw_spell_selector(self, surface, selected_spell, spell_manager, x=16, y=110):
        """Draw spell selection UI with background panel"""
        slot_width = 52
        slot_height = 50
        panel_width = 5 * slot_width + 30
        panel_height = slot_height + 40
        
        # Draw panel background
        pygame.draw.rect(surface, (*DARK_BLUE[:3], 200), (x - 8, y - 8, panel_width, panel_height))
        pygame.draw.rect(surface, YELLOW, (x - 8, y - 8, panel_width, panel_height), 2)
        
        # Draw label
        label = self.font_tiny.render("SPELLS", True, YELLOW)
        surface.blit(label, (x, y - 6))
        
        for i, (name, color) in enumerate(zip(self.spell_names, self.spell_colors)):
            # Draw slot background
            slot_x = x + i * slot_width + 4
            slot_y = y + 12
            
            # Draw slot base
            pygame.draw.rect(surface, DARK_BROWN, (slot_x, slot_y, slot_width - 8, slot_height - 10))
            
            # Highlight selected with glow effect
            if i == selected_spell:
                pygame.draw.rect(surface, color, (slot_x - 3, slot_y - 3, slot_width - 2, slot_height - 4), 3)
                pygame.draw.rect(surface, WHITE, (slot_x, slot_y, slot_width - 8, slot_height - 10), 1)
            
            # Draw spell icon area
            pygame.draw.rect(surface, color, (slot_x + 4, slot_y + 4, slot_width - 16, 24))
            
            # Draw spell initial/abbreviation
            if name == 'Thundr2':
                spell_text = self.font_small.render("T2", True, DARK_BLUE)
                surface.blit(spell_text, (slot_x + 10, slot_y + 8))
            else:
                spell_text = self.font_medium.render(name[0], True, DARK_BLUE)
                surface.blit(spell_text, (slot_x + 12, slot_y + 6))
            
            # Draw spell number
            num_text = self.font_tiny.render(str(i + 1), True, LIGHT_GRAY)
            surface.blit(num_text, (slot_x + 16, slot_y + 30))
        
        # Show active buffs below spell bar
        active_buffs = spell_manager.get_active_buffs()
        if active_buffs:
            buff_y = y + panel_height - 4
            pygame.draw.rect(surface, (*DARK_BLUE[:3], 200), (x - 8, buff_y, panel_width, 24))
            buff_x = x
            for buff in active_buffs:
                buff_color = CYAN if buff == 'shield' else LIME
                pygame.draw.rect(surface, buff_color, (buff_x, buff_y + 4, 12, 12))
                buff_text = self.font_tiny.render(buff.upper(), True, buff_color)
                surface.blit(buff_text, (buff_x + 16, buff_y + 4))
                buff_x += 80
    
    def draw_score(self, surface, score, x=None, y=16):
        """Draw score with background panel"""
        if x is None:
            x = SCREEN_WIDTH - 180
        
        score_str = f"SCORE: {score:,}"
        text_width = self.font_medium.size(score_str)[0]
        panel_width = text_width + 24
        panel_height = 40
        
        # Draw panel background
        pygame.draw.rect(surface, (*DARK_BLUE[:3], 200), (x - 8, y - 8, panel_width, panel_height))
        pygame.draw.rect(surface, YELLOW, (x - 8, y - 8, panel_width, panel_height), 2)
        
        score_text = self.font_medium.render(score_str, True, YELLOW)
        surface.blit(score_text, (x + 4, y + 2))
    
    def draw_level_name(self, surface, name, x=None, y=None):
        """Draw level name at top center with prominent styling"""
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = 24
        
        text = self.font_medium.render(name, True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        
        # Background panel
        panel_rect = pygame.Rect(text_rect.x - 16, text_rect.y - 8, 
                                 text_rect.width + 32, text_rect.height + 16)
        pygame.draw.rect(surface, (*DARK_BLUE[:3], 220), panel_rect)
        pygame.draw.rect(surface, WHITE, panel_rect, 2)
        pygame.draw.rect(surface, YELLOW, panel_rect.inflate(-4, -4), 1)
        
        surface.blit(text, text_rect)
    
    def draw_dialog(self, surface, text, speaker=None):
        """Draw dialog box at bottom of screen"""
        box_height = 100
        box_y = SCREEN_HEIGHT - box_height - 20
        
        # Draw box
        pygame.draw.rect(surface, DARK_BLUE, (20, box_y, SCREEN_WIDTH - 40, box_height))
        pygame.draw.rect(surface, WHITE, (20, box_y, SCREEN_WIDTH - 40, box_height), 2)
        
        # Draw speaker name
        if speaker:
            name_text = self.font_medium.render(speaker, True, YELLOW)
            surface.blit(name_text, (40, box_y + 10))
            text_y = box_y + 40
        else:
            text_y = box_y + 20
        
        # Draw text (word wrap)
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if self.font_medium.size(test_line)[0] < SCREEN_WIDTH - 80:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        for i, line in enumerate(lines):
            line_text = self.font_medium.render(line, True, WHITE)
            surface.blit(line_text, (40, text_y + i * 25))
    
    def draw_menu(self, surface, title, options, selected):
        """Draw a menu screen"""
        # Title
        title_text = self.font_large.render(title, True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        surface.blit(title_text, title_rect)
        
        # Options
        for i, option in enumerate(options):
            if i == selected:
                color = YELLOW
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "
            
            option_text = self.font_medium.render(prefix + option, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 50))
            surface.blit(option_text, option_rect)
    
    def draw_game_over(self, surface, score):
        """Draw game over screen"""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Game Over text
        text = self.font_large.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        surface.blit(text, text_rect)
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        surface.blit(score_text, score_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press ENTER to return to menu", True, LIGHT_GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        surface.blit(inst_text, inst_rect)
    
    def draw_victory(self, surface, score):
        """Draw victory screen"""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Victory text
        text = self.font_large.render("VICTORY!", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        surface.blit(text, text_rect)
        
        # Story
        story = self.font_medium.render("You saved the Princess!", True, MINT)
        story_rect = story.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        surface.blit(story, story_rect)
        
        # Score
        score_text = self.font_medium.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        surface.blit(score_text, score_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press ENTER to return to menu", True, LIGHT_GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        surface.blit(inst_text, inst_rect)
    
    def draw_pause(self, surface):
        """Draw pause overlay"""
        # Darken background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))
        
        # Pause text
        text = self.font_large.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        surface.blit(text, text_rect)
        
        # Instructions
        inst_text = self.font_small.render("Press ESC to resume", True, LIGHT_GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        surface.blit(inst_text, inst_rect)
    
    def draw_hud(self, surface, player):
        """Draw the full HUD"""
        self.draw_health_bar(surface, player.health, player.max_health)
        self.draw_magic_bar(surface, player.magic, player.max_magic)
        self.draw_spell_selector(surface, player.spell_manager.selected_spell, 
                                player.spell_manager)
        self.draw_score(surface, player.score)
    
    def draw_world_map_hud(self, surface, player, current_location):
        """Draw HUD for world map"""
        self.draw_health_bar(surface, player.health, player.max_health)
        self.draw_magic_bar(surface, player.magic, player.max_magic)
        self.draw_score(surface, player.score)
        
        # Location name with prominent panel
        if current_location:
            loc_text = self.font_medium.render(current_location, True, WHITE)
            loc_rect = loc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 35))
            
            panel_rect = pygame.Rect(loc_rect.x - 20, loc_rect.y - 10,
                                    loc_rect.width + 40, loc_rect.height + 20)
            pygame.draw.rect(surface, (*DARK_BLUE[:3], 230), panel_rect)
            pygame.draw.rect(surface, YELLOW, panel_rect, 3)
            pygame.draw.rect(surface, WHITE, panel_rect.inflate(-4, -4), 1)
            
            surface.blit(loc_text, loc_rect)
    
    def draw_controls_help(self, surface):
        """Draw controls help"""
        controls = [
            "Arrow Keys/WASD: Move",
            "Space: Jump",
            "Z: Attack",
            "X: Cast Spell",
            "1-4: Select Spell",
            "Enter: Interact",
            "ESC: Pause"
        ]
        
        y = SCREEN_HEIGHT - len(controls) * 20 - 20
        for control in controls:
            text = self.font_small.render(control, True, LIGHT_GRAY)
            surface.blit(text, (SCREEN_WIDTH - 180, y))
            y += 20
