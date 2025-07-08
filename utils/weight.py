import platform
import serial
import glob

def find_serial_port():
    if platform.system() == 'Linux':
        ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyS*')
        for port in ports:
            try:
                return serial.Serial(port, 2400, timeout=10)
            except Exception:
                continue
    elif platform.system() == 'Windows':
        return None
    return None

def weight():
    serialport = find_serial_port()
    if serialport is None:
        print("No valid serial port found")
        return None  # Return None if no serial port is found

    try:
        while True:
            try:
                if serialport.read() == b'[':
                    command = serialport.read(size=8)
                    fullstring = '000000'

                    if command != b'/////00@':
                        try:
                            fullstring = command.decode("utf-8")
                        except:
                            continue

                        if "" in fullstring:
                            fullstring = fullstring[0:6]
                        else:
                            fullstring = "000000"

                    try:
                        kilo = float(fullstring) / 1000
                        serialport.flushInput()
                        return kilo  # Return the weight in kilograms
                    except Exception as e:
                        print("Conversion error: " + str(e))
                        return None
            except Exception as e:
                print("Exception in serial read loop: " + str(e))
                serialport.close()
                return None
    except Exception as e:
        print("Exception in weight thread: " + str(e))
        return None

if __name__ == "__main__":
    weight()
