#!/usr/bin/env python3
"""
Color Picker GUI with eyedropper tool.
Displays Hex, RGB, HSV values.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QColorDialog, QVBoxLayout,
    QHBoxLayout, QGridLayout, QDialog
)
from PySide6.QtGui import QColor, QPixmap, QFont, QIcon
from PySide6.QtCore import Qt

# For color name detection
try:
    import webcolors
    from webcolors import CSS3_NAMES_TO_HEX
except ImportError:
    webcolors = None
    CSS3_NAMES_TO_HEX = {}

class EyeDropperDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setModal(True)
        # Grab screenshot before showing overlay
        screen = QApplication.primaryScreen()
        self.pixmap = screen.grabWindow(0)
        self.image = self.pixmap.toImage()
        # Display screenshot scaled to full screen
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.label.setScaledContents(True)
        # Layout to fill entire screen
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        # Fullscreen overlay
        self.showFullScreen()
        self.selected_color = None
        self.setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            # Map pos to original image coords
            x = pos.x() * self.image.width() // self.label.width()
            y = pos.y() * self.image.height() // self.label.height()
            x = max(0, min(x, self.image.width() - 1))
            y = max(0, min(y, self.image.height() - 1))
            pixel = self.image.pixel(x, y)
            self.selected_color = QColor(pixel)
        self.accept()

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()
        # Window icon
        self.setWindowIcon(QIcon(r"d:/Ez-Color-Xs/icon128.png"))
        self.setWindowTitle("EZ Color Picker By Xs")
        self.resize(400, 300)
        self.color = QColor(255, 255, 255, 255)

        # Preview
        self.preview = QLabel()
        self.preview.setObjectName("preview")
        self.preview.setFixedSize(150, 150)
        self.preview.setStyleSheet(f"background-color: {self.color.name().upper()}")

        # Labels
        self.hex_label = QLabel()
        self.rgb_label = QLabel()
        self.hsl_label = QLabel()
        self.hsv_label = QLabel()
        self.cmyk_label = QLabel()
        self.hsb_label = QLabel()
        self.decimal_label = QLabel()
        self.name_label = QLabel()

        # Buttons
        btn_dialog = QPushButton("Pick Color...")
        btn_dialog.clicked.connect(self.open_color_dialog)
        btn_eyedrop = QPushButton("Eyedropper")
        btn_eyedrop.clicked.connect(self.open_eyedropper)

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_dialog)
        btn_layout.addWidget(btn_eyedrop)

        # Main layout: preview and data
        main_layout = QVBoxLayout(self)
        # Top: preview and data
        body_layout = QHBoxLayout()
        body_layout.addWidget(self.preview)
        # Data grid
        data_layout = QGridLayout()
        data_layout.setColumnStretch(1, 1)
        data_layout.setHorizontalSpacing(20)
        data_layout.setVerticalSpacing(10)
        # Create copy buttons for each property
        self.hex_copy_btn = QPushButton("Copy")
        self.hex_copy_btn.setFixedSize(24, 24)
        self.hex_copy_btn.clicked.connect(lambda _, lbl=self.hex_label: QApplication.clipboard().setText(lbl.text()))
        self.rgb_copy_btn = QPushButton("Copy")
        self.rgb_copy_btn.setFixedSize(24, 24)
        self.rgb_copy_btn.clicked.connect(lambda _, lbl=self.rgb_label: QApplication.clipboard().setText(lbl.text()))
        self.hsl_copy_btn = QPushButton("Copy")
        self.hsl_copy_btn.setFixedSize(24, 24)
        self.hsl_copy_btn.clicked.connect(lambda _, lbl=self.hsl_label: QApplication.clipboard().setText(lbl.text()))
        self.hsv_copy_btn = QPushButton("Copy")
        self.hsv_copy_btn.setFixedSize(24, 24)
        self.hsv_copy_btn.clicked.connect(lambda _, lbl=self.hsv_label: QApplication.clipboard().setText(lbl.text()))
        self.cmyk_copy_btn = QPushButton("Copy")
        self.cmyk_copy_btn.setFixedSize(24, 24)
        self.cmyk_copy_btn.clicked.connect(lambda _, lbl=self.cmyk_label: QApplication.clipboard().setText(lbl.text()))
        self.hsb_copy_btn = QPushButton("Copy")
        self.hsb_copy_btn.setFixedSize(24, 24)
        self.hsb_copy_btn.clicked.connect(lambda _, lbl=self.hsb_label: QApplication.clipboard().setText(lbl.text()))
        self.decimal_copy_btn = QPushButton("Copy")
        self.decimal_copy_btn.setFixedSize(24, 24)
        self.decimal_copy_btn.clicked.connect(lambda _, lbl=self.decimal_label: QApplication.clipboard().setText(lbl.text()))
        self.name_copy_btn = QPushButton("Copy")
        self.name_copy_btn.setFixedSize(24, 24)
        self.name_copy_btn.clicked.connect(lambda _, lbl=self.name_label: QApplication.clipboard().setText(lbl.text()))
        # Populate grid
        fields = [
            ("HEX", self.hex_label, self.hex_copy_btn),
            ("RGB", self.rgb_label, self.rgb_copy_btn),
            ("HSL", self.hsl_label, self.hsl_copy_btn),
            ("HSV", self.hsv_label, self.hsv_copy_btn),
            ("CMYK", self.cmyk_label, self.cmyk_copy_btn),
            ("HSB", self.hsb_label, self.hsb_copy_btn),
            ("Decimal", self.decimal_label, self.decimal_copy_btn),
            ("Name", self.name_label, self.name_copy_btn),
        ]
        for i, (title, label, btn) in enumerate(fields):
            title_lbl = QLabel(f"{title}:")
            title_lbl.setFont(QFont('', weight=QFont.Bold))
            data_layout.addWidget(title_lbl, i, 0)
            data_layout.addWidget(label, i, 1)
            data_layout.addWidget(btn, i, 2)
        body_layout.addLayout(data_layout)
        main_layout.addLayout(body_layout)
        # Bottom: buttons
        btn_layout.setSpacing(20)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addLayout(btn_layout)
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)

        self.update_labels()

    def update_labels(self):
        r = self.color.red()
        g = self.color.green()
        b = self.color.blue()
        a = self.color.alpha()
        # Normalized RGB
        r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
        # HSV
        h_hsv, s_hsv, v_hsv, _ = self.color.getHsv()
        s_hsv_pct = s_hsv / 2.55
        v_hsv_pct = v_hsv / 2.55
        # HSL
        h_hsl, s_hsl, l, _ = self.color.getHsl()
        s_hsl_pct = s_hsl / 2.55
        l_pct = l / 2.55
        # CMYK
        k = 1 - max(r_norm, g_norm, b_norm)
        if k < 1:
            c = (1 - r_norm - k) / (1 - k)
            m = (1 - g_norm - k) / (1 - k)
            y = (1 - b_norm - k) / (1 - k)
        else:
            c = m = y = 0
        c_pct, m_pct, y_pct, k_pct = c*100, m*100, y*100, k*100
        # Decimal
        decimal_val = (r << 16) + (g << 8) + b
        # Color Name
        if webcolors:
            try:
                name = webcolors.rgb_to_name((r, g, b))
            except ValueError:
                min_colours = {}
                for key, hex_val in CSS3_NAMES_TO_HEX.items():
                    r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
                    dist = (r_c - r)**2 + (g_c - g)**2 + (b_c - b)**2
                    min_colours[dist] = key
                name = min_colours[min(min_colours.keys())]
        else:
            name = "Unknown"
        # Hex and Preview
        hex_rgb = f"#{r:02X}{g:02X}{b:02X}"
        self.preview.setStyleSheet(f"background-color: {hex_rgb}")
        # Set Labels
        self.hex_label.setText(f"HEX: {hex_rgb}")
        self.rgb_label.setText(f"RGB: {r}, {g}, {b}")
        self.hsl_label.setText(f"HSL: {h_hsl}°, {s_hsl_pct:.1f}%, {l_pct:.1f}%")
        self.hsv_label.setText(f"HSV: {h_hsv}°, {s_hsv_pct:.1f}%, {v_hsv_pct:.1f}%")
        self.cmyk_label.setText(f"CMYK: {c_pct:.1f}%, {m_pct:.1f}%, {y_pct:.1f}%, {k_pct:.1f}%")
        self.hsb_label.setText(f"HSB: {h_hsv}°, {s_hsv_pct:.1f}%, {v_hsv_pct:.1f}%")
        self.decimal_label.setText(f"Decimal: {decimal_val}")
        self.name_label.setText(f"Name: {name}")

    def open_color_dialog(self):
        col = QColorDialog.getColor(self.color, self, options=QColorDialog.ShowAlphaChannel)
        if col.isValid():
            self.color = col
            self.update_labels()

    def open_eyedropper(self):
        self.hide()
        dlg = EyeDropperDialog(self)
        if dlg.exec():
            if dlg.selected_color:
                self.color = dlg.selected_color
                self.update_labels()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Futuristic dark theme styling
    app.setStyleSheet("""
QWidget {
    background-color: #f7f9fc;
    color: #333333;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
#preview {
    border: 2px solid #007acc;
    border-radius: 75px;
}
QPushButton {
    background-color: #007acc;
    color: #ffffff;
    border: 1px solid #005a9e;
    padding: 6px 12px;
    border-radius: 4px;
}
QPushButton:hover {
    background-color: #005a9e;
}
QPushButton:pressed {
    background-color: #004f8b;
}
QLabel { qproperty-alignment: 'AlignLeft'; }
""")
    picker = ColorPicker()
    picker.show()
    sys.exit(app.exec())
