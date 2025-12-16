"""
Setup script for PitchOS OCR dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package_name):
    """Check if a package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def main():
    """Setup OCR dependencies for PitchOS."""
    print("🔧 Setting up PitchOS OCR Dependencies\n")
    
    # Required packages for OCR
    ocr_packages = [
        ("easyocr", "easyocr>=1.7.0"),
        ("cv2", "opencv-python>=4.8.0"),
        ("google.cloud.vision", "google-cloud-vision>=3.4.0"),
        ("PIL", "Pillow>=10.0.0"),
        ("numpy", "numpy>=1.24.0")
    ]
    
    print("Checking OCR dependencies...")
    
    missing_packages = []
    
    for import_name, pip_name in ocr_packages:
        if check_package(import_name):
            print(f"✅ {import_name} - Already installed")
        else:
            print(f"❌ {import_name} - Missing")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        
        for package in missing_packages:
            print(f"Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
    else:
        print("\n🎉 All OCR dependencies are already installed!")
    
    # Test OCR functionality
    print("\nTesting OCR functionality...")
    
    try:
        import easyocr
        print("✅ EasyOCR import successful")
        
        # Test EasyOCR initialization
        reader = easyocr.Reader(['en'], gpu=False)
        print("✅ EasyOCR reader initialized")
        
    except Exception as e:
        print(f"❌ EasyOCR test failed: {e}")
    
    try:
        import cv2
        print("✅ OpenCV import successful")
        print(f"   OpenCV version: {cv2.__version__}")
        
    except Exception as e:
        print(f"❌ OpenCV test failed: {e}")
    
    try:
        from google.cloud import vision
        print("✅ Google Cloud Vision import successful")
        
    except Exception as e:
        print(f"⚠️  Google Cloud Vision import failed: {e}")
        print("   This is optional - EasyOCR will work without it")
    
    # Check environment setup
    print("\nChecking environment configuration...")
    
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("⚠️  .env file not found")
        print("   Copy .env.example to .env and add your API keys")
    
    # Final instructions
    print("\n🚀 OCR Setup Complete!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your Google API keys to .env")
    print("3. Run: streamlit run app.py")
    print("4. Select 'Image Upload (OCR)' to test OCR functionality")
    
    print("\nOCR Features Available:")
    print("📸 Hybrid OCR (EasyOCR + Google Vision fallback)")
    print("🔧 Advanced image preprocessing")
    print("📊 Quality analysis and recommendations")
    print("🔄 Batch image processing")
    print("🎯 Automatic slide content structuring")

if __name__ == "__main__":
    main()
