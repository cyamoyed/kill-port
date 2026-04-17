#!/usr/bin/env python3
import os
import subprocess
import time


def test_port_finder():
    """Test port finding functionality"""
    print(f"Current operating system: {os.name}")
    
    # Test command
    if os.name == 'nt':  # Windows
        cmd = 'netstat -ano'
    else:  # Linux/macOS
        cmd = 'lsof -i'
    
    print(f"Testing port finding command: {cmd}")
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        print("Port finding command executed successfully")
        # Print first few lines of result
        lines = result.strip().split('\n')
        print(f"First 5 lines of command output:")
        for line in lines[:5]:
            print(f"  {line}")
        return True
    except Exception as e:
        print(f"Port finding command failed: {str(e)}")
        return False


def test_process_killer():
    """Test process killing functionality"""
    print("\nTesting process killing functionality")
    
    # Test command
    if os.name == 'nt':  # Windows
        cmd = 'taskkill /?'
    else:  # Linux/macOS
        cmd = 'kill --help'
    
    print(f"Testing process killing command: {cmd}")
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
        print("Process killing command executed successfully")
        return True
    except Exception as e:
        print(f"Process killing command failed: {str(e)}")
        return False


def test_gui_libraries():
    """Test GUI library availability"""
    print("\nTesting GUI library availability")
    try:
        import tkinter as tk
        print("tkinter library imported successfully")
        return True
    except ImportError as e:
        print(f"Failed to import tkinter library: {str(e)}")
        return False


def main():
    """Main test function"""
    print("=== Cross-platform compatibility test ===")
    print("=" * 50)
    
    tests = [
        ("Port finding functionality", test_port_finder),
        ("Process killing functionality", test_process_killer),
        ("GUI library availability", test_gui_libraries)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTest: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"[PASS] {test_name} test passed")
        else:
            print(f"[FAIL] {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"Test results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[PASS] All tests passed, cross-platform compatibility is good")
    else:
        print("[FAIL] Some tests failed, further inspection required")


if __name__ == "__main__":
    main()
