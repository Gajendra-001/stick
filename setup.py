#!/usr/bin/env python3
"""
Setup script for Smart Blind Stick Django application.
This script helps set up the development environment.
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python():
    """Check if Python 3.8+ is available."""
    print("🐍 Checking Python version...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ {version}")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def create_virtual_environment():
    """Create virtual environment."""
    if os.path.exists("venv"):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command(f"{sys.executable} -m venv venv", "Creating virtual environment")

def activate_and_install():
    """Activate virtual environment and install dependencies."""
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_path = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        activate_script = "source venv/bin/activate"
        pip_path = "venv/bin/pip"
    
    # Install dependencies
    return run_command(f"{pip_path} install -r requirements.txt", "Installing dependencies")

def setup_environment():
    """Setup environment file."""
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            shutil.copy("env.example", ".env")
            print("✅ Created .env file from env.example")
        else:
            print("⚠️  No env.example file found")
    else:
        print("📁 .env file already exists")

def run_django_commands():
    """Run Django management commands."""
    if os.name == 'nt':  # Windows
        python_path = "venv\\Scripts\\python"
    else:  # Unix/Linux/macOS
        python_path = "venv/bin/python"
    
    commands = [
        (f"{python_path} manage.py makemigrations", "Creating migrations"),
        (f"{python_path} manage.py migrate", "Running migrations"),
        (f"{python_path} manage.py collectstatic --noinput", "Collecting static files"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 Setting up Smart Blind Stick Django Application")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        print("❌ Please install Python 3.8 or higher")
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not activate_and_install():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Run Django commands
    if not run_django_commands():
        print("❌ Failed to run Django setup commands")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your settings")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the development server: python manage.py runserver")
    print("4. Open http://localhost:8000 in your browser")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
