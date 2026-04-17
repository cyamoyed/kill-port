import sys

def main():
    """主入口函数"""
    # 根据运行方式选择不同的接口
    if len(sys.argv) > 1:
        # 命令行模式
        from cli import main as cli_main
        cli_main()
    else:
        # GUI模式
        try:
            # 优先使用PyQt5 GUI
            from gui import show_gui
            show_gui()
        except ImportError:
            # 回退到tkinter GUI
            import os
            import subprocess
            import tkinter as tk
            from tkinter import simpledialog, messagebox

            # 仅在Windows上设置DPI感知
            if os.name == 'nt':
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)

            def kill_port_process(port):
                """根据端口杀死进程"""
                if not port or not port.isdigit():
                    messagebox.showerror("错误", "请输入有效的数字端口！")
                    return

                try:
                    # 根据操作系统选择不同的命令
                    if os.name == 'nt':  # Windows
                        # 查找占用端口的PID
                        result = subprocess.check_output(
                            f'netstat -ano | findstr ":{port}"',
                            shell=True, text=True, stderr=subprocess.STDOUT
                        )

                        if not result.strip():
                            messagebox.showinfo("提示", f"端口 {port} 未被任何进程占用")
                            return

                        # 获取PID
                        pid = result.strip().splitlines()[0].split()[-1]

                        # 强制杀死进程
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:  # Linux/macOS
                        # 查找占用端口的PID
                        try:
                            result = subprocess.check_output(
                                f'lsof -i:{port} -t',
                                shell=True, text=True, stderr=subprocess.STDOUT
                            )
                        except subprocess.CalledProcessError:
                            messagebox.showinfo("提示", f"端口 {port} 未被任何进程占用")
                            return

                        if not result.strip():
                            messagebox.showinfo("提示", f"端口 {port} 未被任何进程占用")
                            return

                        # 获取PID
                        pid = result.strip().splitlines()[0]

                        # 强制杀死进程
                        subprocess.run(f'kill -9 {pid}', shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # 根据平台显示适当的成功消息
                    if os.name == 'nt':
                        messagebox.showinfo("成功", f"已成功杀死端口 {port}\n进程PID：{pid}")
                    else:
                        messagebox.showinfo("成功", f"端口 {port} 已成功释放\n进程PID：{pid}")

                except subprocess.CalledProcessError:
                    messagebox.showinfo("提示", f"端口 {port} 未被占用")
                except PermissionError:
                    if os.name == 'nt':
                        messagebox.showerror("权限错误", "需要管理员权限才能执行此操作")
                    else:
                        messagebox.showerror("权限错误", "需要 root 权限才能执行此操作")
                except Exception as e:
                    messagebox.showerror("失败", f"错误：{str(e)}")

            def show_input_box():
                """显示兼容的输入框"""
                root = tk.Tk()
                root.withdraw()  # 隐藏主窗口
                
                # 跨平台窗口置顶设置
                if os.name == 'nt':  # Windows
                    root.attributes('-topmost', True)
                else:  # Linux/macOS
                    # 在Linux和macOS上也尝试设置窗口置顶
                    try:
                        root.attributes('-topmost', True)
                    except Exception:
                        pass

                # 根据平台设置适当的对话框标题
                title = "端口进程杀死工具"
                prompt = "请输入要关闭的端口号："

                port = simpledialog.askstring(title, prompt)
                if port:
                    kill_port_process(port.strip())

            show_input_box()

if __name__ == "__main__":
    main()