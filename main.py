import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import time

# Import your Flask app
from app import app as flask_app

def run_flask():
    flask_app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fruitful Harvest Assistant")
        self.setGeometry(100, 100, 900, 700)
        
        # Create web view
        self.browser = QWebEngineView()
        self.browser.load(QUrl("http://localhost:5000"))
        self.setCentralWidget(self.browser)
        
        # Hide status bar
        self.statusBar().hide()

if __name__ == "__main__":
    print("🟢 Starting Fruitful Harvest Assistant...")
    print("   Application window will open shortly...")
    
    # Start Flask in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    time.sleep(2)
    
    # Start Qt app
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())