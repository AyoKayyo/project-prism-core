import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPalette
from utils.config_manager import load_config

# --- STYLESHEET (COMET THEME) ---
STYLESHEET = """
QMainWindow {
    background-color: #0d1117;
}
QLabel {
    color: #c9d1d9;
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}
QLabel#Header {
    font-size: 24px;
    font-weight: bold;
    color: #58a6ff;
}
QLabel#Status {
    font-size: 14px;
    color: #2ea043;
}
QFrame#Card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
}
QPushButton {
    background-color: #238636;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #2ea043;
}
QPushButton:pressed {
    background-color: #238636;
}
QPushButton#Secondary {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
}
QPushButton#Secondary:hover {
    background-color: #30363d;
}
"""

class CommandCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.ai_name = self.config.get("ai_name", "Riley")
        self.mode = self.config.get("evolution_mode", "Standard")
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle(f"{self.ai_name} // Command Center")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(STYLESHEET)
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # --- LEFT SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("Card")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Logo / Title
        title = QLabel("COMMAND\nCENTER")
        title.setObjectName("Header")
        sidebar_layout.addWidget(title)
        
        sidebar_layout.addStretch()
        
        # Menu Buttons
        btn_dashboard = QPushButton("Dashboard")
        btn_neural = QPushButton("Neural Net")
        btn_logs = QPushButton("System Logs")
        btn_settings = QPushButton("Settings")
        btn_settings.setObjectName("Secondary")
        
        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_neural)
        sidebar_layout.addWidget(btn_logs)
        sidebar_layout.addWidget(btn_settings)
        
        sidebar_layout.addStretch()
        
        # Version
        ver_label = QLabel("v2.5.0-comet")
        ver_label.setStyleSheet("color: #8b949e; font-size: 10px;")
        sidebar_layout.addWidget(ver_label)
        
        main_layout.addWidget(sidebar)
        
        # --- RIGHT CONTENT (DASHBOARD) ---
        content_area = QVBoxLayout()
        
        # Status Bar
        status_frame = QFrame()
        status_frame.setObjectName("Card")
        status_layout = QHBoxLayout(status_frame)
        
        status_indicator = QLabel("● SYSTEM ONLINE")
        status_indicator.setObjectName("Status")
        
        mode_label = QLabel(f"MODE: {self.mode.upper()}")
        mode_label.setStyleSheet("color: #8b949e; font-weight: bold;")
        
        status_layout.addWidget(status_indicator)
        status_layout.addStretch()
        status_layout.addWidget(mode_label)
        
        content_area.addWidget(status_frame)
        
        # Main Hero Card
        hero_frame = QFrame()
        hero_frame.setObjectName("Card")
        hero_layout = QVBoxLayout(hero_frame)
        hero_layout.setContentsMargins(40, 40, 40, 40)
        
        greeting = QLabel(f"Welcome back, User.")
        greeting.setStyleSheet("font-size: 32px; color: white;")
        
        subtitle = QLabel(f"{self.ai_name} is ready for interaction.")
        subtitle.setStyleSheet("font-size: 18px; color: #8b949e;")
        
        hero_layout.addWidget(greeting)
        hero_layout.addWidget(subtitle)
        hero_layout.addStretch()
        
        # Action Buttons
        btn_launch = QPushButton("INITIATE CHAT LINK")
        btn_launch.setStyleSheet("padding: 15px; font-size: 16px;")
        
        hero_layout.addWidget(btn_launch)
        
        content_area.addWidget(hero_frame)
        
        # Stats Row
        stats_layout = QHBoxLayout()
        
        stat1 = self.create_stat_card("Uptime", "00:04:12")
        stat2 = self.create_stat_card("Memory", "128 MB")
        stat3 = self.create_stat_card("Ping", "24ms")
        
        stats_layout.addWidget(stat1)
        stats_layout.addWidget(stat2)
        stats_layout.addWidget(stat3)
        
        content_area.addLayout(stats_layout)
        
        main_layout.addLayout(content_area)

    def create_stat_card(self, label_text, value_text):
        card = QFrame()
        card.setObjectName("Card")
        layout = QVBoxLayout(card)
        
        lbl = QLabel(label_text)
        lbl.setStyleSheet("color: #8b949e; font-size: 12px;")
        
        val = QLabel(value_text)
        val.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        
        layout.addWidget(lbl)
        layout.addWidget(val)
        return card

def run_app():
    app = QApplication(sys.argv)
    window = CommandCenter()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
