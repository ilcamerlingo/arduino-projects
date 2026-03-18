"""
stepmotor.py - Pilote moteur pas-à-pas 28BYJ-48 via ULN2003
Compatible ESP32-S3 (MicroPython)
Adapté du tutoriel Freenove pour ESP32-S3-N16R8
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
