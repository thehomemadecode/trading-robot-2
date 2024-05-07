import platform
import subprocess
import shutil
import os

rversion = "2.0.0b"

def run_command(command):
    """
    Runs a shell command and waits for it to complete.
    """
    result = subprocess.run(command, shell=True)
    return result.returncode

def main():
    # Detect the platform
    is_windows = platform.system().lower() == "windows"
    
    # Define commands based on the operating system
    python_cmd = "python" if is_windows else "python3"
    copy_cmd = shutil.copy
    
    # List of commands to run
    commands = [
        f"{python_cmd} getallexchangeinfo.py",
        f"{python_cmd} makeCandlestickDB.py",
        f"{python_cmd} makehistory.py",
    ]
    
    # Execute each command
    for cmd in commands:
        if run_command(cmd) != 0:
            print(f"Command failed: {cmd}")
            return
    
    # File operations
    try:
        # Change the paths as needed
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        
        # Assuming alldata.txt is not needed as it's commented out in your original code
        # If needed, uncomment the next line
        # copy_cmd(os.path.join(current_dir, "alldata.txt"), parent_dir)
        copy_cmd(os.path.join(current_dir, "candlestick.db"), parent_dir)
        candlestick_db_path = os.path.join(current_dir, "candlestick.db")
        os.remove(candlestick_db_path)
        config_ini_path = os.path.join(current_dir, "config.ini")
        copy_cmd(config_ini_path, parent_dir)
        alldata_txt_path = os.path.join(current_dir, "alldata.txt")
        if os.path.exists(alldata_txt_path):
            os.remove(alldata_txt_path)
        
    except Exception as e:
        print(f"Error copying files: {e}")

if __name__ == '__main__':
    main() 
