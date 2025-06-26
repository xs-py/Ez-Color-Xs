#!/usr/bin/env python3
"""
Color Picker GUI with eyedropper tool.
Displays Hex, RGB, HSV values.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QColorDialog, QVBoxLayout,
    QHBoxLayout, QDialog
)
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt

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
        self.setWindowTitle("Color Picker")
        self.resize(400, 300)
        self.color = QColor(255, 255, 255, 255)

        # Preview
        self.preview = QLabel()
        self.preview.setFixedSize(100, 100)
        self.preview.setStyleSheet(f"background-color: {self.color.name().upper()}")

        # Labels
        self.hex_label = QLabel()
        self.rgb_label = QLabel()
        self.hsv_label = QLabel()

        # Buttons
        btn_dialog = QPushButton("Pick Color...")
        btn_dialog.clicked.connect(self.open_color_dialog)
        btn_eyedrop = QPushButton("Eyedropper")
        btn_eyedrop.clicked.connect(self.open_eyedropper)

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_dialog)
        btn_layout.addWidget(btn_eyedrop)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.preview, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.hex_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.rgb_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.hsv_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(btn_layout)

        self.update_labels()

    def update_labels(self):
        r = self.color.red()
        g = self.color.green()
        b = self.color.blue()
        a = self.color.alpha()
        h, s, v, _ = self.color.getHsv()
        s_pct = s / 2.55
        v_pct = v / 2.55
        hex_rgb = f"#{r:02X}{g:02X}{b:02X}"
        self.preview.setStyleSheet(f"background-color: {hex_rgb}")
        self.hex_label.setText(f"Hex: {hex_rgb}  Alpha: {a}")
        self.rgb_label.setText(f"RGB: {r}, {g}, {b}  Alpha: {a}")
        self.hsv_label.setText(f"HSV: {h}°, {s_pct:.1f}%, {v_pct:.1f}%")

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
    picker = ColorPicker()
    picker.show()
    sys.exit(app.exec())
