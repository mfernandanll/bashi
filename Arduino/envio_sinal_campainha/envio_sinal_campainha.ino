int analogPin = A1;
int leitura_sinal = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  leitura_sinal = analogRead(analogPin);

//  if (Serial.available() > 0) {
//    Serial.write(leitura_sinal);
//  }
//  Serial.print(leitura_sinal);
//  delay(500);
//  if (leitura_sinal > 50){
//    Serial.println("Campainha tocando");
//
//    if (Serial.available() > 0){
//     Serial.write(leitura_sinal);
//    }
//
//  }
//  Serial.print(" d: ");
  Serial.print((String)leitura_sinal);
//  Serial.println();
  delay(300);
}
