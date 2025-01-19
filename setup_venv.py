import os
import subprocess
import sys

def setup_venv():
    venv_dir = "venv"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_file = os.path.join(script_dir, "requirements.txt")

    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found. Please make sure it exists.")
        sys.exit(1)

    if not os.path.exists(venv_dir):
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        print("Virtual environment created.")

    if os.name == "nt":
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
    print(f"To activate the virtual environment, run:\nsource {activate_script}")

    try:
        pip_path = os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip")
        subprocess.check_call([pip_path, "install", "-r", requirements_file])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to install dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    setup_venv()
