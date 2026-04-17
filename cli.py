import argparse
import os
import subprocess
import sys

def kill_port_process(port):
    """Kill process by port"""
    if not port or not port.isdigit():
        print("Error: Please enter a valid numeric port!")
        return False

    try:
        # Choose different command based on operating system
        if os.name == 'nt':  # Windows
            # Find PID occupying the port
            result = subprocess.check_output(
                f'netstat -ano | findstr ":{port}"',
                shell=True, text=True, stderr=subprocess.STDOUT
            )

            if not result.strip():
                print(f"Info: Port {port} is not occupied by any process")
                return True

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
                print(f"Info: Port {port} is not occupied by any process")
                return True

            if not result.strip():
                print(f"Info: Port {port} is not occupied by any process")
                return True

            # Get PID
            pid = result.strip().splitlines()[0]

            # Force kill the process
            subprocess.run(f'kill -9 {pid}', shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Show appropriate success message based on platform
        print(f"Success: Port {port} has been successfully released\nProcess PID: {pid}")
        return True

    except subprocess.CalledProcessError:
        print(f"Info: Port {port} is not occupied")
        return True
    except PermissionError:
        if os.name == 'nt':
            print("Permission Error: Administrator privileges are required to perform this operation")
        else:
            print("Permission Error: Root privileges are required to perform this operation")
        return False
    except Exception as e:
        print(f"Failure: Error: {str(e)}")
        return False

def main():
    """Command line main function"""
    parser = argparse.ArgumentParser(
        description='Port Process Killer - used to quickly find and kill processes occupying specified ports',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Add positional argument
    parser.add_argument('port', nargs='?', type=str, help='Port number to close')
    
    # Add option arguments
    parser.add_argument('-v', '--version', action='store_true', help='Show version information')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode, only output error messages')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle version information
    if args.version:
        print('kill-port 1.0.0')
        return
    
    # Handle port argument
    if not args.port:
        parser.print_help()
        return
    
    # Execute kill operation
    success = kill_port_process(args.port)
    
    # Set exit code based on result
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()