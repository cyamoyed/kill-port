#!/usr/bin/env python3
"""
打包脚本 - 用于生成跨平台可执行文件
支持 Windows、macOS 和 Linux 平台
"""

import os
import sys
import subprocess
import shutil
import argparse


def install_dependencies():
    """安装必要的依赖"""
    print("安装必要的依赖...")
    try:
        # 安装PyInstaller
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      check=True, capture_output=True, text=True)
        # 安装PyQt5
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt5"], 
                      check=True, capture_output=True, text=True)
        print("依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False
    return True


def package_windows():
    """打包Windows EXE文件"""
    print("开始打包Windows EXE文件...")
    try:
        # 使用PyInstaller打包
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--name", "kill-port", 
             "--windowed", "--onefile", "main.py"],
            check=True, capture_output=True, text=True
        )
        print("Windows EXE文件打包成功")
        print(f"可执行文件位置: dist/kill-port.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Windows EXE文件打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def package_macos():
    """打包macOS DMG文件"""
    print("开始打包macOS DMG文件...")
    try:
        # 使用PyInstaller打包
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--name", "kill-port", 
             "--windowed", "--onefile", "main.py"],
            check=True, capture_output=True, text=True
        )
        print("macOS可执行文件打包成功")
        print(f"可执行文件位置: dist/kill-port")
        
        # 这里可以添加创建DMG的步骤
        # 由于需要在macOS上执行，这里只做提示
        print("提示: 请在macOS上使用create-dmg工具创建DMG文件")
        print("命令示例: create-dmg --volname 'kill-port' --window-pos 200 120 --window-size 600 300 ")
        print("          --app-drop-link 450 100 --icon 'kill-port.app' 150 100 dist/kill-port.app")
        return True
    except subprocess.CalledProcessError as e:
        print(f"macOS可执行文件打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def package_linux():
    """打包Linux AppImage文件"""
    print("开始打包Linux AppImage文件...")
    try:
        # 使用PyInstaller打包
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--name", "kill-port", 
             "--windowed", "--onefile", "main.py"],
            check=True, capture_output=True, text=True
        )
        print("Linux可执行文件打包成功")
        print(f"可执行文件位置: dist/kill-port")
        
        # 这里可以添加创建AppImage的步骤
        # 由于需要在Linux上执行，这里只做提示
        print("提示: 请在Linux上使用AppImageTool创建AppImage文件")
        print("命令示例: appimagetool dist/kill-port kill-port.AppImage")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Linux可执行文件打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def clean_build():
    """清理构建文件"""
    print("清理构建文件...")
    for dir_name in ["build", "dist"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    for file_name in ["kill-port.spec"]:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"已删除文件: {file_name}")
    print("清理完成")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="跨平台打包脚本")
    parser.add_argument("--platform", choices=["windows", "macos", "linux", "all"], 
                       default="all", help="指定打包平台")
    parser.add_argument("--clean", action="store_true", help="清理构建文件")
    parser.add_argument("--install-deps", action="store_true", help="安装依赖")
    
    args = parser.parse_args()
    
    # 清理构建文件
    if args.clean:
        clean_build()
        return
    
    # 安装依赖
    if args.install_deps:
        if not install_dependencies():
            return
    
    # 根据平台打包
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