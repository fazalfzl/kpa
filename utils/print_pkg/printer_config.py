import platform
from datetime import datetime

from escpos.printer import Usb
import usb.core
import usb.util
from time import sleep
from escpos import printer
from utils.logger import get_logger
log = get_logger(__name__)

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
            log.info("✅ Printer is already initialized.")
            return

        try:
            self.p = printer.Usb(int(idVendor, 16), int(idProduct, 16),
                                 in_ep=int(inputEndPoint, 16),
                                 out_ep=int(outputEndPoint, 16))
            sleep(0.5)
            self.printer_initialized = True
            log.info("✅ Printer initialized.")
        except Exception as e:
            log.info("❌ Printer initialization failed:", e)

    def print_receipt(self, receipt_content ,total):
        """Print the receipt with a bold header using ESC/POS commands."""
        if not self.is_printer_initialized():
            log.info("❌ Printer is not initialized. Cannot print.")
            return

        try:
            self.p._raw(b'\x1B\x40')  # Reset printer
            # Set default text style
            self.p._raw(b'\x1b\x45\x00')  # Disable bold
            self.p._raw(b'\x1b\x61\x00')  # Align left
            self.p._raw(b'\x1b\x21\x00')  # Font A, no double width, no double height

            # Print the date and time
            self.p.text(datetime.now().strftime("%Y-%m-%d \n%H:%M:%S\n"))

            # Set bold and centered for the header, with Font B
            self.p._raw(b'\x1b\x45\x01')  # Enable bold
            self.p._raw(b'\x1b\x61\x01')  # Align center
            self.p._raw(b'\x1b\x21\x31')  # Font B, double width, double height

            # Print the bold header with Font B
            self.p._raw(b'\x1b\x61\x01')  # Align center
            self.p.image('three.jpg')  # Path to the image

            # Reset to normal text style
            self.p._raw(b'\x1B\x40')  # Reset printer
            self.p._raw(b'\x1b\x45\x00')  # Disable bold
            self.p._raw(b'\x1b\x61\x00')  # Align left
            # self.p._raw(b'\x1b\x21\x10')  # Font A, no double width, double height
            self.p._raw(b'\x1b\x21\x00')  # Font A, no double width, no double height
            # Print the rest of the receipt
            self.p.text(receipt_content + "\n")

            # Print the total amount
            # bold , centered, Font B
            self.p._raw(b'\x1b\x45\x01')  # Enable bold
            self.p._raw(b'\x1b\x61\x01')  # Align center
            self.p._raw(b'\x1b\x21\x31')  # Font B, double width, double height
            self.p.text(f"TOTAL: {total:.2f}\n")

            # Cut the paper
            self.p.cut()
            # log.info("✅ Receipt printed successfully with bold header in Font B.")
            # self.p._raw(b'\x1B\x70\x00\x19\xFA')
        except Exception as e:
            log.exception(f"❌ Failed to print receipt: {e}")

    def open_cash_drawer(self):
        if self.printer_tester.is_printer_initialized():
            self.printer_tester.p._raw(b'\x1B\x70\x00\x19\xFA')
            log.info("✅ Cash drawer opened from title bar button.")
        else:
            log.info("❌ Printer not initialized. Cannot open cash drawer.")

    def stringtohex(self, strin):
        try:
            return hex(int(strin.strip(), 16))
        except Exception as e:
            log.exception("ERROR at stringtohex:", e)
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
                log.exception("ERROR in is_usbtmc_device:", e)
                return False

        try:
            return list(usb.core.find(find_all=True, custom_match=is_usbtmc_device))
        except Exception as e:
            log.exception("ERROR in list_devices:", e)
            return []

    def test_printer(self):
        if not self.printer_initialized:
            log.error("❌ Printer is not initialized.")
            return

        try:
            self.p.text("Hello World\n")
            self.p.cut()
            log.info("✅ Hello World printed successfully.")
        except Exception as e:
            log.error("❌ Failed to print Hello World:", e)
        finally:
            self.cleanup()

    def cleanup(self):
        """Release USB resources and reset the printer."""
        if self.p:
            try:
                self.p.close()
            except Exception as e:
                log.error("⚠️Error closing printer:", e)
        if self.device:
            try:
                usb.util.dispose_resources(self.device)
                log.info("✅ USB resources released.")
            except Exception as e:
                log.error("⚠️Error releasing USB resources:", e)
        self.p = None
        self.device = None
        self.printer_initialized = False

    def run(self):
        if platform.system() == 'Windows':
            log.info("This script is for Linux (USB printer detection won't work on Windows).")
            # Output Endpoint Address: 0x1
            # Input Endpoint Address: 0x81
            vendor_id = self.stringtohex("0x0483")
            product_id = self.stringtohex("0x5743")
            in_ep = self.stringtohex("0x81")  # IN endpoint
            out_ep = self.stringtohex("0x1")  # OUT endpoint

            VENDOR_ID = 0x0483  # Example Epson printer
            PRODUCT_ID = 0x5743  # Example Epson printer
            self.device = Usb(VENDOR_ID, PRODUCT_ID)

            if self.device is None:
                log.info("❌ USB printer not found.")
                return

            self.initialize_printer(vendor_id, product_id, in_ep, out_ep)

            return

        devices = self.list_devices()
        if not devices:
            log.info("❌ No USB printer devices found.")
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

                log.info(f"🖨️ Found USB device: Vendor={idVendor}, Product={idProduct}")
                self.device = dev
                self.initialize_printer(idVendor, idProduct, inputEndPoint, outputEndPoint)
                if self.printer_initialized:
                    break
            except Exception as e:
                log.error("⚠️Error parsing device info:", e)
