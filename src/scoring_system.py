"""Scoring and validation systems for PitchOS."""

import re
import math
from typing import List, Dict, Any, Tuple
from src.config import config
from src.models import DeckSummary, IdeaValidationReport, TeamProductMarketFit

class PitchScoringSystem:
    """Comprehensive scoring system for startup pitches."""
    
    def __init__(self):
        """Initialize the scoring system."""
        pass
    
    def calculate_readiness_score(self, deck_summary: DeckSummary, pitch_content: str) -> float:
        """Calculate overall pitch readiness score (0-100)."""
        
        # Element weights based on VC importance
        weights = {
            'problem': 0.15,      # Clear problem definition
            'solution': 0.15,     # Solution clarity
            'market': 0.12,       # Market opportunity
            'traction': 0.20,     # Most important - proof of execution
            'business_model': 0.12, # Revenue model
            'team': 0.10,         # Team capability
            'financials': 0.10,   # Financial projections
            'competition': 0.04,  # Competitive analysis
            'vision': 0.02        # Long-term vision
        }
        
        total_score = 0
        
        for element_name, weight in weights.items():
            element = getattr(deck_summary, element_name)
            # Combine clarity and completeness scores
            element_score = (element.clarity_score + element.completeness_score) / 2
            total_score += element_score * weight * 10  # Scale to 0-100
        
        # Apply bonuses and penalties
        bonus_score = self._calculate_bonus_score(pitch_content)
        penalty_score = self._calculate_penalty_score(pitch_content)
        
        final_score = total_score + bonus_score - penalty_score
        
        return max(0, min(100, final_score))
    
    def calculate_hype_meter(self, pitch_content: str) -> float:
        """Calculate hype level (0-100)."""
        hype_score = 0
        content_lower = pitch_content.lower()
        
        # Check for hype terms
        for term in config.HYPE_TERMS:
            count = len(re.findall(rf'\b{re.escape(term.lower())}\b', content_lower))
            hype_score += count * 4  # Each hype term adds 4 points
        
        # Check for excessive superlatives
        superlatives = [
            'best', 'greatest', 'ultimate', 'revolutionary', 'groundbreaking',
            'unprecedented', 'amazing', 'incredible', 'fantastic', 'perfect'
        ]
        
        for superlative in superlatives:
            count = len(re.findall(rf'\b{superlative}\b', content_lower))
            hype_score += count * 3
        
        # Check for excessive exclamation marks
        exclamation_count = pitch_content.count('!')
        if exclamation_count > 5:
            hype_score += (exclamation_count - 5) * 2
        
        # Check for ALL CAPS words
        caps_words = re.findall(r'\b[A-Z]{3,}\b', pitch_content)
        hype_score += len(caps_words) * 2
        
        # Check for percentage claims without sources
        percentage_claims = re.findall(r'\d+%', pitch_content)
        if len(percentage_claims) > 3 and 'source' not in content_lower:
            hype_score += 10
        
        return min(100, hype_score)
    
    def detect_startup_archetype(self, pitch_content: str, deck_summary: DeckSummary) -> str:
        """Detect startup archetype based on content analysis."""
        content_lower = pitch_content.lower()
        
        archetype_scores = {}
        
        # Define archetype indicators with weights
        archetype_indicators = {
            "Builder": {
                "keywords": ["product", "technology", "engineering", "development", "build", "create", "technical"],
                "weight": 1.0
            },
            "Visionary": {
                "keywords": ["future", "vision", "transform", "revolution", "change the world", "paradigm", "disrupt"],
                "weight": 1.2
            },
            "Hustler": {
                "keywords": ["sales", "growth", "customers", "revenue", "market", "business", "profit", "scale"],
                "weight": 1.0
            },
            "Academic": {
                "keywords": ["research", "study", "analysis", "data", "scientific", "methodology", "peer-reviewed"],
                "weight": 0.8
            },
            "Disruptor": {
                "keywords": ["disrupt", "traditional", "outdated", "new way", "challenge", "status quo", "innovative"],
                "weight": 1.1
            },
            "Optimizer": {
                "keywords": ["efficiency", "optimize", "improve", "better", "streamline", "automate", "faster"],
                "weight": 0.9
            },
            "Connector": {
                "keywords": ["network", "platform", "connect", "community", "social", "marketplace", "ecosystem"],
                "weight": 1.0
            },
            "Researcher": {
                "keywords": ["insights", "discovery", "findings", "investigation", "explore", "understand", "learn"],
                "weight": 0.8
            }
        }
        
        # Calculate scores for each archetype
        for archetype, config_data in archetype_indicators.items():
            score = 0
            for keyword in config_data["keywords"]:
                count = content_lower.count(keyword)
                score += count * config_data["weight"]
            
            # Bonus for team background alignment
            team_content = deck_summary.team.content.lower()
            for keyword in config_data["keywords"]:
                if keyword in team_content:
                    score += 2
            
            archetype_scores[archetype] = score
        
        # Return the archetype with highest score
        if not archetype_scores or max(archetype_scores.values()) == 0:
            return "Builder"  # Default
        
        return max(archetype_scores, key=archetype_scores.get)
    
    def validate_idea(self, pitch_content: str, deck_summary: DeckSummary) -> IdeaValidationReport:
        """Comprehensive idea validation."""
        issues = []
        content_lower = pitch_content.lower()
        
        # Market validation checks
        market_issues = self._validate_market_claims(pitch_content, deck_summary.market.content)
        issues.extend(market_issues)
        
        # Problem-solution fit
        problem_solution_issues = self._validate_problem_solution_fit(deck_summary)
        issues.extend(problem_solution_issues)
        
        # Traction validation
        traction_issues = self._validate_traction_claims(deck_summary.traction.content)
        issues.extend(traction_issues)
        
        # Business model validation
        business_model_issues = self._validate_business_model(deck_summary.business_model.content)
        issues.extend(business_model_issues)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(deck_summary, len(issues))
        
        # Calculate specific scores
        market_validation_score = max(0, 10 - len(market_issues) * 2)
        technical_feasibility_score = deck_summary.solution.clarity_score
        
        return IdeaValidationReport(
            logic_pass=len(issues) < 4,  # Pass if fewer than 4 major issues
            issues_detected=issues,
            confidence_score=confidence_score,
            market_validation_score=market_validation_score,
            technical_feasibility_score=technical_feasibility_score
        )
    
    def analyze_team_product_market_fit(self, deck_summary: DeckSummary) -> TeamProductMarketFit:
        """Analyze team-product-market alignment."""
        
        # Calculate individual scores
        team_score = (deck_summary.team.clarity_score + deck_summary.team.completeness_score) / 2
        product_score = (deck_summary.solution.clarity_score + deck_summary.solution.completeness_score) / 2
        market_score = (deck_summary.market.clarity_score + deck_summary.market.completeness_score) / 2
        
        # Calculate alignment score (how well balanced the three areas are)
        scores = [team_score, product_score, market_score]
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        alignment_score = max(0, 10 - variance)  # Lower variance = better alignment
        
        # Generate rationale
        rationale = self._generate_tpm_rationale(team_score, product_score, market_score, alignment_score)
        
        return TeamProductMarketFit(
            team_score=team_score,
            product_score=product_score,
            market_score=market_score,
            alignment_score=alignment_score,
            rationale=rationale
        )
    
    def _calculate_bonus_score(self, pitch_content: str) -> float:
        """Calculate bonus points for strong elements."""
        bonus = 0
        content_lower = pitch_content.lower()
        
        # Bonus for concrete metrics
        if re.search(r'\d+%.*growth', content_lower):
            bonus += 5
        
        if re.search(r'\$\d+.*revenue', content_lower):
            bonus += 5
        
        # Bonus for customer validation
        if any(term in content_lower for term in ['customer', 'user', 'pilot', 'beta']):
            bonus += 3
        
        # Bonus for partnerships
        if 'partnership' in content_lower or 'partner' in content_lower:
            bonus += 2
        
        return bonus
    
    def _calculate_penalty_score(self, pitch_content: str) -> float:
        """Calculate penalty points for weak elements."""
        penalty = 0
        content_lower = pitch_content.lower()
        
        # Penalty for too much jargon
        jargon_count = sum(1 for term in config.HYPE_TERMS if term.lower() in content_lower)
        if jargon_count > 5:
            penalty += (jargon_count - 5) * 2
        
        # Penalty for vague language
        vague_terms = ['synergy', 'leverage', 'optimize', 'streamline', 'innovative', 'cutting-edge']
        vague_count = sum(1 for term in vague_terms if term in content_lower)
        if vague_count > 3:
            penalty += (vague_count - 3) * 1.5
        
        return penalty

    def _validate_market_claims(self, pitch_content: str, market_content: str) -> List[str]:
        """Validate market size and opportunity claims."""
        issues = []
        content_lower = pitch_content.lower()

        # Check for unsupported market size claims
        if re.search(r'\$\d+.*billion.*market', content_lower):
            if not any(source in content_lower for source in ['gartner', 'mckinsey', 'forrester', 'idc', 'research']):
                issues.append("Large market size claims lack credible sources")

        # Check for TAM/SAM/SOM clarity
        if 'tam' in content_lower or 'total addressable market' in content_lower:
            if not ('sam' in content_lower or 'serviceable addressable market' in content_lower):
                issues.append("TAM mentioned but SAM/SOM not clearly defined")

        # Check for market validation
        if market_content and len(market_content) > 50:
            if not any(term in market_content.lower() for term in ['survey', 'interview', 'research', 'validation']):
                issues.append("Market opportunity lacks validation evidence")

        return issues

    def _validate_problem_solution_fit(self, deck_summary: DeckSummary) -> List[str]:
        """Validate problem-solution alignment."""
        issues = []

        problem_score = deck_summary.problem.clarity_score
        solution_score = deck_summary.solution.clarity_score

        # Check if problem and solution are well-aligned
        if abs(problem_score - solution_score) > 4:
            issues.append("Problem-solution alignment needs improvement")

        # Check if both are clearly defined
        if problem_score < 6 or solution_score < 6:
            issues.append("Problem or solution not clearly articulated")

        # Check for solution complexity vs problem simplicity
        problem_content = deck_summary.problem.content.lower()
        solution_content = deck_summary.solution.content.lower()

        if len(solution_content) > len(problem_content) * 3:
            issues.append("Solution seems overly complex for the stated problem")

        return issues

    def _validate_traction_claims(self, traction_content: str) -> List[str]:
        """Validate traction and growth claims."""
        issues = []

        if not traction_content or len(traction_content) < 20:
            issues.append("Insufficient traction evidence provided")
            return issues

        traction_lower = traction_content.lower()

        # Check for specific metrics
        has_metrics = any(pattern in traction_lower for pattern in [
            r'\d+.*user', r'\d+.*customer', r'\d+.*revenue', r'\d+%.*growth'
        ])

        if not has_metrics:
            issues.append("Traction lacks specific, measurable metrics")

        # Check for unrealistic growth claims
        if re.search(r'\d{3,}%.*growth', traction_lower):  # 100%+ growth
            if 'month' in traction_lower:
                issues.append("Extremely high growth claims may not be sustainable")

        return issues

    def _validate_business_model(self, business_model_content: str) -> List[str]:
        """Validate business model and monetization."""
        issues = []

        if not business_model_content or len(business_model_content) < 20:
            issues.append("Business model not clearly defined")
            return issues

        model_lower = business_model_content.lower()

        # Check for revenue streams
        revenue_indicators = ['subscription', 'saas', 'transaction', 'commission', 'advertising', 'freemium']
        if not any(indicator in model_lower for indicator in revenue_indicators):
            issues.append("Revenue model not clearly specified")

        # Check for pricing information
        if not any(term in model_lower for term in ['price', 'pricing', '$', 'cost', 'fee']):
            issues.append("Pricing strategy not mentioned")

        return issues

    def _calculate_confidence_score(self, deck_summary: DeckSummary, issue_count: int) -> float:
        """Calculate overall confidence score (0-1)."""

        # Base score from element quality
        element_scores = [
            deck_summary.problem.clarity_score,
            deck_summary.solution.clarity_score,
            deck_summary.market.clarity_score,
            deck_summary.traction.clarity_score,
            deck_summary.business_model.clarity_score
        ]

        base_score = sum(element_scores) / (len(element_scores) * 10)  # Normalize to 0-1

        # Penalty for issues
        issue_penalty = min(0.4, issue_count * 0.1)  # Max 40% penalty

        confidence_score = max(0, base_score - issue_penalty)

        return confidence_score

    def _generate_tpm_rationale(self, team_score: float, product_score: float,
                              market_score: float, alignment_score: float) -> str:
        """Generate rationale for team-product-market fit."""

        scores = {"Team": team_score, "Product": product_score, "Market": market_score}
        strongest = max(scores, key=scores.get)
        weakest = min(scores, key=scores.get)

        if alignment_score > 8:
            return f"Strong alignment across all areas. {strongest} is the standout strength."
        elif alignment_score > 6:
            return f"Good overall balance with {strongest} leading. {weakest} could use strengthening."
        elif alignment_score > 4:
            return f"Moderate alignment. Significant gap between {strongest} ({scores[strongest]:.1f}) and {weakest} ({scores[weakest]:.1f})."
        else:
            return f"Poor alignment detected. Major imbalance between {strongest} and {weakest} areas needs attention."
