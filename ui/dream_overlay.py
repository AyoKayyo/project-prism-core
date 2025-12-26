import sys
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QFont

class DreamOverlay(QWidget):
    """
    Visual Cortex: The transparent black overlay that dims the screen during Dream Mode.
    Blocks mouse clicks and shows Riley's dream state.
    """
    # Signal to tell the system "The user clicked, WAKE UP!"
    wake_up_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Block mouse clicks so they don't hit the app underneath
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.hide()
        
        # Style: 90% Opacity Black (OLED Friendly)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 230))
        self.setPalette(palette)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # Visual Elements
        self.icon = QLabel("✨")
        self.icon.setFont(QFont("Arial", 64))
        self.icon.setStyleSheet("color: #a8a8a8; margin-bottom: 10px;")
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status = QLabel("Riley is Dreaming...")
        self.status.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.status.setStyleSheet("color: #ffffff;")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.details = QLabel("Running on Local Llama-3 • Zero Token Cost")
        self.details.setStyleSheet("color: #888888; font-size: 16px;")
        self.details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.hint = QLabel("(Click anywhere to wake)")
        self.hint.setStyleSheet("color: #444444; font-size: 13px; margin-top: 40px;")
        self.hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon)
        layout.addWidget(self.status)
        layout.addWidget(self.details)
        layout.addWidget(self.hint)

    def mousePressEvent(self, event):
        """Any click sends the signal to wake up"""
        self.wake_up_signal.emit()
