# TUTORIEL - Moteur Pas à Pas ESP32-S3-N16R8 (MODE AUTOMATIQUE)

**Date :** Mars 2026
**Plateforme :** MacBook Pro (Ghostty, Thonny, VSCode)
**Matériel :** ESP32-S3-N16R8 + ULN2003 + Moteur pas à pas 28BYJ-48
**Langage :** MicroPython
**Mode :** Automatique (Aller → Pause → Retour → Pause → Boucle)
**Auteur :** Bosley pour Il Camerlingo (corrections par Sonnet 4.6)

---

## 📋 SOMMAIRE

1. [Matériel nécessaire](#matériel-nécessaire)
2. [Schéma de câblage](#schéma-de-câblage)
3. [Installation MicroPython](#installation-micropython)
4. [Code Python - Mode Automatique](#code-python)
5. [Utilisation avec Thonny](#utilisation-avec-thonny)
6. [Tableau des vitesses](#tableau-des-vitesses)
7. [Dépannage](#dépannage)

---

## MATÉRIEL NÉCESSAIRE

| Composant | Quantité | Notes |
|-----------|----------|-------|
| ESP32-S3-N16R8 | 1 | 16MB Flash, 8MB PSRAM |
| Module ULN2003 | 1 | Driver pour moteur pas à pas |
| Moteur 28BYJ-48 | 1 | Moteur pas à pas 5V avec réducteur 1:64 |
| Câbles Dupont | 6 | Mâle-Femelle |
| Câble USB-C | 1 | Connexion MacBook → ESP32 |

### Caractéristiques du moteur 28BYJ-48
- **Angle par pas** : 5.625° (64 pas par tour moteur)
- **Réducteur** : 1:64
- **Pas par tour complet** : 64 × 64 = **2048 pas**
- **Tension** : 5V DC (fonctionne aussi en 3.3V avec moins de couple)
- **Couple** : ~34 mN.m

---

## SCHÉMA DE CÂBLAGE

### Connexion ESP32-S3-N16R8 → ULN2003

```
ESP32-S3-N16R8          ULN2003 Driver
    5V    ───────────────  VCC (alimentation moteur) ⚠️ IMPORTANT
    GND   ───────────────  GND
    
    GPIO4  ───────────────  IN1 (Blue)
    GPIO5  ───────────────  IN2 (Pink)
    GPIO6  ───────────────  IN3 (Yellow)
    GPIO7  ───────────────  IN4 (Orange)
    
ULN2003 ───────────────── Moteur 28BYJ-48 (connecteur blanc)
```

### ⚠️ IMPORTANT - Alimentation

**LE PLUS FREQUENT :** Le moteur ne fonctionne pas car branché sur **3V3** au lieu de **5V**.

| Broche | Tension | Résultat |
|--------|---------|----------|
| **3V3** | 3.3V | ❌ Moteur tourne faiblement ou pas du tout |
| **5V** | 5V | ✅ Fonctionnement nominal |
| **VIN** | 5V externe | ✅ Alternative si USB insuffisant |

**Sur ESP32-S3-N16R8 :** La broche **5V** est souvent à côté de **3V3** (près du connecteur USB-C).

### Tableau de connexion détaillé

| ULN2003 | Couleur fil | ESP32-S3 GPIO | Fonction |
|---------|-------------|---------------|----------|
| IN1 | Bleu | GPIO4 | Bobine A |
| IN2 | Rose | GPIO5 | Bobine B |
| IN3 | Jaune | GPIO6 | Bobine C |
| IN4 | Orange | GPIO7 | Bobine D |
| GND | Noir | GND | Masse |
| VCC | Rouge | **5V** (pas 3V3!) | Alimentation 5V |

### ⚠️ Pins à éviter sur ESP32-S3

**NE PAS UTILISER :**
- GPIO19-20 : USB natif (communication)
- GPIO26-32 : Flash interne
- GPIO33-37 : PSRAM (8MB)

**Pins recommandés :** GPIO0-5, GPIO6-18, GPIO21, GPIO35-48

---

## INSTALLATION MICROPYTHON

### Étape 1 : Installer esptool

```bash
# Sur Mac avec Homebrew
brew install esptool

# Vérifier l'installation
esptool version
```

### Étape 2 : Télécharger le firmware

**⚠️ IMPORTANT :** Le fichier doit faire ~1.5 Mo, pas 162 octets !

```bash
# Créer le répertoire de travail
mkdir -p ~/projects/esp32-stepper
cd ~/projects/esp32-stepper

# Télécharger le firmware ESP32-S3 (variante GENERIC_S3)
# Si curl échoue, télécharge manuellement depuis :
# https://micropython.org/download/ESP32_GENERIC_S3/

wget "https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20240105-v1.22.1.bin" \
  -O esp32s3-firmware.bin

# Vérifier la taille (doit faire ~1.5 Mo)
ls -lh esp32s3-firmware.bin
```

**Si le fichier fait moins de 1 Mo, il est corrompu.** Retélécharge-le manuellement depuis le site.

### Étape 3 : Flasher le firmware

```bash
# 1. Brancher l'ESP32-S3 en USB-C

# 2. Trouver le port
ls /dev/cu.usbmodem*
# Exemple : /dev/cu.usbmodem1101

# 3. Effacer la mémoire flash
esptool --chip esp32s3 --port /dev/cu.usbmodemXXX erase-flash

# 4. Flasher le firmware
esptool --chip esp32s3 --port /dev/cu.usbmodemXXX \
  write-flash -z 0x0 esp32s3-firmware.bin
```

**Résultat attendu :**
```
Hash of data verified.
Hard resetting via RTS pin...
```

### Étape 4 : Vérification

Ouvrir **Thonny** et vérifier que l'ESP32 répond au prompt `>>>`.

---

## CODE PYTHON

### Fichier 1 : `stepmotor.py` (Bibliothèque moteur)

**Créé par Sonnet 4.6 - Version professionnelle corrigée**

```python
"""
stepmotor.py - Pilote moteur pas-à-pas 28BYJ-48 via ULN2003
Compatible ESP32-S3 (MicroPython)
Adapté du tutoriel Freenove pour ESP32-S3-N16R8
Corrections par Sonnet 4.6 (Claude)
"""

from machine import Pin
import time

# Séquence 4 pas / 4 phases (full-step)
# Ordre des bobines : A -> B -> C -> D (sens horaire)
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]

# Séquence 4 pas / 8 phases (half-step) — plus douce, moins de bruit
HALF_STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]


class mystepmotor:
    """
    Contrôle un moteur pas-à-pas 28BYJ-48 via le driver ULN2003.

    Paramètres:
        pin_a, pin_b, pin_c, pin_d : numéros GPIO connectés à IN1, IN2, IN3, IN4 du ULN2003

    Constantes utiles:
        STEPS_PER_REV = 2048  (moteur 28BYJ-48 en full-step, rapport réduction 1:64)
                               En half-step : 4096 pas par tour
    """

    # 32 poles × 64 reduction ratio = 2048 full steps per revolution
    STEPS_PER_REV = 2048

    def __init__(self, pin_a, pin_b, pin_c, pin_d, half_step=False):
        self.pins = [
            Pin(pin_a, Pin.OUT),
            Pin(pin_b, Pin.OUT),
            Pin(pin_c, Pin.OUT),
            Pin(pin_d, Pin.OUT),
        ]
        self.half_step = half_step
        self.sequence = HALF_STEP_SEQUENCE if half_step else STEP_SEQUENCE
        self.seq_len = len(self.sequence)
        self.current_step = 0
        self.stop()

    def _set_coils(self, step_index):
        """Active les bobines selon l'index de séquence."""
        pattern = self.sequence[step_index % self.seq_len]
        for i, pin in enumerate(self.pins):
            pin.value(pattern[i])

    def moveSteps(self, direction, steps, us):
        """
        Fait tourner le moteur d'un nombre de pas donné.

        Args:
            direction (int): 1 = sens horaire, 0 = sens anti-horaire
            steps (int)    : nombre de pas à effectuer
            us (int)       : délai en microsecondes entre chaque pas
                             → plus grand = plus lent
                             → minimum ~2000 µs (2 ms) pour ce moteur
                             → valeur recommandée lente : 20000 µs (20 ms)
        """
        delta = 1 if direction else -1
        for _ in range(steps):
            self.current_step = (self.current_step + delta) % self.seq_len
            self._set_coils(self.current_step)
            time.sleep_us(us)
        # NOTE : on ne coupe PAS les bobines ici, le moteur tient en position

    def moveAround(self, direction, turns, us):
        """
        Fait tourner le moteur d'un nombre de tours complets.

        Args:
            direction (int): 1 = horaire, 0 = anti-horaire
            turns (int)    : nombre de tours
            us (int)       : délai µs entre chaque pas
        """
        steps_per_rev = self.seq_len * (self.STEPS_PER_REV // len(STEP_SEQUENCE))
        self.moveSteps(direction, steps_per_rev * turns, us)

    def moveAngle(self, direction, angle_deg, us):
        """
        Fait tourner le moteur d'un angle en degrés.

        Args:
            direction (int) : 1 = horaire, 0 = anti-horaire
            angle_deg (float): angle en degrés (ex: 90, 180, 360)
            us (int)        : délai µs entre chaque pas
        """
        steps = int(self.STEPS_PER_REV * angle_deg / 360)
        self.moveSteps(direction, steps, us)

    def stop(self):
        """Coupe toutes les bobines (désactive le moteur, plus de consommation)."""
        for pin in self.pins:
            pin.value(0)
```

### Fichier 2 : `main_stepper.py` (Programme principal)

```python
"""
main_stepper.py — Moteur pas-à-pas 28BYJ-48 + ULN2003 sur ESP32-S3-N16R8
Tutoriel Freenove adapté — Réglage vitesse et nombre de tours
Corrections par Sonnet 4.6 (Claude)
"""

from stepmotor import mystepmotor
import time

# ============================================================
#  BROCHAGE GPIO — ESP32-S3-N16R8
#  Modifiez ces valeurs selon votre câblage physique
#  ULN2003 :  IN1   IN2   IN3   IN4
#  ESP32-S3 : GPIO4 GPIO5 GPIO6 GPIO7  (exemple)
# ============================================================
PIN_IN1 = 4   # Bobine A
PIN_IN2 = 5   # Bobine B
PIN_IN3 = 6   # Bobine C
PIN_IN4 = 7   # Bobine D

# ============================================================
#  PARAMÈTRES FACILEMENT MODIFIABLES
# ============================================================

# --- Nombre de tours à effectuer dans chaque sens ---
NOMBRE_DE_TOURS = 10   # ← MODIFIEZ ICI (ex: 1, 5, 10)

# --- Vitesse : délai en microsecondes entre chaque pas ---
#   Plus la valeur est GRANDE → moteur plus LENT
#   Plus la valeur est PETITE → moteur plus RAPIDE
#
#   Repères pratiques :
#     2 000 µs  (2 ms)   = vitesse MAXIMALE (risque de pas perdus)
#     5 000 µs  (5 ms)   = vitesse rapide normale
#    10 000 µs  (10 ms)  = vitesse modérée
#    20 000 µs  (20 ms)  = LENTE — bonne pour observer les LED du ULN2003
#    50 000 µs  (50 ms)  = très lente, visible à l'œil nu clairement
#
#   VITESSE MINIMALE RECOMMANDÉE (la plus lente stable) : 20 000 µs
DELAI_US = 20000       # ← MODIFIEZ ICI pour changer la vitesse

# --- Pause entre les deux sens de rotation (millisecondes) ---
#   Appliquee apres le sens horaire ET apres le sens anti-horaire
#   2000 = 2 secondes | 5000 = 5 secondes | 0 = aucune pause
PAUSE_MS = 2000        # ← MODIFIEZ ICI

# --- Mode de pas ---
#   False = full-step  (2048 pas/tour, plus de couple)
#   True  = half-step  (4096 pas/tour, plus doux, moins de bruit)
HALF_STEP = False

# ============================================================
#  PROGRAMME PRINCIPAL
# ============================================================

print("=== Moteur pas-à-pas ESP32-S3 + ULN2003 ===")
print(f"Brochage : IN1=GPIO{PIN_IN1}, IN2=GPIO{PIN_IN2}, IN3=GPIO{PIN_IN3}, IN4=GPIO{PIN_IN4}")
print(f"Tours    : {NOMBRE_DE_TOURS}")
print(f"Vitesse  : {DELAI_US} µs / pas ({DELAI_US/1000:.1f} ms)")
print(f"Mode     : {'half-step' if HALF_STEP else 'full-step'}")
print()

# Création de l'objet moteur
moteur = mystepmotor(PIN_IN1, PIN_IN2, PIN_IN3, PIN_IN4, half_step=HALF_STEP)

try:
    while True:
        # --- Sens HORAIRE ---
        print(f"→ Rotation HORAIRE  : {NOMBRE_DE_TOURS} tour(s)...")
        moteur.moveAround(direction=1, turns=NOMBRE_DE_TOURS, us=DELAI_US)
        moteur.stop()
        print("  Pause...")
        time.sleep_ms(PAUSE_MS)

        # --- Sens ANTI-HORAIRE ---
        print(f"← Rotation ANTI-HORAIRE : {NOMBRE_DE_TOURS} tour(s)...")
        moteur.moveAround(direction=0, turns=NOMBRE_DE_TOURS, us=DELAI_US)
        moteur.stop()
        print("  Pause...")
        time.sleep_ms(PAUSE_MS)

except KeyboardInterrupt:
    moteur.stop()
    print("\nArrêt propre du moteur. Bobines coupées.")
```

---

## UTILISATION AVEC THONNY

### Configuration Thonny

1. **Ouvrir Thonny** (Applications → Thonny)
2. **Outils → Options → Interpréteur**
3. Sélectionner : **"MicroPython (ESP32)"**
4. Port : `/dev/cu.usbmodem*` (auto-détecté)
5. Cliquer **OK**

### Transfert et exécution

1. **Brancher** l'ESP32-S3 en USB-C
2. **Copier** les 2 fichiers dans Thonny :
   - `stepmotor.py` (bibliothèque)
   - `main_stepper.py` (programme principal)
3. **Modifier** les paramètres dans `main_stepper.py` si besoin :
   - `NOMBRE_DE_TOURS = 10`
   - `DELAI_US = 20000`
   - `PAUSE_MS = 2000`
   - `PIN_IN1 = 4` (etc. selon ton câblage)
4. **Fichier → Enregistrer sous → MicroPython device**
   - Nom : `stepmotor.py` puis `main_stepper.py`
5. Appuyer sur **F5** (ou icône ▶️ verte) pour exécuter `main_stepper.py`

### Arrêt d'urgence

Dans Thonny, cliquer sur **STOP** (icône rouge ⏹️) pour interrompre le programme.

---

## TABLEAU DES VITESSES

| Délai (µs) | Délai (ms) | Tours/min | Description | Usage recommandé |
|------------|------------|-----------|-------------|------------------|
| **2000** | 2 | ~15 | Vitesse MAXIMALE | ⚠️ Risque de pas perdus |
| **5000** | 5 | ~6 | Rapide | Vitesse normale |
| **10000** | 10 | ~3 | Modérée | Standard |
| **20000** | 20 | ~1.5 | LENTE | ⭐ Recommandé pour débuter |
| **50000** | 50 | ~0.6 | Très lente | Visible à l'œil nu |

### Exemples de configurations

**Configuration ultra-lente (test) :**
```python
NOMBRE_DE_TOURS = 1
DELAI_US = 50000
PAUSE_MS = 1000
```

**Configuration standard :**
```python
NOMBRE_DE_TOURS = 10
DELAI_US = 20000
PAUSE_MS = 2000
```

**Configuration rapide :**
```python
NOMBRE_DE_TOURS = 5
DELAI_US = 5000
PAUSE_MS = 1000
```

---

## DÉPANNAGE

### Le moteur ne tourne pas

**Vérifications obligatoires :**

1. ✅ **Alimentation 5V** (pas 3V3 !)
   - La LED rouge sur le module ULN2003 doit être allumée
   - Si pas de LED → Problème de 5V ou GND

2. ✅ **Câblage GPIO**
   - Vérifier chaque fil : GPIO4→IN1, GPIO5→IN2, GPIO6→IN3, GPIO7→IN4
   - Couleurs : Bleu, Rose, Jaune, Orange

3. ✅ **Moteur sur connecteur blanc**
   - Ordre des fils : Bleu, Rose, Jaune, Orange (de gauche à droite)

4. ✅ **Commencer lent**
   - `DELAI_US = 50000` (très lent) pour tester

### Le moteur tremble mais ne tourne pas

- Augmenter `DELAI_US` (ralentir)
- Vérifier l'ordre des fils sur le connecteur blanc
- Vérifier que les GPIO correspondent bien (4-5-6-7)

### Le moteur s'arrête en cours de route

- Réduire la vitesse (augmenter `DELAI_US`)
- Vérifier l'alimentation 5V (USB peut être insuffisant)
- Le moteur 28BYJ-48 consomme ~100mA

### Thonny ne détecte pas l'ESP32

```bash
# Lister les ports disponibles
ls /dev/cu.usbmodem* /dev/cu.usbserial-*

# Si vide, débrancher/rebrancher l'USB
# Ou redémarrer l'ESP32 avec bouton RST
```

### Programme ne démarre pas au boot

Renommer le fichier principal en **`main.py`** sur l'ESP32. Ce fichier s'exécute automatiquement au démarrage.

---

## MODIFICATIONS RAPIDES

### Changer le nombre de tours
```python
NOMBRE_DE_TOURS = 5  # Au lieu de 10
```

### Changer la vitesse
```python
DELAI_US = 30000  # Plus lent
# ou
DELAI_US = 10000  # Plus rapide
```

### Changer le temps de pause
```python
PAUSE_MS = 5000  # 5 secondes de pause
```

### Changer les pins GPIO
```python
PIN_IN1 = 12
PIN_IN2 = 13
PIN_IN3 = 14
PIN_IN4 = 15
```

### Activer le mode half-step (plus doux)
```python
HALF_STEP = True  # 4096 pas/tour, moins de bruit
```

---

## CRÉDITS

**Tutoriel original :** Freenove ESP32-S3
**Adaptation :** Bosley pour Il Camerlingo
**Corrections et améliorations :** Sonnet 4.6 (Claude)
**Date :** Mars 2026

---

## FICHIERS PRÊTS À L'EMPLOI

Les fichiers suivants sont prêts à être utilisés :
1. `stepmotor.py` — Bibliothèque de contrôle moteur
2. `main_stepper.py` — Programme principal avec paramètres modifiables

**Installation :**
1. Copier les 2 fichiers sur l'ESP32-S3 via Thonny
2. Modifier les paramètres dans `main_stepper.py` si nécessaire
3. Exécuter `main_stepper.py`

---

**Version finale validée — 14 mars 2026**
