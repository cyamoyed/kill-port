import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox, 
                             QStatusBar, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

class KillPortWorker(QThread):
    """后台工作线程，用于执行端口杀死操作"""
    finished = pyqtSignal(bool, str, str)  # 成功标志, 消息, PID
    
    def __init__(self, port):
        super().__init__()
        self.port = port
    
    def run(self):
        try:
            if not self.port or not self.port.isdigit():
                self.finished.emit(False, "请输入有效的数字端口！", "")
                return
            
            port = self.port
            pid = ""
            
            if os.name == 'nt':  # Windows
                result = subprocess.check_output(
                    f'netstat -ano | findstr ":{port}"',
                    shell=True, text=True, stderr=subprocess.STDOUT
                )
                
                if not result.strip():
                    self.finished.emit(False, f"端口 {port} 未被任何进程占用", "")
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
                    self.finished.emit(False, f"端口 {port} 未被任何进程占用", "")
                    return
                
                if not result.strip():
                    self.finished.emit(False, f"端口 {port} 未被任何进程占用", "")
                    return
                
                pid = result.strip().splitlines()[0]
                subprocess.run(f'kill -9 {pid}', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.finished.emit(True, f"端口 {port} 已成功释放", pid)
            
        except subprocess.CalledProcessError:
            self.finished.emit(False, f"端口 {port} 未被占用", "")
        except PermissionError:
            if os.name == 'nt':
                self.finished.emit(False, "需要管理员权限才能执行此操作", "")
            else:
                self.finished.emit(False, "需要 root 权限才能执行此操作", "")
        except Exception as e:
            self.finished.emit(False, f"错误：{str(e)}", "")

class KillPortGUI(QWidget):
    """端口进程杀死工具的GUI界面"""
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # 设置窗口属性
        self.setWindowTitle('端口进程杀死工具')
        self.setGeometry(100, 100, 400, 200)
        self.setMinimumSize(350, 180)
        
        # 创建布局
        main_layout = QVBoxLayout()
        
        # 创建标题
        title_label = QLabel('端口进程杀死工具')
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        port_label = QLabel('端口号:')
        port_label.setFont(QFont('Arial', 10))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('请输入要关闭的端口号')
        self.port_input.setFont(QFont('Arial', 10))
        input_layout.addWidget(port_label)
        input_layout.addWidget(self.port_input)
        main_layout.addLayout(input_layout)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        self.kill_button = QPushButton('杀死进程')
        self.kill_button.setFont(QFont('Arial', 10))
        self.kill_button.clicked.connect(self.kill_port)
        self.exit_button = QPushButton('退出')
        self.exit_button.setFont(QFont('Arial', 10))
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.kill_button)
        button_layout.addWidget(self.exit_button)
        main_layout.addLayout(button_layout)
        
        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.status_bar.showMessage('就绪')
        main_layout.addWidget(self.status_bar)
        
        # 设置布局
        self.setLayout(main_layout)
        
        # 设置窗口居中
        self.center()
    
    def center(self):
        """将窗口居中显示"""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def kill_port(self):
        """处理杀死端口进程的操作"""
        port = self.port_input.text().strip()
        if not port:
            QMessageBox.warning(self, '警告', '请输入端口号')
            return
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.status_bar.showMessage('正在处理...')
        self.kill_button.setEnabled(False)
        
        # 创建并启动工作线程
        self.worker = KillPortWorker(port)
        self.worker.finished.connect(self.on_kill_finished)
        self.worker.start()
    
    def on_kill_finished(self, success, message, pid):
        """处理杀死操作完成的回调"""
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        self.kill_button.setEnabled(True)
        
        if success:
            QMessageBox.information(self, '成功', f"{message}\n进程PID：{pid}")
            self.status_bar.showMessage('操作成功')
        else:
            QMessageBox.warning(self, '提示', message)
            self.status_bar.showMessage('操作完成')

def show_gui():
    """显示GUI界面"""
    app = QApplication(sys.argv)
    gui = KillPortGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    show_gui()