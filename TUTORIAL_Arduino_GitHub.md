# Tutoriel : Sauvegarder ses sketches Arduino sur GitHub

## 1. Créer un compte et repository GitHub

1. Allez sur https://github.com
2. Créez un compte (gratuit)
3. Cliquez sur "New repository"
4. Nom : `arduino-projects` (ou autre)
5. Cochez "Add a README file"
6. Cliquez "Create repository"

## 2. Installer Git sur votre ordinateur

### Mac
```bash
# Git est souvent déjà installé, vérifiez :
git --version

# Sinon, installez via Homebrew :
brew install git
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install git
```

### Windows
Téléchargez sur https://git-scm.com/download/win

## 3. Configurer Git (une seule fois)

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"
```

## 4. Organiser vos sketches Arduino

Créez une structure propre :

```
Arduino-Projects/
├── README.md
├── libraries.txt          # Liste des librairies utilisées
├── Blink/
│   ├── Blink.ino
│   └── README.md          # Description du projet
├── Temperature-Sensor/
│   ├── Temperature-Sensor.ino
│   ├── schema.fzz         # Schéma Fritzing (optionnel)
│   └── README.md
└── Robot-Control/
    ├── Robot-Control.ino
    ├── Motor.cpp
    ├── Motor.h
    └── README.md
```

## 5. Initialiser le repository local

Dans votre dossier Arduino :

```bash
# Se placer dans le dossier
cd ~/Documents/Arduino-Projects

# Initialiser Git
git init

# Créer un fichier .gitignore
cat > .gitignore << 'EOF'
# Fichiers compilés
*.hex
*.elf
*.bin

# Fichiers temporaires
*.tmp
*.log

# IDE spécifiques
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit: Arduino projects backup"
```

## 6. Connecter à GitHub

Sur GitHub, copiez l'URL de votre repo (ex: `https://github.com/votrenom/arduino-projects.git`)

```bash
# Connecter au repository distant
git remote add origin https://github.com/votrenom/arduino-projects.git

# Pousser sur GitHub
git branch -M main
git push -u origin main
```

## 7. Mettre à jour régulièrement

### Après chaque modification :

```bash
# Voir les changements
git status

# Ajouter les fichiers modifiés
git add .

# Ou ajouter un fichier spécifique
git add MonProjet/MonProjet.ino

# Commit avec message descriptif
git commit -m "Fix: correction bug capteur température"

# Pousser sur GitHub
git push
```

créer un alias :

```alias arduino-push='cd ~/Documents/Arduino-Projects && git add . && git commit -m "Update: $(date)" && git push'```



```arduino-push```

## 8. Bonnes pratiques

### Messages de commit clairs :
```
"Add: nouveau projet robot suiveur de ligne"
"Fix: correction délai capteur ultrasonic"
"Update: amélioration précision PID"
"Doc: ajout schéma de câblage"
```

### README.md pour chaque projet :
```markdown
# Nom du Projet

## Description
Court texte expliquant ce que fait le projet

## Matériel nécessaire
- Arduino Uno
- Capteur DHT22
- Écran LCD 16x2
- etc.

## Librairies
- DHT sensor library by Adafruit
- LiquidCrystal_I2C by Frank de Brabander

## Schéma de câblage
![Schéma](schema.png)

## Utilisation
Explications pour utiliser le code
```

### Taguer les versions (releases) :
```bash
# Créer un tag pour une version stable
git tag -a v1.0 -m "Version 1.0 - Fonctionnelle"

# Pousser les tags
git push --tags
```

## 9. Récupérer sur une autre machine

```bash
# Cloner le repository
git clone https://github.com/votrenom/arduino-projects.git

# Ouvrir dans l'IDE Arduino
# Fichier → Ouvrir → Sélectionner le dossier du projet
```

## 10. Sauvegarde automatique (optionnel)

### Avec un script bash (`backup-arduino.sh`) :

```bash
#!/bin/bash
cd ~/Documents/Arduino-Projects
git add .
git commit -m "Backup: $(date '+%Y-%m-%d %H:%M')"
git push origin main
echo "Backup terminé !"
```

Rendez exécutable : `chmod +x backup-arduino.sh`

### Exécuter automatiquement (cron Mac/Linux) :
```bash
# Éditer crontab
crontab -e

# Ajouter ligne pour backup quotidien à 18h
0 18 * * * /chemin/vers/backup-arduino.sh
```

---

## Résumé des commandes essentielles

| Action | Commande |
|--------|----------|
| Voir l'état | `git status` |
| Ajouter fichiers | `git add .` |
| Sauvegarder | `git commit -m "message"` |
| Envoyer sur GitHub | `git push` |
| Récupérer | `git pull` |
| Voir l'historique | `git log --oneline` |

---

**Conseil :** Committez souvent, poussez régulièrement !
