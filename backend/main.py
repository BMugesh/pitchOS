"""
FastAPI Backend for PitchOS React Frontend
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import asyncio
from io import BytesIO
from PIL import Image

# Add src directory to path for PitchOS imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)  # Add parent directory to Python path
sys.path.insert(0, src_dir)     # Add src directory to Python path

print(f"Current directory: {current_dir}")
print(f"Parent directory: {parent_dir}")
print(f"Src directory: {src_dir}")
print(f"Src directory exists: {os.path.exists(src_dir)}")

from dotenv import load_dotenv
load_dotenv()

# FastAPI app
app = FastAPI(
    title="PitchOS API",
    description="AI-Powered Startup Pitch Deck Analyzer API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PitchAnalysisRequest(BaseModel):
    content: str
    mode: str = "expert"
    source_type: str = "text"

class PitchAnalysisResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    features: dict

# Global analyzer instance
analyzer = None

def get_analyzer():
    """Get or create analyzer instance."""
    global analyzer
    if analyzer is None:
        try:
            import src.pitch_analyzer
            from src.pitch_analyzer import PitchAnalyzer
            print("Attempting to create PitchAnalyzer instance...")
            analyzer = PitchAnalyzer()
            print("PitchAnalyzer created successfully!")
        except Exception as e:
            print(f"Failed to create analyzer: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to initialize analyzer: {str(e)}")
    return analyzer

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""

    # Check available features
    features = {
        "core_analysis": True,
        "file_upload": True,
        "ocr_processing": False,
        "analyzer_import": False
    }

    # Check OCR availability
    try:
        import easyocr
        import cv2
        features["ocr_processing"] = True
    except ImportError:
        pass

    # Check analyzer import
    try:
        import src.pitch_analyzer
        from src.pitch_analyzer import PitchAnalyzer
        features["analyzer_import"] = True
    except Exception as e:
        features["analyzer_error"] = str(e)

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        features=features
    )

@app.get("/api/test")
async def test_analyzer():
    """Test analyzer initialization."""
    try:
        from src.pitch_analyzer import PitchAnalyzer
        analyzer = PitchAnalyzer()
        return {"success": True, "message": "Analyzer initialized successfully"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/analyze", response_model=PitchAnalysisResponse)
async def analyze_pitch(request: PitchAnalysisRequest):
    """Analyze pitch content."""

    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Pitch content cannot be empty")

        # Get analyzer
        pitch_analyzer = get_analyzer()

        # Perform analysis
        result = pitch_analyzer.analyze_pitch(
            request.content,
            request.mode,
            request.source_type
        )
        
        # Convert result to dict
        result_dict = {
            "deck_summary": {
                "problem": {
                    "content": result.deck_summary.problem.content,
                    "clarity_score": result.deck_summary.problem.clarity_score,
                    "completeness_score": result.deck_summary.problem.completeness_score
                },
                "solution": {
                    "content": result.deck_summary.solution.content,
                    "clarity_score": result.deck_summary.solution.clarity_score,
                    "completeness_score": result.deck_summary.solution.completeness_score
                },
                "market": {
                    "content": result.deck_summary.market.content,
                    "clarity_score": result.deck_summary.market.clarity_score,
                    "completeness_score": result.deck_summary.market.completeness_score
                },
                "traction": {
                    "content": result.deck_summary.traction.content,
                    "clarity_score": result.deck_summary.traction.clarity_score,
                    "completeness_score": result.deck_summary.traction.completeness_score
                },
                "business_model": {
                    "content": result.deck_summary.business_model.content,
                    "clarity_score": result.deck_summary.business_model.clarity_score,
                    "completeness_score": result.deck_summary.business_model.completeness_score
                },
                "team": {
                    "content": result.deck_summary.team.content,
                    "clarity_score": result.deck_summary.team.clarity_score,
                    "completeness_score": result.deck_summary.team.completeness_score
                },
                "financials": {
                    "content": result.deck_summary.financials.content,
                    "clarity_score": result.deck_summary.financials.clarity_score,
                    "completeness_score": result.deck_summary.financials.completeness_score
                },
                "competition": {
                    "content": result.deck_summary.competition.content,
                    "clarity_score": result.deck_summary.competition.clarity_score,
                    "completeness_score": result.deck_summary.competition.completeness_score
                },
                "vision": {
                    "content": result.deck_summary.vision.content,
                    "clarity_score": result.deck_summary.vision.clarity_score,
                    "completeness_score": result.deck_summary.vision.completeness_score
                }
            },
            "readiness_score": result.readiness_score,
            "hype_meter": result.hype_meter,
            "startup_archetype": result.startup_archetype,
            "storytelling_score": result.storytelling_score,
            "emotional_hook_score": result.emotional_hook_score,
            "investor_simulations": [
                {
                    "persona": reaction.persona,
                    "avatar": reaction.avatar,
                    "reaction": reaction.reaction,
                    "investment_likelihood": reaction.investment_likelihood.value,
                    "key_concerns": reaction.key_concerns,
                    "excitement_level": reaction.excitement_level
                }
                for reaction in result.investor_simulations
            ],
            "vc_qa_battle": {
                "questions": [
                    {
                        "question": qa.question,
                        "ideal_response": qa.ideal_response,
                        "difficulty_level": qa.difficulty_level,
                        "category": qa.category
                    }
                    for qa in result.vc_qa_battle.questions
                ]
            },
            "pitch_flags": result.pitch_flags,
            "crowd_feedback": [
                {
                    "comment": feedback.comment,
                    "sentiment": feedback.sentiment,
                    "emoji": feedback.emoji,
                    "category": feedback.category
                }
                for feedback in result.crowd_feedback
            ],
            "idea_validation_report": {
                "logic_pass": result.idea_validation_report.logic_pass,
                "issues_detected": result.idea_validation_report.issues_detected,
                "confidence_score": result.idea_validation_report.confidence_score,
                "market_validation_score": result.idea_validation_report.market_validation_score,
                "technical_feasibility_score": result.idea_validation_report.technical_feasibility_score
            },
            "team_product_market_fit": {
                "team_score": result.team_product_market_fit.team_score,
                "product_score": result.team_product_market_fit.product_score,
                "market_score": result.team_product_market_fit.market_score,
                "alignment_score": result.team_product_market_fit.alignment_score,
                "rationale": result.team_product_market_fit.rationale
            },
            "recommendations": result.recommendations
        }
        
        return PitchAnalysisResponse(success=True, data=result_dict)
        
    except Exception as e:
        return PitchAnalysisResponse(success=False, error=str(e))

@app.post("/api/upload-file")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process file (PDF, DOC, TXT)."""
    
    try:
        from src.file_processor import FileProcessor
        
        processor = FileProcessor()
        content = processor.process_uploaded_file(file)
        
        if not content:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Clean and validate
        content = processor.clean_content(content)
        
        if not processor.validate_content(content):
            raise HTTPException(status_code=400, detail="File content doesn't appear to be a pitch deck")
        
        return {"success": True, "content": content, "filename": file.filename}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    """Upload and process images with OCR."""
    
    try:
        from src.ocr_processor import HybridOCRProcessor
        
        processor = HybridOCRProcessor()
        results = []
        
        for file in files:
            # Load image
            image_data = await file.read()
            image = Image.open(BytesIO(image_data))
            
            # Process with OCR
            ocr_result = processor.process_image(image, file.filename)
            
            results.append({
                "filename": file.filename,
                "text": ocr_result.text,
                "method": ocr_result.method,
                "confidence": ocr_result.confidence,
                "is_valid": ocr_result.is_valid,
                "issues": ocr_result.issues,
                "processing_time": ocr_result.processing_time
            })
        
        # Combine all text
        combined_text = []
        for i, result in enumerate(results):
            if result["text"].strip():
                combined_text.append(f"--- Slide {i+1} ({result['filename']}) ---")
                combined_text.append(result["text"])
                combined_text.append("")
        
        return {
            "success": True,
            "combined_text": "\n".join(combined_text),
            "results": results
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
