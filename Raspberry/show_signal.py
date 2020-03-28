import serial
import time

porta = serial.Serial("/dev/ttyACM0",9600)
i = 0
for i in range(10):
    resposta = porta.read(5)
    print(resposta.decode("utf-8"))
    time.sleep(0.3)

porta.close()
