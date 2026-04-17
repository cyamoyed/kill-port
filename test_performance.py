#!/usr/bin/env python3
"""
性能测试脚本
测试应用程序的启动速度和性能
"""

import os
import time
import subprocess
import sys


def test_startup_time():
    """测试应用程序的启动时间"""
    print("测试应用程序启动时间...")
    
    # 测试命令行模式启动时间
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "main.py", "--version"],
            capture_output=True, text=True, timeout=10
        )
        end_time = time.time()
        cli_startup_time = end_time - start_time
        print(f"命令行模式启动时间: {cli_startup_time:.4f} 秒")
    except Exception as e:
        print(f"命令行模式启动测试失败: {e}")
        cli_startup_time = None
    
    # 测试GUI模式启动时间（非阻塞）
    start_time = time.time()
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        # 等待一段时间后终止进程
        time.sleep(2)
        process.terminate()
        process.wait(timeout=1)
        end_time = time.time()
        gui_startup_time = end_time - start_time
        print(f"GUI模式启动时间: {gui_startup_time:.4f} 秒")
    except Exception as e:
        print(f"GUI模式启动测试失败: {e}")
        gui_startup_time = None
    
    return cli_startup_time, gui_startup_time


def test_memory_usage():
    """测试应用程序的内存使用情况"""
    print("\n测试应用程序内存使用情况...")
    
    # 测试命令行模式内存使用
    try:
        if os.name == 'nt':  # Windows
            # 使用tasklist命令
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV", "/NH"],
                capture_output=True, text=True
            )
            print("命令行模式内存使用（Windows）:")
            print(result.stdout)
        else:  # Linux/macOS
            # 使用ps命令
            result = subprocess.run(
                ["ps", "aux", "|", "grep", "python"],
                shell=True, capture_output=True, text=True
            )
            print("命令行模式内存使用（Linux/macOS）:")
            print(result.stdout)
    except Exception as e:
        print(f"内存使用测试失败: {e}")


def test_functionality_speed():
    """测试核心功能的执行速度"""
    print("\n测试核心功能执行速度...")
    
    # 测试端口查找速度
    start_time = time.time()
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True, text=True, timeout=5
            )
        else:  # Linux/macOS
            result = subprocess.run(
                ["lsof", "-i"],
                capture_output=True, text=True, timeout=5
            )
        end_time = time.time()
        port_scan_time = end_time - start_time
        print(f"端口扫描时间: {port_scan_time:.4f} 秒")
    except Exception as e:
        print(f"端口扫描测试失败: {e}")


def main():
    """主函数"""
    print("=== 性能测试 ===")
    print("=" * 50)
    
    # 测试启动时间
    cli_time, gui_time = test_startup_time()
    
    # 测试内存使用
    test_memory_usage()
    
    # 测试功能执行速度
    test_functionality_speed()
    
    print("\n" + "=" * 50)
    print("性能测试完成")
    
    # 生成性能报告
    print("\n性能报告:")
    if cli_time:
        print(f"- 命令行模式启动时间: {cli_time:.4f} 秒")
    if gui_time:
        print(f"- GUI模式启动时间: {gui_time:.4f} 秒")
    print("- 建议: 如果启动时间超过2秒，考虑进一步优化")


if __name__ == "__main__":
    main()