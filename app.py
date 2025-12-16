"""
PitchOS - AI-Powered Startup Pitch Deck Analyzer
Main Streamlit Application
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import PitchOS components
from src.pitch_analyzer import PitchAnalyzer
from src.ui_components import PitchOSUI
from src.file_processor import FileProcessor
from src.config import config

def main():
    """Main application entry point."""
    
    # Initialize UI
    ui = PitchOSUI()
    ui.render_header()
    
    # Check for API key
    if not config.GOOGLE_API_KEY:
        st.error("🔑 Google API Key not found!")
        st.markdown("""
        To use PitchOS, you need to set up your Google Gemini API key:
        
        1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create a `.env` file in the project root
        3. Add: `GOOGLE_API_KEY=your_api_key_here`
        4. Restart the application
        """)
        st.stop()
    
    # Mode selection
    mode = ui.render_mode_selector()
    
    # Input section
    pitch_content = ui.render_input_section()
    
    if not pitch_content.strip():
        st.info("👆 Please enter your pitch content above to get started!")
        
        # Show example pitch
        with st.expander("📝 See Example Pitch"):
            st.markdown("""
            **Example Startup Pitch:**
            
            **Problem:** Small businesses struggle with inventory management, leading to 30% revenue loss from stockouts and overstock.
            
            **Solution:** InventoryAI is an AI-powered inventory optimization platform that predicts demand and automates reordering.
            
            **Market:** The global inventory management software market is $3.2B and growing at 15% annually.
            
            **Traction:** 150 paying customers, $50K MRR, 25% month-over-month growth. Customers see 40% reduction in stockouts.
            
            **Business Model:** SaaS subscription starting at $99/month per location, with enterprise plans up to $999/month.
            
            **Team:** CEO with 10 years retail experience, CTO from Amazon supply chain, advisor from Shopify.
            
            **Financials:** Seeking $2M Series A to reach $1M ARR by year-end. Unit economics: $200 CAC, $2400 LTV.
            
            **Competition:** Traditional solutions like TradeGecko lack AI. We're 10x more accurate at demand forecasting.
            
            **Vision:** Become the operating system for small business inventory, expanding to 100K+ businesses globally.
            """)
        
        st.stop()
    
    # Analyze button
    if st.button("🚀 Analyze My Pitch", type="primary", use_container_width=True):
        
        with st.spinner("🧠 Analyzing your pitch with AI..."):
            try:
                # Initialize analyzer
                analyzer = PitchAnalyzer()
                
                # Determine source type
                source_type = "text"
                if "--- Slide" in pitch_content:  # OCR content contains slide markers
                    source_type = "ocr"

                # Perform analysis
                result = analyzer.analyze_pitch(pitch_content, mode, source_type)
                
                # Store result in session state
                st.session_state.analysis_result = result
                st.session_state.pitch_content = pitch_content
                st.session_state.analysis_mode = mode
                
                st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("Please check your API key and try again.")
                return
    
    # Display results if available
    if hasattr(st.session_state, 'analysis_result'):
        result = st.session_state.analysis_result

        # Show OCR processing info if applicable
        if hasattr(st.session_state, 'ocr_results'):
            ui.render_ocr_quality_summary(st.session_state.ocr_results)
            st.markdown("---")

        # Analysis Summary
        ui.render_analysis_summary(result)
        
        # Readiness Score
        ui.render_readiness_score(result.readiness_score)
        
        # Deck Summary
        ui.render_deck_summary(result.deck_summary)
        
        # Investor Reactions
        ui.render_investor_reactions(result.investor_simulations)
        
        # VC Q&A Battle
        ui.render_vc_qa_battle(result.vc_qa_battle)
        
        # Hype Meter
        ui.render_hype_meter(result.hype_meter)
        
        # Startup Archetype
        ui.render_startup_archetype(result.startup_archetype)
        
        # Crowd Feedback
        ui.render_crowd_feedback(result.crowd_feedback)
        
        # Red Flags
        ui.render_red_flags(result.pitch_flags)
        
        # Team-Product-Market Fit
        ui.render_team_product_market_fit(result.team_product_market_fit)
        
        # Validation Report
        ui.render_validation_report(result.idea_validation_report)
        
        # Recommendations
        ui.render_recommendations(result.recommendations, st.session_state.analysis_mode)
        
        # Footer
        ui.render_footer()
        
        # Download results option
        st.markdown("---")
        if st.button("📥 Download Analysis Report"):
            # Generate downloadable report
            report = generate_report(result, st.session_state.pitch_content)
            st.download_button(
                label="Download Report",
                data=report,
                file_name="pitchos_analysis_report.md",
                mime="text/markdown"
            )

def generate_report(result, pitch_content: str) -> str:
    """Generate a downloadable analysis report."""
    
    report = f"""# PitchOS Analysis Report

## Pitch Summary
{pitch_content[:500]}...

## Overall Scores
- **Readiness Score:** {result.readiness_score:.1f}/100
- **Storytelling Score:** {result.storytelling_score:.1f}/10
- **Emotional Hook Score:** {result.emotional_hook_score:.1f}/10
- **Hype Meter:** {result.hype_meter:.1f}/100

## Startup Archetype
**{result.startup_archetype}**

## Investor Reactions
"""
    
    for reaction in result.investor_simulations:
        report += f"""
### {reaction.persona} ({reaction.investment_likelihood.value})
{reaction.reaction}

**Key Concerns:**
"""
        for concern in reaction.key_concerns:
            report += f"- {concern}\n"
    
    report += f"""
## Key Issues Detected
"""
    for flag in result.pitch_flags:
        report += f"- {flag}\n"
    
    report += f"""
## Recommendations
"""
    for rec in result.recommendations.get("next_steps", []):
        report += f"- {rec}\n"
    
    report += f"""
## Team-Product-Market Fit
- Team: {result.team_product_market_fit.team_score:.1f}/10
- Product: {result.team_product_market_fit.product_score:.1f}/10
- Market: {result.team_product_market_fit.market_score:.1f}/10
- Alignment: {result.team_product_market_fit.alignment_score:.1f}/10

{result.team_product_market_fit.rationale}

---
*Generated by PitchOS - AI Pitch Deck Analyzer*
"""
    
    return report

if __name__ == "__main__":
    main()
