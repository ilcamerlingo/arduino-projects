# TUTORIEL : Pousser un sketch Arduino avec bibliothèques sur GitHub

**Date de création :** 27 février 2026  
**Cas concret :** sketch_dec23c_ADRESSE_100_101 avec DCC_Decoder  
**Prérequis :** Repository GitHub `arduino-projects` déjà créé et initialisé

---

## 🎯 OBJECTIF

Déplacer un sketch Arduino (.ino) ainsi que ses bibliothèques associées (.h et .cpp) depuis le dossier `Arduino/libraries/` vers le repository GitHub, avec création d'un README.md.

---

## 📁 ÉTAPES DE LA PROCÉDURE

### ÉTAPE 1 : Se placer dans le bon dossier

```bash
cd ~/Documents/Arduino-Projects
```

**Vérification :** Vous devez voir vos autres projets (Blink, DCC_Basic_Acc_Decoder, etc.)

---

### ÉTAPE 2 : Créer le dossier du projet

**RÈGLE CRUCIALE :** Le dossier doit avoir le même nom que le fichier `.ino`

```bash
mkdir -p sketch_dec23c_ADRESSE_100_101
```

**Vérification :**
```bash
ls -la | grep sketch_dec23c
```

Vous devez voir : `drwxr-xr-x  sketch_dec23c_ADRESSE_100_101`

---

### ÉTAPE 3 : Localiser le fichier source

**IMPORTANT :** Le fichier peut ne pas être là où vous pensez.

**Méthode pour trouver le fichier :**
```bash
find /Users/ilcamerlingo/Documents/Arduino -name "*.ino" | grep -i dec23c
```

**Dans notre cas, le fichier était ici :**
```
/Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/sketch_dec23c_ADRESSE_100_101/sketch_dec23c_ADRESSE_100_101.ino
```

**Note :** Le dossier était directement dans `DCC_Decoder/`, PAS dans `DCC_Decoder/examples/` (erreur courante).

---

### ÉTAPE 4 : Copier le fichier .ino

```bash
cp /Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/sketch_dec23c_ADRESSE_100_101/sketch_dec23c_ADRESSE_100_101.ino sketch_dec23c_ADRESSE_100_101/
```

**Vérification :**
```bash
ls -la sketch_dec23c_ADRESSE_100_101/
```

Vous devez voir :
```
-rw-r--r--  sketch_dec23c_ADRESSE_100_101.ino
```

---

### ÉTAPE 5 : Copier les bibliothèques associées

Le sketch utilise la bibliothèque DCC_Decoder. Copier les fichiers .h et .cpp :

**Fichier header (.h) :**
```bash
cp /Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/DCC_Decoder.h sketch_dec23c_ADRESSE_100_101/
```

**Fichier source (.cpp) :**
```bash
cp /Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/DCC_Decoder.cpp sketch_dec23c_ADRESSE_100_101/
```

**Vérification :**
```bash
ls -la sketch_dec23c_ADRESSE_100_101/
```

Vous devez voir :
```
-rw-r--r--  DCC_Decoder.cpp
-rw-r--r--  DCC_Decoder.h
-rw-r--r--  sketch_dec23c_ADRESSE_100_101.ino
```

---

### ÉTAPE 6 : Créer le README.md

**Se placer dans le dossier du projet :**
```bash
cd sketch_dec23c_ADRESSE_100_101
```

**Créer le fichier README.md :**
```bash
cat > README.md << 'EOF'
# Sketch DCC - Adresses 100-101

## Description

Ce sketch Arduino permet de contrôler des accessoires de modélisme ferroviaire via le protocole DCC (Digital Command Control) sur les adresses 100 et 101.

## Fonctionnalités

- Décodage des signaux DCC
- Gestion des adresses 100 et 101
- Contrôle d'accessoires (aiguillages, signaux, éclairages)

## Matériel requis

- Arduino Uno (ou compatible)
- Shield DCC ou circuit de décodage DCC
- Alimentation DCC
- Accessoires à contrôler

## Bibliothèques utilisées

- DCC_Decoder : Bibliothèque de décodage DCC

## Installation

1. Copier ce dossier dans votre répertoire Arduino
2. Ouvrir le fichier .ino dans l'IDE Arduino
3. Téléverser sur l'Arduino

## Auteur

Il Camerlingo

## Date

Février 2026
EOF
```

**Vérification :**
```bash
ls -la
```

Vous devez voir :
```
-rw-r--r--  DCC_Decoder.cpp
-rw-r--r--  DCC_Decoder.h
-rw-r--r--  README.md
-rw-r--r--  sketch_dec23c_ADRESSE_100_101.ino
```

**Revenir au dossier parent :**
```bash
cd ..
```

---

### ÉTAPE 7 : Ajouter à Git

```bash
git add sketch_dec23c_ADRESSE_100_101/
```

**Vérifier ce qui est ajouté :**
```bash
git status
```

