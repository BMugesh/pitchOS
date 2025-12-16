"""Advanced image preprocessing for better OCR results in PitchOS."""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Tuple, List, Optional
from src.config import config

class ImagePreprocessor:
    """Advanced image preprocessing for OCR optimization."""
    
    def __init__(self):
        """Initialize image preprocessor."""
        pass
    
    def preprocess_for_ocr(self, image: Image.Image, aggressive: bool = False) -> Image.Image:
        """
        Comprehensive preprocessing pipeline for OCR.
        
        Args:
            image: Input PIL Image
            aggressive: Whether to apply more aggressive preprocessing
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to OpenCV format
        cv_image = self._pil_to_cv2(image)
        
        # Step 1: Resize if necessary
        cv_image = self._resize_image(cv_image)
        
        # Step 2: Convert to grayscale
        if len(cv_image.shape) == 3:
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv_image
        
        # Step 3: Noise reduction
        denoised = self._denoise_image(gray, aggressive)
        
        # Step 4: Contrast enhancement
        enhanced = self._enhance_contrast(denoised, aggressive)
        
        # Step 5: Sharpening
        sharpened = self._sharpen_image(enhanced, aggressive)
        
        # Step 6: Binarization (if aggressive)
        if aggressive:
            processed = self._binarize_image(sharpened)
        else:
            processed = sharpened
        
        # Convert back to PIL
        return self._cv2_to_pil(processed)
    
    def preprocess_slide_image(self, image: Image.Image) -> Image.Image:
        """Specialized preprocessing for presentation slides."""
        cv_image = self._pil_to_cv2(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY) if len(cv_image.shape) == 3 else cv_image
        
        # Detect if image has dark background (common in slides)
        mean_brightness = np.mean(gray)
        is_dark_background = mean_brightness < 128
        
        if is_dark_background:
            # Invert for better OCR on dark slides
            gray = cv2.bitwise_not(gray)
        
        # Apply morphological operations to clean up text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        
        # Enhance contrast specifically for text
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(cleaned)
        
        return self._cv2_to_pil(enhanced)
    
    def detect_text_regions(self, image: Image.Image) -> List[Tuple[int, int, int, int]]:
        """
        Detect text regions in the image using EAST text detector or MSER.
        
        Returns:
            List of bounding boxes (x, y, width, height)
        """
        cv_image = self._pil_to_cv2(image)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY) if len(cv_image.shape) == 3 else cv_image
        
        # Use MSER (Maximally Stable Extremal Regions) for text detection
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)
        
        bounding_boxes = []
        for region in regions:
            x, y, w, h = cv2.boundingRect(region.reshape(-1, 1, 2))
            
            # Filter out very small or very large regions
            if 10 < w < image.width * 0.8 and 10 < h < image.height * 0.8:
                # Filter by aspect ratio (text regions are usually wider than tall)
                aspect_ratio = w / h
                if 0.1 < aspect_ratio < 20:
                    bounding_boxes.append((x, y, w, h))
        
        return bounding_boxes
    
    def crop_text_regions(self, image: Image.Image) -> List[Image.Image]:
        """Crop individual text regions for better OCR."""
        text_regions = self.detect_text_regions(image)
        cropped_images = []
        
        for x, y, w, h in text_regions:
            # Add some padding
            padding = 5
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.width - x, w + 2 * padding)
            h = min(image.height - y, h + 2 * padding)
            
            cropped = image.crop((x, y, x + w, y + h))
            cropped_images.append(cropped)
        
        return cropped_images
    
    def _pil_to_cv2(self, pil_image: Image.Image) -> np.ndarray:
        """Convert PIL Image to OpenCV format."""
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def _cv2_to_pil(self, cv_image: np.ndarray) -> Image.Image:
        """Convert OpenCV image to PIL format."""
        if len(cv_image.shape) == 3:
            return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        else:
            return Image.fromarray(cv_image)
    
    def _resize_image(self, cv_image: np.ndarray) -> np.ndarray:
        """Resize image if it's too large."""
        height, width = cv_image.shape[:2]
        
        if width > config.IMAGE_MAX_WIDTH or height > config.IMAGE_MAX_HEIGHT:
            scale = min(config.IMAGE_MAX_WIDTH / width, config.IMAGE_MAX_HEIGHT / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(cv_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return cv_image
    
    def _denoise_image(self, gray_image: np.ndarray, aggressive: bool = False) -> np.ndarray:
        """Apply noise reduction."""
        if aggressive:
            # More aggressive denoising
            return cv2.bilateralFilter(gray_image, 9, 75, 75)
        else:
            # Gentle denoising
            return cv2.fastNlMeansDenoising(gray_image)
    
    def _enhance_contrast(self, gray_image: np.ndarray, aggressive: bool = False) -> np.ndarray:
        """Enhance image contrast."""
        if aggressive:
            # Histogram equalization
            return cv2.equalizeHist(gray_image)
        else:
            # CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            return clahe.apply(gray_image)
    
    def _sharpen_image(self, gray_image: np.ndarray, aggressive: bool = False) -> np.ndarray:
        """Apply sharpening filter."""
        if aggressive:
            # Strong sharpening kernel
            kernel = np.array([[-1, -1, -1, -1, -1],
                              [-1,  2,  2,  2, -1],
                              [-1,  2,  8,  2, -1],
                              [-1,  2,  2,  2, -1],
                              [-1, -1, -1, -1, -1]]) / 8.0
        else:
            # Gentle sharpening kernel
            kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])
        
        return cv2.filter2D(gray_image, -1, kernel)
    
    def _binarize_image(self, gray_image: np.ndarray) -> np.ndarray:
        """Convert to binary image using adaptive thresholding."""
        # Use Otsu's thresholding combined with Gaussian adaptive thresholding
        _, binary1 = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        binary2 = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        
        # Combine both methods
        combined = cv2.bitwise_and(binary1, binary2)
        
        return combined
    
    def analyze_image_quality(self, image: Image.Image) -> dict:
        """Analyze image quality metrics."""
        cv_image = self._pil_to_cv2(image)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY) if len(cv_image.shape) == 3 else cv_image
        
        # Blur detection using Laplacian variance
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        blur_score = min(laplacian_var / 1000.0, 1.0)
        
        # Brightness analysis
        brightness = np.mean(gray)
        
        # Contrast analysis
        contrast = gray.std()
        
        # Noise estimation
        noise_level = self._estimate_noise(gray)
        
        return {
            'blur_score': blur_score,
            'brightness': brightness,
            'contrast': contrast,
            'noise_level': noise_level,
            'overall_quality': (blur_score + min(contrast / 50.0, 1.0)) / 2
        }
    
    def _estimate_noise(self, gray_image: np.ndarray) -> float:
        """Estimate noise level in the image."""
        # Use Laplacian to estimate noise
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        noise_level = laplacian.var()
        return min(noise_level / 10000.0, 1.0)
    
    def get_preprocessing_recommendations(self, image: Image.Image) -> List[str]:
        """Get recommendations for image preprocessing."""
        quality_metrics = self.analyze_image_quality(image)
        recommendations = []
        
        if quality_metrics['blur_score'] < 0.3:
            recommendations.append("Image is blurry - consider retaking with better focus")
        
        if quality_metrics['brightness'] < 50:
            recommendations.append("Image is too dark - increase lighting or exposure")
        elif quality_metrics['brightness'] > 200:
            recommendations.append("Image is too bright - reduce exposure")
        
        if quality_metrics['contrast'] < 20:
            recommendations.append("Low contrast - try adjusting camera settings")
        
        if quality_metrics['noise_level'] > 0.7:
            recommendations.append("High noise detected - try better lighting or lower ISO")
        
        if not recommendations:
            recommendations.append("Image quality is good for OCR processing")
        
        return recommendations
