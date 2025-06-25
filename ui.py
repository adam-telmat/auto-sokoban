
import pygame
import time
from typing import Tuple, Optional, Dict, Any, List
from board import Board, TileType
from game import SokobanGame, GameState
from sounds import SoundManager

class Colors:
    """Palette de couleurs - Design moderne"""
    BACKGROUND = (40, 44, 52)          # Fond sombre élégant
    WALL = (85, 85, 85)                # Murs gris foncé
    FLOOR = (200, 200, 200)            # Sol clair
    FLOOR_ALT = (180, 180, 180)        # Sol alternatif (damier)
    GOAL = (100, 200, 100)             # Objectifs verts
    BOX = (139, 69, 19)                # Caisses marron
    BOX_ON_GOAL = (34, 139, 34)        # Caisse sur objectif
    PLAYER = (255, 100, 100)           # Joueur rouge
    
    # Interface
    UI_BACKGROUND = (30, 30, 30)       # Fond interface
    UI_TEXT = (255, 255, 255)          # Texte blanc
    UI_ACCENT = (100, 150, 255)        # Accent bleu
    BUTTON_NORMAL = (60, 60, 60)       # Bouton normal
    BUTTON_HOVER = (80, 80, 80)        # Bouton survolé
    BUTTON_PRESSED = (40, 40, 40)      # Bouton pressé

