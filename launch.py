#!/usr/bin/env python3

import os
import sys

def setup_database():
    """Configuration automatique de la base de données"""
    if not os.path.exists('database.py') and os.path.exists('database_simple.py'):
        print("📁 Configuration automatique de la base de données...")
        try:
            # Copie le fichier database_simple vers database
            with open('database_simple.py', 'r', encoding='utf-8') as src:
                content = src.read()
            with open('database.py', 'w', encoding='utf-8') as dst:
                dst.write(content)
            print("✅ Base de données configurée avec succès")
        except Exception as e:
            print(f"❌ Erreur configuration BDD: {e}")
            return False
    return True

def check_dependencies():
    """Vérification des dépendances"""
    required_modules = ['pygame', 'numpy']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Modules manquants: {', '.join(missing)}")
        print("📦 Installez-les avec: pip install pygame numpy")
        return False
    
    print("✅ Toutes les dépendances sont présentes")
    return True

def main():
    """Fonction principale de lancement"""
    print("🧠 SOKOBAN PYTHON GÉNIE - MODE 900 IQ 🧠")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_dependencies():
        sys.exit(1)
    
    if not setup_database():
        sys.exit(1)
    
    # Lancement du jeu
    try:
        print("🚀 Lancement du jeu...")
        from main import MainApp
        app = MainApp()
        app.run()
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous que tous les fichiers sont présents")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur d'exécution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 