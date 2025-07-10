import serial

def serial_monitor():
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
            data = serialport.read(1)
            if data:
                print(data)
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    finally:
        serialport.close()

if __name__ == "__main__":
    serial_monitor()
