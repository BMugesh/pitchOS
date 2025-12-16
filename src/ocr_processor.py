"""Hybrid OCR processor for PitchOS with EasyOCR primary and Google Cloud Vision fallback."""

import base64
import io
import re
from typing import List, Dict, Tuple, Optional, Any
import numpy as np
import cv2
from PIL import Image
import easyocr
import requests
from src.config import config

class OCRResult:
    """OCR result with metadata."""
    
    def __init__(self, text: str, method: str, confidence: float = 0.0, 
                 processing_time: float = 0.0, issues: List[str] = None):
        self.text = text
        self.method = method  # 'easyocr' or 'google_vision'
        self.confidence = confidence
        self.processing_time = processing_time
        self.issues = issues or []
        self.is_valid = self._validate_text()
    
    def _validate_text(self) -> bool:
        """Validate if extracted text is meaningful."""
        if not self.text or len(self.text.strip()) < config.OCR_MIN_TEXT_LENGTH:
            return False
        
        # Check ratio of alphabetic characters
        alpha_chars = sum(1 for c in self.text if c.isalpha())
        total_chars = len(self.text.replace(' ', ''))
        
        if total_chars == 0:
            return False
            
        alpha_ratio = alpha_chars / total_chars
        return alpha_ratio >= config.OCR_MIN_ALPHA_RATIO

class HybridOCRProcessor:
    """Hybrid OCR processor with EasyOCR primary and Google Cloud Vision fallback."""
    
    def __init__(self):
        """Initialize OCR processor."""
        self.easyocr_reader = None
        self._init_easyocr()
    
    def _init_easyocr(self):
        """Initialize EasyOCR reader."""
        try:
            self.easyocr_reader = easyocr.Reader(config.OCR_LANGUAGES, gpu=False)
        except Exception as e:
            print(f"Warning: Failed to initialize EasyOCR: {e}")
            self.easyocr_reader = None
    
    def process_image(self, image: Image.Image, filename: str = "") -> OCRResult:
        """Process single image with hybrid OCR approach."""
        import time
        
        # Preprocess image
        processed_image = self._preprocess_image(image)
        
        # Try EasyOCR first
        start_time = time.time()
        easyocr_result = self._extract_with_easyocr(processed_image)
        easyocr_time = time.time() - start_time
        
        if easyocr_result.is_valid:
            easyocr_result.processing_time = easyocr_time
            return easyocr_result
        
        # Fallback to Google Cloud Vision
        start_time = time.time()
        vision_result = self._extract_with_google_vision(processed_image)
        vision_time = time.time() - start_time
        
        if vision_result.is_valid:
            vision_result.processing_time = vision_time
            vision_result.issues.append("EasyOCR failed, used Google Vision fallback")
            return vision_result
        
        # Both failed
        return OCRResult(
            text="",
            method="failed",
            confidence=0.0,
            processing_time=easyocr_time + vision_time,
            issues=["Both EasyOCR and Google Vision failed to extract meaningful text"]
        )
    
    def process_batch(self, images: List[Tuple[Image.Image, str]]) -> List[OCRResult]:
        """Process multiple images in batch."""
        results = []
        
        for image, filename in images:
            result = self.process_image(image, filename)
            results.append(result)
        
        return results
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image to improve OCR accuracy."""
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Resize if too large
        height, width = cv_image.shape[:2]
        if width > config.IMAGE_MAX_WIDTH or height > config.IMAGE_MAX_HEIGHT:
            scale = min(config.IMAGE_MAX_WIDTH / width, config.IMAGE_MAX_HEIGHT / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            cv_image = cv2.resize(cv_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # Apply sharpening
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        
        # Convert back to PIL
        processed_image = Image.fromarray(sharpened)
        
        return processed_image
    
    def _extract_with_easyocr(self, image: Image.Image) -> OCRResult:
        """Extract text using EasyOCR."""
        if not self.easyocr_reader:
            return OCRResult("", "easyocr", 0.0, 0.0, ["EasyOCR not initialized"])
        
        try:
            # Convert PIL to numpy array
            img_array = np.array(image)
            
            # Extract text
            results = self.easyocr_reader.readtext(img_array)
            
            # Combine all text
            text_parts = []
            total_confidence = 0.0
            
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filter low confidence results
                    text_parts.append(text)
                    total_confidence += confidence
            
            combined_text = ' '.join(text_parts)
            avg_confidence = total_confidence / len(results) if results else 0.0
            
            return OCRResult(
                text=combined_text,
                method="easyocr",
                confidence=avg_confidence
            )
            
        except Exception as e:
            return OCRResult("", "easyocr", 0.0, 0.0, [f"EasyOCR error: {str(e)}"])
    
    def _extract_with_google_vision(self, image: Image.Image) -> OCRResult:
        """Extract text using Google Cloud Vision API."""
        if not config.GOOGLE_CLOUD_VISION_API_KEY:
            return OCRResult("", "google_vision", 0.0, 0.0, ["Google Cloud Vision API key not configured"])
        
        try:
            # Convert image to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # Prepare API request
            url = f"https://vision.googleapis.com/v1/images:annotate?key={config.GOOGLE_CLOUD_VISION_API_KEY}"
            
            payload = {
                "requests": [
                    {
                        "image": {
                            "content": image_base64
                        },
                        "features": [
                            {
                                "type": "TEXT_DETECTION",
                                "maxResults": 50
                            }
                        ]
                    }
                ]
            }
            
            # Make API call
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract text
            if 'responses' in result and result['responses']:
                annotations = result['responses'][0].get('textAnnotations', [])
                if annotations:
                    # First annotation contains full text
                    full_text = annotations[0].get('description', '')
                    
                    # Calculate average confidence
                    confidences = []
                    for annotation in annotations[1:]:  # Skip first (full text)
                        if 'confidence' in annotation:
                            confidences.append(annotation['confidence'])
                    
                    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.8
                    
                    return OCRResult(
                        text=full_text,
                        method="google_vision",
                        confidence=avg_confidence
                    )
            
            return OCRResult("", "google_vision", 0.0, 0.0, ["No text detected by Google Vision"])
            
        except Exception as e:
            return OCRResult("", "google_vision", 0.0, 0.0, [f"Google Vision error: {str(e)}"])
    
    def get_image_quality_score(self, image: Image.Image) -> float:
        """Calculate image quality score for OCR suitability."""
        try:
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Calculate Laplacian variance (blur detection)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize to 0-1 scale
            quality_score = min(laplacian_var / 1000.0, 1.0)
            
            return quality_score
            
        except Exception:
            return 0.5  # Default medium quality
    
    def suggest_image_improvements(self, image: Image.Image) -> List[str]:
        """Suggest improvements for better OCR results."""
        suggestions = []
        
        try:
            quality_score = self.get_image_quality_score(image)
            
            if quality_score < config.IMAGE_QUALITY_THRESHOLD:
                suggestions.append("Image appears blurry - try taking a sharper photo")
            
            # Check image size
            width, height = image.size
            if width < 800 or height < 600:
                suggestions.append("Image resolution is low - try using a higher resolution")
            
            # Check if image is too dark or too bright
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            mean_brightness = np.mean(gray)
            
            if mean_brightness < 50:
                suggestions.append("Image is too dark - try better lighting")
            elif mean_brightness > 200:
                suggestions.append("Image is too bright - reduce exposure")
            
        except Exception:
            suggestions.append("Unable to analyze image quality")
        
        return suggestions
