"""
main_stepper.py — Moteur pas-à-pas 28BYJ-48 + ULN2003 sur ESP32-S3-N16R8
Tutoriel Freenove adapté — Réglage vitesse et nombre de tours
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
DELAI_US = 10000       # ← MODIFIEZ ICI pour changer la vitesse

# --- Pause entre les deux sens de rotation (millisecondes) ---
#   Appliquee apres le sens horaire ET apres le sens anti-horaire
#   2000 = 2 secondes | 5000 = 5 secondes | 0 = aucune pause
PAUSE_MS = 2000        # ← MODIFIEZ ICI

# --- Mode de pas ---
#   False = full-step  (2048 pas/tour, plus de couple)
#   True  = half-step  (4096 pas/tour, plus doux, moins de bruit)
HALF_STEP = True

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
