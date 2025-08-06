import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"[OK] Python version: {sys.version.split()[0]}")

def check_chrome_installation():
    """Check if Google Chrome is installed"""
    try:
        # Try to run chrome with version flag
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Chrome found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # Try alternative chrome command
        result = subprocess.run(['chromium-browser', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] Chromium found: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("[WARNING] Google Chrome or Chromium not found!")
    print("Please install Google Chrome from: https://www.google.com/chrome/")
    return False

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        print("[OK] Required packages found")
        return True
    except ImportError as e:
        print(f"[ERROR] Missing packages: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['downloads', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("[OK] Directories created/verified")

def main():
    """Main function to set up and run the application"""
    print("Delhi High Court Data Fetcher - Setup & Run")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check Chrome installation
    chrome_ok = check_chrome_installation()
    
    # Check requirements
    requirements_ok = check_requirements()
    
    # Create directories
    create_directories()
    
    # Warnings for missing components
    if not chrome_ok:
        print("\n[WARNING] Chrome not found. The application may not work correctly.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)
    
    if not requirements_ok:
        print("\n[ERROR] Required packages missing. Please install them first:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check if app.py exists
    if not Path('app.py').exists():
        print("[ERROR] app.py not found in current directory!")
        sys.exit(1)
    
    print("\n[STARTING] Delhi High Court Data Fetcher...")
    print("[INFO] Access the application at: http://localhost:5000")
    print("[INFO] Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = 'True'
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n[STOPPED] Server stopped by user")
    except Exception as e:
        print(f"\n[ERROR] Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
