import copy
from typing import List, Tuple, Dict, Optional
from enum import IntEnum

class TileType(IntEnum):
    """Types de tuiles - Représentation numérique génie"""
    WALL = -1       # Obstacle
    EMPTY = 0       # Espace vide  
    GOAL = 1        # Emplacement cible
    BOX = 2         # Caisse
    PLAYER = 3      # Personnage
    BOX_ON_GOAL = 4 # Caisse sur objectif

class Direction:
    """Directions de mouvement - Vecteurs intelligents"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    
    @staticmethod
    def get_direction(direction_str: str) -> Tuple[int, int]:
        """Conversion string -> vecteur"""
        directions = {
            'UP': Direction.UP,
            'DOWN': Direction.DOWN, 
            'LEFT': Direction.LEFT,
            'RIGHT': Direction.RIGHT
        }
        return directions.get(direction_str, (0, 0))

class Board:
    """Plateau de jeu - Cerveau logique du Sokoban"""
    
    def __init__(self, level_data: List[List[int]]):
        """Initialisation avec validation génie"""
        self.original_board = copy.deepcopy(level_data)
        self.board = copy.deepcopy(level_data)
        self.width = len(level_data[0]) if level_data else 0
        self.height = len(level_data)
        
        # Historique des mouvements pour undo/redo
        self.move_history: List[Dict] = []
        self.move_count = 0
        self.push_count = 0
        
        # Positions importantes
        self.player_pos = self._find_player()
        self.goal_positions = self._find_goals()
        self.initial_box_positions = self._find_boxes()
        
    def _find_player(self) -> Tuple[int, int]:
        """Trouve la position du joueur - Détection intelligente"""
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == TileType.PLAYER:
                    return (x, y)
        return (0, 0)  # Fallback sécurisé
    
    def _find_goals(self) -> List[Tuple[int, int]]:
        """Trouve tous les objectifs - Cartographie génie"""
        goals = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] in [TileType.GOAL, TileType.BOX_ON_GOAL]:
                    goals.append((x, y))
        return goals
    
    def _find_boxes(self) -> List[Tuple[int, int]]:
        """Trouve toutes les caisses - Intelligence de reconnaissance"""
        boxes = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] in [TileType.BOX, TileType.BOX_ON_GOAL]:
                    boxes.append((x, y))
        return boxes
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Validation de position - Logique de sécurité"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_tile(self, x: int, y: int) -> int:
        """Récupération sécurisée de tuile"""
        if self.is_valid_position(x, y):
            return self.board[y][x]
        return TileType.WALL  # Considère l'extérieur comme mur
    
    def set_tile(self, x: int, y: int, tile_type: int):
        """Modification sécurisée de tuile"""
        if self.is_valid_position(x, y):
            self.board[y][x] = tile_type
    
    def can_move_player(self, direction: str) -> bool:
        """Validation de mouvement joueur - Logique prédictive"""
        dx, dy = Direction.get_direction(direction)
        new_x, new_y = self.player_pos[0] + dx, self.player_pos[1] + dy
        
        # Vérification des limites et murs
        if not self.is_valid_position(new_x, new_y):
            return False
        if self.get_tile(new_x, new_y) == TileType.WALL:
            return False
            
        # Si c'est une caisse, vérifier si on peut la pousser
        if self.get_tile(new_x, new_y) in [TileType.BOX, TileType.BOX_ON_GOAL]:
            return self.can_push_box(new_x, new_y, direction)
            
        return True
    
    def can_push_box(self, box_x: int, box_y: int, direction: str) -> bool:
        """Validation de poussée de caisse - Intelligence de prédiction"""
        dx, dy = Direction.get_direction(direction)
        new_box_x, new_box_y = box_x + dx, box_y + dy
        
        # Vérification position valide
        if not self.is_valid_position(new_box_x, new_box_y):
            return False
            
        # Vérification obstruction
        target_tile = self.get_tile(new_box_x, new_box_y)
        return target_tile in [TileType.EMPTY, TileType.GOAL]
    
    def move_player(self, direction: str) -> bool:
        """Mouvement du joueur - Logique complexe intégrée"""
        if not self.can_move_player(direction):
            return False
            
        # Sauvegarde pour historique
        self._save_move_state()
        
        dx, dy = Direction.get_direction(direction)
        old_x, old_y = self.player_pos
        new_x, new_y = old_x + dx, old_y + dy
        
        # Gestion poussée de caisse
        is_push = False
        if self.get_tile(new_x, new_y) in [TileType.BOX, TileType.BOX_ON_GOAL]:
            is_push = True
            self._push_box(new_x, new_y, direction)
            self.push_count += 1
        
        # Nettoyage ancienne position joueur
        if (old_x, old_y) in self.goal_positions:
            self.set_tile(old_x, old_y, TileType.GOAL)
        else:
            self.set_tile(old_x, old_y, TileType.EMPTY)
        
        # Placement nouvelle position joueur
        self.set_tile(new_x, new_y, TileType.PLAYER)
        self.player_pos = (new_x, new_y)
        self.move_count += 1
        
        return True
    
    def _push_box(self, box_x: int, box_y: int, direction: str):
        """Poussée de caisse - Mécanique précise"""
        dx, dy = Direction.get_direction(direction)
        new_box_x, new_box_y = box_x + dx, box_y + dy
        
        # Nettoyage ancienne position caisse
        if (box_x, box_y) in self.goal_positions:
            self.set_tile(box_x, box_y, TileType.GOAL)
        else:
            self.set_tile(box_x, box_y, TileType.EMPTY)
        
        # Placement nouvelle position caisse
        if (new_box_x, new_box_y) in self.goal_positions:
            self.set_tile(new_box_x, new_box_y, TileType.BOX_ON_GOAL)
        else:
            self.set_tile(new_box_x, new_box_y, TileType.BOX)
    
    def _save_move_state(self):
        """Sauvegarde état pour undo - Mémoire génie"""
        state = {
            'board': copy.deepcopy(self.board),
            'player_pos': self.player_pos,
            'move_count': self.move_count,
            'push_count': self.push_count
        }
        self.move_history.append(state)
        
        # Limitation mémoire (garde les 100 derniers mouvements)
        if len(self.move_history) > 100:
            self.move_history.pop(0)
    
    def undo_move(self) -> bool:
        """Annulation mouvement - Voyage temporel"""
        if not self.move_history:
            return False
            
        state = self.move_history.pop()
        self.board = state['board']
        self.player_pos = state['player_pos']
        self.move_count = state['move_count']
        self.push_count = state['push_count']
        return True
    
    def is_solved(self) -> bool:
        """Vérification victoire - Détection de génie stricte"""
        # Compte les caisses sur les objectifs
        boxes_on_goals = 0
        total_boxes = 0
        
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_tile(x, y)
                if tile == TileType.BOX_ON_GOAL:
                    boxes_on_goals += 1
                if tile in [TileType.BOX, TileType.BOX_ON_GOAL]:
                    total_boxes += 1
        
        # Le niveau est résolu si TOUTES les caisses sont sur des objectifs
        # et le nombre de caisses sur objectifs = nombre total d'objectifs
        return (boxes_on_goals == len(self.goal_positions) and 
                boxes_on_goals == total_boxes and 
                len(self.goal_positions) > 0)
    
    def reset(self):
        """Réinitialisation niveau - Reset intelligent"""
        self.board = copy.deepcopy(self.original_board)
        self.player_pos = self._find_player()
        self.move_history.clear()
        self.move_count = 0
        self.push_count = 0
    
    def get_board_copy(self) -> List[List[int]]:
        """Copie sécurisée du plateau"""
        return copy.deepcopy(self.board)
    
    def get_stats(self) -> Dict[str, int]:
        """Statistiques de partie - Analytics génie"""
        return {
            'moves': self.move_count,
            'pushes': self.push_count,
            'boxes_placed': sum(1 for gx, gy in self.goal_positions 
                              if self.get_tile(gx, gy) == TileType.BOX_ON_GOAL),
            'total_boxes': len(self.initial_box_positions),
            'completion_percent': int((sum(1 for gx, gy in self.goal_positions 
                                         if self.get_tile(gx, gy) == TileType.BOX_ON_GOAL) 
                                     / len(self.initial_box_positions)) * 100) if self.initial_box_positions else 100
        } 