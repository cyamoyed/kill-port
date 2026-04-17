#!/usr/bin/env python3
import os
import subprocess
import time


def test_port_finder():
    """测试端口查找功能"""
    print(f"当前操作系统: {os.name}")
    
    # 测试命令
    if os.name == 'nt':  # Windows
        cmd = 'netstat -ano'
    else:  # Linux/macOS
        cmd = 'lsof -i'
    
    print(f"测试端口查找命令: {cmd}")
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        print("端口查找命令执行成功")
        # 打印前几行结果
        lines = result.strip().split('\n')
        print(f"命令输出前5行:")
        for line in lines[:5]:
            print(f"  {line}")
        return True
    except Exception as e:
        print(f"端口查找命令执行失败: {str(e)}")
        return False


def test_process_killer():
    """测试进程杀死功能"""
    print("\n测试进程杀死功能")
    
    # 测试命令
    if os.name == 'nt':  # Windows
        cmd = 'taskkill /?'
    else:  # Linux/macOS
        cmd = 'kill --help'
    
    print(f"测试进程杀死命令: {cmd}")
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        print("进程杀死命令执行成功")
        return True
    except Exception as e:
        print(f"进程杀死命令执行失败: {str(e)}")
        return False


def test_gui_libraries():
    """测试GUI库是否可用"""
    print("\n测试GUI库是否可用")
    try:
        import tkinter as tk
        print("tkinter库导入成功")
        return True
    except ImportError as e:
        print(f"tkinter库导入失败: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("=== 跨平台兼容性测试 ===")
    print("=" * 50)
    
    tests = [
        ("端口查找功能", test_port_finder),
        ("进程杀死功能", test_process_killer),
        ("GUI库可用性", test_gui_libraries)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n测试: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"[PASS] {test_name} 测试通过")
        else:
            print(f"[FAIL] {test_name} 测试失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("[PASS] 所有测试通过，跨平台兼容性良好")
    else:
        print("[FAIL] 部分测试失败，需要进一步检查")


if __name__ == "__main__":
    main()
