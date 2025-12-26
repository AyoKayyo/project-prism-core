import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from lab_dream_ui import DreamOverlay
from consciousness import RileyConsciousness

class MasterControlUnit(QMainWindow):
    """
    Master Control: Connects Riley's Brain (QThread) to her Face (UI).
    This is the verification system that proves signals work.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Riley OS: Master Control")
        self.resize(1000, 700)
        self.setStyleSheet("background-color: #1e1e1e;")
        
        # 1. SETUP UI (The Body)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        self.status_label = QLabel("System Status: OFFLINE")
        self.status_label.setStyleSheet("color: #00ff00; font-size: 18px; font-family: monospace;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.info_label = QLabel("Waiting for Nervous System...\n(Don't move mouse for 10s to test)")
        self.info_label.setStyleSheet("color: #888; font-size: 14px;")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        # 2. INSTALL VISUAL CORTEX
        self.dream_overlay = DreamOverlay(self)
        self.dream_overlay.resize(self.size())
        
        # 3. BOOT NERVOUS SYSTEM
        self.brain = RileyConsciousness()
        
        # 4. WIRE THE CONNECTIONS (Brain -> Body)
        self.brain.signal_dream_start.connect(self.enter_dream_mode)
        self.brain.signal_dream_wake.connect(self.wake_up)
        self.brain.signal_log_update.connect(self.update_log)
        self.brain.signal_morning_briefing.connect(self.show_briefing)
        
        # 5. WIRE THE CONNECTIONS (Body -> Brain)
        # When user clicks the overlay, we force wake logic
        self.dream_overlay.wake_up_signal.connect(self.wake_up)
        
        # START
        self.brain.start()

    def resizeEvent(self, event):
        """Keep overlay sized to window"""
        self.dream_overlay.resize(self.size())
        super().resizeEvent(event)

    # --- SLOTS (Reacting to Signals) ---
    def enter_dream_mode(self):
        """React to signal_dream_start"""
        self.update_log("💤 SIGNAL RECEIVED: ENGAGE DREAM MODE")
        self.dream_overlay.show()
        self.dream_overlay.raise_()

    def wake_up(self):
        """React to signal_dream_wake OR user click"""
        self.update_log("☀️ SIGNAL RECEIVED: WAKE UP PROTOCOL")
        self.dream_overlay.hide()

    def update_log(self, text):
        """React to signal_log_update"""
        self.status_label.setText(f"System Status: {text}")

    def show_briefing(self, text):
        """React to signal_morning_briefing"""
        print(f"\n[CHAT BOX OUTPUT] >> {text}")
        self.info_label.setText(f"Morning Briefing Received:\n{text[:100]}...")

    def closeEvent(self, event):
        """Clean shutdown"""
        self.brain.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MasterControlUnit()
    window.show()
    sys.exit(app.exec())