Vous devez voir :
```
Changes to be committed:
  new file:   sketch_dec23c_ADRESSE_100_101/DCC_Decoder.cpp
  new file:   sketch_dec23c_ADRESSE_100_101/DCC_Decoder.h
  new file:   sketch_dec23c_ADRESSE_100_101/README.md
  new file:   sketch_dec23c_ADRESSE_100_101/sketch_dec23c_ADRESSE_100_101.ino
```

---

### ÉTAPE 8 : Créer le commit

```bash
git commit -m "Add: sketch_dec23c_ADRESSE_100_101 avec bibliothèques DCC_Decoder"
```

**Si ça réussit, vous verrez :**
```
[main XXXXXXX] Add: sketch_dec23c_ADRESSE_100_101 avec bibliothèques DCC_Decoder
 4 files changed, XXX insertions(+)
 create mode 100644 sketch_dec23c_ADRESSE_100_101/DCC_Decoder.cpp
 create mode 100644 sketch_dec23c_ADRESSE_100_101/DCC_Decoder.h
 create mode 100644 sketch_dec23c_ADRESSE_100_101/README.md
 create mode 100644 sketch_dec23c_ADRESSE_100_101/sketch_dec23c_ADRESSE_100_101.ino
```

---

### ÉTAPE 9 : Pousser sur GitHub

```bash
git push origin main
```

**Si ça réussit, vous verrez :**
```
Enumerating objects:...
Writing objects: 100%...
To https://github.com/ilcamerlingo/arduino-projects
   XXXXXXX..XXXXXXX  main -> main
```

---

### ÉTAPE 10 : Vérifier sur GitHub

1. Ouvrir votre navigateur
2. Aller sur : https://github.com/ilcamerlingo/arduino-projects
3. Vérifier que le dossier `sketch_dec23c_ADRESSE_100_101/` existe
4. Cliquer pour voir les 4 fichiers

---

## ❌ RÉSOLUTION DES ERREURS

### Erreur : "No such file or directory"
**Cause :** Le chemin est incorrect
**Solution :** Utiliser `find` pour localiser le fichier
```bash
find /Users/ilcamerlingo/Documents/Arduino -name "*.ino" | grep -i nom_du_fichier
```

### Erreur : "zsh: no matches found"
**Cause :** Le caractère `*` est interprété par le shell
**Solution :** Copier fichier par fichier, sans utiliser `*`

### Erreur : "fatal: not a git repository"
**Cause :** Vous n'êtes pas dans Arduino-Projects
**Solution :**
```bash
cd ~/Documents/Arduino-Projects
```

### Erreur : "pathspec did not match any files"
**Cause :** Le fichier n'existe pas encore
**Solution :** Vérifier avec `ls -la` que le fichier est bien créé

### Erreur : "failed to push some refs"
**Cause :** Des changements sur GitHub ne sont pas en local
**Solution :**
```bash
git pull origin main
git push origin main
```

---

## 🚀 RÉCAPITULATIF DES COMMANDES (copier-coller rapide)

```bash
# 1. Se placer
cd ~/Documents/Arduino-Projects

# 2. Créer dossier
mkdir -p sketch_dec23c_ADRESSE_100_101

# 3. Copier .ino
cp /Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/sketch_dec23c_ADRESSE_100_101/sketch_dec23c_ADRESSE_100_101.ino sketch_dec23c_ADRESSE_100_101/

# 4. Copier bibliothèques
cp /Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/DCC_Decoder.h sketch_dec23c_ADRESSE_100_101/
cp /Users/ilcamerlingo/Documents/Arduino/libraries/DCC_Decoder/DCC_Decoder.cpp sketch_dec23c_ADRESSE_100_101/

# 5. Créer README
cd sketch_dec23c_ADRESSE_100_101
cat > README.md << 'EOF'
# Titre du projet

## Description
Description du projet

## Matériel
- Arduino
- Composants

## Auteur
Votre nom
EOF
cd ..

# 6. Git add
git add sketch_dec23c_ADRESSE_100_101/

# 7. Commit
git commit -m "Add: nom_du_projet"

# 8. Push
git push origin main
```

---

## 📝 POUR ADAPTER À UN AUTRE PROJET

1. **Remplacer le nom du dossier :**
   - `sketch_dec23c_ADRESSE_100_101` → `votre_nom_de_projet`

2. **Adapter le chemin source :**
   - Trouver avec `find` où se trouve votre fichier .ino

3. **Adapter les bibliothèques :**
   - Copier uniquement les fichiers .h et .cpp nécessaires

4. **Modifier le README :**
   - Adapter le titre, la description, le matériel

---

## ✅ CHECKLIST AVANT PUSH

- [ ] Dossier créé avec le même nom que le fichier .ino
- [ ] Fichier .ino copié
- [ ] Bibliothèques .h et .cpp copiées (si nécessaire)
- [ ] README.md créé
- [ ] `git add` effectué
- [ ] `git commit` avec message descriptif
- [ ] `git push origin main` réussi
- [ ] Vérification sur GitHub

---

**Document créé le :** 27 février 2026  
**Dernier projet traité :** sketch_dec23c_ADRESSE_100_101  
**Statut :** ✅ Procédure validée et fonctionnelle
