// Utilisation de la librairie DCC Decoder pour lire les trames DCC
#include "DCC_Decoder.h"

// Adresse de base du Arduino-Decodeur
#define baseAdresse 100  

// Déclaration des éléments par rapport aux broches de l'Arduino
const int Led_Verte = 3;
const int Led_Rouge = 4;

// Cette fonction est appelée par la librairie pour 
// chaque activation / désactivation au niveau des adresses
void BasicAccDecoderPacket_Handler(int address, boolean activate, byte data) {
  // Décodage standard de l'adresse DCC accessoire
  address -= 1;
  address *= 4;
  address += 1;
  address += (data & 0x06) >> 1;
  // address = address - 4; // à décommenter si nécessaire selon la centrale

  boolean enable = (data & 0x01) ? 1 : 0;

  Serial.print("Adresse : ");
  Serial.println(address);
  Serial.print("Enable : ");
  Serial.println(enable);

  switch (address) {

    // Adresse 100 : LED rouge
    case (baseAdresse):
      if (enable) {
        digitalWrite(Led_Rouge, HIGH);  // ON
      } else {
        digitalWrite(Led_Rouge, LOW);   // OFF
      }
      break;

    // Adresse 101 : LED verte
    case (baseAdresse + 1):
      if (enable) {
        digitalWrite(Led_Verte, HIGH);  // ON
      } else {
        digitalWrite(Led_Verte, LOW);   // OFF
      }
      break;

    // Tu peux ajouter ici d'autres adresses plus tard (baseAdresse + 2, etc.)
  }
}

void setup() {
  Serial.begin(9600);
  while (!Serial);
  Serial.println("C'est parti !");

  pinMode(Led_Rouge, OUTPUT);
  pinMode(Led_Verte, OUTPUT);

  // Au démarrage, les deux LEDs éteintes
  digitalWrite(Led_Rouge, LOW);
  digitalWrite(Led_Verte, LOW);

  // Initialisation de la librairie DCC Decoder
  DCC.SetBasicAccessoryDecoderPacketHandler(BasicAccDecoderPacket_Handler, true);
  DCC.SetupDecoder(0x00, 0x00, digitalPinToInterrupt(2));
}


volatile unsigned int interCount = 0;
const unsigned int periode = 1000; // toutes les secondes


void loop() {
  // Lecture continue des trames DCC
  DCC.loop();
}