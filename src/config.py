"""Configuration settings for PitchOS."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # Google APIs
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CLOUD_VISION_API_KEY = os.getenv("GOOGLE_CLOUD_VISION_API_KEY")
    
    # Streamlit settings
    STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
    STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    
    # Application settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Model settings
    MODEL_NAME = "gemini-1.5-flash"
    MAX_TOKENS = 8192
    TEMPERATURE = 0.7
    
    # UI settings
    PAGE_TITLE = "PitchOS - AI Pitch Deck Analyzer"
    PAGE_ICON = "🚀"
    LAYOUT = "wide"
    
    # Scoring thresholds
    READINESS_THRESHOLDS = {
        "excellent": 90,
        "good": 75,
        "fair": 60,
        "poor": 40
    }
    
    # Investor personas
    INVESTOR_PERSONAS = [
        {
            "name": "Risk-Averse VC",
            "avatar": "🏦",
            "focus": ["traction", "financials", "market_validation"],
            "style": "conservative"
        },
        {
            "name": "Visionary Angel",
            "avatar": "👼",
            "focus": ["vision", "team", "innovation"],
            "style": "optimistic"
        },
        {
            "name": "Corporate Strategic",
            "avatar": "🏢",
            "focus": ["market_fit", "scalability", "partnerships"],
            "style": "strategic"
        }
    ]
    
    # Startup archetypes
    STARTUP_ARCHETYPES = [
        "Builder", "Visionary", "Hustler", "Academic", 
        "Disruptor", "Optimizer", "Connector", "Researcher"
    ]
    
    # Hype terms to detect
    HYPE_TERMS = [
        "revolutionary", "game-changing", "disruptive", "paradigm shift",
        "web3", "blockchain", "AI-powered", "machine learning",
        "synergy", "leverage", "scalable", "unicorn potential",
        "first-mover advantage", "blue ocean", "viral growth"
    ]

    # OCR Configuration
    OCR_LANGUAGES = ['en']  # EasyOCR supported languages
    OCR_MIN_TEXT_LENGTH = 20  # Minimum text length to consider valid
    OCR_MIN_ALPHA_RATIO = 0.3  # Minimum ratio of alphabetic characters

    # Image preprocessing settings
    IMAGE_MAX_WIDTH = 1920
    IMAGE_MAX_HEIGHT = 1080
    IMAGE_QUALITY_THRESHOLD = 0.7  # For blur detection

    # Supported image formats
    SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']

config = Config()
