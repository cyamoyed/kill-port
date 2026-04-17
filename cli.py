import argparse
import os
import subprocess
import sys

def kill_port_process(port):
    """根据端口杀死进程"""
    if not port or not port.isdigit():
        print("错误: 请输入有效的数字端口！")
        return False

    try:
        # 根据操作系统选择不同的命令
        if os.name == 'nt':  # Windows
            # 查找占用端口的PID
            result = subprocess.check_output(
                f'netstat -ano | findstr ":{port}"',
                shell=True, text=True, stderr=subprocess.STDOUT
            )

            if not result.strip():
                print(f"提示: 端口 {port} 未被任何进程占用")
                return True

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
                print(f"提示: 端口 {port} 未被任何进程占用")
                return True

            if not result.strip():
                print(f"提示: 端口 {port} 未被任何进程占用")
                return True

            # 获取PID
            pid = result.strip().splitlines()[0]

            # 强制杀死进程
            subprocess.run(f'kill -9 {pid}', shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 根据平台显示适当的成功消息
        print(f"成功: 端口 {port} 已成功释放\n进程PID：{pid}")
        return True

    except subprocess.CalledProcessError:
        print(f"提示: 端口 {port} 未被占用")
        return True
    except PermissionError:
        if os.name == 'nt':
            print("权限错误: 需要管理员权限才能执行此操作")
        else:
            print("权限错误: 需要 root 权限才能执行此操作")
        return False
    except Exception as e:
        print(f"失败: 错误：{str(e)}")
        return False

def main():
    """命令行主函数"""
    parser = argparse.ArgumentParser(
        description='端口进程杀死工具 - 用于快速查找并杀死占用指定端口的进程',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # 添加位置参数
    parser.add_argument('port', nargs='?', type=str, help='要关闭的端口号')
    
    # 添加选项参数
    parser.add_argument('-v', '--version', action='store_true', help='显示版本信息')
    parser.add_argument('-q', '--quiet', action='store_true', help='安静模式，只输出错误信息')
    
    # 解析参数
    args = parser.parse_args()
    
    # 处理版本信息
    if args.version:
        print('kill-port 1.0.0')
        return
    
    # 处理端口参数
    if not args.port:
        parser.print_help()
        return
    
    # 执行杀死操作
    success = kill_port_process(args.port)
    
    # 根据结果设置退出码
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()