
import time
from typing import Optional, Dict, Any
from board import Board, TileType
from levels import LevelManager
from database import Database
from sounds import SoundManager

class GameState:
    """États du jeu - Machine à états intelligente"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_COMPLETE = "level_complete"
    GAME_WON = "game_won"

class SokobanGame:
    """Jeu principal - Cerveau orchestrateur"""
    
    def __init__(self, database: Database, sound_manager: SoundManager):
        """Initialisation du génie du jeu"""
        self.database = database
        self.sound_manager = sound_manager
        self.level_manager = LevelManager()
        
        # État du jeu
        self.state = GameState.MENU
        self.current_level = 1
        self.board: Optional[Board] = None
        
        # Métriques de performance
        self.level_start_time = 0
        self.total_play_time = 0
        self.best_scores = {}
        
        # Configuration
        self.auto_save = True
        self.animations_enabled = True
        
        # Initialisation
        self._load_level(self.current_level)
        self._load_best_scores()
        
    def _load_level(self, level_num: int) -> bool:
        """Chargement de niveau - Logique de progression"""
        try:
            level_data = self.level_manager.get_level(level_num)
            if level_data:
                self.board = Board(level_data)
                self.current_level = level_num
                self.level_start_time = time.time()
                self.state = GameState.PLAYING
                self.sound_manager.play_sound('level_start')
                return True
        except Exception as e:
            print(f"❌ Erreur chargement niveau {level_num}: {e}")
        return False
    
    def _load_best_scores(self):
        """Chargement des meilleurs scores - Mémoire de génie"""
        try:
            scores = self.database.get_all_scores()
            self.best_scores = {score['level']: score for score in scores}
        except Exception as e:
            print(f"❌ Erreur chargement scores: {e}")
            self.best_scores = {}
    
    def move_player(self, direction: str) -> bool:
        """Mouvement joueur avec validation génie"""
        if self.state != GameState.PLAYING or not self.board:
            return False
            
        # Tentative de mouvement
        if self.board.move_player(direction):
            # Sons selon le contexte
            if self.board.push_count > 0:
                self.sound_manager.play_sound('box_push')
            else:
                self.sound_manager.play_sound('player_move')
            
            # Vérification victoire
            if self.board.is_solved():
                self._handle_level_complete()
            
            # Sauvegarde auto si activée
            if self.auto_save:
                self._save_progress()
            
            return True
        else:
            self.sound_manager.play_sound('invalid_move')
            return False
    
    def _handle_level_complete(self):
        """Gestion fin de niveau - Récompense du génie"""
        if not self.board:
            return
            
        self.state = GameState.LEVEL_COMPLETE
        completion_time = time.time() - self.level_start_time
        stats = self.board.get_stats()
        
        # Calcul du score (moins de mouvements/temps = meilleur score)
        score = self._calculate_score(stats['moves'], stats['pushes'], completion_time)
        
        # Sauvegarde du score
        self._save_score(self.current_level, score, stats['moves'], 
                        stats['pushes'], int(completion_time))
        
        # Sons de victoire
        self.sound_manager.play_sound('level_complete')
        
        print(f"🎉 Niveau {self.current_level} terminé!")
        print(f"   Mouvements: {stats['moves']}, Poussées: {stats['pushes']}")
        print(f"   Temps: {completion_time:.1f}s, Score: {score}")
        
        # Auto-progression vers niveau suivant
        if self.level_manager.has_level(self.current_level + 1):
            self._auto_next_level()
        else:
            self.state = GameState.GAME_WON
            self.sound_manager.play_sound('game_complete')
            print("🏆 Félicitations! Tous les niveaux terminés!")
    
    def _calculate_score(self, moves: int, pushes: int, time_seconds: float) -> int:
        """Calcul score génie - Algorithme d'évaluation"""
        # Score basé sur efficacité: moins de mouvements et temps = meilleur score
        base_score = 10000
        move_penalty = moves * 10
        push_penalty = pushes * 50  # Les poussées coûtent plus cher
        time_penalty = int(time_seconds * 5)
        
        final_score = max(100, base_score - move_penalty - push_penalty - time_penalty)
        return final_score
    
    def _save_score(self, level: int, score: int, moves: int, pushes: int, time_sec: int):
        """Sauvegarde score - Persistance intelligente"""
        try:
            # Vérifier si c'est un nouveau record
            current_best = self.best_scores.get(level)
            if not current_best or score > current_best['score']:
                self.database.save_score(level, score, moves, pushes, time_sec)
                self.best_scores[level] = {
                    'level': level, 'score': score, 'moves': moves,
                    'pushes': pushes, 'time': time_sec
                }
                print(f"🌟 Nouveau record niveau {level}!")
        except Exception as e:
            print(f"❌ Erreur sauvegarde score: {e}")
    
    def _auto_next_level(self):
        """Progression automatique - Intelligence adaptative"""
        # Attendre 2 secondes avant de passer au niveau suivant
        import threading
        def delayed_next():
            time.sleep(2)
            if self.state == GameState.LEVEL_COMPLETE:
                self.next_level()
        
        threading.Thread(target=delayed_next, daemon=True).start()
    
    def next_level(self) -> bool:
        """Niveau suivant - Progression génie"""
        next_level_num = self.current_level + 1
        if self.level_manager.has_level(next_level_num):
            return self._load_level(next_level_num)
        return False
    
    def previous_level(self) -> bool:
        """Niveau précédent - Navigation intelligente"""
        if self.current_level > 1:
            return self._load_level(self.current_level - 1)
        return False
    
    def select_level(self, level_num: int) -> bool:
        """Sélection niveau spécifique"""
        if self.level_manager.has_level(level_num):
            return self._load_level(level_num)
        return False
    
    def reset_level(self) -> bool:
        """Réinitialisation niveau - Renaissance intelligente"""
        if self.board:
            self.board.reset()
            self.level_start_time = time.time()
            self.state = GameState.PLAYING
            self.sound_manager.play_sound('level_reset')
            return True
        return False
    
    def undo_move(self) -> bool:
        """Annulation mouvement - Voyage temporel"""
        if self.state == GameState.PLAYING and self.board:
            if self.board.undo_move():
                self.sound_manager.play_sound('undo')
                return True
            else:
                self.sound_manager.play_sound('invalid_move')
        return False
    
    def _save_progress(self):
        """Sauvegarde progression - Persistance génie"""
        try:
            if self.board:
                progress_data = {
                    'level': self.current_level,
                    'moves': self.board.move_count,
                    'pushes': self.board.push_count,
                    'board_state': self.board.get_board_copy()
                }
                self.database.save_progress(progress_data)
        except Exception as e:
            print(f"❌ Erreur sauvegarde progression: {e}")
    
    def load_progress(self) -> bool:
        """Chargement progression - Restauration intelligente"""
        try:
            progress = self.database.load_progress()
            if progress:
                self.current_level = progress['level']
                # Charger le niveau et restaurer l'état si nécessaire
                return self._load_level(self.current_level)
        except Exception as e:
            print(f"❌ Erreur chargement progression: {e}")
        return False
    
    def get_game_info(self) -> Dict[str, Any]:
        """Informations jeu - Analytics génie"""
        info = {
            'state': self.state,
            'current_level': self.current_level,
            'total_levels': self.level_manager.get_total_levels(),
            'board_stats': self.board.get_stats() if self.board else {},
            'elapsed_time': time.time() - self.level_start_time if self.level_start_time > 0 else 0,
            'best_score': self.best_scores.get(self.current_level, {}).get('score', 0)
        }
        return info
    
    def toggle_pause(self):
        """Gestion pause - Contrôle temporel"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            self.state = GameState.PLAYING
    
    def update(self):
        """Mise à jour globale - Heartbeat du génie"""
        # Ici on pourrait ajouter des animations, des particules, etc.
        # Pour l'instant, on garde simple mais extensible
        pass
    
    def get_leaderboard(self, level: int = None) -> list:
        """Classement - Compétition de génies"""
        try:
            if level:
                return self.database.get_level_scores(level)
            else:
                return self.database.get_top_scores()
        except Exception as e:
            print(f"❌ Erreur récupération classement: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Statistiques globales - Analytics avancées"""
        try:
            stats = {
                'levels_completed': len(self.best_scores),
                'total_levels': self.level_manager.get_total_levels(),
                'completion_rate': len(self.best_scores) / self.level_manager.get_total_levels() * 100,
                'average_score': sum(score['score'] for score in self.best_scores.values()) / len(self.best_scores) if self.best_scores else 0,
                'total_moves': sum(score['moves'] for score in self.best_scores.values()),
                'total_pushes': sum(score['pushes'] for score in self.best_scores.values()),
                'total_time': sum(score['time'] for score in self.best_scores.values()),
                'current_streak': self._calculate_current_streak()
            }
            return stats
        except Exception as e:
            print(f"❌ Erreur calcul statistiques: {e}")
            return {}
    
    def _calculate_current_streak(self) -> int:
        """Calcul série actuelle - Motivation génie"""
        streak = 0
        level = 1
        while level in self.best_scores:
            streak += 1
            level += 1
        return streak 