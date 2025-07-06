import os
import uuid

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QFileDialog, QHBoxLayout, QMessageBox,
    QRadioButton, QButtonGroup
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt

from database.product_dao import ProductDAO

# store thumbnails here
IMAGE_DIR = os.path.join(os.getcwd(), "product_images")
os.makedirs(IMAGE_DIR, exist_ok=True)


class ProductEditorDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product" if product else "Create Product")
        self.existing_product = product
        self.new_image_filename = None
        # display → stored category
        self._category_map = {
            "Fruits & Vegetables": "fruits_veg",
            "Manual":              "manual",
            "Barcode Only":        "barcode_only",
        }
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_edit = QLineEdit()
        form.addRow("Name:", self.name_edit)

        self.price_edit = QLineEdit()
        form.addRow("Price:", self.price_edit)

        self.barcode_edit = QLineEdit()
        form.addRow("Barcode:", self.barcode_edit)

        self.unit_edit = QComboBox()
        self.unit_edit.addItems(["kg", "pcs"])
        form.addRow("Unit:", self.unit_edit)

        # category radio-group
        cat_layout = QHBoxLayout()
        self.category_group = QButtonGroup(self)
        for idx, label in enumerate(self._category_map):
            rb = QRadioButton(label)
            if idx == 0:
                rb.setChecked(True)
            self.category_group.addButton(rb, id=idx)
            cat_layout.addWidget(rb)
        form.addRow("Category:", cat_layout)

        # image selection button
        self.image_btn = QPushButton("Select Image")
        self.image_btn.setIconSize(QSize(200, 200))
        self.image_btn.clicked.connect(self.browse_image)
        form.addRow("Image:", self.image_btn)

        layout.addLayout(form)

        # Save / Cancel
        btn_h = QHBoxLayout()
        btn_h.addStretch()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_product)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_h.addWidget(self.save_btn)
        btn_h.addWidget(self.cancel_btn)
        layout.addLayout(btn_h)

        if self.existing_product:
            self.name_edit.setText(self.existing_product.name)
            self.price_edit.setText(str(self.existing_product.price))
            self.barcode_edit.setText(self.existing_product.barcode or "")
            self.unit_edit.setCurrentText(self.existing_product.unit)
            category_key = self.existing_product.category
            for i, label in enumerate(self._category_map):
                if self._category_map[label] == category_key:
                    self.category_group.button(i).setChecked(True)
            if self.existing_product.image_path:
                image_path = os.path.join(IMAGE_DIR, self.existing_product.image_path)
                if os.path.exists(image_path):
                    self.image_btn.setIcon(QIcon(image_path))
                    self.image_btn.setText("")

    def browse_image(self):
        src_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not src_path:
            return

        # determine new random filename + keep ext
        ext = os.path.splitext(src_path)[1].lower()
        new_name = f"{uuid.uuid4().hex}{ext}"
        dst_path = os.path.join(IMAGE_DIR, new_name)

        # load, scale & save
        pix = QPixmap(src_path)
        if pix.isNull():
            QMessageBox.warning(self, "Error", "Could not load image.")
            return

        scaled = pix.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        if not scaled.save(dst_path):
            QMessageBox.warning(self, "Error", "Failed to save resized image.")
            return

        # remember the filename for DB, update button
        self.new_image_filename = new_name
        self.image_btn.setIcon(QIcon(dst_path))
        self.image_btn.setText("")  # remove text once image is set

    def save_product(self):
        name = self.name_edit.text().strip()
        price_txt = self.price_edit.text().strip()
        barcode = self.barcode_edit.text().strip() or None
        unit = self.unit_edit.currentText()
        image_filename = self.new_image_filename or None

        if not name or not price_txt:
            QMessageBox.warning(self, "Input Error", "Name and Price are required.")
            return

        try:
            price = float(price_txt)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Price must be a number.")
            return

        # determine selected category
        checked_id = self.category_group.checkedId()
        display_labels = list(self._category_map.keys())
        cat_label = display_labels[checked_id]
        category = self._category_map.get(cat_label, "barcode_only")

        dao = ProductDAO()
        try:
            if self.existing_product:
                dao.update(
                    self.existing_product.id,
                    name=name,
                    price=price,
                    barcode=barcode,
                    unit=unit,
                    category=category,
                    image_path=image_filename
                )
                QMessageBox.information(self, "Success", "Product updated.")
            else:
                dao.create(
                    name=name,
                    price=price,
                    barcode=barcode,
                    unit=unit,
                    image_path=image_filename,
                    category=category
                )
                QMessageBox.information(self, "Success", "Product created.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))