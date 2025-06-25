
import pygame
import sys
from game import SokobanGame
from ui import GameUI
from database import Database
from sounds import SoundManager

class MainApp:
    """Application principale - Orchestrateur de génie"""
    
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Configuration de l'écran
        self.WINDOW_WIDTH = 1024
        self.WINDOW_HEIGHT = 768
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🧠 Sokoban Génie - Mode 900 IQ 🧠")
        
        # Initialisation des composants
        self.database = Database()
        self.sound_manager = SoundManager()
        self.game = SokobanGame(self.database, self.sound_manager)
        self.ui = GameUI(self.screen, self.game, self.sound_manager)
        
        # État de l'application
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
    def handle_events(self):
        """Gestion des événements - Logique d'interaction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.ui.handle_mouse_click(event.pos)
                
    def handle_keydown(self, event):
        """Gestion des touches - Intelligence de contrôle"""
        if event.key == pygame.K_ESCAPE:
            self.quit_game()
        elif event.key in [pygame.K_UP, pygame.K_w]:
            self.game.move_player('UP')
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            self.game.move_player('DOWN')
        elif event.key in [pygame.K_LEFT, pygame.K_a]:
            self.game.move_player('LEFT')
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            self.game.move_player('RIGHT')
        elif event.key == pygame.K_z and pygame.key.get_pressed()[pygame.K_LCTRL]:
            self.game.undo_move()
        elif event.key == pygame.K_r:
            self.game.reset_level()
        elif event.key == pygame.K_n:
            self.game.next_level()
        elif event.key == pygame.K_p:
            self.game.previous_level()
    
    def update(self):
        """Mise à jour logique - Cerveau du jeu"""
        self.game.update()
        
    def render(self):
        """Rendu graphique - Art du génie"""
        self.screen.fill((50, 50, 50))  # Fond sombre élégant
        self.ui.render()
        pygame.display.flip()
        
    def quit_game(self):
        """Fermeture propre - Génie organisé"""
        self.database.close()
        self.running = False
        
    def run(self):
        """Boucle principale - Le cœur battant du génie"""
        print("🧠 Démarrage du Sokoban Génie Mode 900 IQ 🧠")
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = MainApp()
    app.run() 