"""VC Q&A Battle system for PitchOS."""

from typing import List, Dict, Any
import google.generativeai as genai
from src.config import config
from src.models import VCQABattle, QAItem, DeckSummary

class VCQABattleGenerator:
    """Generates tough VC questions and ideal founder responses."""
    
    def __init__(self):
        """Initialize the Q&A generator with Gemini AI."""
        if not config.GOOGLE_API_KEY:
            raise ValueError("Google API key not found.")
        
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def generate_qa_battle(self, pitch_content: str, deck_summary: DeckSummary) -> VCQABattle:
        """Generate a complete VC Q&A battle session."""
        
        # Identify weak points in the pitch
        weak_areas = self._identify_weak_areas(deck_summary)
        
        # Generate targeted questions
        questions = []
        
        # Generate questions for each weak area
        for area in weak_areas[:3]:  # Limit to top 3 weak areas
            question = self._generate_question_for_area(area, pitch_content, deck_summary)
            if question:
                questions.append(question)
        
        # Add general tough questions if we need more
        while len(questions) < 3:
            general_question = self._generate_general_tough_question(pitch_content)
            if general_question:
                questions.append(general_question)
        
        return VCQABattle(questions=questions[:3])  # Limit to 3 questions
    
    def _identify_weak_areas(self, deck_summary: DeckSummary) -> List[str]:
        """Identify the weakest areas in the pitch deck."""
        element_scores = {
            "traction": (deck_summary.traction.clarity_score + deck_summary.traction.completeness_score) / 2,
            "business_model": (deck_summary.business_model.clarity_score + deck_summary.business_model.completeness_score) / 2,
            "competition": (deck_summary.competition.clarity_score + deck_summary.competition.completeness_score) / 2,
            "financials": (deck_summary.financials.clarity_score + deck_summary.financials.completeness_score) / 2,
            "market": (deck_summary.market.clarity_score + deck_summary.market.completeness_score) / 2,
            "team": (deck_summary.team.clarity_score + deck_summary.team.completeness_score) / 2
        }
        
        # Sort by score (lowest first)
        sorted_areas = sorted(element_scores.items(), key=lambda x: x[1])
        return [area[0] for area in sorted_areas if area[1] < 7.0]  # Only include weak areas
    
    def _generate_question_for_area(self, area: str, pitch_content: str, deck_summary: DeckSummary) -> QAItem:
        """Generate a tough question for a specific weak area."""
        
        area_prompts = {
            "traction": """
            Generate a tough VC question about traction and user validation.
            Focus on metrics, growth rates, user retention, and proof of product-market fit.
            """,
            "business_model": """
            Generate a tough VC question about the business model and monetization.
            Focus on unit economics, revenue streams, pricing strategy, and scalability.
            """,
            "competition": """
            Generate a tough VC question about competitive landscape and differentiation.
            Focus on competitive advantages, market positioning, and defensibility.
            """,
            "financials": """
            Generate a tough VC question about financial projections and funding.
            Focus on burn rate, runway, revenue assumptions, and path to profitability.
            """,
            "market": """
            Generate a tough VC question about market size and opportunity.
            Focus on TAM/SAM/SOM, market validation, and go-to-market strategy.
            """,
            "team": """
            Generate a tough VC question about the founding team and execution capability.
            Focus on relevant experience, skill gaps, and ability to scale.
            """
        }
        
        prompt = f"""
        {area_prompts.get(area, "Generate a tough VC question about this startup.")}
        
        PITCH CONTEXT:
        {pitch_content}
        
        SPECIFIC AREA CONTENT:
        {getattr(deck_summary, area).content}
        
        Generate:
        1. A specific, challenging question that a VC would ask
        2. An ideal founder response that addresses the concern
        3. Difficulty level (Easy/Medium/Hard)
        4. Category name
        
        Format:
        QUESTION: [The tough question]
        RESPONSE: [Ideal founder response]
        DIFFICULTY: [Easy/Medium/Hard]
        CATEGORY: [Category name]
        
        Make the question realistic and the response demonstrate deep thinking.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_qa_response(response.text, area)
        except Exception:
            return self._get_fallback_question(area)
    
    def _generate_general_tough_question(self, pitch_content: str) -> QAItem:
        """Generate a general tough VC question."""
        
        general_questions = [
            {
                "question": "What's your biggest assumption that could kill this business if it's wrong?",
                "response": "Our biggest assumption is that enterprises will pay premium prices for our solution. We're mitigating this risk through pilot programs with 5 Fortune 500 companies, and early feedback validates our pricing model.",
                "difficulty": "Hard",
                "category": "Risk Assessment"
            },
            {
                "question": "How do you plan to defend against Google or Amazon entering this space?",
                "response": "While big tech could build similar features, our advantage lies in our specialized focus and deep customer relationships. We're building network effects and data moats that become stronger over time.",
                "difficulty": "Hard",
                "category": "Competition"
            },
            {
                "question": "What happens if your key technical co-founder leaves tomorrow?",
                "response": "We've built redundancy into our technical leadership with documented processes and cross-training. Our CTO has also helped us build a strong engineering culture that can continue executing our roadmap.",
                "difficulty": "Medium",
                "category": "Team Risk"
            }
        ]
        
        import random
        selected = random.choice(general_questions)
        
        return QAItem(
            question=selected["question"],
            ideal_response=selected["response"],
            difficulty_level=selected["difficulty"],
            category=selected["category"]
        )
    
    def _parse_qa_response(self, response_text: str, area: str) -> QAItem:
        """Parse AI response into QAItem."""
        lines = response_text.strip().split('\n')
        
        question = f"How do you address concerns about {area}?"
        response = "We have a comprehensive strategy to address this area."
        difficulty = "Medium"
        category = area.title()
        
        for line in lines:
            line = line.strip()
            if line.startswith("QUESTION:"):
                question = line.replace("QUESTION:", "").strip()
            elif line.startswith("RESPONSE:"):
                response = line.replace("RESPONSE:", "").strip()
            elif line.startswith("DIFFICULTY:"):
                difficulty = line.replace("DIFFICULTY:", "").strip()
            elif line.startswith("CATEGORY:"):
                category = line.replace("CATEGORY:", "").strip()
        
        return QAItem(
            question=question,
            ideal_response=response,
            difficulty_level=difficulty,
            category=category
        )
    
    def _get_fallback_question(self, area: str) -> QAItem:
        """Get fallback question when AI fails."""
        fallback_questions = {
            "traction": {
                "question": "What metrics prove you have product-market fit?",
                "response": "Our key metrics show strong PMF: 40% month-over-month growth, 85% user retention, and NPS of 72.",
                "difficulty": "Medium",
                "category": "Traction"
            },
            "business_model": {
                "question": "How do your unit economics work at scale?",
                "response": "Our LTV:CAC ratio is 4:1 with a 14-month payback period, improving as we scale due to operational leverage.",
                "difficulty": "Hard",
                "category": "Business Model"
            },
            "competition": {
                "question": "What's your sustainable competitive advantage?",
                "response": "Our network effects and proprietary data create increasing returns to scale that competitors can't easily replicate.",
                "difficulty": "Medium",
                "category": "Competition"
            }
        }
        
        fallback = fallback_questions.get(area, {
            "question": f"How do you plan to improve your {area}?",
            "response": f"We have a detailed strategy to strengthen our {area} through focused execution.",
            "difficulty": "Medium",
            "category": area.title()
        })
        
        return QAItem(**fallback)
