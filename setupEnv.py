import os
import subprocess
import sys

def create_venv():
    # Define paths
    venv_path = os.path.join(os.getcwd(), ".venv")
    requirements_file = os.path.join(os.getcwd(), "requirements.txt")

    # Create the virtual environment if it doesn't exist
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        print("Virtual environment created!")
    
    # Automatically install requirements
    if os.path.exists(requirements_file):
        print("Installing dependencies from requirements.txt...")
        pip_path = os.path.join(venv_path, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'pip')
        subprocess.check_call([pip_path, "install", "-r", requirements_file])
        print("Dependencies installed!")
    else:
        print("No requirements.txt file found. Skipping dependency installation.")

if __name__ == "__main__":
    create_venv()
