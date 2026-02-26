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
