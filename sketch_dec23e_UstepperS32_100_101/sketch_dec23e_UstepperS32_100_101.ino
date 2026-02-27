#include <UstepperS32.h>

UstepperS32 stepper;

// Entrées de commande
const uint8_t PIN_CW  = 2;   // Rotation horaire 180°
const uint8_t PIN_CCW = 3;   // Rotation antihoraire 180°

const long STEPS_180 = 25600L; // 180° avec 400 pas/tour

// Variables pour mémoriser l'état précédent
bool lastStateCW  = HIGH;
bool lastStateCCW = HIGH;

void setup(void)
{
  stepper.setup(CLOSEDLOOP, 400);
  stepper.checkOrientation(3.0);
  stepper.setMaxAcceleration(2);
  stepper.setMaxVelocity(5);
  stepper.setControlThreshold(15);
  Serial.begin(9600);

  pinMode(PIN_CW,  INPUT_PULLUP);   // Bouton vers GND
  pinMode(PIN_CCW, INPUT_PULLUP);
}

void loop(void)
{
  bool currentCW  = digitalRead(PIN_CW);
  bool currentCCW = digitalRead(PIN_CCW);

  // Front descendant sur PIN_CW : HIGH -> LOW
  if (lastStateCW == HIGH && currentCW == LOW) {
    stepper.moveSteps(STEPS_180);    // +180°
  }

  // Front descendant sur PIN_CCW : HIGH -> LOW
  if (lastStateCCW == HIGH && currentCCW == LOW) {
    stepper.moveSteps(-STEPS_180);   // -180°
  }

  // Mettre à jour les états précédents
  lastStateCW  = currentCW;
  lastStateCCW = currentCCW;

  // Petit délai pour limiter le rebond simple
  delay(20);
}