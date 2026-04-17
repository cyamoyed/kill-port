import sys

def main():
    """Main entry function"""
    # Choose different interface based on running mode
    if len(sys.argv) > 1:
        # Command line mode
        from cli import main as cli_main
        cli_main()
    else:
        # GUI mode
        try:
            # Prefer PyQt5 GUI
            from gui import show_gui
            show_gui()
        except ImportError:
            # Fall back to tkinter GUI
            import os
            import subprocess
            import tkinter as tk
            from tkinter import simpledialog, messagebox

            # Set DPI awareness only on Windows
            if os.name == 'nt':
                import ctypes
                ctypes.windll.shcore.SetProcessDpiAwareness(1)

            def kill_port_process(port):
                """Kill process by port"""
                if not port or not port.isdigit():
                    messagebox.showerror("Error", "Please enter a valid numeric port!")
                    return

                try:
                    # Choose different command based on operating system
                    if os.name == 'nt':  # Windows
                        # Find PID occupying the port
                        result = subprocess.check_output(
                            f'netstat -ano | findstr ":{port}"',
                            shell=True, text=True, stderr=subprocess.STDOUT
                        )

                        if not result.strip():
                            messagebox.showinfo("Info", f"Port {port} is not occupied by any process")
                            return

                        # Get PID
                        pid = result.strip().splitlines()[0].split()[-1]

                        # Force kill the process
                        subprocess.run(f'taskkill /F /PID {pid}', shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:  # Linux/macOS
                        # Find PID occupying the port
                        try:
                            result = subprocess.check_output(
                                f'lsof -i:{port} -t',
                                shell=True, text=True, stderr=subprocess.STDOUT
                            )
                        except subprocess.CalledProcessError:
                            messagebox.showinfo("Info", f"Port {port} is not occupied by any process")
                            return

                        if not result.strip():
                            messagebox.showinfo("Info", f"Port {port} is not occupied by any process")
                            return

                        # Get PID
                        pid = result.strip().splitlines()[0]

                        # Force kill the process
                        subprocess.run(f'kill -9 {pid}', shell=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # Show appropriate success message based on platform
                    if os.name == 'nt':
                        messagebox.showinfo("Success", f"Successfully killed port {port}\nProcess PID: {pid}")
                    else:
                        messagebox.showinfo("Success", f"Port {port} has been successfully released\nProcess PID: {pid}")

                except subprocess.CalledProcessError:
                    messagebox.showinfo("Info", f"Port {port} is not occupied")
                except PermissionError:
                    if os.name == 'nt':
                        messagebox.showerror("Permission Error", "Administrator privileges are required to perform this operation")
                    else:
                        messagebox.showerror("Permission Error", "Root privileges are required to perform this operation")
                except Exception as e:
                    messagebox.showerror("Failure", f"Error: {str(e)}")

            def show_input_box():
                """Show compatible input box"""
                root = tk.Tk()
                root.withdraw()  # Hide main window
                
                # Cross-platform window topmost setting
                if os.name == 'nt':  # Windows
                    root.attributes('-topmost', True)
                else:  # Linux/macOS
                    # Also try to set window topmost on Linux and macOS
                    try:
                        root.attributes('-topmost', True)
                    except Exception:
                        pass

                # Set appropriate dialog title based on platform
                title = "Port Process Killer"
                prompt = "Please enter the port number to close:"

                port = simpledialog.askstring(title, prompt)
                if port:
                    kill_port_process(port.strip())

            show_input_box()

if __name__ == "__main__":
    main()