"""
Fix dependency compatibility issues for PitchOS
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Command: {command}")
        if result.returncode == 0:
            print("✅ Success")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print("❌ Failed")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def fix_numpy_pandas_compatibility():
    """Fix numpy/pandas compatibility issues."""
    print("🔧 Fixing numpy/pandas compatibility issues...\n")
    
    # Step 1: Uninstall problematic packages
    print("Step 1: Uninstalling potentially conflicting packages...")
    packages_to_uninstall = ["numpy", "pandas", "streamlit"]
    
    for package in packages_to_uninstall:
        run_command(f"pip uninstall {package} -y")
    
    print("\n" + "="*50)
    
    # Step 2: Clear pip cache
    print("Step 2: Clearing pip cache...")
    run_command("pip cache purge")
    
    print("\n" + "="*50)
    
    # Step 3: Install compatible versions
    print("Step 3: Installing compatible versions...")
    
    # Install numpy first (specific compatible version)
    print("Installing numpy...")
    run_command("pip install numpy==1.24.3")
    
    # Install pandas with compatible numpy
    print("Installing pandas...")
    run_command("pip install pandas==2.0.3")
    
    # Install streamlit
    print("Installing streamlit...")
    run_command("pip install streamlit==1.28.0")
    
    print("\n" + "="*50)
    
    # Step 4: Install other PitchOS dependencies
    print("Step 4: Installing PitchOS dependencies...")
    
    dependencies = [
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.1",
        "python-docx>=0.8.11",
        "plotly>=5.15.0",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.7.0"
    ]
    
    for dep in dependencies:
        print(f"Installing {dep}...")
        run_command(f"pip install {dep}")
    
    print("\n" + "="*50)
    
    # Step 5: Install OCR dependencies (optional)
    print("Step 5: Installing OCR dependencies (optional)...")
    
    ocr_deps = [
        "opencv-python>=4.8.0",
        "easyocr>=1.7.0",
        "google-cloud-vision>=3.4.0"
    ]
    
    for dep in ocr_deps:
        print(f"Installing {dep}...")
        success = run_command(f"pip install {dep}")
        if not success:
            print(f"⚠️ Failed to install {dep} - OCR features may not work")
    
    print("\n" + "="*50)

def verify_installation():
    """Verify that the installation works."""
    print("🔍 Verifying installation...")
    
    try:
        import numpy
        print(f"✅ numpy {numpy.__version__}")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ pandas {pandas.__version__}")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import streamlit
        print(f"✅ streamlit {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ google-generativeai")
    except ImportError as e:
        print(f"❌ google-generativeai import failed: {e}")
        return False
    
    # Test OCR dependencies (optional)
    try:
        import cv2
        print(f"✅ opencv-python {cv2.__version__}")
    except ImportError:
        print("⚠️ opencv-python not available (OCR features disabled)")
    
    try:
        import easyocr
        print("✅ easyocr")
    except ImportError:
        print("⚠️ easyocr not available (OCR features disabled)")
    
    return True

def create_minimal_test():
    """Create a minimal test to verify PitchOS works."""
    test_code = '''
import streamlit as st
import sys
sys.path.append("src")

try:
    from src.config import config
    from src.pitch_analyzer import PitchAnalyzer
    from src.ui_components import PitchOSUI
    
    st.title("🚀 PitchOS - Dependency Test")
    st.success("✅ All core dependencies loaded successfully!")
    
    if config.GOOGLE_API_KEY:
        st.info("🔑 Google API key configured")
    else:
        st.warning("⚠️ Google API key not found - add to .env file")
    
    st.markdown("### Test Results:")
    st.markdown("- ✅ Streamlit working")
    st.markdown("- ✅ PitchOS modules imported")
    st.markdown("- ✅ Dependencies compatible")
    
    st.markdown("### Next Steps:")
    st.markdown("1. Add your Google API key to .env file")
    st.markdown("2. Run: `streamlit run app.py`")
    
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.markdown("Please run `python fix_dependencies.py` to fix issues")
'''
    
    with open("test_app.py", "w") as f:
        f.write(test_code)
    
    print("✅ Created test_app.py")

def main():
    """Main function to fix dependencies."""
    print("🔧 PitchOS Dependency Fix Tool\n")
    
    print("This will fix the numpy/pandas compatibility issue you're experiencing.")
    print("The error occurs when numpy and pandas versions are incompatible.\n")
    
    response = input("Do you want to proceed with fixing dependencies? (y/n): ")
    
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    # Fix compatibility issues
    fix_numpy_pandas_compatibility()
    
    # Verify installation
    if verify_installation():
        print("\n🎉 Dependencies fixed successfully!")
        
        # Create test app
        create_minimal_test()
        
        print("\n📋 Next Steps:")
        print("1. Test with: streamlit run test_app.py")
        print("2. If test works, run: streamlit run app.py")
        print("3. Make sure your .env file has GOOGLE_API_KEY set")
        
    else:
        print("\n❌ Some issues remain. You may need to:")
        print("1. Create a fresh virtual environment")
        print("2. Install dependencies from scratch")
        print("3. Check for system-level conflicts")

if __name__ == "__main__":
    main()
