"""
🧠 SOUNDS.PY - SYSTÈME AUDIO GÉNIE 🧠
Gestion des sons et musique avec Pygame
Architecture modulaire pour expérience immersive
"""

import pygame
import os
from typing import Dict, Optional
from enum import Enum

class SoundType(Enum):
    """Types de sons - Classification intelligente"""
    PLAYER_MOVE = "player_move"
    BOX_PUSH = "box_push"
    INVALID_MOVE = "invalid_move"
    LEVEL_START = "level_start"
    LEVEL_COMPLETE = "level_complete"
    GAME_COMPLETE = "game_complete"
    LEVEL_RESET = "level_reset"
    UNDO = "undo"
    MENU_SELECT = "menu_select"
    MENU_NAVIGATE = "menu_navigate"

class SoundManager:
    """Gestionnaire audio - Maître du son"""
    
    def __init__(self, sound_volume: float = 0.7, music_volume: float = 0.5):
        """Initialisation du système audio"""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self.sound_volume = sound_volume
        self.music_volume = music_volume
        self.sounds_enabled = True
        self.music_enabled = True
        
        # Dictionnaire des sons chargés
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.current_music = None
        
        # Chargement initial des sons
        self._load_sounds()
        self._setup_music()
        
        print("🎵 Système audio initialisé")
    
    def _load_sounds(self):
        """Chargement des effets sonores - Collection audio"""
        # Sons par défaut générés proceduralement si pas de fichiers
        sound_configs = {
            SoundType.PLAYER_MOVE.value: self._generate_move_sound(),
            SoundType.BOX_PUSH.value: self._generate_push_sound(),
            SoundType.INVALID_MOVE.value: self._generate_error_sound(),
            SoundType.LEVEL_START.value: self._generate_start_sound(),
            SoundType.LEVEL_COMPLETE.value: self._generate_success_sound(),
            SoundType.GAME_COMPLETE.value: self._generate_victory_sound(),
            SoundType.LEVEL_RESET.value: self._generate_reset_sound(),
            SoundType.UNDO.value: self._generate_undo_sound(),
            SoundType.MENU_SELECT.value: self._generate_select_sound(),
            SoundType.MENU_NAVIGATE.value: self._generate_navigate_sound()
        }
        
        # Tentative de chargement de fichiers externes
        sound_folder = "assets/sounds"
        if os.path.exists(sound_folder):
            self._load_sound_files(sound_folder)
        else:
            # Utilisation des sons générés
            for sound_name, sound_data in sound_configs.items():
                try:
                    sound = pygame.sndarray.make_sound(sound_data)
                    sound.set_volume(self.sound_volume)
                    self.sounds[sound_name] = sound
                except Exception as e:
                    print(f"⚠️ Erreur génération son {sound_name}: {e}")
    
    def _load_sound_files(self, folder_path: str):
        """Chargement fichiers audio externes"""
        sound_extensions = ['.wav', '.ogg', '.mp3']
        
        for sound_type in SoundType:
            sound_name = sound_type.value
            sound_loaded = False
            
            for ext in sound_extensions:
                sound_file = os.path.join(folder_path, f"{sound_name}{ext}")
                if os.path.exists(sound_file):
                    try:
                        sound = pygame.mixer.Sound(sound_file)
                        sound.set_volume(self.sound_volume)
                        self.sounds[sound_name] = sound
                        sound_loaded = True
                        break
                    except Exception as e:
                        print(f"⚠️ Erreur chargement {sound_file}: {e}")
            
            if not sound_loaded:
                print(f"ℹ️ Son {sound_name} non trouvé, utilisation du son généré")
    
    def _generate_move_sound(self):
        """Génération son mouvement - Synthèse audio"""
        import numpy as np
        duration = 0.1
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Son doux de pas
        frequency = 800
        wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 10)
        
        # Stéréo
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.3
        stereo_wave[:, 1] = wave * 0.3
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_push_sound(self):
        """Génération son poussée - Audio procédural"""
        import numpy as np
        duration = 0.2
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Son plus grave et plus long pour poussée
        frequency = 400
        wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 5)
        
        # Ajout d'harmoniques
        wave += 0.3 * np.sin(2 * np.pi * frequency * 2 * t) * np.exp(-t * 8)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.5
        stereo_wave[:, 1] = wave * 0.5
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_error_sound(self):
        """Génération son erreur - Feedback négatif"""
        import numpy as np
        duration = 0.15
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Son désagréable pour erreur
        frequency = 200
        wave = np.sin(2 * np.pi * frequency * t) * (1 - t / duration)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.4
        stereo_wave[:, 1] = wave * 0.4
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_success_sound(self):
        """Génération son succès - Récompense audio"""
        import numpy as np
        duration = 0.5
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Mélodie ascendante
        frequencies = [523, 659, 784]  # Do, Mi, Sol
        wave = np.zeros_like(t)
        
        for i, freq in enumerate(frequencies):
            start = i * len(t) // 3
            end = (i + 1) * len(t) // 3
            segment = t[start:end] - t[start]
            wave[start:end] = np.sin(2 * np.pi * freq * segment) * np.exp(-segment * 2)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.6
        stereo_wave[:, 1] = wave * 0.6
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_victory_sound(self):
        """Génération son victoire - Triomphe audio"""
        import numpy as np
        duration = 1.0
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        # Fanfare simple
        frequencies = [523, 659, 784, 1047]  # Do, Mi, Sol, Do aigu
        wave = np.zeros_like(t)
        
        for i, freq in enumerate(frequencies):
            start = i * len(t) // 4
            end = (i + 1) * len(t) // 4
            segment = t[start:end] - t[start]
            wave[start:end] = np.sin(2 * np.pi * freq * segment) * (1 - segment / (duration/4))
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.7
        stereo_wave[:, 1] = wave * 0.7
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_start_sound(self):
        """Son de début de niveau"""
        import numpy as np
        duration = 0.3
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        frequency = 1000
        wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 3)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.4
        stereo_wave[:, 1] = wave * 0.4
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_reset_sound(self):
        """Son de reset"""
        import numpy as np
        duration = 0.25
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        frequency = 600
        wave = np.sin(2 * np.pi * frequency * t) * (1 - t / duration)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.4
        stereo_wave[:, 1] = wave * 0.4
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_undo_sound(self):
        """Son d'annulation"""
        import numpy as np
        duration = 0.15
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        frequency = 700
        wave = np.sin(2 * np.pi * frequency * t * (1 - 0.5 * t / duration))
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.3
        stereo_wave[:, 1] = wave * 0.3
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_select_sound(self):
        """Son de sélection menu"""
        import numpy as np
        duration = 0.1
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        frequency = 1200
        wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 15)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.3
        stereo_wave[:, 1] = wave * 0.3
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _generate_navigate_sound(self):
        """Son de navigation menu"""
        import numpy as np
        duration = 0.08
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        frequency = 1000
        wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 20)
        
        stereo_wave = np.zeros((len(wave), 2))
        stereo_wave[:, 0] = wave * 0.2
        stereo_wave[:, 1] = wave * 0.2
        
        return (stereo_wave * 32767).astype(np.int16)
    
    def _setup_music(self):
        """Configuration musique de fond"""
        music_folder = "assets/music"
        if os.path.exists(music_folder):
            # Recherche fichiers musique
            music_files = []
            for file in os.listdir(music_folder):
                if file.lower().endswith(('.mp3', '.ogg', '.wav')):
                    music_files.append(os.path.join(music_folder, file))
            
            if music_files:
                self.current_music = music_files[0]
                print(f"🎵 Musique trouvée: {self.current_music}")
        else:
            print("ℹ️ Dossier musique non trouvé, jeu silencieux")
    
    def play_sound(self, sound_name: str):
        """Lecture d'un son - Audio réactif"""
        if not self.sounds_enabled:
            return
            
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"⚠️ Erreur lecture son {sound_name}: {e}")
        else:
            print(f"⚠️ Son non trouvé: {sound_name}")
    
    def start_music(self):
        """Démarrage musique de fond"""
        if not self.music_enabled or not self.current_music:
            return
            
        try:
            pygame.mixer.music.load(self.current_music)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # Boucle infinie
            print("🎵 Musique démarrée")
        except Exception as e:
            print(f"⚠️ Erreur lecture musique: {e}")
    
    def stop_music(self):
        """Arrêt musique"""
        pygame.mixer.music.stop()
    
    def set_sound_volume(self, volume: float):
        """Réglage volume sons"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume: float):
        """Réglage volume musique"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def toggle_sounds(self):
        """Basculement sons on/off"""
        self.sounds_enabled = not self.sounds_enabled
        return self.sounds_enabled
    
    def toggle_music(self):
        """Basculement musique on/off"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.start_music()
        else:
            self.stop_music()
        return self.music_enabled
    
    def cleanup(self):
        """Nettoyage ressources audio"""
        self.stop_music()
        pygame.mixer.quit()
        print("🎵 Système audio fermé") 