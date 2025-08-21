# ui/report/report_dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit
from PyQt5.QtCore import QDate
from core.services.bill_service import BillService
from datetime import datetime
class ReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sales Report")
        self.resize(800, 600)
        self.bill_service = BillService()
        self._build_ui()
        self._load_bills()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Filter controls
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("From:"))
        self.from_date = QDateEdit(QDate.currentDate().addDays(-7))
        self.from_date.setCalendarPopup(True)
        filter_layout.addWidget(self.from_date)

        filter_layout.addWidget(QLabel("To:"))
        self.to_date = QDateEdit(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        filter_layout.addWidget(self.to_date)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Bill ID or Customer")
        filter_layout.addWidget(self.search_input)

        self.filter_btn = QPushButton("Filter")
        self.filter_btn.clicked.connect(self._load_bills)
        filter_layout.addWidget(self.filter_btn)

        layout.addLayout(filter_layout)

        # Table for bills
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Bill ID", "Date", "Customer", "Total"])
        layout.addWidget(self.table)

        # Sales summary
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)



    def _load_bills(self):
        from_date = self.from_date.date().toPyDate()
        to_date = self.to_date.date().toPyDate()
        search = self.search_input.text().strip().lower()

        bills = []
        for b in self.bill_service.list_bills():
            # Convert string date to datetime.date
            try:
                bill_date = datetime.fromisoformat(b.date).date()
            except Exception:
                continue  # skip malformed dates

            if from_date <= bill_date <= to_date and (
                search in str(b.id).lower() or search in (b.customer_id or "").lower()
            ):
                bills.append((b, bill_date))

        self.table.setRowCount(len(bills))
        total_sales = 0
        for row, (bill, bill_date) in enumerate(bills):
            self.table.setItem(row, 0, QTableWidgetItem(str(bill.id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(bill.date)))
            self.table.setItem(row, 2, QTableWidgetItem(bill.customer_id or ""))
            self.table.setItem(row, 3, QTableWidgetItem(f"₹{bill.total:.2f}"))
            total_sales += bill.total

        self.summary_label.setText(f"Total Bills: {len(bills)} | Total Sales: ₹{total_sales:.2f}")