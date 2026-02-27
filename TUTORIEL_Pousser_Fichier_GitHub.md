# TUTORIEL - Pousser un fichier sur GitHub

**Objectif :** Envoyer un fichier (tutoriel, code, document) sur votre repository GitHub  
**Date :** 27 février 2026  
**Niveau :** Débutant

---

## 📋 AVANT DE COMMENCER

### Ce dont vous avez besoin
- Un fichier à envoyer (ex: `mon_tutoriel.md`)
- Le fichier doit être dans votre dossier `Downloads` ou sur le Bureau
- Votre repository GitHub déjà créé (ex: `arduino-projects`)

### Prérequis
- Git configuré sur votre Mac (déjà fait)
- Repository initialisé (déjà fait)

---

## ÉTAPE 1 : Se placer dans le bon dossier

**Ouvrir le Terminal** et taper :

```bash
cd ~/Documents/Arduino-Projects
```

**Vérification :** Vous devez voir vos autres projets quand vous faites `ls`

---

## ÉTAPE 2 : Copier le fichier depuis Downloads

**Si votre fichier est dans Téléchargements :**

```bash
mv ~/Downloads/NOM_DU_FICHIER.md .
```

**Remplacer** `NOM_DU_FICHIER.md` par le vrai nom du fichier.

**Exemple concret :**
```bash
mv ~/Downloads/ETAPE_4_Organisation_Arduino.md .
```

**Vérification :** Le fichier doit apparaître quand vous faites `ls`

---

## ÉTAPE 3 : Ajouter le fichier à Git

```bash
git add NOM_DU_FICHIER.md
```

**Exemple :**
```bash
git add ETAPE_4_Organisation_Arduino.md
```

**Cette commande dit à Git :** "Je veux sauvegarder ce fichier"

---

## ÉTAPE 4 : Créer un commit (snapshot)

```bash
git commit -m "Add: description_du_fichier"
```

**Exemple :**
```bash
git commit -m "Add: Tutoriel organisation Arduino étape 4"
```

**Cette commande dit :** "Je valide ces changements avec un message"

**Conseil pour le message :**
- Commencer par "Add: " si c'est un nouveau fichier
- Décrire brièvement ce que contient le fichier
- Exemples : "Add: Guide installation", "Add: Documentation projet X"

---

## ÉTAPE 5 : Envoyer sur GitHub

```bash
git push origin main
```

**Cette commande dit :** "J'envoie tout sur GitHub"

**Si ça demande un mot de passe :**
- Entrer votre **Personal Access Token** (pas votre mot de passe GitHub)
- Le token ressemble à : `ghp_xxxxxxxxxxxxxxxxxxxx`

---

## ÉTAPE 6 : Vérifier sur GitHub

1. Ouvrir votre navigateur
2. Aller sur : https://github.com/ilcamerlingo/arduino-projects
3. Rafraîchir la page (F5 ou Cmd+R)
4. Vous devez voir votre fichier dans la liste !

---

## 📋 RÉCAPITULATIF DES COMMANDES

```bash
# 1. Se placer dans le dossier
cd ~/Documents/Arduino-Projects

# 2. Copier le fichier depuis Downloads
mv ~/Downloads/NOM_DU_FICHIER.md .

# 3. Ajouter à Git
git add NOM_DU_FICHIER.md

# 4. Créer le commit
git commit -m "Add: description"

# 5. Pousser sur GitHub
git push origin main
```

---

## ❌ RÉSOLUTION DES ERREURS

### "No such file or directory"
**Problème :** Le fichier n'est pas dans Downloads  
**Solution :** Chercher où est le fichier :
```bash
find ~ -name "NOM_DU_FICHIER.md" 2>/dev/null
```
Puis utiliser le chemin trouvé.

### "fatal: not a git repository"
**Problème :** Vous n'êtes pas dans le bon dossier  
**Solution :**
```bash
cd ~/Documents/Arduino-Projects
```

### "pathspec did not match any files"
**Problème :** Le nom de fichier est incorrect  
**Solution :** Vérifier le nom exact avec :
```bash
ls ~/Downloads/
```

### "failed to push some refs"
**Problème :** Des changements sur GitHub ne sont pas en local  
**Solution :**
```bash
git pull origin main
git push origin main
```

---

## ✅ CHECKLIST AVANT PUSH

- [ ] Je suis dans `~/Documents/Arduino-Projects`
- [ ] Le fichier est bien copié depuis Downloads
- [ ] J'ai fait `git add` avec le bon nom de fichier
- [ ] J'ai fait `git commit` avec un message clair
- [ ] J'ai fait `git push origin main`
- [ ] Je vois le fichier sur GitHub

---

## 🎯 EXERCICE PRATIQUE

**Maintenant, essayez avec ce tutoriel même !**

1. Téléchargez ce fichier (si vous l'avez reçu par Telegram)
2. Suivez les 5 étapes ci-dessus
3. Vérifiez sur GitHub que le fichier est bien là

**Si ça marche :** Bravo, vous maîtrisez Git ! 🎉

**Si ça ne marche pas :** Recommencez en vérifiant chaque étape.

---

*Créé le : 27 février 2026*  
*Par : Bosley*  
*Pour : Il Camerlingo*
