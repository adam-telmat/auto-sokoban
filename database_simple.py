"""
🧠 DATABASE SIMPLE - PERSISTANCE GÉNIE 🧠
Système de base de données SQLite simplifié
"""

import sqlite3
import json
from typing import List, Dict, Optional, Any
import threading

class Database:
    """Base de données - Mémoire persistante du génie"""
    
    def __init__(self, db_path: str = "sokoban_genius.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._create_tables()
        
    def _create_tables(self):
        """Création des tables"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
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
                
                conn.commit()
                conn.close()
                print("✅ Base de données initialisée")
                
            except Exception as e:
                print(f"❌ Erreur initialisation BDD: {e}")
    
    def save_score(self, level: int, score: int, moves: int, pushes: int, 
                   time_seconds: int, player_name: str = "Anonymous") -> bool:
        """Sauvegarde score"""
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
    
    def get_all_scores(self) -> List[Dict[str, Any]]:
        """Récupération tous les scores"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
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
        """Classement d'un niveau"""
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
                print(f"❌ Erreur récupération classement: {e}")
                return []
    
    def get_top_scores(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Top scores globaux"""
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
        """Sauvegarde progression"""
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
        """Chargement progression"""
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
    
    def close(self):
        """Fermeture propre"""
        print("✅ Base de données fermée") 