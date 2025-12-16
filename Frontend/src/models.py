"""Data models for PitchOS."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

class InvestmentLikelihood(str, Enum):
    """Investment likelihood levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    VERY_LOW = "Very Low"

class PitchElement(BaseModel):
    """Individual pitch deck element."""
    content: str
    clarity_score: float = Field(ge=0, le=10)
    completeness_score: float = Field(ge=0, le=10)

class DeckSummary(BaseModel):
    """Summary of pitch deck elements."""
    problem: PitchElement
    solution: PitchElement
    market: PitchElement
    traction: PitchElement
    business_model: PitchElement
    team: PitchElement
    financials: PitchElement
    competition: PitchElement
    vision: PitchElement

class InvestorReaction(BaseModel):
    """Investor persona reaction."""
    persona: str
    avatar: str
    reaction: str
    investment_likelihood: InvestmentLikelihood
    key_concerns: List[str]
    excitement_level: float = Field(ge=0, le=10)

class QAItem(BaseModel):
    """Q&A battle item."""
    question: str
    ideal_response: str
    difficulty_level: str
    category: str

class VCQABattle(BaseModel):
    """VC Q&A Battle results."""
    questions: List[QAItem]

class IdeaValidationReport(BaseModel):
    """Idea validation analysis."""
    logic_pass: bool
    issues_detected: List[str]
    confidence_score: float = Field(ge=0, le=1)
    market_validation_score: float = Field(ge=0, le=10)
    technical_feasibility_score: float = Field(ge=0, le=10)

class TeamProductMarketFit(BaseModel):
    """Team-Product-Market fit analysis."""
    team_score: float = Field(ge=0, le=10)
    product_score: float = Field(ge=0, le=10)
    market_score: float = Field(ge=0, le=10)
    alignment_score: float = Field(ge=0, le=10)
    rationale: str

class CrowdFeedback(BaseModel):
    """AI crowd feedback item."""
    comment: str
    sentiment: str  # positive, negative, neutral
    emoji: str
    category: str  # technical, business, presentation, etc.

class PitchAnalysisResult(BaseModel):
    """Complete pitch analysis result."""
    deck_summary: DeckSummary
    readiness_score: float = Field(ge=0, le=100)
    investor_simulations: List[InvestorReaction]
    vc_qa_battle: VCQABattle
    hype_meter: float = Field(ge=0, le=100)
    startup_archetype: str
    pitch_flags: List[str]
    crowd_feedback: List[CrowdFeedback]
    idea_validation_report: IdeaValidationReport
    team_product_market_fit: TeamProductMarketFit
    recommendations: Dict[str, List[str]]
    visual_communication_score: Optional[float] = Field(ge=0, le=10, default=None)
    storytelling_score: float = Field(ge=0, le=10)
    emotional_hook_score: float = Field(ge=0, le=10)
