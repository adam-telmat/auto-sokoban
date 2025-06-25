
import sqlite3
import json
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
import threading

class Database:
    """Base de données - Mémoire persistante du génie"""
    
    def __init__(self, db_path: str = "sokoban_genius.db"):
        """Initialisation avec création automatique des tables"""
        self.db_path = db_path
        self.lock = threading.Lock()  # Thread safety
        self._create_tables()
        
    def _create_tables(self):
        """Création des tables - Architecture de données génie"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Table des scores
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level INTEGER NOT NULL,
                        score INTEGER NOT NULL,
                        moves INTEGER NOT NULL,
                        pushes INTEGER NOT NULL,
                        time_seconds INTEGER NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        player_name TEXT DEFAULT 'Anonymous'
                    )
                ''')
                
                # Table de progression
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level INTEGER NOT NULL,
                        moves INTEGER NOT NULL,
                        pushes INTEGER NOT NULL,
                        board_state TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(level)
                    )
                ''')
                
                # Table des statistiques globales
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS statistics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        total_games INTEGER DEFAULT 0,
                        total_time INTEGER DEFAULT 0,
                        levels_completed INTEGER DEFAULT 0,
                        best_streak INTEGER DEFAULT 0,
                        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Table des préférences
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT NOT NULL,
                        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Index pour optimisation
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores_level ON scores(level)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_scores_score ON scores(score DESC)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_progress_level ON progress(level)')
                
                conn.commit()
                conn.close()
                
                print("✅ Base de données initialisée avec succès")
                
            except Exception as e:
                print(f"❌ Erreur initialisation BDD: {e}")
    
    def save_score(self, level: int, score: int, moves: int, pushes: int, 
                   time_seconds: int, player_name: str = "Anonymous") -> bool:
        """Sauvegarde score - Persistance de performance"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO scores (level, score, moves, pushes, time_seconds, player_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (level, score, moves, pushes, time_seconds, player_name))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur sauvegarde score: {e}")
                return False
    
    def get_best_score(self, level: int) -> Optional[Dict[str, Any]]:
        """Récupération meilleur score - Excellence mémorisée"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT level, score, moves, pushes, time_seconds, timestamp, player_name
                    FROM scores 
                    WHERE level = ? 
                    ORDER BY score DESC, moves ASC, time_seconds ASC 
                    LIMIT 1
                ''', (level,))
                
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    return {
                        'level': result[0],
                        'score': result[1],
                        'moves': result[2],
                        'pushes': result[3],
                        'time': result[4],
                        'timestamp': result[5],
                        'player': result[6]
                    }
                return None
                
            except Exception as e:
                print(f"❌ Erreur récupération meilleur score: {e}")
                return None
    
    def get_all_scores(self) -> List[Dict[str, Any]]:
        """Récupération tous les meilleurs scores - Collection génie"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Récupère le meilleur score pour chaque niveau
                cursor.execute('''
                    SELECT level, MAX(score) as score, moves, pushes, time_seconds, player_name
                    FROM scores 
                    GROUP BY level
                    ORDER BY level
                ''')
                
                results = cursor.fetchall()
                conn.close()
                
                scores = []
                for result in results:
                    scores.append({
                        'level': result[0],
                        'score': result[1],
                        'moves': result[2],
                        'pushes': result[3],
                        'time': result[4],
                        'player': result[5]
                    })
                
                return scores
                
            except Exception as e:
                print(f"❌ Erreur récupération scores: {e}")
                return []
    
    def get_level_scores(self, level: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Classement d'un niveau - Compétition locale"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT score, moves, pushes, time_seconds, timestamp, player_name
                    FROM scores 
                    WHERE level = ?
                    ORDER BY score DESC, moves ASC, time_seconds ASC
                    LIMIT ?
                ''', (level, limit))
                
                results = cursor.fetchall()
                conn.close()
                
                scores = []
                for i, result in enumerate(results, 1):
                    scores.append({
                        'rank': i,
                        'score': result[0],
                        'moves': result[1],
                        'pushes': result[2],
                        'time': result[3],
                        'timestamp': result[4],
                        'player': result[5]
                    })
                
                return scores
                
            except Exception as e:
                print(f"❌ Erreur récupération classement niveau: {e}")
                return []
    
    def get_top_scores(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Top scores globaux - Hall of Fame"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT level, score, moves, pushes, time_seconds, timestamp, player_name
                    FROM scores 
                    ORDER BY score DESC, moves ASC, time_seconds ASC
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                conn.close()
                
                scores = []
                for i, result in enumerate(results, 1):
                    scores.append({
                        'rank': i,
                        'level': result[0],
                        'score': result[1],
                        'moves': result[2],
                        'pushes': result[3],
                        'time': result[4],
                        'timestamp': result[5],
                        'player': result[6]
                    })
                
                return scores
                
            except Exception as e:
                print(f"❌ Erreur récupération top scores: {e}")
                return []
    
    def save_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Sauvegarde progression - Checkpoint intelligent"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                board_state_json = json.dumps(progress_data['board_state'])
                
                cursor.execute('''
                    INSERT OR REPLACE INTO progress 
                    (level, moves, pushes, board_state)
                    VALUES (?, ?, ?, ?)
                ''', (progress_data['level'], progress_data['moves'], 
                      progress_data['pushes'], board_state_json))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur sauvegarde progression: {e}")
                return False
    
    def load_progress(self) -> Optional[Dict[str, Any]]:
        """Chargement progression - Restauration génie"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT level, moves, pushes, board_state
                    FROM progress 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                ''')
                
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    return {
                        'level': result[0],
                        'moves': result[1],
                        'pushes': result[2],
                        'board_state': json.loads(result[3])
                    }
                return None
                
            except Exception as e:
                print(f"❌ Erreur chargement progression: {e}")
                return None
    
    def clear_progress(self, level: int = None) -> bool:
        """Nettoyage progression - Reset intelligent"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                if level:
                    cursor.execute('DELETE FROM progress WHERE level = ?', (level,))
                else:
                    cursor.execute('DELETE FROM progress')
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur nettoyage progression: {e}")
                return False
    
    def save_preference(self, key: str, value: Any) -> bool:
        """Sauvegarde préférence - Personnalisation génie"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                value_json = json.dumps(value)
                cursor.execute('''
                    INSERT OR REPLACE INTO preferences (key, value)
                    VALUES (?, ?)
                ''', (key, value_json))
                
                conn.commit()
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur sauvegarde préférence: {e}")
                return False
    
    def load_preference(self, key: str, default_value: Any = None) -> Any:
        """Chargement préférence - Récupération personnalisée"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    return json.loads(result[0])
                return default_value
                
            except Exception as e:
                print(f"❌ Erreur chargement préférence: {e}")
                return default_value
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Statistiques globales - Analytics génie"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Statistiques générales
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_games,
                        COUNT(DISTINCT level) as levels_played,
                        AVG(score) as avg_score,
                        MAX(score) as best_score,
                        SUM(time_seconds) as total_time,
                        AVG(moves) as avg_moves,
                        AVG(pushes) as avg_pushes
                    FROM scores
                ''')
                
                stats = cursor.fetchone()
                conn.close()
                
                if stats:
                    return {
                        'total_games': stats[0] or 0,
                        'levels_played': stats[1] or 0,
                        'average_score': round(stats[2] or 0, 2),
                        'best_score': stats[3] or 0,
                        'total_time': stats[4] or 0,
                        'average_moves': round(stats[5] or 0, 2),
                        'average_pushes': round(stats[6] or 0, 2)
                    }
                
                return {}
                
            except Exception as e:
                print(f"❌ Erreur récupération statistiques: {e}")
                return {}
    
    def export_data(self, filepath: str) -> bool:
        """Export données - Sauvegarde complète"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                
                # Export vers fichier SQL
                with open(filepath, 'w', encoding='utf-8') as f:
                    for line in conn.iterdump():
                        f.write(f'{line}\n')
                
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur export données: {e}")
                return False
    
    def vacuum_database(self) -> bool:
        """Optimisation base de données - Maintenance génie"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                conn.execute('VACUUM')
                conn.close()
                return True
                
            except Exception as e:
                print(f"❌ Erreur optimisation BDD: {e}")
                return False
    
    def close(self):
        """Fermeture propre - Fin de session génie"""
        # Optimisation finale
        self.vacuum_database()
        print("✅ Base de données fermée proprement") 