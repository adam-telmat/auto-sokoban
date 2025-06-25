
import pygame
import sys
import os
from typing import Tuple
import json

class FuturisticLauncher:
    """Lanceur futuriste pour Sokoban 3025"""
    
    def __init__(self):
        pygame.init()
        
        # Configuration écran futuriste
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("🚀 SOKOBAN 3025 - MENU FUTURISTE 🚀")
        
        # Couleurs futuristes
        self.COLORS = {
            'bg': (5, 10, 20),
            'primary': (0, 255, 255),
            'secondary': (255, 100, 255),
            'accent': (255, 255, 0),
            'success': (0, 255, 100),
            'text': (255, 255, 255),
            'highlight': (100, 200, 255)
        }
        
        # Polices
        try:
            self.font_title = pygame.font.Font(None, 72)
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_small = pygame.font.Font(None, 24)
        except:
            self.font_title = pygame.font.SysFont('arial', 72, bold=True)
            self.font_large = pygame.font.SysFont('arial', 48, bold=True)
            self.font_medium = pygame.font.SysFont('arial', 32)
            self.font_small = pygame.font.SysFont('arial', 24)
        
        # Animation
        self.animation_time = 0
        self.selected_option = 0
        
        # Menu principal
        self.main_menu_options = [
            "🚀 DÉMARRER L'AVENTURE",
            "🎯 SÉLECTIONNER NIVEAU",
            "⚙️ CONFIGURATION",
            "📊 STATISTIQUES",
            "❌ QUITTER"
        ]
        
        # Configuration par défaut
        self.config = {
            'volume_music': 0.7,
            'volume_effects': 0.8,
            'fullscreen': False,
            'difficulty': 'normal',
            'last_level': 1,
            'high_scores': []
        }
        
        self.load_config()
        
        print("🚀 Lanceur Sokoban 3025 initialisé")
        
    def load_config(self):
        """Charge la configuration"""
        try:
            if os.path.exists('sokoban_3025_config.json'):
                with open('sokoban_3025_config.json', 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
                print("✅ Configuration chargée")
        except Exception as e:
            print(f"⚠️ Erreur chargement config: {e}")
    
    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open('sokoban_3025_config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
            print("💾 Configuration sauvegardée")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde config: {e}")
    
    def render_background(self):
        """Fond propre et élégant"""
        # Dégradé simple
        for y in range(self.SCREEN_HEIGHT):
            intensity = int(15 + 10 * (y / self.SCREEN_HEIGHT))
            color = (intensity, intensity + 5, intensity + 10)
            pygame.draw.line(self.screen, color, (0, y), (self.SCREEN_WIDTH, y))
        
        # Quelques étoiles statiques pour l'ambiance
        import random
        random.seed(42)  # Étoiles fixes
        for _ in range(50):
            x = random.randint(0, self.SCREEN_WIDTH)
            y = random.randint(0, self.SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)
    
    def render_title(self):
        """Titre principal animé"""
        # Titre principal
        title = "SOKOBAN 3025"
        title_surface = self.font_title.render(title, True, self.COLORS['primary'])
        
        # Effet de glow
        glow_surface = self.font_title.render(title, True, self.COLORS['highlight'])
        
        # Position avec léger tremblement
        import math
        shake_x = 2 * math.sin(self.animation_time * 0.1)
        shake_y = 1 * math.cos(self.animation_time * 0.15)
        
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH//2 + shake_x, 120 + shake_y))
        glow_rect = glow_surface.get_rect(center=(self.SCREEN_WIDTH//2 + shake_x + 2, 120 + shake_y + 2))
        
        # Rendu avec glow
        self.screen.blit(glow_surface, glow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Sous-titre
        subtitle = "🚀 ÉDITION FUTURISTE - L'AN 3025 🚀"
        subtitle_surface = self.font_medium.render(subtitle, True, self.COLORS['accent'])
        subtitle_rect = subtitle_surface.get_rect(center=(self.SCREEN_WIDTH//2, 180))
        self.screen.blit(subtitle_surface, subtitle_rect)
    
    def render_main_menu(self):
        """Menu principal propre et cliquable"""
        menu_start_y = 300
        self.menu_buttons = []  # Pour détection clic souris
        
        for i, option in enumerate(self.main_menu_options):
            # Créer rectangle du bouton
            button_width = 400
            button_height = 50
            button_x = (self.SCREEN_WIDTH - button_width) // 2
            button_y = menu_start_y + i * 70
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            # Sauvegarder pour clic souris
            self.menu_buttons.append(button_rect)
            
            # Couleur selon sélection
            if i == self.selected_option:
                # Bouton sélectionné
                pygame.draw.rect(self.screen, self.COLORS['highlight'], button_rect)
                pygame.draw.rect(self.screen, self.COLORS['primary'], button_rect, 3)
                color = self.COLORS['bg']
                font = self.font_large
            else:
                # Bouton normal
                pygame.draw.rect(self.screen, (40, 45, 55), button_rect)
                pygame.draw.rect(self.screen, self.COLORS['text'], button_rect, 2)
                color = self.COLORS['text']
                font = self.font_medium
            
            # Texte centré dans le bouton
            option_surface = font.render(option, True, color)
            option_rect = option_surface.get_rect(center=button_rect.center)
            self.screen.blit(option_surface, option_rect)
        
        # Instructions
        instructions = [
            "🖱️ CLIC SOURIS ou FLÈCHES + ENTRÉE",
            "🎮 En jeu: Clavier uniquement",
            "ÉCHAP: Retour/Sortie"
        ]
        
        instruction_y = self.SCREEN_HEIGHT - 100
        for i, instruction in enumerate(instructions):
            instruction_surface = self.font_small.render(instruction, True, self.COLORS['text'])
            instruction_rect = instruction_surface.get_rect(center=(self.SCREEN_WIDTH//2, instruction_y + i * 20))
            self.screen.blit(instruction_surface, instruction_rect)
    
    def render_level_select(self):
        """Sélection de niveau"""
        # Titre
        title = "🎯 SÉLECTION DE NIVEAU FUTURISTE 🎯"
        title_surface = self.font_large.render(title, True, self.COLORS['primary'])
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Grille de niveaux
        levels_per_row = 5
        level_size = 80
        spacing = 20
        start_x = (self.SCREEN_WIDTH - (levels_per_row * level_size + (levels_per_row - 1) * spacing)) // 2
        start_y = 200
        
        for level in range(1, 26):  # 25 niveaux
            row = (level - 1) // levels_per_row
            col = (level - 1) % levels_per_row
            
            x = start_x + col * (level_size + spacing)
            y = start_y + row * (level_size + spacing)
            
            level_rect = pygame.Rect(x, y, level_size, level_size)
            
            # Couleur selon statut - TOUS LES NIVEAUX DÉBLOQUÉS POUR TESTS
            if level <= self.config['last_level']:
                # Niveau déjà joué
                color = self.COLORS['success']
                text_color = self.COLORS['bg']
            else:
                # Tous les autres niveaux accessibles pour tests
                color = self.COLORS['accent']
                text_color = self.COLORS['bg']
            
            # Dessin du niveau
            pygame.draw.rect(self.screen, color, level_rect)
            pygame.draw.rect(self.screen, self.COLORS['text'], level_rect, 2)
            
            # Numéro du niveau
            level_text = str(level)
            level_surface = self.font_medium.render(level_text, True, text_color)
            level_text_rect = level_surface.get_rect(center=level_rect.center)
            self.screen.blit(level_surface, level_text_rect)
        
        # Instructions
        instruction = "🔓 TOUS LES NIVEAUX DÉBLOQUÉS - CLIC POUR COMMENCER - ÉCHAP POUR RETOUR"
        instruction_surface = self.font_small.render(instruction, True, self.COLORS['accent'])
        instruction_rect = instruction_surface.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT - 50))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def render_config(self):
        """Menu de configuration"""
        title = "⚙️ CONFIGURATION FUTURISTE ⚙️"
        title_surface = self.font_large.render(title, True, self.COLORS['primary'])
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        config_y = 200
        configs = [
            f"Volume Musique: {int(self.config['volume_music'] * 100)}%",
            f"Volume Effets: {int(self.config['volume_effects'] * 100)}%",
            f"Plein Écran: {'OUI' if self.config['fullscreen'] else 'NON'}",
            f"Difficulté: {self.config['difficulty'].upper()}",
            "RETOUR"
        ]
        
        for i, config_text in enumerate(configs):
            color = self.COLORS['highlight'] if i == self.selected_option else self.COLORS['text']
            font = self.font_large if i == self.selected_option else self.font_medium
            
            config_surface = font.render(config_text, True, color)
            config_rect = config_surface.get_rect(center=(self.SCREEN_WIDTH//2, config_y + i * 50))
            self.screen.blit(config_surface, config_rect)
    
    def render_stats(self):
        """Affichage des statistiques"""
        title = "📊 STATISTIQUES FUTURISTES 📊"
        title_surface = self.font_large.render(title, True, self.COLORS['primary'])
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH//2, 100))
        self.screen.blit(title_surface, title_rect)
        
        stats_y = 200
        stats = [
            f"Dernier Niveau Atteint: {self.config['last_level']}/25",
            f"Progression: {int((self.config['last_level']/25)*100)}%",
            f"Meilleurs Scores: {len(self.config['high_scores'])} enregistrés",
            "",
            "RETOUR"
        ]
        
        for i, stat_text in enumerate(stats):
            if stat_text == "":
                continue
                
            color = self.COLORS['highlight'] if stat_text == "RETOUR" else self.COLORS['text']
            stat_surface = self.font_medium.render(stat_text, True, color)
            stat_rect = stat_surface.get_rect(center=(self.SCREEN_WIDTH//2, stats_y + i * 40))
            self.screen.blit(stat_surface, stat_rect)
    
    def handle_main_menu(self, event):
        """Gestion menu principal avec souris + clavier"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.main_menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.main_menu_options)
            elif event.key == pygame.K_RETURN:
                return self.execute_menu_option()
        
        elif event.type == pygame.MOUSEMOTION:
            # Détection survol souris
            if hasattr(self, 'menu_buttons'):
                mouse_pos = event.pos
                for i, button_rect in enumerate(self.menu_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        self.selected_option = i
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Clic souris
            if hasattr(self, 'menu_buttons'):
                mouse_pos = event.pos
                for i, button_rect in enumerate(self.menu_buttons):
                    if button_rect.collidepoint(mouse_pos):
                        self.selected_option = i
                        return self.execute_menu_option()
        
        return 'main_menu'
    
    def execute_menu_option(self):
        """Exécute l'option sélectionnée"""
        option = self.main_menu_options[self.selected_option]
        
        if "DÉMARRER" in option:
            return 'start_game'
        elif "SÉLECTIONNER" in option:
            return 'level_select'
        elif "CONFIGURATION" in option:
            self.selected_option = 0
            return 'config'
        elif "STATISTIQUES" in option:
            return 'stats'
        elif "QUITTER" in option:
            return 'quit'
        
        return 'main_menu'
    
    def handle_level_select(self, event):
        """Gestion sélection niveau"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'main_menu'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Calcul du niveau cliqué
            levels_per_row = 5
            level_size = 80
            spacing = 20
            start_x = (self.SCREEN_WIDTH - (levels_per_row * level_size + (levels_per_row - 1) * spacing)) // 2
            start_y = 200
            
            mouse_x, mouse_y = event.pos
            
            for level in range(1, 26):
                row = (level - 1) // levels_per_row
                col = (level - 1) % levels_per_row
                
                x = start_x + col * (level_size + spacing)
                y = start_y + row * (level_size + spacing)
                
                level_rect = pygame.Rect(x, y, level_size, level_size)
                
                if level_rect.collidepoint(mouse_x, mouse_y):
                    # TOUS LES NIVEAUX ACCESSIBLES POUR TESTS
                    return ('start_level', level)
        
        return 'level_select'
    
    def handle_config(self, event):
        """Gestion configuration"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.save_config()
                return 'main_menu'
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 5
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 5
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 4:  # RETOUR
                    self.save_config()
                    return 'main_menu'
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.modify_config(event.key == pygame.K_RIGHT)
        
        return 'config'
    
    def modify_config(self, increase: bool):
        """Modifie une option de configuration"""
        if self.selected_option == 0:  # Volume musique
            delta = 0.1 if increase else -0.1
            self.config['volume_music'] = max(0, min(1, self.config['volume_music'] + delta))
        elif self.selected_option == 1:  # Volume effets
            delta = 0.1 if increase else -0.1
            self.config['volume_effects'] = max(0, min(1, self.config['volume_effects'] + delta))
        elif self.selected_option == 2:  # Plein écran
            self.config['fullscreen'] = not self.config['fullscreen']
        elif self.selected_option == 3:  # Difficulté
            difficulties = ['facile', 'normal', 'difficile', 'extreme']
            current_idx = difficulties.index(self.config['difficulty'])
            if increase:
                current_idx = (current_idx + 1) % len(difficulties)
            else:
                current_idx = (current_idx - 1) % len(difficulties)
            self.config['difficulty'] = difficulties[current_idx]
    
    def run(self):
        """Boucle principale du lanceur"""
        clock = pygame.time.Clock()
        current_screen = 'main_menu'
        
        print("🚀 Lancement du menu futuriste")
        
        running = True
        while running:
            self.animation_time += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if current_screen == 'main_menu':
                        running = False
                    else:
                        current_screen = 'main_menu'
                        self.selected_option = 0
                else:
                    # Gestion selon l'écran actuel
                    if current_screen == 'main_menu':
                        result = self.handle_main_menu(event)
                        if result == 'start_game':
                            self.launch_game()
                            # Retour au menu après le jeu au lieu de return
                            current_screen = 'main_menu'
                            self.selected_option = 0
                        elif result == 'quit':
                            running = False
                        elif result != 'main_menu':
                            current_screen = result
                    
                    elif current_screen == 'level_select':
                        result = self.handle_level_select(event)
                        if isinstance(result, tuple) and result[0] == 'start_level':
                            self.launch_game(result[1])
                            # Retour au menu après le jeu au lieu de return  
                            current_screen = 'main_menu'
                            self.selected_option = 0
                        elif result != 'level_select':
                            current_screen = result
                    
                    elif current_screen == 'config':
                        result = self.handle_config(event)
                        if result != 'config':
                            current_screen = result
                    
                    elif current_screen == 'stats':
                        if event.type == pygame.KEYDOWN:
                            current_screen = 'main_menu'
            
            # Rendu
            self.render_background()
            self.render_title()
            
            if current_screen == 'main_menu':
                self.render_main_menu()
            elif current_screen == 'level_select':
                self.render_level_select()
            elif current_screen == 'config':
                self.render_config()
            elif current_screen == 'stats':
                self.render_stats()
            
            pygame.display.flip()
            clock.tick(60)
        
        self.save_config()
        pygame.quit()
        sys.exit()
    
    def launch_game(self, start_level: int = 1):
        """Lance le jeu principal"""
        try:
            print(f"🚀 Lancement de Sokoban 3025 - Niveau {start_level}")
            
            # Import et lancement du jeu
            from sokoban_3025 import Sokoban3025
            
            game = Sokoban3025()
            if start_level > 1:
                game.load_level(start_level)
            game.run()
            
            # Réinitialiser l'écran du launcher après retour du jeu
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption("🚀 SOKOBAN 3025 - MENU FUTURISTE 🚀")
            
            print("🔙 Retour au menu principal")
            
        except ImportError as e:
            print(f"❌ Erreur import du jeu: {e}")
            print("Veuillez vous assurer que sokoban_3025.py est présent")
        except Exception as e:
            print(f"❌ Erreur lancement: {e}")

if __name__ == "__main__":
    launcher = FuturisticLauncher()
    launcher.run() 