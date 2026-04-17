#!/usr/bin/env python3
"""
单元测试文件
测试核心功能的正确性
"""

import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

# 添加当前目录到路径
sys.path.insert(0, os.path.abspath('.'))

from cli import kill_port_process


class TestKillPortProcess(unittest.TestCase):
    """测试kill_port_process函数"""
    
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    def test_windows_success(self, mock_run, mock_check_output):
        """测试Windows平台成功杀死进程"""
        # 模拟netstat命令输出
        mock_check_output.return_value = 'TCP    0.0.0.0:8080           0.0.0.0:0              LISTENING       1234'
        
        # 模拟taskkill命令
        mock_run.return_value = None
        
        # 保存原始os.name
        original_os_name = os.name
        try:
            # 模拟Windows平台
            os.name = 'nt'
            
            # 执行函数
            result = kill_port_process('8080')
            
            # 验证结果
            self.assertTrue(result)
            mock_check_output.assert_called_once_with(
                'netstat -ano | findstr ":8080"',
                shell=True, text=True, stderr=subprocess.STDOUT
            )
            mock_run.assert_called_once_with(
                'taskkill /F /PID 1234',
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        finally:
            # 恢复原始os.name
            os.name = original_os_name
    
    @patch('subprocess.check_output')
    def test_windows_port_not_found(self, mock_check_output):
        """测试Windows平台端口未被占用"""
        # 模拟netstat命令无输出
        mock_check_output.return_value = ''
        
        # 保存原始os.name
        original_os_name = os.name
        try:
            # 模拟Windows平台
            os.name = 'nt'
            
            # 执行函数
            result = kill_port_process('8080')
            
            # 验证结果
            self.assertTrue(result)
        finally:
            # 恢复原始os.name
            os.name = original_os_name
    
    @patch('subprocess.check_output')
    @patch('subprocess.run')
    def test_linux_success(self, mock_run, mock_check_output):
        """测试Linux平台成功杀死进程"""
        # 模拟lsof命令输出
        mock_check_output.return_value = '1234'
        
        # 模拟kill命令
        mock_run.return_value = None
        
        # 保存原始os.name
        original_os_name = os.name
        try:
            # 模拟Linux平台
            os.name = 'posix'
            
            # 执行函数
            result = kill_port_process('8080')
            
            # 验证结果
            self.assertTrue(result)
            mock_check_output.assert_called_once_with(
                'lsof -i:8080 -t',
                shell=True, text=True, stderr=subprocess.STDOUT
            )
            mock_run.assert_called_once_with(
                'kill -9 1234',
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        finally:
            # 恢复原始os.name
            os.name = original_os_name
    
    @patch('subprocess.check_output')
    def test_linux_port_not_found(self, mock_check_output):
        """测试Linux平台端口未被占用"""
        # 模拟lsof命令抛出异常
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'lsof')
        
        # 保存原始os.name
        original_os_name = os.name
        try:
            # 模拟Linux平台
            os.name = 'posix'
            
            # 执行函数
            result = kill_port_process('8080')
            
            # 验证结果
            self.assertTrue(result)
        finally:
            # 恢复原始os.name
            os.name = original_os_name
    
    def test_invalid_port(self):
        """测试无效端口"""
        result = kill_port_process('abc')
        self.assertFalse(result)
    
    def test_empty_port(self):
        """测试空端口"""
        result = kill_port_process('')
        self.assertFalse(result)
    
    @patch('subprocess.check_output')
    def test_permission_error(self, mock_check_output):
        """测试权限错误"""
        # 模拟抛出权限错误
        mock_check_output.side_effect = PermissionError
        
        # 保存原始os.name
        original_os_name = os.name
        try:
            # 模拟Windows平台
            os.name = 'nt'
            
            # 执行函数
            result = kill_port_process('8080')
            
            # 验证结果
            self.assertFalse(result)
        finally:
            # 恢复原始os.name
            os.name = original_os_name
    
    @patch('subprocess.check_output')
    def test_generic_error(self, mock_check_output):
        """测试通用错误"""
        # 模拟抛出通用错误
        mock_check_output.side_effect = Exception('Generic error')
        
        # 保存原始os.name
        original_os_name = os.name
        try:
            # 模拟Windows平台
            os.name = 'nt'
            
            # 执行函数
            result = kill_port_process('8080')
            
            # 验证结果
            self.assertFalse(result)
        finally:
            # 恢复原始os.name
            os.name = original_os_name


if __name__ == '__main__':
    unittest.main()