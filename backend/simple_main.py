"""
Simple PitchOS Backend - Minimal working version
This version provides basic functionality without complex dependencies
"""

import os
import sys
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Simple models
class HealthResponse(BaseModel):
    status: str
    version: str
    features: Dict[str, Any]

class PitchAnalysisRequest(BaseModel):
    content: str
    mode: str = "expert"
    source_type: str = "text"

class PitchAnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="PitchOS API",
    description="AI-powered pitch deck analyzer",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    
    features = {
        "core_analysis": True,
        "file_upload": True,
        "ocr_processing": False,
        "simple_mode": True
    }
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        features=features
    )

@app.post("/api/analyze", response_model=PitchAnalysisResponse)
async def analyze_pitch(request: PitchAnalysisRequest):
    """Analyze pitch content - Simple mock version."""
    
    try:
        if not request.content.strip():
            raise HTTPException(status_code=400, detail="Pitch content cannot be empty")
        
        # Simple mock analysis
        analysis = {
            "summary": {
                "title": "Pitch Analysis Complete",
                "overall_score": 7.5,
                "key_strengths": [
                    "Clear problem statement",
                    "Strong market opportunity",
                    "Experienced team"
                ],
                "areas_for_improvement": [
                    "Financial projections need more detail",
                    "Competitive analysis could be stronger",
                    "Go-to-market strategy needs refinement"
                ]
            },
            "detailed_feedback": {
                "problem_solution_fit": {
                    "score": 8.0,
                    "feedback": "The problem is well-defined and the solution addresses a real market need."
                },
                "market_opportunity": {
                    "score": 7.5,
                    "feedback": "Large addressable market with clear growth potential."
                },
                "business_model": {
                    "score": 7.0,
                    "feedback": "Revenue model is clear but could benefit from more detailed unit economics."
                },
                "team": {
                    "score": 8.5,
                    "feedback": "Strong founding team with relevant experience and complementary skills."
                },
                "financials": {
                    "score": 6.5,
                    "feedback": "Financial projections are present but need more supporting assumptions."
                }
            },
            "investor_perspective": {
                "investment_likelihood": "Medium-High",
                "key_concerns": [
                    "Market competition",
                    "Scalability questions",
                    "Customer acquisition costs"
                ],
                "next_steps": [
                    "Provide detailed financial model",
                    "Show customer validation",
                    "Demonstrate early traction"
                ]
            }
        }
        
        return PitchAnalysisResponse(
            success=True,
            analysis=analysis
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return PitchAnalysisResponse(
            success=False,
            error=f"Analysis failed: {str(e)}"
        )

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload."""
    
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Simple file handling - just return success
        return {
            "success": True,
            "filename": file.filename,
            "message": "File uploaded successfully (mock)"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Upload failed: {str(e)}"
        }

if __name__ == "__main__":
    print("🚀 Starting Simple PitchOS Backend...")
    print("📍 Backend URL: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔄 CORS enabled for: http://localhost:3000")
    
    uvicorn.run(
        "simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
