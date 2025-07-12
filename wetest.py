import serial
ser = serial.Serial('COM3', 2400)

while True:
    # read 8 bytes from the serial port
    data = ser.read()
    print(data)
    # time.sleep(1)

