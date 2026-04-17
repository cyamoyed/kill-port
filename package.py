#!/usr/bin/env python3


"""
Packaging script - used to generate cross-platform executable files
Supports Windows, macOS, and Linux platforms
"""

import os
import sys
import subprocess
import shutil
import argparse


def install_dependencies():
    """Install necessary dependencies"""
    print("Installing necessary dependencies...")
    try:
        # Install PyInstaller
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      check=True, capture_output=True, text=True)
        # Install PyQt5
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"], 
                      check=True, capture_output=True, text=True)
        print("Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False
    return True


def package_windows():
    """Package Windows EXE file"""
    print("Starting to package Windows EXE file...")
    try:
        # Package using PyInstaller
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--name", "kill-port", 
             "--windowed", "--onefile", "main.py"],
            check=True, capture_output=True, text=True
        )
        print("Windows EXE file packaged successfully")
        print(f"Executable file location: dist/kill-port.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to package Windows EXE file: {e}")
        print(f"Error output: {e.stderr}")
        return False


def package_macos():
    """Package macOS DMG file"""
    print("Starting to package macOS DMG file...")
    try:
        # Package using PyInstaller
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--name", "kill-port", 
             "--windowed", "--onefile", "main.py"],
            check=True, capture_output=True, text=True
        )
        print("macOS executable file packaged successfully")
        print(f"Executable file location: dist/kill-port")
        
        # DMG creation steps can be added here
        # Since this needs to be executed on macOS, only a hint is provided here
        print("Hint: Please use create-dmg tool on macOS to create DMG file")
        print("Command example: create-dmg --volname 'kill-port' --window-pos 200 120 --window-size 600 300 ")
        print("          --app-drop-link 450 100 --icon 'kill-port.app' 150 100 dist/kill-port.app")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to package macOS executable file: {e}")
        print(f"Error output: {e.stderr}")
        return False


def package_linux():
    """Package Linux AppImage file"""
    print("Starting to package Linux AppImage file...")
    try:
        # Package using PyInstaller
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--name", "kill-port", 
             "--windowed", "--onefile", "main.py"],
            check=True, capture_output=True, text=True
        )
        print("Linux executable file packaged successfully")
        print(f"Executable file location: dist/kill-port")
        
        # AppImage creation steps can be added here
        # Since this needs to be executed on Linux, only a hint is provided here
        print("Hint: Please use AppImageTool on Linux to create AppImage file")
        print("Command example: appimagetool dist/kill-port kill-port.AppImage")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to package Linux executable file: {e}")
        print(f"Error output: {e.stderr}")
        return False


def clean_build():
    """Clean build files"""
    print("Cleaning build files...")
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Directory deleted: {dir_name}")
    for file_name in ["kill-port.spec"]:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File deleted: {file_name}")
    print("Cleanup completed")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Cross-platform packaging script")
    parser.add_argument("--platform", choices=["windows", "macos", "linux", "all"], 
                       default="all", help="Specify packaging platform")
    parser.add_argument("--clean", action="store_true", help="Clean build files")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies")
    
    args = parser.parse_args()
    
    # Clean build files
    if args.clean:
        clean_build()
        return
    
    # Install dependencies
    if args.install_deps:
        if not install_dependencies():
            return
    
    # Package according to platform
    if args.platform == "all":
        if sys.platform == "win32":
            package_windows()
        elif sys.platform == "darwin":
            package_macos()
        else:
            package_linux()
    elif args.platform == "windows":
        package_windows()
    elif args.platform == "macos":
        package_macos()
    elif args.platform == "linux":
        package_linux()


if __name__ == "__main__":
    main()