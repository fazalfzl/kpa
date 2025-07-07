import platform
import usb.core
import usb.util
from time import sleep
from escpos import printer

USBTMC_bInterfaceClass = 7
USBTMC_bInterfaceSubClass = 1

class PrinterTester:
    def __init__(self):
        self.p = None
        self.printer_initialized = False
        self.device = None

    def is_printer_initialized(self):
        """Check if the printer is already initialized."""
        return self.printer_initialized and self.p is not None

    def initialize_printer(self, idVendor, idProduct, inputEndPoint, outputEndPoint):
        if self.is_printer_initialized():
            print("✅ Printer is already initialized.")
            return

        try:
            self.p = printer.Usb(int(idVendor, 16), int(idProduct, 16),
                                 in_ep=int(inputEndPoint, 16),
                                 out_ep=int(outputEndPoint, 16))
            sleep(0.5)
            self.printer_initialized = True
            print("✅ Printer initialized.")
        except Exception as e:
            print("❌ Printer initialization failed:", e)

    def print_receipt(self, receipt_content):
        """Print the receipt with a bold header using ESC/POS commands."""
        if not self.is_printer_initialized():
            print("❌ Printer is not initialized. Cannot print.")
            return

        try:
            # Print the bold header
            self.p.set(bold=True)  # Enable bold text
            self.p.text("KPA STORES\n".center(40))  # Print the bold headline
            self.p.set(bold=False)  # Disable bold text

            # Print the rest of the receipt
            self.p.text(receipt_content + "\n")
            self.p.cut()
            print("✅ Receipt printed successfully with bold header.")
        except Exception as e:
            print(f"❌ Failed to print receipt: {e}")

    def stringtohex(self, strin):
        try:
            return hex(int(strin.strip(), 16))
        except Exception as e:
            print("ERROR at stringtohex:", e)
            return None

    def list_devices(self):
        def is_usbtmc_device(dev):
            try:
                for cfg in dev:
                    d = usb.util.find_descriptor(cfg,
                        bInterfaceClass=USBTMC_bInterfaceClass,
                        bInterfaceSubClass=USBTMC_bInterfaceSubClass)
                    return d is not None
            except Exception as e:
                print("ERROR in is_usbtmc_device:", e)
                return False

        try:
            return list(usb.core.find(find_all=True, custom_match=is_usbtmc_device))
        except Exception as e:
            print("ERROR in list_devices:", e)
            return []


    def test_printer(self):
        if not self.printer_initialized:
            print("❌ Printer is not initialized.")
            return

        try:
            self.p.text("Hello World\n")
            self.p.cut()
            print("✅ Hello World printed successfully.")
        except Exception as e:
            print("❌ Failed to print Hello World:", e)
        finally:
            self.cleanup()

    def cleanup(self):
        """Release USB resources and reset the printer."""
        if self.p:
            try:
                self.p.close()
            except Exception as e:
                print("⚠️ Error closing printer:", e)
        if self.device:
            try:
                usb.util.dispose_resources(self.device)
                print("✅ USB resources released.")
            except Exception as e:
                print("⚠️ Error releasing USB resources:", e)
        self.p = None
        self.device = None
        self.printer_initialized = False

    def run(self):
        if platform.system() == 'Windows':
            print("This script is for Linux (USB printer detection won't work on Windows).")
            return

        devices = self.list_devices()
        if not devices:
            print("❌ No USB printer devices found.")
            return

        for dev in devices:
            try:
                desc = str(dev)
                vens = "0x" + desc.split("idVendor", 1)[1].split("0x")[1].split(" ")[0]
                prods = "0x" + desc.split("idProduct", 1)[1].split("0x")[1].split(" ")[0]
                invals = "0x" + desc.split("bEndpointAddress", 2)[1].split("0x")[1].split(" ")[0]
                outvals = "0x" + desc.split("bEndpointAddress", 2)[2].split("0x")[1].split(" ")[0]
                idVendor = self.stringtohex(vens)
                idProduct = self.stringtohex(prods)
                inputEndPoint = self.stringtohex(invals)
                outputEndPoint = self.stringtohex(outvals)

                print(f"🖨️ Found USB device: Vendor={idVendor}, Product={idProduct}")
                self.device = dev
                self.initialize_printer(idVendor, idProduct, inputEndPoint, outputEndPoint)
                if self.printer_initialized:
                    break
            except Exception as e:
                print("⚠️ Error parsing device info:", e)