"""Investor persona simulation system for PitchOS."""

from typing import Dict, List, Any
import google.generativeai as genai
from src.config import config
from src.models import InvestorReaction, InvestmentLikelihood, DeckSummary

class InvestorPersonaSimulator:
    """Simulates different investor persona reactions to pitches."""
    
    def __init__(self):
        """Initialize the simulator with Gemini AI."""
        if not config.GOOGLE_API_KEY:
            raise ValueError("Google API key not found.")
        
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(config.MODEL_NAME)
    
    def simulate_all_personas(self, pitch_content: str, deck_summary: DeckSummary) -> List[InvestorReaction]:
        """Simulate reactions from all investor personas."""
        reactions = []
        
        for persona_config in config.INVESTOR_PERSONAS:
            reaction = self._simulate_persona_reaction(
                persona_config, pitch_content, deck_summary
            )
            reactions.append(reaction)
        
        return reactions
    
    def _simulate_persona_reaction(self, persona_config: Dict[str, Any], 
                                 pitch_content: str, deck_summary: DeckSummary) -> InvestorReaction:
        """Simulate a specific investor persona's reaction."""
        
        persona_prompts = {
            "Risk-Averse VC": self._get_risk_averse_prompt(),
            "Visionary Angel": self._get_visionary_angel_prompt(),
            "Corporate Strategic": self._get_corporate_strategic_prompt()
        }
        
        base_prompt = persona_prompts.get(persona_config['name'], self._get_default_prompt())
        
        full_prompt = f"""
        {base_prompt}
        
        PITCH TO ANALYZE:
        {pitch_content}
        
        KEY ELEMENTS SUMMARY:
        - Problem: {deck_summary.problem.content}
        - Solution: {deck_summary.solution.content}
        - Market: {deck_summary.market.content}
        - Traction: {deck_summary.traction.content}
        - Business Model: {deck_summary.business_model.content}
        - Team: {deck_summary.team.content}
        
        Provide your reaction in this format:
        REACTION: [Your 2-3 sentence reaction as this investor persona]
        LIKELIHOOD: [High/Medium/Low/Very Low]
        CONCERNS: [List your top 3 concerns, separated by semicolons]
        EXCITEMENT: [Rate 0-10 your excitement level]
        
        Stay true to your persona's investment philosophy and risk tolerance.
        """
        
        try:
            response = self.model.generate_content(full_prompt)
            return self._parse_persona_response(response.text, persona_config)
        except Exception as e:
            # Fallback to default reaction
            return self._get_fallback_reaction(persona_config)
    
    def _get_risk_averse_prompt(self) -> str:
        """Get prompt for Risk-Averse VC persona."""
        return """
        You are a Risk-Averse VC partner at a top-tier fund. You focus on:
        - Proven traction and revenue
        - Large, validated markets
        - Experienced teams with track records
        - Clear path to profitability
        - Defensible competitive advantages
        
        You are skeptical of unproven concepts and require strong evidence.
        You prefer B2B models over B2C. You ask tough questions about unit economics.
        """
    
    def _get_visionary_angel_prompt(self) -> str:
        """Get prompt for Visionary Angel persona."""
        return """
        You are a Visionary Angel investor who made early bets on companies like Uber, Airbnb.
        You focus on:
        - Transformative potential and big vision
        - Passionate, driven founders
        - Disruptive business models
        - Long-term market opportunities
        - Innovation and technology breakthroughs
        
        You're willing to take bigger risks for bigger rewards.
        You believe in backing exceptional founders even in uncertain markets.
        """
    
    def _get_corporate_strategic_prompt(self) -> str:
        """Get prompt for Corporate Strategic investor."""
        return """
        You are a Corporate Strategic investor from a Fortune 500 company.
        You focus on:
        - Strategic fit with parent company
        - Partnership and acquisition potential
        - Market expansion opportunities
        - Technology that enhances core business
        - Scalable solutions for enterprise clients
        
        You think about synergies, integration possibilities, and strategic value.
        You have longer investment horizons and deeper pockets.
        """
    
    def _get_default_prompt(self) -> str:
        """Get default investor prompt."""
        return """
        You are an experienced startup investor evaluating this pitch.
        Consider the business opportunity, team, market, and execution potential.
        """
    
    def _parse_persona_response(self, response_text: str, persona_config: Dict[str, Any]) -> InvestorReaction:
        """Parse the AI response into structured data."""
        lines = response_text.strip().split('\n')
        
        reaction = "Interesting concept, but need more details to make an informed decision."
        likelihood = InvestmentLikelihood.MEDIUM
        concerns = ["Need more information"]
        excitement = 5.0
        
        for line in lines:
            line = line.strip()
            if line.startswith("REACTION:"):
                reaction = line.replace("REACTION:", "").strip()
            elif line.startswith("LIKELIHOOD:"):
                likelihood_text = line.replace("LIKELIHOOD:", "").strip().lower()
                if "high" in likelihood_text:
                    likelihood = InvestmentLikelihood.HIGH
                elif "very low" in likelihood_text:
                    likelihood = InvestmentLikelihood.VERY_LOW
                elif "low" in likelihood_text:
                    likelihood = InvestmentLikelihood.LOW
                else:
                    likelihood = InvestmentLikelihood.MEDIUM
            elif line.startswith("CONCERNS:"):
                concerns_text = line.replace("CONCERNS:", "").strip()
                concerns = [c.strip() for c in concerns_text.split(';') if c.strip()]
            elif line.startswith("EXCITEMENT:"):
                try:
                    excitement = float(line.replace("EXCITEMENT:", "").strip())
                    excitement = max(0, min(10, excitement))  # Clamp to 0-10
                except ValueError:
                    excitement = 5.0
        
        return InvestorReaction(
            persona=persona_config['name'],
            avatar=persona_config['avatar'],
            reaction=reaction,
            investment_likelihood=likelihood,
            key_concerns=concerns[:3],  # Limit to top 3
            excitement_level=excitement
        )
    
    def _get_fallback_reaction(self, persona_config: Dict[str, Any]) -> InvestorReaction:
        """Get fallback reaction when AI fails."""
        fallback_reactions = {
            "Risk-Averse VC": "Solid concept, but I need to see more traction and clearer unit economics before considering investment.",
            "Visionary Angel": "I love the vision and potential, but execution will be key. The team seems passionate about solving this problem.",
            "Corporate Strategic": "This could have strategic value for our portfolio, but we'd need to evaluate integration possibilities more thoroughly."
        }
        
        return InvestorReaction(
            persona=persona_config['name'],
            avatar=persona_config['avatar'],
            reaction=fallback_reactions.get(persona_config['name'], "Need more information to evaluate properly."),
            investment_likelihood=InvestmentLikelihood.MEDIUM,
            key_concerns=["Need more detailed analysis"],
            excitement_level=5.0
        )
