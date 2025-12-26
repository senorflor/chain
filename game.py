"""
Main game class for Chain
"""

import pygame
from settings import *
from player import Player
from world_map import WorldMap
from level import Level
from ui import UI
from sounds import get_sound_manager


class Game:
    """Main game class that handles all game logic"""
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = STATE_MENU
        self.paused = False
        
        # Menu
        self.menu_options = ['New Game', 'Controls', 'Quit']
        self.menu_selection = 0
        self.showing_controls = False
        
        # Game objects
        self.player = None
        self.world_map = None
        self.current_level = None
        
        # UI
        self.ui = UI()
        
        # Sound
        self.sound = get_sound_manager()
        
        # Events from last frame
        self.events = []
    
    def new_game(self):
        """Start a new game"""
        self.world_map = WorldMap()
        start_pos = self.world_map.get_start_position()
        
        self.player = Player(start_pos[0], start_pos[1], mode='world')
        self.current_level = None
        self.state = STATE_WORLD_MAP
        self.sound.play_music('world')
    
    def enter_level(self, level_marker):
        """Enter a side-scrolling level"""
        self.current_level = Level(level_marker.level_id, level_marker.level_type)
        self.player.set_mode('level')
        self.player.reset_position(self.current_level.start_x, self.current_level.start_y)
        self.state = STATE_LEVEL
        
        # Play appropriate music
        if level_marker.level_id == 'boss':
            self.sound.play_music('boss')
        else:
            self.sound.play_music('level')
    
    def exit_level(self, completed=False):
        """Exit current level and return to world map"""
        if completed and self.current_level:
            self.world_map.complete_level(self.current_level.level_id)
            
            # Check for victory (boss defeated)
            if self.current_level.level_id == 'boss':
                self.state = STATE_VICTORY
                return
        
        # Return to world map
        start_pos = self.world_map.get_start_position()
        self.player.set_mode('world')
        self.player.reset_position(start_pos[0], start_pos[1])
        self.current_level = None
        self.state = STATE_WORLD_MAP
        self.sound.play_music('world')
    
    def handle_events(self):
        """Handle pygame events"""
        self.events = []
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            self.events.append(event)
            
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    self.handle_menu_input(event)
                elif self.state == STATE_PAUSE:
                    self.handle_pause_input(event)
                elif self.state == STATE_GAME_OVER:
                    self.handle_game_over_input(event)
                elif self.state == STATE_VICTORY:
                    self.handle_victory_input(event)
                elif event.key == pygame.K_ESCAPE:
                    if self.state == STATE_LEVEL:
                        self.state = STATE_PAUSE
                    elif self.state == STATE_WORLD_MAP:
                        self.state = STATE_MENU
    
    def handle_menu_input(self, event):
        """Handle menu navigation"""
        if self.showing_controls:
            if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                self.showing_controls = False
                self.sound.play_sound('menu')
            return
        
        if event.key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
            self.sound.play_sound('menu')
        elif event.key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
            self.sound.play_sound('menu')
        elif event.key == pygame.K_RETURN:
            self.sound.play_sound('menu')
            if self.menu_options[self.menu_selection] == 'New Game':
                self.new_game()
            elif self.menu_options[self.menu_selection] == 'Controls':
                self.showing_controls = True
            elif self.menu_options[self.menu_selection] == 'Quit':
                self.running = False
    
    def handle_pause_input(self, event):
        """Handle pause menu"""
        if event.key == pygame.K_ESCAPE:
            self.state = STATE_LEVEL
        elif event.key == pygame.K_q:
            self.exit_level(completed=False)
    
    def handle_game_over_input(self, event):
        """Handle game over screen"""
        if event.key == pygame.K_RETURN:
            self.state = STATE_MENU
            self.sound.play_music('menu')
    
    def handle_victory_input(self, event):
        """Handle victory screen"""
        if event.key == pygame.K_RETURN:
            self.state = STATE_MENU
            self.sound.play_music('menu')
    
    def update(self):
        """Update game state"""
        if self.state == STATE_WORLD_MAP:
            self.update_world_map()
        elif self.state == STATE_LEVEL:
            self.update_level()
    
    def update_world_map(self):
        """Update world map state"""
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, self.events)
        
        # Get walkable tiles
        walkable_tiles = self.world_map.get_walkable_tiles()
        self.player.update(walkable_tiles)
        
        # Update world map
        self.world_map.update(self.player)
        
        # Check for level entry
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                marker = self.world_map.get_current_level_marker(self.player.rect)
                if marker and not marker.completed:
                    self.enter_level(marker)
    
    def update_level(self):
        """Update side-scrolling level"""
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, self.events)
        
        # Get tiles for collision
        tiles = self.current_level.get_tiles()
        self.player.update(tiles)
        
        # Update level
        self.current_level.update(self.player)
        
        # Check item collection
        items_before = len(self.current_level.item_manager.items)
        self.current_level.item_manager.check_collection(self.player)
        if len(self.current_level.item_manager.items) < items_before:
            self.sound.play_sound('pickup')
        
        # Check enemy collisions
        self.check_combat()
        
        # Check if player fell in a pit
        if self.player.fell_in_pit(self.current_level.height):
            # Lose 1 health and respawn at last safe position
            self.player.health -= 1
            self.sound.play_sound('hit')
            if self.player.health <= 0:
                self.state = STATE_GAME_OVER
            else:
                self.player.respawn_at_safe_position()
                self.player.invincibility = PLAYER_INVINCIBILITY_FRAMES
        
        # Check player death
        if self.player.health <= 0:
            self.state = STATE_GAME_OVER
        
        # Check for level skip cheat (press C to complete level)
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                self.current_level.completed = True
        
        # Check level completion
        if self.current_level.completed:
            self.exit_level(completed=True)
    
    def check_combat(self):
        """Handle combat between player and enemies"""
        camera_offset = self.current_level.get_camera_offset()
        
        # Player attack
        attack_rect = self.player.get_attack_rect()
        if attack_rect:
            for enemy in self.current_level.enemies:
                if attack_rect.colliderect(enemy.rect):
                    if enemy.take_damage(1):
                        self.player.add_score(enemy.score)
                        self.sound.play_sound('enemy_death')
                    else:
                        self.sound.play_sound('hit')
        
        # Spell projectiles
        projectiles = self.player.spell_manager.get_projectiles()
        for projectile in projectiles:
            for enemy in self.current_level.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    if enemy.take_damage(projectile.damage):
                        self.player.add_score(enemy.score)
                        self.sound.play_sound('enemy_death')
                    projectile.kill()
                    break
        
        # Thunder effects
        effects = self.player.spell_manager.get_effects()
        for effect in effects:
            for enemy in self.current_level.enemies:
                if effect.can_hit(enemy):
                    if enemy.take_damage(effect.damage):
                        self.player.add_score(enemy.score)
                        self.sound.play_sound('enemy_death')
        
        # Enemy contact damage (or instant kill if invincible)
        for enemy in list(self.current_level.enemies):
            if self.player.rect.colliderect(enemy.rect):
                if self.player.invincible_mode:
                    # Invincible mode instantly eliminates enemies!
                    self.player.add_score(enemy.score)
                    enemy.kill()
                    self.sound.play_sound('enemy_death')
                else:
                    if self.player.take_damage(enemy.damage):
                        pass  # Player died
                    else:
                        self.sound.play_sound('hit')
            
            # Check boss projectiles
            if hasattr(enemy, 'projectiles'):
                for proj in list(enemy.projectiles):
                    if self.player.rect.colliderect(proj.rect):
                        if self.player.invincible_mode:
                            proj.kill()  # Destroy projectile
                        else:
                            self.player.take_damage(proj.damage)
                            proj.kill()
    
    def draw(self):
        """Draw the current game state"""
        self.screen.fill(DARK_BLUE)
        
        if self.state == STATE_MENU:
            self.draw_menu()
        elif self.state == STATE_WORLD_MAP:
            self.draw_world_map()
        elif self.state == STATE_LEVEL:
            self.draw_level()
        elif self.state == STATE_PAUSE:
            self.draw_level()  # Draw level in background
            self.ui.draw_pause(self.screen)
        elif self.state == STATE_GAME_OVER:
            if self.current_level:
                self.draw_level()
            self.ui.draw_game_over(self.screen, self.player.score if self.player else 0)
        elif self.state == STATE_VICTORY:
            self.ui.draw_victory(self.screen, self.player.score if self.player else 0)
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw main menu"""
        # Start menu music if not playing
        if self.sound.current_music != 'menu':
            self.sound.play_music('menu')
        
        # Draw title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("CHAIN", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 32)
        subtitle = subtitle_font.render("Quest for the Lost Princess", True, CYAN)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)
        
        if self.showing_controls:
            self.draw_controls_screen()
        else:
            # Draw menu options
            self.ui.draw_menu(self.screen, "", self.menu_options, self.menu_selection)
        
        # Draw decorative chain character
        from sprites import create_chain_sprite
        chain_sprite = create_chain_sprite(True, pygame.time.get_ticks() // 100)
        # Scale up for menu
        big_chain = pygame.transform.scale(chain_sprite, 
                                          (chain_sprite.get_width() * 2, 
                                           chain_sprite.get_height() * 2))
        self.screen.blit(big_chain, (100, SCREEN_HEIGHT - 200))
    
    def draw_controls_screen(self):
        """Draw controls help screen"""
        controls = [
            ("Movement", "Arrow Keys / WASD"),
            ("Jump", "Space"),
            ("Attack", "Z"),
            ("Cast Spell", "X"),
            ("Select Spell", "1, 2, 3, 4"),
            ("Interact", "Enter"),
            ("Pause", "ESC"),
        ]
        
        y = 220
        for action, key in controls:
            action_text = self.ui.font_medium.render(action + ":", True, YELLOW)
            key_text = self.ui.font_medium.render(key, True, WHITE)
            self.screen.blit(action_text, (200, y))
            self.screen.blit(key_text, (400, y))
            y += 40
        
        back_text = self.ui.font_small.render("Press ENTER or ESC to go back", True, LIGHT_GRAY)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)
    
    def draw_world_map(self):
        """Draw world map view"""
        self.world_map.draw(self.screen)
        
        # Draw player
        camera_offset = self.world_map.get_camera_offset()
        self.player.draw(self.screen, camera_offset)
        
        # Draw HUD
        location = self.world_map.get_location_name(self.player.rect)
        self.ui.draw_world_map_hud(self.screen, self.player, location)
    
    def draw_level(self):
        """Draw side-scrolling level"""
        self.current_level.draw(self.screen)
        
        # Draw player
        camera_offset = self.current_level.get_camera_offset()
        self.player.draw(self.screen, camera_offset)
        
        # Draw spell effects (projectiles, etc.)
        projectiles = self.player.spell_manager.get_projectiles()
        for proj in projectiles:
            draw_x = proj.rect.x - camera_offset[0]
            draw_y = proj.rect.y - camera_offset[1]
            self.screen.blit(proj.image, (draw_x, draw_y))
        
        effects = self.player.spell_manager.get_effects()
        for effect in effects:
            draw_x = effect.rect.x - camera_offset[0]
            draw_y = effect.rect.y - camera_offset[1]
            self.screen.blit(effect.image, (draw_x, draw_y))
        
        # Draw HUD
        self.ui.draw_hud(self.screen, self.player)
        self.ui.draw_level_name(self.screen, self.current_level.name)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
