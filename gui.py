import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QStatusBar, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

class KillPortWorker(QThread):
    """Background worker thread for executing port killing operations"""
    finished = pyqtSignal(bool, str, str)  # success flag, message, PID
    
    def __init__(self, port):
        super().__init__()
        self.port = port
    
    def run(self):
        try:
            if not self.port or not self.port.isdigit():
                self.finished.emit(False, "Please enter a valid numeric port!", "")
                return
            
            port = self.port
            pid = ""
            
            if os.name == 'nt':  # Windows
                result = subprocess.check_output(
                    f'netstat -ano | findstr ":{port}"',
                    shell=True, text=True, stderr=subprocess.STDOUT
                )
                
                if not result.strip():
                    self.finished.emit(False, f"Port {port} is not occupied by any process", "")
                    return
                
                pid = result.strip().splitlines()[0].split()[-1]
                subprocess.run(f'taskkill /F /PID {pid}', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:  # Linux/macOS
                try:
                    result = subprocess.check_output(
                        f'lsof -i:{port} -t',
                        shell=True, text=True, stderr=subprocess.STDOUT
                    )
                except subprocess.CalledProcessError:
                    self.finished.emit(False, f"Port {port} is not occupied by any process", "")
                    return
                
                if not result.strip():
                    self.finished.emit(False, f"Port {port} is not occupied by any process", "")
                    return
                
                pid = result.strip().splitlines()[0]
                subprocess.run(f'kill -9 {pid}', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.finished.emit(True, f"Port {port} has been successfully released", pid)
            
        except subprocess.CalledProcessError:
            self.finished.emit(False, f"Port {port} is not occupied", "")
        except PermissionError:
            if os.name == 'nt':
                self.finished.emit(False, "Administrator privileges are required to perform this operation", "")
            else:
                self.finished.emit(False, "Root privileges are required to perform this operation", "")
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}", "")

class KillPortGUI(QWidget):
    """GUI interface for Port Process Killer"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Port Process Killer')
        self.setGeometry(100, 100, 400, 200)
        self.setMinimumSize(350, 180)
        
        # Create layout
        main_layout = QVBoxLayout()
        
        # Create title
        title_label = QLabel('Port Process Killer')
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Create input area
        input_layout = QHBoxLayout()
        port_label = QLabel('Port:')
        port_label.setFont(QFont('Arial', 10))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('Please enter the port number to close')
        self.port_input.setFont(QFont('Arial', 10))
        input_layout.addWidget(port_label)
        input_layout.addWidget(self.port_input)
        main_layout.addLayout(input_layout)
        
        # Create button area
        button_layout = QHBoxLayout()
        self.kill_button = QPushButton('Kill Process')
        self.kill_button.setFont(QFont('Arial', 10))
        self.kill_button.clicked.connect(self.kill_port)
        self.exit_button = QPushButton('Exit')
        self.exit_button.setFont(QFont('Arial', 10))
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.kill_button)
        button_layout.addWidget(self.exit_button)
        main_layout.addLayout(button_layout)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage('Ready')
        main_layout.addWidget(self.status_bar)
        
        # Set layout
        self.setLayout(main_layout)
        
        # Center window
        self.center()
    
    def center(self):
        """Center the window on screen"""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def kill_port(self):
        """Handle port killing operation"""
        port = self.port_input.text().strip()
        if not port:
            QMessageBox.warning(self, 'Warning', 'Please enter a port number')
            return
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_bar.showMessage('Processing...')
        self.kill_button.setEnabled(False)
        
        # Create and start worker thread
        self.worker = KillPortWorker(port)
        self.worker.finished.connect(self.on_kill_finished)
        self.worker.start()
    
    def on_kill_finished(self, success, message, pid):
        """Handle callback when kill operation is completed"""
        # Hide progress bar
        self.progress_bar.setVisible(False)
        self.kill_button.setEnabled(True)
        
        if success:
            QMessageBox.information(self, 'Success', f"{message}\nProcess PID: {pid}")
            self.status_bar.showMessage('Operation successful')
        else:
            QMessageBox.warning(self, 'Info', message)
            self.status_bar.showMessage('Operation completed')

def show_gui():
    """Show GUI interface"""
    app = QApplication(sys.argv)
    gui = KillPortGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    show_gui()