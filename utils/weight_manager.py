import platform
import threading
import time
import random
import serial

class WeightManager:
    def __init__(self):
        self._current_weight = 0.0
        self._running = False
        self._lock = threading.Lock()

    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._weight_loop, daemon=True).start()

    def stop(self):
        self._running = False

    def get_weight(self):
        with self._lock:
            return self._current_weight

    def _update_weight(self, new_weight):
        with self._lock:
            self._current_weight = new_weight

    def _weight_loop(self):
        if platform.system() == 'Windows':
            while self._running:
                fake_weight = round(random.uniform(1.000, 10.000), 3)
                self._update_weight(fake_weight)
                time.sleep(0.5)
        else:
            self._read_serial_loop()

    def _read_serial_loop(self):
        port_paths = ["/dev/ttyS0", "/dev/ttyAMA0"]
        serialport = None

        for port in port_paths:
            try:
                serialport = serial.Serial(port, 2400, timeout=1)
                break
            except Exception:
                continue

        if not serialport:
            print("⚠️ No valid serial port found")
            return

        try:
            while self._running:
                if serialport.read() == b'[':
                    data = serialport.read(8)
                    if data != b'/////00@':
                        try:
                            fullstring = data.decode("utf-8")
                            if "" in fullstring:
                                weight_str = fullstring[0:6]
                                weight_kg = float(weight_str) / 1000
                                self._update_weight(round(weight_kg, 3))
                        except:
                            continue
                serialport.flushInput()
        except Exception as e:
            print(f"❌ Serial read error: {e}")
        finally:
            serialport.close()
