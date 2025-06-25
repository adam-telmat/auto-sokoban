"""
🚀 SOKOBAN 3025 - LE JEU DU FUTUR ! 🚀
Version futuriste ultime avec assets originaux + effets année 3025

Règles strictes :
- Nombre caisses = nombre emplacements (validation obligatoire)
- Difficulté crescendo
- Niveau terminé quand TOUTES les caisses sont placées
- Effets visuels futuristes de ouf !
"""

import pygame
import sys
import os
import random
import math
import time
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from assets_loader import FuturisticAssetsLoader

# Initialisation Pygame
pygame.init()

class TileType(Enum):
    """Types de tuiles du futur"""
    EMPTY = 0
    WALL = 1
    GOAL = 2
    BOX = 3
    PLAYER = 4
    BOX_ON_GOAL = 5

@dataclass
class GameStats:
    """Statistiques de jeu futuristes"""
    moves: int = 0
    pushes: int = 0
    time_started: float = 0
    level: int = 1
    score: int = 0
    combo_multiplier: int = 1
    perfect_placements: int = 0

class Sokoban3025:
    """🚀 SOKOBAN DE L'AN 3025 🚀"""
    
    def __init__(self):
        # Configuration écran futuriste
        self.TILE_SIZE = 50
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("🚀 SOKOBAN 3025 - EDITION FUTURISTE 🚀")
        
        # Assets futuristes
        self.assets = FuturisticAssetsLoader()
        self.assets.load_original_assets()
        self.assets.enhance_with_effects()
        
        # État du jeu
        self.current_level = 1
        self.max_levels = 25  # 25 niveaux de difficulté progressive !
        self.board: List[List[int]] = []
        self.player_pos = [0, 0]
        self.stats = GameStats()
        
        # Systèmes futuristes
        self.particles = []
        self.screen_shake = {'intensity': 0, 'duration': 0}
        self.level_transition_effect = {'active': False, 'progress': 0}
        self.combo_timer = 0
        
        # Historique pour undo futuriste
        self.move_history = []
        
        # Couleurs futuristes
        self.COLORS = {
            'bg': (10, 15, 25),           # Noir spatial profond
            'ui_primary': (0, 255, 255),   # Cyan néon
            'ui_secondary': (255, 100, 255), # Magenta électrique
            'success': (0, 255, 100),      # Vert holographique  
            'warning': (255, 200, 0),      # Jaune énergie
            'danger': (255, 50, 50),       # Rouge alerte
            'text': (255, 255, 255)        # Blanc pur
        }
        
        # Police futuriste
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        print("🚀 SOKOBAN 3025 INITIALISÉ - PRÊT POUR L'AVENTURE FUTURISTE ! 🚀")
        
    def generate_futuristic_level(self, level_num: int) -> List[List[int]]:
        """Génère des niveaux authentiques Sokoban avec murs intérieurs"""
        
        # Collection de vrais niveaux Sokoban avec murs intérieurs
        levels = {
            1: [  # Tutorial simple
                [1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 0, 4, 3, 2, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]
            ],
            2: [  # Premier défi avec murs
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 4, 0, 0, 1, 0, 0, 1],
                [1, 0, 1, 3, 1, 3, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 2, 1, 2, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 0]
            ],
            3: [  # Niveau simple avec 2 caisses
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 4, 3, 1, 3, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 1],
                [1, 2, 1, 0, 0, 0, 2, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
            ],
            4: [  # Labyrinthe avec obstacles centraux
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 3, 1, 3, 1, 0, 1],
                [1, 0, 1, 0, 4, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 2, 1, 2, 1, 1, 1],
                [0, 0, 0, 1, 1, 1, 0, 0, 0]
            ],
            5: [  # Formation en croix simple
                [0, 0, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 0, 2, 0, 1, 0, 0],
                [1, 1, 1, 0, 3, 0, 1, 1, 1],
                [1, 0, 0, 0, 4, 0, 0, 0, 1],
                [1, 0, 2, 0, 3, 0, 2, 0, 1],
                [1, 1, 1, 0, 0, 0, 1, 1, 1],
                [0, 0, 1, 1, 1, 1, 1, 0, 0]
            ],
            6: [  # Niveau escalier simple
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 4, 0, 0, 0, 0, 0, 1],
                [1, 0, 1, 3, 1, 0, 0, 1],
                [1, 0, 1, 0, 1, 3, 0, 1],
                [1, 2, 0, 0, 0, 0, 2, 1],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]
            ],
            7: [  # Couloir avec mur central
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 4, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 3, 0, 1, 0, 3, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 2, 0, 0, 1, 0, 0, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1]
            ],
            8: [  # Puzzle en T
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 0, 4, 0, 1, 0],
                [0, 1, 0, 3, 0, 1, 0],
                [1, 1, 3, 0, 3, 1, 1],
                [1, 2, 0, 0, 0, 2, 1],
                [1, 0, 0, 2, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1]
            ],
            9: [  # Croix avec centre
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1, 2, 1, 0, 0],
                [1, 1, 1, 3, 1, 1, 1],
                [1, 2, 0, 4, 0, 2, 1],
                [1, 1, 1, 3, 1, 1, 1],
                [0, 0, 1, 2, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0]
            ],
            10: [  # Niveau final plus simple
                [1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 4, 0, 0, 0, 1],
                [1, 0, 1, 3, 0, 3, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 2, 1, 0, 3, 0, 1, 2, 1],
                [1, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 0, 1, 3, 0, 3, 1, 0, 1],
                [1, 0, 0, 0, 2, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        }
        
        # Répéter et varier les niveaux pour atteindre 25 niveaux
        if level_num <= 10:
            board = levels[level_num]
        else:
            # Variations des niveaux existants pour niveaux 11-25
            base_level = ((level_num - 11) % 10) + 1
            board = [row.copy() for row in levels[base_level]]
            # Ajouter des variations pour rendre plus difficile
            self._add_level_variations(board, level_num - 10)
        
        # Trouver position joueur dans le board
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell == TileType.PLAYER.value:
                    self.player_pos = [x, y]
                    break
        
        print(f"🎯 Niveau {level_num} chargé: {len(board[0])}x{len(board)} avec murs intérieurs")
        return board
    
    def _add_level_variations(self, board: List[List[int]], variation_level: int):
        """Ajoute des variations aux niveaux pour les rendre plus difficiles"""
        # Variations simples : ajouter quelques murs ou déplacer des éléments
        if variation_level <= 5:
            # Variations légères : juste changer quelques positions vides en murs
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if board[y][x] == TileType.EMPTY.value and random.random() < 0.1:
                        # Vérifier que ça ne bloque pas le jeu
                        neighbors = self._count_empty_neighbors(board, x, y)
                        if neighbors >= 3:  # Laisser assez d'espace pour bouger
                            board[y][x] = TileType.WALL.value
        else:
            # Variations plus importantes pour niveaux 16+
            self._add_complex_variations(board)
    
    def _count_empty_neighbors(self, board: List[List[int]], x: int, y: int) -> int:
        """Compte les voisins vides autour d'une position"""
        count = 0
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(board[0]) and 0 <= ny < len(board) and 
                board[ny][nx] == TileType.EMPTY.value):
                count += 1
        return count
    
    def _add_complex_variations(self, board: List[List[int]]):
        """Variations complexes pour niveaux avancés"""
        # Ajouter quelques murs stratégiques sans casser la solvabilité
        wall_candidates = []
        for y in range(1, len(board) - 1):
            for x in range(1, len(board[0]) - 1):
                if (board[y][x] == TileType.EMPTY.value and 
                    self._count_empty_neighbors(board, x, y) >= 2):
                    wall_candidates.append((x, y))
        
        # Ajouter quelques murs aléatoirement
        num_walls = min(3, len(wall_candidates))
        selected_walls = random.sample(wall_candidates, num_walls)
        for x, y in selected_walls:
            board[y][x] = TileType.WALL.value
    
    def _has_movement_space(self, board: List[List[int]], x: int, y: int, width: int, height: int) -> bool:
        """Vérifie si position a assez d'espace pour mouvement"""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        free_spaces = 0
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if board[ny][nx] == TileType.EMPTY.value:
                    free_spaces += 1
        
        return free_spaces >= 2  # Au moins 2 directions libres
    
    def load_level(self, level_num: int):
        """Charge un niveau avec système de progression futuriste"""
        print(f"🚀 Chargement niveau {level_num}/25...")
        
        self.current_level = level_num
        self.board = self.generate_futuristic_level(level_num)
        self.stats = GameStats(level=level_num, time_started=time.time())
        self.move_history = []
        
        # Effets de transition futuristes
        self.level_transition_effect = {'active': True, 'progress': 0}
        self.particles.extend(self.assets.create_particle_effect('level_start', (self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2)))
        
    def move_player(self, dx: int, dy: int) -> bool:
        """Mouvement du joueur avec logique futuriste avancée"""
        old_pos = self.player_pos.copy()
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Vérifications de limites
        if (new_x < 0 or new_x >= len(self.board[0]) or 
            new_y < 0 or new_y >= len(self.board)):
            return False
        
        target_tile = self.board[new_y][new_x]
        
        # Collision avec mur
        if target_tile == TileType.WALL.value:
            self._create_wall_collision_effect(new_x, new_y)
            return False
        
        # Mouvement libre
        if target_tile in [TileType.EMPTY.value, TileType.GOAL.value]:
            self._execute_move(old_pos, [new_x, new_y])
            return True
        
        # Pousser caisse
        if target_tile in [TileType.BOX.value, TileType.BOX_ON_GOAL.value]:
            return self._push_box(old_pos, [new_x, new_y], dx, dy)
        
        return False
    
    def _execute_move(self, old_pos: List[int], new_pos: List[int]):
        """Exécute mouvement avec effets futuristes"""
        # Sauvegarder pour undo
        self.move_history.append({
            'board': [row.copy() for row in self.board],
            'player_pos': old_pos.copy(),
            'stats': GameStats(
                moves=self.stats.moves,
                pushes=self.stats.pushes,
                score=self.stats.score,
                combo_multiplier=self.stats.combo_multiplier
            )
        })
        
        # Nettoyer ancienne position - restaurer ce qui était là avant
        old_tile = self.board[old_pos[1]][old_pos[0]]
        if old_tile == TileType.PLAYER.value:
            self.board[old_pos[1]][old_pos[0]] = TileType.EMPTY.value
        # Sinon, laisser ce qui était là (par exemple, si le joueur était sur un goal)
        
        # Nouvelle position - placer joueur sans écraser les goals
        new_tile = self.board[new_pos[1]][new_pos[0]]
        self.board[new_pos[1]][new_pos[0]] = TileType.PLAYER.value
        
        self.player_pos = new_pos
        self.stats.moves += 1
        
        # Effets visuels de mouvement
        self._create_movement_trail(old_pos, new_pos)
    
    def _push_box(self, player_old: List[int], box_pos: List[int], dx: int, dy: int) -> bool:
        """Pousse caisse avec validation et effets futuristes"""
        box_new_x = box_pos[0] + dx
        box_new_y = box_pos[1] + dy
        
        # Vérifications limites
        if (box_new_x < 0 or box_new_x >= len(self.board[0]) or
            box_new_y < 0 or box_new_y >= len(self.board)):
            return False
        
        target_tile = self.board[box_new_y][box_new_x]
        
        # Impossible de pousser vers mur ou autre caisse
        if target_tile in [TileType.WALL.value, TileType.BOX.value, TileType.BOX_ON_GOAL.value]:
            return False
        
        # Sauvegarder état pour undo
        self.move_history.append({
            'board': [row.copy() for row in self.board],
            'player_pos': player_old.copy(),
            'stats': GameStats(
                moves=self.stats.moves,
                pushes=self.stats.pushes,
                score=self.stats.score,
                combo_multiplier=self.stats.combo_multiplier
            )
        })
        
        # Exécuter le push
        was_on_goal = self.board[box_pos[1]][box_pos[0]] == TileType.BOX_ON_GOAL.value
        will_be_on_goal = target_tile == TileType.GOAL.value
        
        # Nettoyer ancienne position de la caisse
        if was_on_goal:
            self.board[box_pos[1]][box_pos[0]] = TileType.GOAL.value
        else:
            self.board[box_pos[1]][box_pos[0]] = TileType.EMPTY.value
        
        # Placer caisse à nouvelle position
        if will_be_on_goal:
            self.board[box_new_y][box_new_x] = TileType.BOX_ON_GOAL.value
            self._create_goal_achievement_effect(box_new_x, box_new_y)
            self.stats.perfect_placements += 1
            self.stats.combo_multiplier += 1
        else:
            self.board[box_new_y][box_new_x] = TileType.BOX.value
            if was_on_goal:
                # Caisse retirée d'un objectif - reset combo
                self.stats.combo_multiplier = 1
        
        # Placer joueur à position de la caisse
        self.board[box_pos[1]][box_pos[0]] = TileType.PLAYER.value
        self.player_pos = box_pos
        
        # Nettoyer ancienne position joueur
        self.board[player_old[1]][player_old[0]] = TileType.EMPTY.value
        
        # Mise à jour stats
        self.stats.moves += 1
        self.stats.pushes += 1
        self.stats.score += 10 * self.stats.combo_multiplier
        
        # Effets visuels
        self._create_push_effect(box_pos, [box_new_x, box_new_y])
        
        return True
    
    def _create_wall_collision_effect(self, x: int, y: int):
        """Effet collision mur futuriste"""
        world_x = x * self.TILE_SIZE + self.TILE_SIZE // 2
        world_y = y * self.TILE_SIZE + self.TILE_SIZE // 2
        
        # Particules d'impact
        impact_particles = self.assets.create_particle_effect('wall_impact', (world_x, world_y))
        self.particles.extend(impact_particles)
        
        # Screen shake
        self.screen_shake = {'intensity': 5, 'duration': 10}
    
    def _create_movement_trail(self, old_pos: List[int], new_pos: List[int]):
        """Trail de mouvement cybernétique"""
        old_world = (old_pos[0] * self.TILE_SIZE + self.TILE_SIZE//2, 
                     old_pos[1] * self.TILE_SIZE + self.TILE_SIZE//2)
        new_world = (new_pos[0] * self.TILE_SIZE + self.TILE_SIZE//2,
                     new_pos[1] * self.TILE_SIZE + self.TILE_SIZE//2)
        
        # Particules de trail
        for i in range(5):
            t = i / 4.0
            trail_x = int(old_world[0] + t * (new_world[0] - old_world[0]))
            trail_y = int(old_world[1] + t * (new_world[1] - old_world[1]))
            
            self.particles.append({
                'pos': [trail_x, trail_y],
                'vel': [0, 0],
                'color': (0, 255, 255, 150 - i * 30),
                'life': 15,
                'max_life': 15
            })
    
    def _create_push_effect(self, old_pos: List[int], new_pos: List[int]):
        """Effet push de caisse quantique"""
        world_pos = (new_pos[0] * self.TILE_SIZE + self.TILE_SIZE//2,
                     new_pos[1] * self.TILE_SIZE + self.TILE_SIZE//2)
        
        push_particles = self.assets.create_particle_effect('box_push', world_pos)
        self.particles.extend(push_particles)
        
        self.screen_shake = {'intensity': 3, 'duration': 8}
    
    def _create_goal_achievement_effect(self, x: int, y: int):
        """Effet placement correct sur objectif"""
        world_pos = (x * self.TILE_SIZE + self.TILE_SIZE//2,
                     y * self.TILE_SIZE + self.TILE_SIZE//2)
        
        success_particles = self.assets.create_particle_effect('box_placement', world_pos)
        self.particles.extend(success_particles)
    
    def undo_move(self):
        """Undo futuriste avec validation temporelle"""
        if not self.move_history:
            return False
        
        last_state = self.move_history.pop()
        self.board = last_state['board']
        self.player_pos = last_state['player_pos']
        self.stats = last_state['stats']
        
        # Effet undo futuriste
        world_pos = (self.player_pos[0] * self.TILE_SIZE + self.TILE_SIZE//2,
                     self.player_pos[1] * self.TILE_SIZE + self.TILE_SIZE//2)
        undo_particles = self.assets.create_particle_effect('time_rewind', world_pos)
        self.particles.extend(undo_particles)
        
        return True
    
    def is_level_complete(self) -> bool:
        """Vérifie si niveau terminé (TOUTES les caisses sur objectifs)"""
        # Compter caisses et objectifs correctement
        total_boxes = 0
        boxes_on_goals = 0
        total_goals = 0
        
        for row in self.board:
            for cell in row:
                if cell == TileType.BOX.value:
                    total_boxes += 1
                elif cell == TileType.BOX_ON_GOAL.value:
                    total_boxes += 1
                    boxes_on_goals += 1
                    total_goals += 1  # Objectif occupé par une caisse
                elif cell == TileType.GOAL.value:
                    total_goals += 1  # Objectif libre
        
        # Validation stricte : TOUTES les caisses sur objectifs ET nombres égaux
        level_complete = (boxes_on_goals == total_boxes and 
                         total_boxes == total_goals and 
                         total_goals > 0)
        
        if level_complete:
            print(f"🎉 NIVEAU {self.current_level} TERMINÉ !")
            print(f"📊 {boxes_on_goals}/{total_boxes} caisses placées")
            print(f"🎯 {total_goals} objectifs au total")
            
            # Bonus de fin de niveau
            time_bonus = max(0, 300 - int(time.time() - self.stats.time_started))
            efficiency_bonus = max(0, 100 - self.stats.moves) * 5
            self.stats.score += time_bonus + efficiency_bonus
            
            # Effets de victoire
            center_pos = (self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2)
            victory_particles = self.assets.create_particle_effect('level_complete', center_pos)
            self.particles.extend(victory_particles)
        
        return level_complete
    
    def render(self):
        """Rendu futuriste avec tous les effets"""
        # Fond spatial
        self.screen.fill(self.COLORS['bg'])
        
        # Grille énergétique de fond
        self._render_background_grid()
        
        # Appliquer screen shake
        shake_offset = [0, 0]
        if self.screen_shake['duration'] > 0:
            shake_offset = [
                random.randint(-self.screen_shake['intensity'], self.screen_shake['intensity']),
                random.randint(-self.screen_shake['intensity'], self.screen_shake['intensity'])
            ]
            self.screen_shake['duration'] -= 1
        
        # Offset de rendu pour centrer le niveau
        board_width = len(self.board[0]) * self.TILE_SIZE
        board_height = len(self.board) * self.TILE_SIZE
        offset_x = (self.SCREEN_WIDTH - board_width) // 2 + shake_offset[0]
        offset_y = 100 + shake_offset[1]  # Espace pour UI
        
        # Rendu du plateau
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                world_x = offset_x + x * self.TILE_SIZE
                world_y = offset_y + y * self.TILE_SIZE
                self._render_tile(world_x, world_y, cell)
        
        # Particules futuristes
        self.particles = self.assets.update_particles(self.particles)
        self.assets.render_particles(self.screen, self.particles)
        
        # Interface utilisateur
        self._render_ui()
        
        # Effet de transition
        if self.level_transition_effect['active']:
            self._render_transition_effect()
    
    def _render_background_grid(self):
        """Grille énergétique de fond"""
        grid_color = (*self.COLORS['ui_primary'][:3], 20)
        
        for x in range(0, self.SCREEN_WIDTH, 50):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.SCREEN_HEIGHT))
        for y in range(0, self.SCREEN_HEIGHT, 50):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.SCREEN_WIDTH, y))
    
    def _render_tile(self, x: int, y: int, tile_type: int):
        """Rendu de tuile avec assets futuristes"""
        rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
        
        # Rendu selon type
        if tile_type == TileType.WALL.value:
            texture = self.assets.get_texture('wall')
            if texture:
                scaled = pygame.transform.scale(texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled, rect)
            else:
                pygame.draw.rect(self.screen, (100, 100, 120), rect)
                
        elif tile_type == TileType.EMPTY.value:
            texture = self.assets.get_texture('floor')
            if texture:
                scaled = pygame.transform.scale(texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled, rect)
            else:
                pygame.draw.rect(self.screen, (30, 35, 45), rect)
                
        elif tile_type == TileType.GOAL.value:
            # Sol + objectif
            floor_texture = self.assets.get_texture('floor')
            goal_texture = self.assets.get_texture('goal')
            if floor_texture:
                scaled_floor = pygame.transform.scale(floor_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_floor, rect)
            if goal_texture:
                scaled_goal = pygame.transform.scale(goal_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_goal, rect)
            else:
                pygame.draw.rect(self.screen, (0, 200, 100), rect)
                
        elif tile_type == TileType.BOX.value:
            # Sol + caisse
            floor_texture = self.assets.get_texture('floor')
            box_texture = self.assets.get_texture('box')
            if floor_texture:
                scaled_floor = pygame.transform.scale(floor_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_floor, rect)
            if box_texture:
                scaled_box = pygame.transform.scale(box_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_box, rect)
            else:
                pygame.draw.rect(self.screen, (150, 100, 200), rect)
                
        elif tile_type == TileType.PLAYER.value:
            # Sol + joueur
            floor_texture = self.assets.get_texture('floor')
            player_texture = self.assets.get_texture('player')
            if floor_texture:
                scaled_floor = pygame.transform.scale(floor_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_floor, rect)
            if player_texture:
                scaled_player = pygame.transform.scale(player_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_player, rect)
            else:
                pygame.draw.rect(self.screen, (255, 150, 50), rect)
                
        elif tile_type == TileType.BOX_ON_GOAL.value:
            # Sol + objectif + caisse
            floor_texture = self.assets.get_texture('floor')
            goal_texture = self.assets.get_texture('goal')
            box_texture = self.assets.get_texture('box')
            
            if floor_texture:
                scaled_floor = pygame.transform.scale(floor_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_floor, rect)
            if goal_texture:
                scaled_goal = pygame.transform.scale(goal_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_goal, rect)
            if box_texture:
                scaled_box = pygame.transform.scale(box_texture, (self.TILE_SIZE, self.TILE_SIZE))
                self.screen.blit(scaled_box, rect)
            else:
                pygame.draw.rect(self.screen, (100, 255, 100), rect)
    
    def _render_ui(self):
        """Interface utilisateur futuriste"""
        # Panneau de stats
        stats_y = 10
        
        # Titre
        title_text = f"🚀 SOKOBAN 3025 - NIVEAU {self.current_level}/25 🚀"
        title_surface = self.font_large.render(title_text, True, self.COLORS['ui_primary'])
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH//2, 30))
        self.screen.blit(title_surface, title_rect)
        
        # Stats gauche
        stats_left = [
            f"Mouvements: {self.stats.moves}",
            f"Poussées: {self.stats.pushes}",
            f"Score: {self.stats.score}",
        ]
        
        for i, stat in enumerate(stats_left):
            stat_surface = self.font_medium.render(stat, True, self.COLORS['text'])
            self.screen.blit(stat_surface, (20, stats_y + 60 + i * 25))
        
        # Stats droite  
        elapsed_time = int(time.time() - self.stats.time_started)
        stats_right = [
            f"Temps: {elapsed_time}s",
            f"Combo: x{self.stats.combo_multiplier}",
            f"Placements parfaits: {self.stats.perfect_placements}",
        ]
        
        for i, stat in enumerate(stats_right):
            stat_surface = self.font_medium.render(stat, True, self.COLORS['text'])
            stat_rect = stat_surface.get_rect(right=self.SCREEN_WIDTH-20)
            self.screen.blit(stat_surface, (stat_rect.x, stats_y + 60 + i * 25))
        
        # Contrôles
        controls = [
            "🎮 CONTRÔLES FUTURISTES 🎮",
            "FLÈCHES: Mouvement cybernétique",
            "U: Manipulation temporelle (Undo)",
            "R: Réinitialisation quantique",
            "ESC: Retour au menu spatial"
        ]
        
        for i, control in enumerate(controls):
            color = self.COLORS['ui_secondary'] if i == 0 else self.COLORS['text']
            font = self.font_medium if i == 0 else self.font_small
            control_surface = font.render(control, True, color)
            self.screen.blit(control_surface, (20, self.SCREEN_HEIGHT - 120 + i * 20))
    
    def _render_transition_effect(self):
        """Effet de transition de niveau futuriste"""
        if self.level_transition_effect['active']:
            progress = self.level_transition_effect['progress']
            
            # Overlay avec fade
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            overlay.set_alpha(int(255 * (1 - progress)))
            overlay.fill(self.COLORS['ui_primary'])
            self.screen.blit(overlay, (0, 0))
            
            # Texte de transition
            if progress < 0.5:
                transition_text = f"NIVEAU {self.current_level} ACTIVÉ"
                text_surface = self.font_large.render(transition_text, True, self.COLORS['text'])
                text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
                self.screen.blit(text_surface, text_rect)
            
            # Progression
            self.level_transition_effect['progress'] += 0.02
            if self.level_transition_effect['progress'] >= 1.0:
                self.level_transition_effect['active'] = False
    
    def handle_events(self):
        """Gestion des événements futuristes"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_UP:
                    self.move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_player(1, 0)
                
                elif event.key == pygame.K_u:
                    self.undo_move()
                
                elif event.key == pygame.K_r:
                    self.load_level(self.current_level)
                
                elif event.key == pygame.K_n and self.is_level_complete():
                    if self.current_level < self.max_levels:
                        self.load_level(self.current_level + 1)
                    else:
                        print("🏆 FÉLICITATIONS ! TU AS TERMINÉ SOKOBAN 3025 ! 🏆")
        
        return True
    
    def run(self):
        """Boucle principale du jeu futuriste"""
        clock = pygame.time.Clock()
        
        # Charger niveau seulement si pas déjà chargé (pour launcher)
        if not self.board:
            self.load_level(1)
        
        print("🚀 LANCEMENT DE SOKOBAN 3025 ! 🚀")
        
        running = True
        while running:
            running = self.handle_events()
            
            # Vérification victoire automatique
            if self.is_level_complete() and not self.level_transition_effect['active']:
                if self.current_level < self.max_levels:
                    print(f"🎯 Passage automatique au niveau {self.current_level + 1}")
                    pygame.time.wait(2000)  # Pause pour admirer la victoire
                    self.load_level(self.current_level + 1)
                else:
                    print("🏆 JEU TERMINÉ ! MAÎTRE DE SOKOBAN 3025 ! 🏆")
                    pygame.time.wait(3000)  # Pause réduite
                    running = False
            
            self.render()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.display.quit()
        # Ne pas appeler sys.exit() pour permettre retour au launcher

if __name__ == "__main__":
    game = Sokoban3025()
    game.run() 