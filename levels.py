"""
🧠 LEVELS.PY - GESTIONNAIRE DE NIVEAUX GÉNIE 🧠
Collection de niveaux avec difficulté progressive
Système extensible pour ajout de nouveaux défis
"""

from typing import List, Dict, Optional
from board import TileType

class LevelManager:
    """Gestionnaire de niveaux - Architecte de défis"""
    
    def __init__(self):
        """Initialisation avec collection de niveaux"""
        self.levels = self._create_levels()
        
    def _create_levels(self) -> Dict[int, List[List[int]]]:
        """Création des niveaux - Design de puzzles génie"""
        
        # Représentation: WALL=-1, EMPTY=0, GOAL=1, BOX=2, PLAYER=3
        W, E, G, B, P = TileType.WALL, TileType.EMPTY, TileType.GOAL, TileType.BOX, TileType.PLAYER
        
        levels = {
            # Niveau 1 - Tutorial simple
            1: [
                [W, W, W, W, W, W, W],
                [W, E, E, E, E, E, W],
                [W, E, P, B, G, E, W],
                [W, E, E, E, E, E, W],
                [W, W, W, W, W, W, W]
            ],
            
            # Niveau 2 - Premier vrai défi
            2: [
                [W, W, W, W, W, W, W, W],
                [W, P, E, E, W, E, E, W],
                [W, E, W, B, W, B, E, W],
                [W, E, E, E, E, E, E, W],
                [W, W, W, G, W, G, W, W],
                [E, E, W, W, W, W, W, E],
                [E, E, E, E, E, E, E, E]
            ],
            
            # Niveau 3 - Couloir en L
            3: [
                [W, W, W, W, W, W, W, W, W],
                [W, P, E, E, E, E, E, E, W],
                [W, W, W, W, W, B, E, E, W],
                [E, E, E, E, W, E, E, E, W],
                [E, E, E, E, W, E, W, W, W],
                [E, E, E, E, W, B, W, E, E],
                [E, E, W, W, W, E, W, G, E],
                [E, E, W, G, E, E, W, W, E],
                [E, E, W, W, W, W, W, E, E]
            ],
            
            # Niveau 4 - Labyrinthe avec obstacles
            4: [
                [W, W, W, W, W, W, W, W, W],
                [W, E, E, E, W, E, E, E, W],
                [W, E, W, B, W, B, W, E, W],
                [W, E, W, E, P, E, W, E, W],
                [W, E, E, E, W, E, E, E, W],
                [W, W, W, G, W, G, W, W, W],
                [E, E, E, W, W, W, E, E, E]
            ],
            
            # Niveau 5 - Formation en croix
            5: [
                [E, E, W, W, W, W, W, E, E],
                [E, E, W, E, G, E, W, E, E],
                [W, W, W, E, B, E, W, W, W],
                [W, E, E, B, P, B, E, E, W],
                [W, E, G, E, B, E, G, E, W],
                [W, W, W, E, E, E, W, W, W],
                [E, E, W, G, E, G, W, E, E],
                [E, E, W, W, W, W, W, E, E]
            ],
            
            # Niveau 6 - Spirale avec piège
            6: [
                [W, W, W, W, W, W, W, W, W, W],
                [W, P, E, E, E, E, E, E, E, W],
                [W, W, W, W, W, E, W, W, E, W],
                [W, E, E, E, W, E, W, B, E, W],
                [W, E, G, E, W, E, W, E, W, W],
                [W, E, W, E, E, E, E, E, E, W],
                [W, E, W, W, W, B, W, W, E, W],
                [W, E, E, E, E, E, E, G, E, W],
                [W, W, W, W, W, W, W, W, W, W]
            ],
            
            # Niveau 7 - Double couloir
            7: [
                [W, W, W, W, W, W, W, W, W, W, W],
                [W, P, E, E, W, E, E, E, G, G, W],
                [W, E, W, B, W, B, W, W, E, E, W],
                [W, E, W, E, E, E, W, E, E, E, W],
                [W, E, E, E, W, E, E, E, W, W, W],
                [W, W, W, W, W, W, W, W, W, E, E]
            ],
            
            # Niveau 8 - Puzzle en U
            8: [
                [W, W, W, W, W, W, W, W, W],
                [W, G, G, G, W, E, E, E, W],
                [W, E, W, E, W, E, W, B, W],
                [W, E, W, E, E, E, W, E, W],
                [W, E, W, E, W, B, W, E, W],
                [W, E, E, E, W, E, E, E, W],
                [W, B, W, W, W, P, W, W, W],
                [W, E, E, E, E, E, E, E, E],
                [W, W, W, W, W, W, W, W, W]
            ],
            
            # Niveau 9 - Formation en diamant
            9: [
                [E, E, E, W, W, W, E, E, E],
                [E, E, W, W, P, W, W, E, E],
                [E, W, W, E, B, E, W, W, E],
                [W, W, E, B, G, B, E, W, W],
                [W, G, E, E, B, E, E, G, W],
                [W, W, E, B, G, B, E, W, W],
                [E, W, W, E, B, E, W, W, E],
                [E, E, W, W, G, W, W, E, E],
                [E, E, E, W, W, W, E, E, E]
            ],
            
            # Niveau 10 - Boss final complexe
            10: [
                [W, W, W, W, W, W, W, W, W, W, W],
                [W, E, E, E, W, P, W, E, E, E, W],
                [W, E, W, B, W, E, W, B, W, E, W],
                [W, E, W, E, E, E, E, E, W, E, W],
                [W, G, E, B, W, B, W, B, E, G, W],
                [W, E, W, E, E, E, E, E, W, E, W],
                [W, E, W, B, W, G, W, B, W, E, W],
                [W, E, E, E, W, E, W, E, E, E, W],
                [W, G, W, W, W, G, W, W, W, G, W],
                [W, W, W, W, W, W, W, W, W, W, W]
            ]
        }
        
        return levels
    
    def get_level(self, level_num: int) -> Optional[List[List[int]]]:
        """Récupération de niveau - Accès sécurisé"""
        return self.levels.get(level_num)
    
    def has_level(self, level_num: int) -> bool:
        """Vérification existence niveau"""
        return level_num in self.levels
    
    def get_total_levels(self) -> int:
        """Nombre total de niveaux"""
        return len(self.levels)
    
    def get_level_info(self, level_num: int) -> Dict[str, any]:
        """Informations détaillées sur un niveau"""
        if not self.has_level(level_num):
            return {}
            
        level_data = self.levels[level_num]
        
        # Analyse du niveau
        total_cells = 0
        boxes = 0
        goals = 0
        walls = 0
        
        for row in level_data:
            for cell in row:
                total_cells += 1
                if cell == TileType.BOX:
                    boxes += 1
                elif cell == TileType.GOAL:
                    goals += 1
                elif cell == TileType.WALL:
                    walls += 1
        
        # Calcul difficulté estimée
        difficulty = self._calculate_difficulty(level_data)
        
        return {
            'level': level_num,
            'width': len(level_data[0]) if level_data else 0,
            'height': len(level_data),
            'total_cells': total_cells,
            'boxes': boxes,
            'goals': goals,
            'walls': walls,
            'difficulty': difficulty,
            'estimated_moves': self._estimate_minimum_moves(level_data)
        }
    
    def _calculate_difficulty(self, level_data: List[List[int]]) -> str:
        """Calcul de difficulté - Analyse génie"""
        boxes = sum(row.count(TileType.BOX) for row in level_data)
        walls = sum(row.count(TileType.WALL) for row in level_data)
        size = len(level_data) * len(level_data[0])
        
        # Ratio complexité
        wall_ratio = walls / size
        box_density = boxes / (size - walls) if (size - walls) > 0 else 0
        
        if boxes <= 1 and wall_ratio < 0.3:
            return "Facile"
        elif boxes <= 3 and wall_ratio < 0.5:
            return "Moyen"
        elif boxes <= 6 and wall_ratio < 0.7:
            return "Difficile"
        else:
            return "Expert"
    
    def _estimate_minimum_moves(self, level_data: List[List[int]]) -> int:
        """Estimation minimum de mouvements - Heuristique simple"""
        boxes = sum(row.count(TileType.BOX) for row in level_data)
        size = len(level_data) * len(level_data[0])
        
        # Estimation basique basée sur la taille et nombre de caisses
        base_moves = boxes * 10  # 10 mouvements par caisse en moyenne
        complexity_bonus = int((size ** 0.5) * 2)  # Bonus selon la taille
        
        return base_moves + complexity_bonus
    
    def get_levels_by_difficulty(self, difficulty: str) -> List[int]:
        """Filtrage par difficulté - Sélection intelligente"""
        matching_levels = []
        
        for level_num in self.levels:
            info = self.get_level_info(level_num)
            if info.get('difficulty') == difficulty:
                matching_levels.append(level_num)
                
        return sorted(matching_levels)
    
    def add_custom_level(self, level_num: int, level_data: List[List[int]]) -> bool:
        """Ajout niveau personnalisé - Extensibilité génie"""
        try:
            # Validation basique
            if not self._validate_level(level_data):
                return False
                
            self.levels[level_num] = level_data
            return True
        except Exception:
            return False
    
    def _validate_level(self, level_data: List[List[int]]) -> bool:
        """Validation niveau - Contrôle qualité"""
        if not level_data or not level_data[0]:
            return False
            
        # Vérifications basiques
        player_count = sum(row.count(TileType.PLAYER) for row in level_data)
        box_count = sum(row.count(TileType.BOX) for row in level_data)
        goal_count = sum(row.count(TileType.GOAL) for row in level_data)
        
        # Un seul joueur, au moins une caisse, nombre égal caisses/objectifs
        return (player_count == 1 and box_count > 0 and box_count == goal_count)
    
    def get_random_level(self) -> int:
        """Niveau aléatoire - Surprise génie"""
        import random
        return random.choice(list(self.levels.keys()))
    
    def export_level(self, level_num: int) -> str:
        """Export niveau format texte"""
        if not self.has_level(level_num):
            return ""
            
        level_data = self.levels[level_num]
        symbols = {
            TileType.WALL: '#',
            TileType.EMPTY: ' ',
            TileType.GOAL: '.',
            TileType.BOX: '$',
            TileType.PLAYER: '@'
        }
        
        result = []
        for row in level_data:
            line = ''.join(symbols.get(cell, '?') for cell in row)
            result.append(line)
            
        return '\n'.join(result) 