class Button:
    """Bouton interactif - Composant UI génie"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, font: pygame.font.Font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.pressed = False
        
    def handle_event(self, event) -> bool:
        """Gestion événements bouton"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.pressed and self.rect.collidepoint(event.pos):
                self.pressed = False
                if self.action:
                    self.action()
                return True
            self.pressed = False
        return False
    
    def render(self, screen: pygame.Surface):
        """Rendu bouton"""
        # Couleur selon état
        if self.pressed:
            color = Colors.BUTTON_PRESSED
        elif self.hovered:
            color = Colors.BUTTON_HOVER
        else:
            color = Colors.BUTTON_NORMAL
            
        # Fond bouton
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, Colors.UI_ACCENT, self.rect, 2)
        
        # Texte centré
        text_surface = self.font.render(self.text, True, Colors.UI_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class GameUI:
    """Interface utilisateur principale - Maître de l'affichage"""
    
    def __init__(self, screen: pygame.Surface, game: SokobanGame, sound_manager: SoundManager):
        self.screen = screen
        self.game = game
        self.sound_manager = sound_manager
        
        # Configuration affichage
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.tile_size = 40
        
        # Polices
        self._setup_fonts()
        
        # Boutons
        self.buttons: List[Button] = []
        self._create_buttons()
        
        # État animation
        self.animation_time = 0
        self.show_victory_animation = False
        self.victory_start_time = 0
        
        print("🎨 Interface utilisateur initialisée")
    
    def _setup_fonts(self):
        """Configuration des polices - Typographie génie"""
        pygame.font.init()
        try:
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 18)
        except:
            # Fallback si polices non disponibles
            self.font_large = pygame.font.SysFont('arial', 48)
            self.font_medium = pygame.font.SysFont('arial', 32)
            self.font_small = pygame.font.SysFont('arial', 24)
            self.font_tiny = pygame.font.SysFont('arial', 18)
    
    def _create_buttons(self):
        """Création des boutons - Interface interactive"""
        button_width = 120
        button_height = 40
        margin = 10
        start_x = self.screen_width - button_width - margin
        
        buttons_config = [
            ("Annuler", lambda: self.game.undo_move()),
            ("Reset", lambda: self.game.reset_level()),
            ("Précédent", lambda: self.game.previous_level()),
            ("Suivant", lambda: self.game.next_level()),
            ("Quitter", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)))
        ]
        
        for i, (text, action) in enumerate(buttons_config):
            y = 50 + i * (button_height + margin)
            button = Button(start_x, y, button_width, button_height, 
                          text, self.font_small, action)
            self.buttons.append(button)
    
    def handle_mouse_click(self, pos: Tuple[int, int]):
        """Gestion clics souris - Interaction intelligente"""
        # Vérifier boutons d'abord
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.action()
                self.sound_manager.play_sound('menu_select')
                return
        
        # Clic sur plateau de jeu
        if self.game.board and self.game.state == GameState.PLAYING:
            board_click_pos = self._screen_to_board_pos(pos)
            if board_click_pos:
                self._handle_board_click(board_click_pos)
    
    def _screen_to_board_pos(self, screen_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Conversion coordonnées écran -> plateau"""
        if not self.game.board:
            return None
            
        # Calcul offset pour centrer le plateau
        board_pixel_width = self.game.board.width * self.tile_size
        board_pixel_height = self.game.board.height * self.tile_size
        offset_x = (self.screen_width - 200 - board_pixel_width) // 2  # -200 pour espace boutons
        offset_y = (self.screen_height - board_pixel_height) // 2
        
        # Conversion position
        board_x = (screen_pos[0] - offset_x) // self.tile_size
        board_y = (screen_pos[1] - offset_y) // self.tile_size
        
        # Vérification limites
        if 0 <= board_x < self.game.board.width and 0 <= board_y < self.game.board.height:
            return (board_x, board_y)
        return None
    
    def _handle_board_click(self, board_pos: Tuple[int, int]):
        """Gestion clic sur le plateau - Interaction directe"""
        if not self.game.board:
            return
            
        click_x, click_y = board_pos
        player_x, player_y = self.game.board.player_pos
        
        # Calcul direction si case adjacente
        dx, dy = click_x - player_x, click_y - player_y
        
        if abs(dx) + abs(dy) == 1:  # Case adjacente
            direction = ""
            if dx == 1: direction = "RIGHT"
            elif dx == -1: direction = "LEFT"
            elif dy == 1: direction = "DOWN"
            elif dy == -1: direction = "UP"
            
            if direction:
                self.game.move_player(direction)
    
    def render(self):
        """Rendu principal - Orchestration visuelle"""
        # Fond d'écran
        self.screen.fill(Colors.BACKGROUND)
        
        # Rendu selon l'état du jeu
        if self.game.state == GameState.PLAYING:
            self._render_game()
        elif self.game.state == GameState.LEVEL_COMPLETE:
            self._render_level_complete()
        elif self.game.state == GameState.GAME_WON:
            self._render_game_won()
        elif self.game.state == GameState.PAUSED:
            self._render_paused()
        
        # Interface commune
        self._render_ui()
        self._render_buttons()
        
        # Mise à jour animation
        self.animation_time += 1
    
    def _render_game(self):
        """Rendu du jeu - Affichage principal"""
        if not self.game.board:
            return
            
        # Calcul position centrale du plateau
        board_pixel_width = self.game.board.width * self.tile_size
        board_pixel_height = self.game.board.height * self.tile_size
        offset_x = (self.screen_width - 200 - board_pixel_width) // 2
        offset_y = (self.screen_height - board_pixel_height) // 2
        
        # Rendu des tuiles
        for y in range(self.game.board.height):
            for x in range(self.game.board.width):
                tile_type = self.game.board.get_tile(x, y)
                screen_x = offset_x + x * self.tile_size
                screen_y = offset_y + y * self.tile_size
                
                self._render_tile(screen_x, screen_y, tile_type, x, y)
    
    def _render_tile(self, screen_x: int, screen_y: int, tile_type: int, board_x: int, board_y: int):
        """Rendu d'une tuile - Art pixelaire"""
        rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
        
        # Couleur de base selon le type
        if tile_type == TileType.WALL:
            color = Colors.WALL
        elif tile_type == TileType.GOAL:
            color = Colors.GOAL
        elif tile_type == TileType.BOX:
            color = Colors.BOX
        elif tile_type == TileType.PLAYER:
            # Animation du joueur
            brightness = 0.8 + 0.2 * abs(pygame.math.Vector2(0.5, 0.5).rotate(self.animation_time * 5).x)
            color = tuple(int(c * brightness) for c in Colors.PLAYER)
        elif tile_type == TileType.BOX_ON_GOAL:
            color = Colors.BOX_ON_GOAL
        else:  # EMPTY
            # Effet damier
            if (board_x + board_y) % 2 == 0:
                color = Colors.FLOOR
            else:
                color = Colors.FLOOR_ALT
        
        # Rendu tuile de base
        pygame.draw.rect(self.screen, color, rect)
        
        # Bordure pour certains éléments
        if tile_type in [TileType.WALL, TileType.BOX, TileType.BOX_ON_GOAL]:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
        
        # Effet spécial pour objectifs
        if tile_type == TileType.GOAL:
            inner_rect = pygame.Rect(screen_x + 5, screen_y + 5, 
                                   self.tile_size - 10, self.tile_size - 10)
            pygame.draw.rect(self.screen, Colors.FLOOR, inner_rect)
            pygame.draw.rect(self.screen, Colors.GOAL, inner_rect, 2)
        
        # Animation pour joueur
        if tile_type == TileType.PLAYER:
            # Petit cercle au centre
            center = (screen_x + self.tile_size // 2, screen_y + self.tile_size // 2)
            pygame.draw.circle(self.screen, (255, 255, 255), center, 3)
    
    def _render_level_complete(self):
        """Rendu fin de niveau - Célébration"""
        self._render_game()  # Garder le plateau visible
        
        # Overlay semi-transparent
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Texte de victoire
        title = self.font_large.render("🎉 NIVEAU TERMINÉ! 🎉", True, Colors.UI_TEXT)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 100))
        self.screen.blit(title, title_rect)
        
        # Statistiques
        if self.game.board:
            stats = self.game.board.get_stats()
            stats_text = [
                f"Mouvements: {stats['moves']}",
                f"Poussées: {stats['pushes']}",
                f"Efficacité: {stats['completion_percent']}%"
            ]
            
            for i, stat in enumerate(stats_text):
                text = self.font_medium.render(stat, True, Colors.UI_TEXT)
                text_rect = text.get_rect(center=(self.screen_width // 2, 
                                                self.screen_height // 2 - 20 + i * 40))
                self.screen.blit(text, text_rect)
    
    def _render_game_won(self):
        """Rendu victoire totale - Triomphe"""
        # Fond animé
        for i in range(0, self.screen_width, 20):
            color_intensity = int(128 + 127 * abs(pygame.math.Vector2(1, 0).rotate(
                self.animation_time * 2 + i * 0.1).x))
            color = (color_intensity // 3, color_intensity // 2, color_intensity)
            pygame.draw.rect(self.screen, color, (i, 0, 20, self.screen_height))
        
        # Texte principal
        title = self.font_large.render("🏆 FÉLICITATIONS! 🏆", True, Colors.UI_TEXT)
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Tous les niveaux terminés!", True, Colors.UI_TEXT)
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        self.screen.blit(subtitle, subtitle_rect)
    
    def _render_paused(self):
        """Rendu pause"""
        self._render_game()
        
        # Overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Texte pause
        pause_text = self.font_large.render("⏸️ PAUSE", True, Colors.UI_TEXT)
        pause_rect = pause_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(pause_text, pause_rect)
    
    def _render_ui(self):
        """Rendu interface utilisateur - HUD informatif"""
        # Zone information à gauche
        info_x = 10
        info_y = 10
        
        game_info = self.game.get_game_info()
        
        # Titre et niveau
        title = self.font_medium.render(f"🧠 Sokoban Génie", True, Colors.UI_TEXT)
        self.screen.blit(title, (info_x, info_y))
        
        level_text = self.font_medium.render(f"Niveau: {game_info['current_level']}/{game_info['total_levels']}", 
                                           True, Colors.UI_ACCENT)
        self.screen.blit(level_text, (info_x, info_y + 40))
        
        # Statistiques en cours
        if 'board_stats' in game_info and game_info['board_stats']:
            stats = game_info['board_stats']
            stats_texts = [
                f"Mouvements: {stats['moves']}",
                f"Poussées: {stats['pushes']}",
                f"Progression: {stats['completion_percent']}%"
            ]
            
            for i, stat_text in enumerate(stats_texts):
                text = self.font_small.render(stat_text, True, Colors.UI_TEXT)
                self.screen.blit(text, (info_x, info_y + 80 + i * 25))
        
        # Temps écoulé
        elapsed_time = game_info.get('elapsed_time', 0)
        time_text = self.font_small.render(f"Temps: {elapsed_time:.1f}s", True, Colors.UI_TEXT)
        self.screen.blit(time_text, (info_x, info_y + 170))
        
        # Meilleur score
        best_score = game_info.get('best_score', 0)
        if best_score > 0:
            score_text = self.font_small.render(f"Record: {best_score}", True, Colors.GOAL)
            self.screen.blit(score_text, (info_x, info_y + 195))
    
    def _render_buttons(self):
        """Rendu des boutons - Interface interactive"""
        for button in self.buttons:
            button.render(self.screen)
    
    def handle_events(self, events):
        """Gestion événements UI"""
        for event in events:
            # Gestion boutons
            for button in self.buttons:
                if button.handle_event(event):
                    break
            
            # Gestion survol pour sons
            if event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    was_hovered = button.hovered
                    button.hovered = button.rect.collidepoint(event.pos)
                    if button.hovered and not was_hovered:
                        self.sound_manager.play_sound('menu_navigate')
    
    def cleanup(self):
        """Nettoyage ressources UI"""
        pygame.font.quit()
        print("🎨 Interface utilisateur fermée") 