"""
Test script for PitchOS components
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.append('src')

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from src.config import config
        print("✅ Config imported successfully")
        
        from src.models import PitchAnalysisResult, DeckSummary
        print("✅ Models imported successfully")
        
        from src.pitch_analyzer import PitchAnalyzer
        print("✅ PitchAnalyzer imported successfully")
        
        from src.ui_components import PitchOSUI
        print("✅ UI Components imported successfully")
        
        from src.file_processor import FileProcessor
        print("✅ File Processor imported successfully")
        
        from src.scoring_system import PitchScoringSystem
        print("✅ Scoring System imported successfully")
        
        from src.investor_personas import InvestorPersonaSimulator
        print("✅ Investor Personas imported successfully")
        
        from src.vc_qa_battle import VCQABattleGenerator
        print("✅ VC Q&A Battle imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration settings."""
    print("\nTesting configuration...")
    
    from src.config import config
    
    print(f"Model name: {config.MODEL_NAME}")
    print(f"Page title: {config.PAGE_TITLE}")
    print(f"API key configured: {'Yes' if config.GOOGLE_API_KEY else 'No'}")
    
    if not config.GOOGLE_API_KEY:
        print("⚠️  Warning: Google API key not found. Set GOOGLE_API_KEY in .env file.")
    else:
        print("✅ Configuration looks good")

def test_sample_analysis():
    """Test analysis with sample pitch."""
    print("\nTesting sample analysis...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Skipping analysis test - no API key")
        return
    
    sample_pitch = """
    Problem: Small businesses struggle with inventory management, leading to 30% revenue loss.
    Solution: InventoryAI is an AI-powered inventory optimization platform.
    Market: The global inventory management software market is $3.2B.
    Traction: 150 paying customers, $50K MRR, 25% month-over-month growth.
    Business Model: SaaS subscription starting at $99/month per location.
    Team: CEO with 10 years retail experience, CTO from Amazon.
    Financials: Seeking $2M Series A to reach $1M ARR.
    Competition: Traditional solutions lack AI. We're 10x more accurate.
    Vision: Become the operating system for small business inventory.
    """
    
    try:
        from src.pitch_analyzer import PitchAnalyzer
        
        analyzer = PitchAnalyzer()
        print("✅ Analyzer initialized")
        
        # Test basic analysis (without full AI call to save API credits)
        from src.scoring_system import PitchScoringSystem
        from src.models import PitchElement, DeckSummary
        
        scoring = PitchScoringSystem()
        
        # Create mock deck summary for testing
        mock_element = PitchElement(content="Test content", clarity_score=7.0, completeness_score=8.0)
        mock_summary = DeckSummary(
            problem=mock_element,
            solution=mock_element,
            market=mock_element,
            traction=mock_element,
            business_model=mock_element,
            team=mock_element,
            financials=mock_element,
            competition=mock_element,
            vision=mock_element
        )
        
        # Test scoring functions
        readiness_score = scoring.calculate_readiness_score(mock_summary, sample_pitch)
        hype_score = scoring.calculate_hype_meter(sample_pitch)
        archetype = scoring.detect_startup_archetype(sample_pitch, mock_summary)
        
        print(f"✅ Readiness score: {readiness_score:.1f}")
        print(f"✅ Hype score: {hype_score:.1f}")
        print(f"✅ Archetype: {archetype}")
        
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")

def test_file_processor():
    """Test file processing capabilities."""
    print("\nTesting file processor...")
    
    try:
        from src.file_processor import FileProcessor
        
        processor = FileProcessor()
        
        # Test content validation
        valid_content = "Problem: Test problem. Solution: Test solution. Market: Test market."
        invalid_content = "Too short"
        
        assert processor.validate_content(valid_content) == True
        assert processor.validate_content(invalid_content) == False
        
        # Test content cleaning
        messy_content = "  Problem:   Test   problem.  \n\n  Solution:   Test   solution.  "
        clean_content = processor.clean_content(messy_content)
        
        assert "Problem: Test problem. Solution: Test solution." in clean_content
        
        print("✅ File processor tests passed")
        
    except Exception as e:
        print(f"❌ File processor test failed: {e}")

def main():
    """Run all tests."""
    print("🚀 PitchOS System Test\n")
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed. Please check dependencies.")
        return
    
    # Test configuration
    test_config()
    
    # Test file processor
    test_file_processor()
    
    # Test sample analysis
    test_sample_analysis()
    
    print("\n🎉 All tests completed!")
    print("\nTo run PitchOS:")
    print("1. Make sure you have set GOOGLE_API_KEY in your .env file")
    print("2. Run: streamlit run app.py")
    print("3. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()
