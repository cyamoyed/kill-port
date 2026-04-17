# Port Process Killer (kill-port)

A cross-platform port process killer tool used to quickly find and kill processes occupying specified ports. Supports Windows, macOS, and Linux platforms, providing both GUI and command-line operation modes.

## Features

- 🎯 **Cross-platform support**：Compatible with Windows, macOS, and Linux operating systems
- 🖥️ **Dual interface mode**：Provides both Graphical User Interface (GUI) and Command Line Interface (CLI)
- ⚡ **Quick operation**：One-click to kill processes occupying specified ports
- 📋 **Detailed feedback**：Displays operation results and process PID
- 🔒 **Permission prompt**：Provides clear prompts when administrator/root privileges are required
- 🛠️ **Automated packaging**：Supports generating executable files for each platform

## Supported Platforms

- **Windows**：Generates EXE executable files
- **macOS**：Generates DMG installation packages
- **Linux**：Generates AppImage or DEB packages

## Installation Guide

### Method 1: Using Pre-compiled Executable Files

1. Go to the [GitHub Releases](https://github.com/cyamoyed/kill-port/releases) page to download the executable file for your platform
2. For Windows, download the `kill-port.exe` file
3. For macOS, download the `kill-port.dmg` file and install it
4. For Linux, download the `kill-port.AppImage` file and give it executable permissions

### Method 2: Installing from Source Code

1. Clone the repository：
   ```bash
   git clone https://github.com/cyamoyed/kill-port.git
   cd kill-port
   ```

2. Install dependencies：
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package：
   ```bash
   pip install .
   ```

## Usage Guide

### GUI Mode

1. **Windows**：Double-click the `kill-port.exe` file
2. **macOS**：Open the `kill-port.app` application
3. **Linux**：Run the `kill-port` executable file

In the popup window：
- Enter the port number to close in the input box
- Click the "Kill Process" button
- View the operation result and process PID

### Command Line Mode

```bash
# Basic usage
kill-port <port>

# Show version information
kill-port --version

# Quiet mode, only output error messages
kill-port --quiet <port>

# Show help information
kill-port --help
```

#### Examples

```bash
# Kill process occupying port 8080
kill-port 8080

# Show version information
kill-port --version

# Quiet mode to kill process occupying port 3000
kill-port --quiet 3000
```

## Frequently Asked Questions (FAQ)

### Q: What should I do when prompted "Administrator privileges required"?
A: On Windows, right-click the executable file and select "Run as administrator"；On macOS/Linux, run with the `sudo` command.

### Q: After execution, it prompts "Port not occupied", but I'm sure there's a process using the port?
A: It may be due to insufficient permissions to view all processes, please try running as administrator/root.

### Q: Why do I need to create a DMG file after packaging on macOS?
A: DMG is a common application distribution format on macOS, which needs to be created using specialized tools on macOS systems.

### Q: Why do I need to create an AppImage file after packaging on Linux?
A: AppImage is a cross-Linux distribution application packaging format that can run directly on different Linux systems.

## Troubleshooting

1. **Unable to find port occupancy information**：
   - Check if you have sufficient permissions
   - Confirm the port number is correct
   - Try using `netstat` (Windows) or `lsof` (macOS/Linux) to manually check port occupancy

2. **Packaging failure**：
   - Ensure all dependencies are installed
   - Check if PyInstaller is correctly installed
   - Try cleaning build files and repackaging

3. **GUI interface fails to start**：
   - Check if PyQt5 is correctly installed
   - Try using command line mode as an alternative

## Development Guide

### Project Structure

```
kill-port/
├── main.py          # Main entry file
├── gui.py           # PyQt5 GUI implementation
├── cli.py           # Command line interface implementation
├── setup.py         # Package configuration file
├── pyinstaller.spec # PyInstaller configuration file
├── package.py       # Packaging script
├── test_cross_platform.py # Cross-platform test
├── README.md        # Project documentation
└── requirements.txt # Dependencies file
```

### Packaging Process

1. Install dependencies：
   ```bash
   python package.py --install-deps
   ```

2. Package current platform：
   ```bash
   python package.py
   ```

3. Clean build files：
   ```bash
   python package.py --clean
   ```

### Testing

Run cross-platform compatibility test：
```bash
python test_cross_platform.py
```

## Version Control Strategy

- Version number format：`X.Y.Z`
  - X：Major version number, major feature changes
  - Y：Minor version number, new feature additions
  - Z：Patch version number, bug fixes

- Changelog format：
  - Version number
  - Release date
  - Feature change list
  - Bug fix list

## Contribution Guide

Welcome to submit Issues and Pull Requests! Please ensure：

1. Code follows project style
2. Add appropriate tests
3. Update documentation
4. Provide clear commit messages

## License

This project uses the MIT License, see the [LICENSE](LICENSE) file for details.

## Contact

- Author：cyam
- Email：980713832@qq.com
- Project address：https://github.com/cyamoyed/kill-port