# 🎮 process_gameplay_clip.py

Script Python automatisé qui convertit un clip de jeu vidéo (format horizontal) en un format vertical 9:16, prêt pour TikTok, YouTube Shorts ou Instagram Reels.

## ⚙️ Fonctionnalités

- Découpe automatique du clip à 60s max
- Mise en page adaptative :
  - `Just Chatting` : plein écran vertical
  - Jeux : webcam en haut, gameplay en bas
- Ajout de texte (titre, streamer)
- Intégration d’une séquence de fin
- Export final avec audio original en 1080x1920

## 🧱 Structure du projet

.
├── assets/
│ ├── fond_short.png
│ └── fin_de_short.mp4
├── video.mp4 # Clip source
├── output.mp4 # Résultat généré
├── process_gameplay_clip.py
├── requirements.txt
└── .github/
└── workflows/
└── process_clip.yml

markdown
Copier
Modifier

## 🚀 Exécution locale

1. Installer Python 3.10+
2. Installer les dépendances :

```bash
pip install -r requirements.txt
Exécuter :

bash
Copier
Modifier
python process_gameplay_clip.py video.mp4 "Titre du clip" "Streamer" "Nom du jeu"
🐙 Exécution via GitHub Actions
Déclenchement manuel dans l’onglet Actions du dépôt.

Le fichier output.mp4 sera disponible en tant qu’artéfact téléchargeable.

🛠️ Dépendances
MoviePy

FFmpeg (installé automatiquement dans le workflow)