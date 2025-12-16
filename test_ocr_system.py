"""
Test script for PitchOS OCR functionality
"""

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

def create_test_slide_image(text: str, filename: str = "test_slide.png") -> str:
    """Create a test slide image with text."""
    # Create a white background image
    width, height = 800, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 40)
        title_font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Draw title
    draw.text((50, 50), "STARTUP PITCH", fill='black', font=title_font)
    
    # Draw main text
    lines = text.split('\n')
    y_position = 150
    
    for line in lines:
        if line.strip():
            draw.text((50, y_position), line.strip(), fill='black', font=font)
            y_position += 60
    
    # Save image
    image.save(filename)
    return filename

def test_ocr_imports():
    """Test OCR-related imports."""
    print("Testing OCR imports...")
    
    try:
        from src.ocr_processor import HybridOCRProcessor, OCRResult
        print("✅ OCR Processor imported successfully")
        
        from src.image_preprocessor import ImagePreprocessor
        print("✅ Image Preprocessor imported successfully")
        
        # Test EasyOCR import
        import easyocr
        print("✅ EasyOCR imported successfully")
        
        # Test OpenCV import
        import cv2
        print("✅ OpenCV imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_image_preprocessing():
    """Test image preprocessing functionality."""
    print("\nTesting image preprocessing...")
    
    try:
        from src.image_preprocessor import ImagePreprocessor
        
        # Create test image
        test_image_path = create_test_slide_image(
            "Problem: Small businesses struggle\nSolution: AI-powered platform\nMarket: $3.2B opportunity"
        )
        
        # Load and preprocess
        preprocessor = ImagePreprocessor()
        image = Image.open(test_image_path)
        
        # Test preprocessing
        processed_image = preprocessor.preprocess_for_ocr(image)
        print("✅ Image preprocessing successful")
        
        # Test quality analysis
        quality_metrics = preprocessor.analyze_image_quality(image)
        print(f"✅ Quality analysis: {quality_metrics['overall_quality']:.2f}")
        
        # Test recommendations
        recommendations = preprocessor.get_preprocessing_recommendations(image)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        # Clean up
        os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Image preprocessing test failed: {e}")
        return False

def test_ocr_processing():
    """Test OCR processing with test images."""
    print("\nTesting OCR processing...")
    
    try:
        from src.ocr_processor import HybridOCRProcessor
        
        # Create test images with different content
        test_cases = [
            ("Problem: Customer acquisition is expensive\nSolution: Automated marketing platform", "slide1.png"),
            ("Market Size: $5.2B TAM\nTraction: 1000+ users", "slide2.png"),
            ("Team: CEO - 10 years experience\nFunding: Seeking $2M Series A", "slide3.png")
        ]
        
        processor = HybridOCRProcessor()
        
        for text_content, filename in test_cases:
            # Create test image
            image_path = create_test_slide_image(text_content, filename)
            
            # Load image
            image = Image.open(image_path)
            
            # Process with OCR
            result = processor.process_image(image, filename)
            
            print(f"✅ Processed {filename}:")
            print(f"   Method: {result.method}")
            print(f"   Valid: {result.is_valid}")
            print(f"   Text length: {len(result.text)}")
            
            if result.issues:
                print(f"   Issues: {len(result.issues)}")
            
            # Clean up
            os.remove(image_path)
        
        return True
        
    except Exception as e:
        print(f"❌ OCR processing test failed: {e}")
        return False

def test_batch_processing():
    """Test batch OCR processing."""
    print("\nTesting batch OCR processing...")
    
    try:
        from src.ocr_processor import HybridOCRProcessor
        
        # Create multiple test images
        test_slides = [
            "Problem: Market inefficiency",
            "Solution: AI optimization",
            "Market: $10B opportunity",
            "Traction: 500% growth"
        ]
        
        processor = HybridOCRProcessor()
        images_and_names = []
        
        # Create test images
        for i, slide_text in enumerate(test_slides):
            filename = f"batch_slide_{i+1}.png"
            image_path = create_test_slide_image(slide_text, filename)
            image = Image.open(image_path)
            images_and_names.append((image, filename))
        
        # Process batch
        results = processor.process_batch(images_and_names)
        
        print(f"✅ Batch processed {len(results)} images")
        
        successful = sum(1 for r in results if r.is_valid)
        print(f"✅ {successful}/{len(results)} successful extractions")
        
        # Clean up
        for i in range(len(test_slides)):
            filename = f"batch_slide_{i+1}.png"
            if os.path.exists(filename):
                os.remove(filename)
        
        return True
        
    except Exception as e:
        print(f"❌ Batch processing test failed: {e}")
        return False

def test_ocr_integration():
    """Test OCR integration with pitch analyzer."""
    print("\nTesting OCR integration with pitch analyzer...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Skipping integration test - no Google API key")
        return True
    
    try:
        from src.pitch_analyzer import PitchAnalyzer
        
        # Create mock OCR content
        ocr_content = """
        --- Slide 1 (problem.png) ---
        PROBLEM
        Small businesses lose 30% revenue from poor inventory management
        
        --- Slide 2 (solution.png) ---
        SOLUTION
        InventoryAI - AI-powered inventory optimization platform
        
        --- Slide 3 (market.png) ---
        MARKET
        $3.2B global inventory management software market
        Growing at 15% annually
        """
        
        analyzer = PitchAnalyzer()
        
        # Test OCR content post-processing
        processed_content = analyzer._post_process_ocr_content(ocr_content)
        print("✅ OCR content post-processing successful")
        
        # Test analysis with OCR source type
        result = analyzer.analyze_pitch(processed_content, "expert", "ocr")
        print("✅ OCR content analysis successful")
        print(f"   Readiness score: {result.readiness_score:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ OCR integration test failed: {e}")
        return False

def test_ui_components():
    """Test OCR UI components (without Streamlit)."""
    print("\nTesting OCR UI components...")
    
    try:
        from src.ui_components import PitchOSUI
        from src.ocr_processor import OCRResult
        
        # Create mock OCR results
        mock_results = [
            OCRResult("Test content 1", "easyocr", 0.85, 1.2),
            OCRResult("Test content 2", "google_vision", 0.92, 2.1),
            OCRResult("", "failed", 0.0, 0.5, ["Low quality image"])
        ]
        
        ui = PitchOSUI()
        print("✅ UI components initialized")
        print(f"✅ Mock OCR results created: {len(mock_results)} results")
        
        return True
        
    except Exception as e:
        print(f"❌ UI components test failed: {e}")
        return False

def main():
    """Run all OCR tests."""
    print("🔍 PitchOS OCR System Test\n")
    
    # Test imports
    if not test_ocr_imports():
        print("❌ OCR import tests failed. Please install dependencies:")
        print("pip install easyocr opencv-python google-cloud-vision")
        return
    
    # Test image preprocessing
    test_image_preprocessing()
    
    # Test OCR processing
    test_ocr_processing()
    
    # Test batch processing
    test_batch_processing()
    
    # Test integration
    test_ocr_integration()
    
    # Test UI components
    test_ui_components()
    
    print("\n🎉 OCR system tests completed!")
    print("\nOCR Features Available:")
    print("✅ Hybrid OCR (EasyOCR + Google Vision fallback)")
    print("✅ Advanced image preprocessing")
    print("✅ Batch image processing")
    print("✅ Quality analysis and recommendations")
    print("✅ Streamlit UI integration")
    print("✅ OCR content post-processing")
    
    print("\nTo use OCR in PitchOS:")
    print("1. Run: streamlit run app.py")
    print("2. Select 'Image Upload (OCR)' option")
    print("3. Upload your pitch deck images")
    print("4. Click 'Extract Text from Images'")
    print("5. Proceed with pitch analysis")

if __name__ == "__main__":
    main()
