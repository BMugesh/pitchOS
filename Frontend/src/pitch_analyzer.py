"""Core pitch analysis engine for PitchOS."""

import re
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from src.config import config
from src.models import (
    PitchAnalysisResult, DeckSummary, PitchElement, InvestorReaction,
    VCQABattle, QAItem, IdeaValidationReport, TeamProductMarketFit,
    CrowdFeedback, InvestmentLikelihood
)

class PitchAnalyzer:
    """Main pitch deck analyzer using Gemini AI."""
    
    def __init__(self):
        """Initialize the analyzer with Gemini AI."""
        if not config.GOOGLE_API_KEY:
            raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
        
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def analyze_pitch(self, pitch_content: str, mode: str = "expert", source_type: str = "text") -> PitchAnalysisResult:
        """Analyze a complete pitch deck."""

        # Pre-process content based on source type
        if source_type == "ocr":
            pitch_content = self._post_process_ocr_content(pitch_content)

        # Extract deck elements
        deck_summary = self._extract_deck_elements(pitch_content)
        
        # Calculate scores
        readiness_score = self._calculate_readiness_score(deck_summary, pitch_content)
        storytelling_score = self._calculate_storytelling_score(pitch_content)
        emotional_hook_score = self._calculate_emotional_hook_score(pitch_content)
        hype_meter = self._calculate_hype_meter(pitch_content)
        
        # Generate investor reactions
        investor_simulations = self._simulate_investor_reactions(pitch_content, deck_summary)
        
        # Generate VC Q&A
        vc_qa_battle = self._generate_vc_qa_battle(pitch_content, deck_summary)
        
        # Detect startup archetype
        startup_archetype = self._detect_startup_archetype(pitch_content, deck_summary)
        
        # Detect pitch flags
        pitch_flags = self._detect_pitch_flags(pitch_content)
        
        # Generate crowd feedback
        crowd_feedback = self._generate_crowd_feedback(pitch_content, mode)
        
        # Validate idea
        idea_validation = self._validate_idea(pitch_content, deck_summary)
        
        # Analyze team-product-market fit
        tpm_fit = self._analyze_team_product_market_fit(deck_summary)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            deck_summary, readiness_score, pitch_flags, mode
        )
        
        return PitchAnalysisResult(
            deck_summary=deck_summary,
            readiness_score=readiness_score,
            investor_simulations=investor_simulations,
            vc_qa_battle=vc_qa_battle,
            hype_meter=hype_meter,
            startup_archetype=startup_archetype,
            pitch_flags=pitch_flags,
            crowd_feedback=crowd_feedback,
            idea_validation_report=idea_validation,
            team_product_market_fit=tpm_fit,
            recommendations=recommendations,
            storytelling_score=storytelling_score,
            emotional_hook_score=emotional_hook_score
        )
    
    def _extract_deck_elements(self, pitch_content: str) -> DeckSummary:
        """Extract key elements from pitch content."""
        prompt = f"""
        Analyze this startup pitch and extract the following elements. Rate each element's clarity (0-10) and completeness (0-10):

        Pitch Content:
        {pitch_content}

        Extract and analyze:
        1. Problem - What problem does this solve?
        2. Solution - How does the product/service solve it?
        3. Market - Target market and size
        4. Traction - Current progress, users, revenue
        5. Business Model - How they make money
        6. Team - Founders and key team members
        7. Financials - Revenue projections, funding needs
        8. Competition - Competitive landscape
        9. Vision - Long-term vision and goals

        Return as JSON with this structure:
        {{
            "problem": {{"content": "...", "clarity_score": 8.5, "completeness_score": 7.0}},
            "solution": {{"content": "...", "clarity_score": 9.0, "completeness_score": 8.5}},
            ...
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            
            return DeckSummary(
                problem=PitchElement(**result.get("problem", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                solution=PitchElement(**result.get("solution", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                market=PitchElement(**result.get("market", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                traction=PitchElement(**result.get("traction", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                business_model=PitchElement(**result.get("business_model", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                team=PitchElement(**result.get("team", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                financials=PitchElement(**result.get("financials", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                competition=PitchElement(**result.get("competition", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0})),
                vision=PitchElement(**result.get("vision", {"content": "Not clearly defined", "clarity_score": 3.0, "completeness_score": 2.0}))
            )
        except Exception as e:
            # Fallback to basic analysis if JSON parsing fails
            return self._basic_element_extraction(pitch_content)
    
    def _basic_element_extraction(self, pitch_content: str) -> DeckSummary:
        """Fallback method for basic element extraction."""
        # Simple keyword-based extraction as fallback
        default_element = PitchElement(content="Analysis pending", clarity_score=5.0, completeness_score=5.0)
        
        return DeckSummary(
            problem=default_element,
            solution=default_element,
            market=default_element,
            traction=default_element,
            business_model=default_element,
            team=default_element,
            financials=default_element,
            competition=default_element,
            vision=default_element
        )
    
    def _calculate_readiness_score(self, deck_summary: DeckSummary, pitch_content: str) -> float:
        """Calculate overall pitch readiness score (0-100)."""
        # Weight different elements
        weights = {
            'problem': 0.15,
            'solution': 0.15,
            'market': 0.12,
            'traction': 0.18,
            'business_model': 0.12,
            'team': 0.10,
            'financials': 0.10,
            'competition': 0.05,
            'vision': 0.03
        }
        
        total_score = 0
        for element_name, weight in weights.items():
            element = getattr(deck_summary, element_name)
            element_score = (element.clarity_score + element.completeness_score) / 2
            total_score += element_score * weight * 10  # Scale to 0-100
        
        return min(100, max(0, total_score))
    
    def _calculate_storytelling_score(self, pitch_content: str) -> float:
        """Calculate storytelling quality score."""
        # Simple heuristic based on narrative elements
        story_indicators = [
            r'\b(story|journey|began|started|founded)\b',
            r'\b(problem|pain|frustration|challenge)\b',
            r'\b(solution|answer|solve|fix)\b',
            r'\b(vision|future|imagine|dream)\b'
        ]
        
        score = 0
        for pattern in story_indicators:
            if re.search(pattern, pitch_content, re.IGNORECASE):
                score += 2.5
        
        return min(10, score)
    
    def _calculate_emotional_hook_score(self, pitch_content: str) -> float:
        """Calculate emotional engagement score."""
        emotional_words = [
            r'\b(passionate|excited|love|hate|frustrated|amazing|incredible)\b',
            r'\b(transform|change|impact|difference|better|improve)\b',
            r'\b(people|users|customers|lives|world|society)\b'
        ]
        
        score = 0
        for pattern in emotional_words:
            matches = len(re.findall(pattern, pitch_content, re.IGNORECASE))
            score += min(matches * 0.5, 3.33)  # Cap contribution per category
        
        return min(10, score)
    
    def _calculate_hype_meter(self, pitch_content: str) -> float:
        """Calculate hype level (0-100)."""
        hype_score = 0
        
        for term in config.HYPE_TERMS:
            count = len(re.findall(rf'\b{re.escape(term)}\b', pitch_content, re.IGNORECASE))
            hype_score += count * 5  # Each hype term adds 5 points
        
        # Add points for excessive superlatives
        superlatives = r'\b(best|greatest|ultimate|revolutionary|groundbreaking|unprecedented)\b'
        superlative_count = len(re.findall(superlatives, pitch_content, re.IGNORECASE))
        hype_score += superlative_count * 3
        
        return min(100, hype_score)

    def _simulate_investor_reactions(self, pitch_content: str, deck_summary: DeckSummary) -> List[InvestorReaction]:
        """Simulate different investor persona reactions."""
        reactions = []

        for persona_config in config.INVESTOR_PERSONAS:
            prompt = f"""
            You are a {persona_config['name']} with a {persona_config['style']} investment approach.
            Focus areas: {', '.join(persona_config['focus'])}

            Analyze this pitch and provide your reaction:
            {pitch_content}

            Provide:
            1. Your honest reaction (2-3 sentences)
            2. Investment likelihood (High/Medium/Low/Very Low)
            3. Top 3 concerns
            4. Excitement level (0-10)

            Be authentic to your persona's investment style.
            """

            try:
                response = self.model.generate_content(prompt)
                reaction_text = response.text.strip()

                # Parse response (simplified - in production, use structured prompts)
                likelihood = InvestmentLikelihood.MEDIUM  # Default
                if "high" in reaction_text.lower():
                    likelihood = InvestmentLikelihood.HIGH
                elif "low" in reaction_text.lower():
                    likelihood = InvestmentLikelihood.LOW
                elif "very low" in reaction_text.lower():
                    likelihood = InvestmentLikelihood.VERY_LOW

                reactions.append(InvestorReaction(
                    persona=persona_config['name'],
                    avatar=persona_config['avatar'],
                    reaction=reaction_text[:200] + "..." if len(reaction_text) > 200 else reaction_text,
                    investment_likelihood=likelihood,
                    key_concerns=["Market validation", "Scalability", "Competition"],  # Simplified
                    excitement_level=7.0  # Default
                ))
            except Exception:
                # Fallback reaction
                reactions.append(InvestorReaction(
                    persona=persona_config['name'],
                    avatar=persona_config['avatar'],
                    reaction="Interesting concept, but need more details to make an informed decision.",
                    investment_likelihood=InvestmentLikelihood.MEDIUM,
                    key_concerns=["Need more information"],
                    excitement_level=5.0
                ))

        return reactions

    def _generate_vc_qa_battle(self, pitch_content: str, deck_summary: DeckSummary) -> VCQABattle:
        """Generate tough VC questions and ideal responses."""
        prompt = f"""
        Based on this pitch, generate 3 tough investor questions that VCs would ask:

        {pitch_content}

        For each question, provide:
        1. The tough question
        2. An ideal founder response
        3. Difficulty level (Easy/Medium/Hard)
        4. Category (Business Model/Market/Team/Traction/etc.)

        Make questions realistic and challenging.
        """

        try:
            response = self.model.generate_content(prompt)
            # Simplified parsing - in production, use structured JSON responses
            questions = [
                QAItem(
                    question="How do you plan to scale without burning cash in a competitive market?",
                    ideal_response="We've identified a clear path to profitability through our enterprise-first strategy, focusing on high-LTV customers while maintaining lean operations.",
                    difficulty_level="Hard",
                    category="Business Model"
                ),
                QAItem(
                    question="What's your defensibility beyond being first to market?",
                    ideal_response="Our IP portfolio, exclusive partnerships, and network effects create strong barriers to entry that compound over time.",
                    difficulty_level="Medium",
                    category="Competition"
                ),
                QAItem(
                    question="How will you acquire customers cost-effectively?",
                    ideal_response="Our viral coefficient of 1.3 and organic growth channels reduce CAC by 60% compared to traditional acquisition methods.",
                    difficulty_level="Medium",
                    category="Traction"
                )
            ]

            return VCQABattle(questions=questions)
        except Exception:
            # Fallback questions
            return VCQABattle(questions=[
                QAItem(
                    question="What's your go-to-market strategy?",
                    ideal_response="We have a multi-channel approach focusing on direct sales and strategic partnerships.",
                    difficulty_level="Medium",
                    category="Business Model"
                )
            ])

    def _detect_startup_archetype(self, pitch_content: str, deck_summary: DeckSummary) -> str:
        """Detect startup archetype based on content analysis."""
        # Simple keyword-based detection
        content_lower = pitch_content.lower()

        archetype_indicators = {
            "Builder": ["product", "technology", "engineering", "development", "build"],
            "Visionary": ["future", "vision", "transform", "revolution", "change the world"],
            "Hustler": ["sales", "growth", "customers", "revenue", "market"],
            "Academic": ["research", "study", "analysis", "data", "scientific"],
            "Disruptor": ["disrupt", "traditional", "outdated", "new way", "challenge"],
            "Optimizer": ["efficiency", "optimize", "improve", "better", "streamline"],
            "Connector": ["network", "platform", "connect", "community", "social"],
            "Researcher": ["insights", "discovery", "findings", "investigation", "explore"]
        }

        scores = {}
        for archetype, keywords in archetype_indicators.items():
            score = sum(content_lower.count(keyword) for keyword in keywords)
            scores[archetype] = score

        return max(scores, key=scores.get) if scores else "Builder"

    def _detect_pitch_flags(self, pitch_content: str) -> List[str]:
        """Detect potential red flags in the pitch."""
        flags = []
        content_lower = pitch_content.lower()

        # Check for hype terms
        hype_count = sum(1 for term in config.HYPE_TERMS
                        if term.lower() in content_lower)
        if hype_count > 3:
            flags.append(f"Overuse of hype terms ({hype_count} detected)")

        # Check for vague language
        vague_terms = ["synergy", "leverage", "optimize", "streamline", "innovative"]
        vague_count = sum(1 for term in vague_terms if term in content_lower)
        if vague_count > 2:
            flags.append("Uses vague business jargon")

        # Check for missing key elements
        if "revenue" not in content_lower and "monetization" not in content_lower:
            flags.append("Unclear monetization model")

        if "customer" not in content_lower and "user" not in content_lower:
            flags.append("Target customer not clearly defined")

        return flags

    def _generate_crowd_feedback(self, pitch_content: str, mode: str) -> List[CrowdFeedback]:
        """Generate AI crowd feedback comments."""
        feedback_templates = [
            {"comment": "🔥 This pitch just woke up my inner founder. Let's go!", "sentiment": "positive", "emoji": "🔥", "category": "motivation"},
            {"comment": "A bit too much fluff, bro. Where's the MVP?", "sentiment": "negative", "emoji": "🤔", "category": "technical"},
            {"comment": "Great idea, but needs a co-founder with tech chops.", "sentiment": "neutral", "emoji": "💡", "category": "team"},
            {"comment": "Reminds me of Figma's early deck. Huge potential.", "sentiment": "positive", "emoji": "🚀", "category": "comparison"},
            {"comment": "Market sizing assumptions seem optimistic. Show me the data.", "sentiment": "negative", "emoji": "📊", "category": "business"}
        ]

        # In expert mode, add more technical feedback
        if mode == "expert":
            feedback_templates.extend([
                {"comment": "Unit economics don't add up. CAC > LTV is concerning.", "sentiment": "negative", "emoji": "💰", "category": "financials"},
                {"comment": "Competitive moat isn't defensible long-term.", "sentiment": "negative", "emoji": "🏰", "category": "strategy"}
            ])

        # Select random subset
        import random
        selected = random.sample(feedback_templates, min(5, len(feedback_templates)))

        return [CrowdFeedback(**item) for item in selected]

    def _validate_idea(self, pitch_content: str, deck_summary: DeckSummary) -> IdeaValidationReport:
        """Validate the startup idea logic."""
        issues = []

        # Check market size claims
        if "billion" in pitch_content.lower() and "market" in pitch_content.lower():
            if "source" not in pitch_content.lower() and "research" not in pitch_content.lower():
                issues.append("Market sizing claims lack credible sources")

        # Check problem-solution fit
        problem_score = deck_summary.problem.clarity_score
        solution_score = deck_summary.solution.clarity_score

        if abs(problem_score - solution_score) > 3:
            issues.append("Problem-solution alignment needs improvement")

        # Check traction claims
        if deck_summary.traction.completeness_score < 5:
            issues.append("Traction evidence is insufficient")

        # Calculate confidence score
        element_scores = [
            deck_summary.problem.clarity_score,
            deck_summary.solution.clarity_score,
            deck_summary.market.clarity_score,
            deck_summary.traction.clarity_score
        ]

        confidence_score = sum(element_scores) / (len(element_scores) * 10)  # Normalize to 0-1

        return IdeaValidationReport(
            logic_pass=len(issues) < 3,
            issues_detected=issues,
            confidence_score=confidence_score,
            market_validation_score=deck_summary.market.completeness_score,
            technical_feasibility_score=deck_summary.solution.clarity_score
        )

    def _analyze_team_product_market_fit(self, deck_summary: DeckSummary) -> TeamProductMarketFit:
        """Analyze team-product-market alignment."""
        team_score = deck_summary.team.clarity_score
        product_score = (deck_summary.solution.clarity_score + deck_summary.solution.completeness_score) / 2
        market_score = (deck_summary.market.clarity_score + deck_summary.market.completeness_score) / 2

        # Calculate alignment (how well scores match)
        scores = [team_score, product_score, market_score]
        alignment_score = 10 - (max(scores) - min(scores))  # Higher when scores are similar

        rationale = "Team-product-market alignment analysis based on pitch clarity and completeness."

        return TeamProductMarketFit(
            team_score=team_score,
            product_score=product_score,
            market_score=market_score,
            alignment_score=max(0, alignment_score),
            rationale=rationale
        )

    def _generate_recommendations(self, deck_summary: DeckSummary, readiness_score: float,
                                pitch_flags: List[str], mode: str) -> Dict[str, List[str]]:
        """Generate improvement recommendations."""
        recommendations = {"next_steps": []}

        # Score-based recommendations
        if readiness_score < 60:
            recommendations["next_steps"].append("Focus on core value proposition clarity")
            recommendations["next_steps"].append("Strengthen problem-solution fit narrative")

        if readiness_score < 80:
            recommendations["next_steps"].append("Add more concrete traction metrics")
            recommendations["next_steps"].append("Refine financial projections with realistic assumptions")

        # Element-specific recommendations
        if deck_summary.traction.completeness_score < 6:
            recommendations["next_steps"].append("Gather more user validation and early traction data")

        if deck_summary.team.clarity_score < 7:
            recommendations["next_steps"].append("Highlight team's relevant experience and expertise")

        if deck_summary.competition.completeness_score < 6:
            recommendations["next_steps"].append("Conduct thorough competitive analysis")

        # Flag-based recommendations
        if "hype terms" in str(pitch_flags):
            recommendations["next_steps"].append("Replace buzzwords with concrete, specific language")

        if "monetization" in str(pitch_flags):
            recommendations["next_steps"].append("Clearly define revenue streams and pricing strategy")

        # Mode-specific recommendations
        if mode == "expert":
            recommendations["next_steps"].extend([
                "Validate unit economics with real customer data",
                "Develop IP protection strategy",
                "Plan for Series A metrics and milestones"
            ])

        return recommendations

    def _post_process_ocr_content(self, ocr_content: str) -> str:
        """Post-process OCR extracted content for better analysis."""
        import re

        # Clean up common OCR errors
        content = ocr_content

        # Fix common OCR character substitutions
        ocr_fixes = {
            r'\b0\b': 'O',  # Zero to O
            r'\b1\b': 'I',  # One to I (in context)
            r'\b5\b': 'S',  # Five to S (in context)
            r'\b8\b': 'B',  # Eight to B (in context)
            r'rn': 'm',     # Common OCR error
            r'cl': 'd',     # Common OCR error
            r'vv': 'w',     # Common OCR error
        }

        for pattern, replacement in ocr_fixes.items():
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

        # Remove excessive whitespace and line breaks
        content = re.sub(r'\n\s*\n', '\n\n', content)  # Multiple newlines to double
        content = re.sub(r' +', ' ', content)  # Multiple spaces to single

        # Try to identify and structure slide content
        content = self._structure_slide_content(content)

        return content.strip()

    def _structure_slide_content(self, content: str) -> str:
        """Attempt to structure slide content into logical sections."""
        lines = content.split('\n')
        structured_lines = []

        # Common slide section headers
        section_patterns = [
            r'problem',
            r'solution',
            r'market',
            r'traction',
            r'business model',
            r'team',
            r'financials?',
            r'competition',
            r'vision',
            r'ask',
            r'funding',
            r'revenue',
            r'customers?',
            r'growth'
        ]

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line looks like a section header
            is_header = False
            for pattern in section_patterns:
                if re.search(pattern, line, re.IGNORECASE) and len(line.split()) <= 3:
                    structured_lines.append(f"\n{line.upper()}:")
                    is_header = True
                    break

            if not is_header:
                structured_lines.append(line)

        return '\n'.join(structured_lines)
