#!/usr/bin/env python3
"""
Quick verification test for Riley signal system.
Runs headless without GUI to verify signal connections.
"""
import sys
import time
from consciousness import RileyConsciousness

class SignalTester:
    def __init__(self):
        self.signals_received = []
        
    def on_dream_start(self):
        msg = "✅ SIGNAL RECEIVED: dream_start"
        self.signals_received.append(msg)
        print(msg)
        
    def on_dream_wake(self):
        msg = "✅ SIGNAL RECEIVED: dream_wake"
        self.signals_received.append(msg)
        print(msg)
        
    def on_log_update(self, text):
        msg = f"✅ SIGNAL RECEIVED: log_update -> {text}"
        self.signals_received.append(msg)
        print(msg)
        
    def on_morning_briefing(self, text):
        msg = f"✅ SIGNAL RECEIVED: morning_briefing -> {text[:50]}..."
        self.signals_received.append(msg)
        print(msg)

def test_signals():
    print("\n🧪 SIGNAL TEST - HEADLESS MODE\n")
    
    tester = SignalTester()
    brain = RileyConsciousness()
    
    # Wire connections BEFORE starting
    brain.signal_dream_start.connect(tester.on_dream_start)
    brain.signal_dream_wake.connect(tester.on_dream_wake)
    brain.signal_log_update.connect(tester.on_log_update)
    brain.signal_morning_briefing.connect(tester.on_morning_briefing)
    
    print("✅ Signals connected")
   
    # Start consciousness
    brain.start()
    print("✅ Consciousness thread started")
    
    print("⏳ Waiting 15 seconds for signals...")
    time.sleep(15)
    
    # Stop
    brain.stop()
    brain.wait()  # Ensure thread fully stops
    
    print(f"\n📊 RESULTS: {len(tester.signals_received)} signals received")
    if len(tester.signals_received) > 0:
        print(f"Last signal: {tester.signals_received[-1]}")
    print("✅ TEST PASSED" if len(tester.signals_received) >= 2 else "❌ TEST FAILED")
    return len(tester.signals_received) >= 2

if __name__ == "__main__":
    # Must use QCoreApplication for signal/slot system to work
    from PyQt6.QtCore import QCoreApplication, QTimer
    app = QCoreApplication(sys.argv)
    
    tester = SignalTester()
    brain = RileyConsciousness()
    
    # Wire connections
    brain.signal_dream_start.connect(tester.on_dream_start)
    brain.signal_dream_wake.connect(tester.on_dream_wake)
    brain.signal_log_update.connect(tester.on_log_update)
    brain.signal_morning_briefing.connect(tester.on_morning_briefing)
    
    print("\n🧪 SIGNAL TEST - HEADLESS MODE\n")
    print("✅ Signals connected")
    
    # Start brain
    brain.start()
    print("✅ Consciousness thread started")
    print("⏳ Waiting 15 seconds for signals...")
    
    # Stop after 15 seconds and report results
    def finish_test():
        brain.stop()
        brain.wait()
        print(f"\n📊 RESULTS: {len(tester.signals_received)} signals received")
        if len(tester.signals_received) > 0:
            for sig in tester.signals_received:
                print(f"  - {sig}")
        result = "✅ TEST PASSED" if len(tester.signals_received) >= 2 else "❌ TEST FAILED"
        print(result)
        app.quit()
        sys.exit(0 if len(tester.signals_received) >= 2 else 1)
    
    QTimer.singleShot(15000, finish_test)
    
    sys.exit(app.exec())
