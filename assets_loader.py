"""
🚀 ASSETS_LOADER.PY - CHARGEUR D'ASSETS FUTURISTE 🚀
Utilise les assets du jeu Rust original + effets année 3025
"""

import pygame
import os
from typing import Dict, Optional, Tuple
import numpy as np

class FuturisticAssetsLoader:
    """Chargeur d'assets avec enhancement futuriste"""
    
    def __init__(self):
        self.textures: Dict[str, pygame.Surface] = {}
        self.enhanced_textures: Dict[str, pygame.Surface] = {}
        self.particle_systems: Dict[str, any] = {}
        
        # Configuration futuriste
        self.neon_glow_strength = 3
        self.hologram_alpha = 180
        self.particle_density = 50
        
        print("🚀 Chargeur d'assets futuriste initialisé")
        
    def load_original_assets(self):
        """Charge les assets du jeu Rust original"""
        asset_paths = {
            'tilesheet': 'assets/textures/tilesheet.png',
            'box': 'assets/textures/box.png', 
            'player': 'assets/textures/player.png',
            'wall': 'assets/textures/wall.png',
            'floor': 'assets/textures/floor.png',
            'goal': 'assets/textures/goal.png',
            'next': 'assets/textures/next.png',
            'previous': 'assets/textures/previous.png',
            'auto_solution': 'assets/textures/automatic_solution.png'
        }
        
        for name, path in asset_paths.items():
            if os.path.exists(path):
                try:
                    texture = pygame.image.load(path).convert_alpha()
                    self.textures[name] = texture
                    print(f"✅ Asset chargé: {name}")
                except Exception as e:
                    print(f"⚠️ Erreur chargement {name}: {e}")
                    self._create_fallback_texture(name)
            else:
                print(f"📁 Asset manquant: {name}, création procédurale...")
                self._create_fallback_texture(name)
    
    def _create_fallback_texture(self, name: str):
        """Crée des textures procédurales si assets manquants"""
        size = (40, 40)
        
        if name == 'wall':
            self.textures[name] = self._create_futuristic_wall(size)
        elif name == 'box':
            self.textures[name] = self._create_quantum_box(size)
        elif name == 'player':
            self.textures[name] = self._create_cyber_player(size)
        elif name == 'goal':
            self.textures[name] = self._create_holographic_goal(size)
        elif name == 'floor':
            self.textures[name] = self._create_neon_floor(size)
        else:
            # Texture par défaut
            surface = pygame.Surface(size, pygame.SRCALPHA)
            surface.fill((100, 100, 100, 255))
            self.textures[name] = surface
    
    def _create_futuristic_wall(self, size: Tuple[int, int]) -> pygame.Surface:
        """Mur futuriste avec circuits électroniques"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Base métallique
        base_color = (45, 55, 70)
        surface.fill(base_color)
        
        # Circuits électroniques
        circuit_color = (0, 255, 255, 150)  # Cyan néon
        
        # Lignes horizontales
        for y in range(5, size[1], 8):
            pygame.draw.line(surface, circuit_color, (2, y), (size[0]-2, y), 1)
        
        # Lignes verticales
        for x in range(5, size[0], 8):
            pygame.draw.line(surface, circuit_color, (x, 2), (x, size[1]-2), 1)
        
        # Points de connexion
        for x in range(5, size[0], 8):
            for y in range(5, size[1], 8):
                pygame.draw.circle(surface, (255, 255, 255), (x, y), 2)
                pygame.draw.circle(surface, circuit_color, (x, y), 1)
        
        # Bordure énergétique
        glow_color = (0, 255, 255, 100)
        pygame.draw.rect(surface, glow_color, surface.get_rect(), 2)
        
        return surface
    
    def _create_quantum_box(self, size: Tuple[int, int]) -> pygame.Surface:
        """Caisse quantique avec effet de matière instable"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Base de la caisse
        box_color = (150, 75, 200)  # Violet quantique
        margin = 3
        box_rect = pygame.Rect(margin, margin, size[0]-2*margin, size[1]-2*margin)
        pygame.draw.rect(surface, box_color, box_rect)
        
        # Effet holographique
        for i in range(3):
            alpha = 80 - i * 20
            offset = i + 1
            holo_rect = pygame.Rect(margin+offset, margin+offset, 
                                  size[0]-2*margin-2*offset, size[1]-2*margin-2*offset)
            holo_surface = pygame.Surface((holo_rect.width, holo_rect.height), pygame.SRCALPHA)
            holo_surface.fill((255, 100, 255, alpha))
            surface.blit(holo_surface, holo_rect)
        
        # Particules quantiques
        particle_color = (255, 255, 255, 200)
        import random
        for _ in range(8):
            x = random.randint(margin+2, size[0]-margin-2)
            y = random.randint(margin+2, size[1]-margin-2)
            pygame.draw.circle(surface, particle_color, (x, y), 1)
        
        # Bordure énergétique
        pygame.draw.rect(surface, (255, 0, 255), box_rect, 2)
        
        return surface
    
    def _create_cyber_player(self, size: Tuple[int, int]) -> pygame.Surface:
        """Joueur cybernétique avec augmentations"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        center_x, center_y = size[0] // 2, size[1] // 2
        
        # Corps principal (exosquelette)
        body_color = (255, 150, 50)  # Orange cybernétique
        pygame.draw.circle(surface, body_color, (center_x, center_y), 12)
        
        # Visière HUD
        hud_color = (0, 255, 255, 180)
        pygame.draw.circle(surface, hud_color, (center_x, center_y-3), 8)
        
        # Augmentations cybernétiques
        aug_color = (255, 255, 255)
        # Bras gauche
        pygame.draw.rect(surface, aug_color, (center_x-15, center_y-2, 8, 4))
        # Bras droit  
        pygame.draw.rect(surface, aug_color, (center_x+7, center_y-2, 8, 4))
        # Jambes
        pygame.draw.rect(surface, aug_color, (center_x-3, center_y+8, 6, 8))
        
        # LED de statut
        led_color = (0, 255, 0)  # Vert = opérationnel
        pygame.draw.circle(surface, led_color, (center_x+8, center_y-8), 2)
        
        # Aura énergétique
        aura_color = (255, 255, 0, 50)
        for radius in range(15, 20):
            pygame.draw.circle(surface, aura_color, (center_x, center_y), radius, 1)
        
        return surface
    
    def _create_holographic_goal(self, size: Tuple[int, int]) -> pygame.Surface:
        """Objectif holographique avec projection 3D"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        center_x, center_y = size[0] // 2, size[1] // 2
        
        # Base de projection
        base_color = (100, 255, 100, 100)
        pygame.draw.circle(surface, base_color, (center_x, center_y), 15)
        
        # Anneaux holographiques concentriques
        ring_colors = [(0, 255, 100, 150), (50, 255, 150, 120), (100, 255, 200, 90)]
        for i, color in enumerate(ring_colors):
            radius = 18 - i * 3
            pygame.draw.circle(surface, color, (center_x, center_y), radius, 2)
        
        # Croix de ciblage
        target_color = (255, 255, 255, 200)
        # Horizontale
        pygame.draw.line(surface, target_color, 
                        (center_x-10, center_y), (center_x+10, center_y), 2)
        # Verticale
        pygame.draw.line(surface, target_color,
                        (center_x, center_y-10), (center_x, center_y+10), 2)
        
        # Points de repère
        for angle in [0, 90, 180, 270]:
            import math
            x = center_x + int(12 * math.cos(math.radians(angle)))
            y = center_y + int(12 * math.sin(math.radians(angle)))
            pygame.draw.circle(surface, target_color, (x, y), 2)
        
        return surface
    
    def _create_neon_floor(self, size: Tuple[int, int]) -> pygame.Surface:
        """Sol néon avec grille électronique"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # Base sombre
        base_color = (20, 25, 35)
        surface.fill(base_color)
        
        # Grille néon
        grid_color = (0, 150, 255, 100)  # Bleu néon
        
        # Lignes de grille
        for x in range(0, size[0], 8):
            pygame.draw.line(surface, grid_color, (x, 0), (x, size[1]), 1)
        for y in range(0, size[1], 8):
            pygame.draw.line(surface, grid_color, (0, y), (size[0], y), 1)
        
        # Points d'intersection lumineux
        intersection_color = (255, 255, 255, 180)
        for x in range(0, size[0], 8):
            for y in range(0, size[1], 8):
                pygame.draw.circle(surface, intersection_color, (x, y), 1)
        
        return surface
    
    def enhance_with_effects(self):
        """Ajoute des effets visuels futuristes aux textures"""
        for name, texture in self.textures.items():
            enhanced = self._add_futuristic_effects(texture, name)
            self.enhanced_textures[name] = enhanced
    
    def _add_futuristic_effects(self, texture: pygame.Surface, name: str) -> pygame.Surface:
        """Ajoute effets glow, particles, distorsion"""
        # Créer surface avec effets
        enhanced_size = (texture.get_width() + 10, texture.get_height() + 10)
        enhanced = pygame.Surface(enhanced_size, pygame.SRCALPHA)
        
        # Ajouter glow selon le type
        if name in ['goal', 'player']:
            # Effet de lueur
            glow_color = (255, 255, 255, 30)
            for radius in range(5, 15):
                pygame.draw.circle(enhanced, glow_color, 
                                 (enhanced_size[0]//2, enhanced_size[1]//2), radius, 1)
        
        # Texture originale au centre
        offset_x = (enhanced_size[0] - texture.get_width()) // 2
        offset_y = (enhanced_size[1] - texture.get_height()) // 2
        enhanced.blit(texture, (offset_x, offset_y))
        
        return enhanced
    
    def get_texture(self, name: str) -> Optional[pygame.Surface]:
        """Récupère une texture (enhanced si disponible, sinon originale)"""
        if name in self.enhanced_textures:
            return self.enhanced_textures[name]
        elif name in self.textures:
            return self.textures[name]
        return None
    
    def create_particle_effect(self, effect_type: str, position: Tuple[int, int]):
        """Crée effets de particules pour actions spéciales"""
        particles = []
        
        if effect_type == 'box_placement':
            # Explosion de particules vertes lors de placement correct
            import random
            for _ in range(20):
                particles.append({
                    'pos': [position[0] + random.randint(-10, 10), 
                           position[1] + random.randint(-10, 10)],
                    'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
                    'color': (0, 255, 100),
                    'life': 30,
                    'max_life': 30
                })
        
        elif effect_type == 'level_complete':
            # Feu d'artifice holographique
            import random
            for _ in range(50):
                particles.append({
                    'pos': [position[0], position[1]],
                    'vel': [random.uniform(-5, 5), random.uniform(-5, 5)],
                    'color': (random.randint(100, 255), random.randint(100, 255), 255),
                    'life': 60,
                    'max_life': 60
                })
        
        return particles
    
    def update_particles(self, particles: list) -> list:
        """Met à jour et filtre les particules"""
        active_particles = []
        
        for particle in particles:
            # Mise à jour position
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            
            # Mise à jour vie
            particle['life'] -= 1
            
            # Fade out
            alpha = int(255 * (particle['life'] / particle['max_life']))
            particle['color'] = (*particle['color'][:3], alpha)
            
            # Garder si encore vivante
            if particle['life'] > 0:
                active_particles.append(particle)
        
        return active_particles
    
    def render_particles(self, screen: pygame.Surface, particles: list):
        """Affiche les particules"""
        for particle in particles:
            pos = (int(particle['pos'][0]), int(particle['pos'][1]))
            color = particle['color']
            
            # Dessiner particule avec fade
            if len(color) == 4 and color[3] > 0:
                pygame.draw.circle(screen, color[:3], pos, 2)
                # Effet de lueur
                pygame.draw.circle(screen, (*color[:3], color[3]//3), pos, 4, 1) 