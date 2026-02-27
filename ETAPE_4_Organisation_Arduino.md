# Étape 4 détaillée : Organiser vos sketches Arduino

## 1. Créer le dossier principal

Dans votre terminal, allez dans Documents (ou où vous voulez) :

```bash
cd ~/Documents

# Créer le dossier principal
mkdir Arduino-Projects

# Entrer dans le dossier
cd Arduino-Projects
```

## 2. Créer la structure des dossiers

Pour chaque projet Arduino, créez un sous-dossier :

```bash
# Créer quelques dossiers exemples
mkdir Blink
mkdir Temperature-Sensor
mkdir Robot-Control
```

## 3. Structure complète exemple

Voici à quoi doit ressembler votre dossier :

```
~/Documents/Arduino-Projects/
├── README.md                    (fichier principal)
├── .gitignore                   (fichier à créer)
├── Blink/
│   ├── Blink.ino               (votre sketch)
│   └── README.md               (description du projet)
├── Temperature-Sensor/
│   ├── Temperature-Sensor.ino
│   ├── schema.png              (schéma optionnel)
│   └── README.md
└── Robot-Control/
    ├── Robot-Control.ino
    ├── Motor.h                 (fichiers supplémentaires)
    ├── Motor.cpp
    └── README.md
```

## 4. Créer les fichiers - Méthode simple

### A. Créer le README.md principal

```bash
# Dans le dossier Arduino-Projects
cat > README.md << 'EOF'
# Mes Projets Arduino

Collection de mes sketches Arduino sauvegardés sur GitHub.

## Liste des projets

- **Blink** : LED qui clignote (exemple de base)
- **Temperature-Sensor** : Capteur de température DHT22
- **Robot-Control** : Contrôle de moteurs pour robot

## Comment utiliser

1. Ouvrir l'IDE Arduino
2. Fichier → Ouvrir → Sélectionner le dossier du projet
3. Téléverser sur l'Arduino

## Auteur
Il Camerlingo
EOF
```

### B. Créer le fichier .gitignore

```bash
cat > .gitignore << 'EOF'
# Fichiers compilés Arduino (inutiles à sauvegarder)
*.hex
*.elf
*.bin
*.eep

# Fichiers temporaires
*.tmp
*.log
*~

# Dossiers de l'IDE
build/

# OS
.DS_Store
Thumbs.db
EOF
```

### C. Créer un projet exemple (Blink)

```bash
# Créer le dossier Blink
cd Blink

# Créer le fichier Blink.ino
cat > Blink.ino << 'EOF'
// Blink.ino
// Fait clignoter la LED intégrée sur la broche 13

const int LED_PIN = 13;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);  // Allumer
  delay(1000);                  // Attendre 1 seconde
  digitalWrite(LED_PIN, LOW);   // Éteindre
  delay(1000);                  // Attendre 1 seconde
}
EOF

# Créer le README du projet
cat > README.md << 'EOF'
# Blink

## Description
Programme de base qui fait clignoter la LED intégrée de l'Arduino.

## Matériel
- Arduino Uno (ou compatible)
- LED intégrée sur broche 13 (pas de matériel externe)

## Schéma
Aucun, utilise juste la LED intégrée.

## Fonctionnement
La LED s'allume 1 seconde, s'éteint 1 seconde, en boucle.
EOF

# Revenir au dossier parent
cd ..
```

## 5. Si vous avez déjà des sketches existants

Déplacez-les dans la structure :

```bash
# Exemple : vous avez un sketch dans Téléchargements
mv ~/Téléchargements/MonProjet.ino ~/Documents/Arduino-Projects/MonProjet/

# Ou copier sans supprimer l'original
cp ~/Téléchargements/MonProjet.ino ~/Documents/Arduino-Projects/MonProjet/
```

## 6. Vérifier que tout est en place

```bash
# Lister le contenu
ls -la

# Vous devriez voir :
# - README.md
# - .gitignore
# - Blink/
# - Temperature-Sensor/
# - etc.

# Vérifier un projet spécifique
ls -la Blink/
# Devrait afficher : Blink.ino et README.md
```

## 7. Commande récapitulative (tout faire d'un coup)

Si vous voulez tout créer rapidement :

```bash
cd ~/Documents

# Créer la structure
mkdir -p Arduino-Projects/{Blink,Temperature-Sensor,Robot-Control}

# Créer le README principal
cd Arduino-Projects
cat > README.md << 'EOF'
# Mes Projets Arduino

Collection de mes projets Arduino.

## Projets
- Blink : LED clignotante
- Temperature-Sensor : Capteur DHT22
- Robot-Control : Contrôle moteurs
EOF

# Créer .gitignore
cat > .gitignore << 'EOF'
*.hex
*.elf
*.bin
.DS_Store
EOF

# Créer un exemple Blink
cd Blink
cat > Blink.ino << 'EOF'
const int LED = 13;

void setup() {
  pinMode(LED, OUTPUT);
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(1000);
  digitalWrite(LED, LOW);
  delay(1000);
}
EOF

echo "Structure créée !"
```

## 8. Ouvrir dans l'IDE Arduino

1. Ouvrez l'IDE Arduino
2. Fichier → Ouvrir...
3. Allez dans `Documents/Arduino-Projects/Blink/`
4. Sélectionnez `Blink.ino`
5. Vérifiez que ça compile (bouton ✓)

## Résumé visuel

```
Avant :                                    Après :

~/Documents/                              ~/Documents/Arduino-Projects/
├── sketch_jan12a.ino  ❌ (n'importe où)  ├── README.md
├── sketch_fev03b.ino  ❌                  ├── .gitignore
└── mon_projet.ino     ❌                  ├── Blink/
                                            │   ├── Blink.ino
                                            │   └── README.md
                                            └── ...
```

## Erreurs courantes à éviter

❌ **Ne pas faire :**
- Mettre des espaces dans les noms de dossiers : `Mon Projet/` → faire `MonProjet/`
- Mettre plusieurs .ino dans le même dossier
- Oublier le .gitignore (ça sauvegarde les fichiers inutiles)

✅ **À faire :**
- Un dossier = un projet
- Nom du dossier = nom du fichier .ino
- Toujours un README.md pour expliquer

---
**Vous êtes prêt pour l'étape 5 : le premier commit !**
