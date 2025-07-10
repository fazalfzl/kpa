import serial
import time

def read_weight():
    port_paths = ["/dev/ttyUSB0", "/dev/ttyAMA0"]
    serialport = None

    for port in port_paths:
        try:
            serialport = serial.Serial(port, 2400, timeout=1)
            print(f"✅ Connected to: {port}")
            break
        except Exception:
            continue

    if not serialport:
        print("❌ No valid serial port found.")
        return

    try:
        while True:
            if serialport.read() == b'[':
                data = serialport.read(8)
                if data != b'/////00@':
                    try:
                        decoded = data.decode("utf-8")
                        if "" in decoded:
                            weight_str = decoded[0:6]
                            weight = float(weight_str) / 1000
                            print(f"Weight: {weight:.3f} kg")
                    except Exception:
                        continue
            serialport.flushInput()
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    finally:
        serialport.close()

if __name__ == "__main__":
    read_weight()
