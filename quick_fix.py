"""
Quick fix for PitchOS dependency issues
"""

import subprocess
import sys

def run_command(cmd):
    """Run command and show output."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Success")
    else:
        print(f"❌ Error: {result.stderr}")
    return result.returncode == 0

def main():
    print("🔧 Quick Fix for PitchOS Dependencies\n")
    
    # Fix the numpy/pandas compatibility issue
    print("Fixing numpy/pandas compatibility...")
    
    # Uninstall and reinstall with compatible versions
    commands = [
        "pip uninstall numpy pandas streamlit -y",
        "pip install numpy==1.24.3",
        "pip install pandas==2.0.3", 
        "pip install streamlit==1.28.0",
        "pip install google-generativeai python-dotenv PyPDF2 python-docx plotly Pillow requests pydantic"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"Failed at: {cmd}")
            break
    
    print("\n🎉 Dependencies should be fixed!")
    print("Now try: streamlit run app.py")

if __name__ == "__main__":
    main()
