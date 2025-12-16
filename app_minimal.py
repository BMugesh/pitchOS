"""
PitchOS - Minimal Version (without OCR dependencies)
Use this if you're having dependency issues with the full version
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    """Minimal PitchOS application."""
    
    # Page config
    st.set_page_config(
        page_title="PitchOS - AI Pitch Deck Analyzer",
        page_icon="🚀",
        layout="wide"
    )
    
    # Header
    st.markdown('<h1 style="text-align: center;">🚀 PitchOS</h1>', unsafe_allow_html=True)
    st.markdown("### *AI-Powered Startup Pitch Deck Analyzer*")
    st.markdown("---")
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🔑 Google API Key not found!")
        st.markdown("""
        **Setup Instructions:**
        1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Add it to your `.env` file: `GOOGLE_API_KEY=your_key_here`
        3. Restart the application
        """)
        st.stop()
    
    # Mode selection
    st.sidebar.markdown("## 🧭 Analysis Mode")
    mode = st.sidebar.radio("Choose analysis depth:", ["Beginner", "Expert"])
    
    # Input section
    st.markdown("## 📝 Submit Your Pitch")
    
    pitch_content = st.text_area(
        "Paste your pitch deck content here:",
        height=200,
        placeholder="Describe your startup: problem, solution, market, traction, team, business model, financials, competition, vision..."
    )
    
    if not pitch_content.strip():
        st.info("👆 Please enter your pitch content above to get started!")
        
        # Example pitch
        with st.expander("📝 See Example Pitch"):
            st.markdown("""
            **Problem:** Small businesses lose 30% revenue from poor inventory management
            
            **Solution:** InventoryAI - AI-powered inventory optimization platform
            
            **Market:** $3.2B global inventory management software market, growing 15% annually
            
            **Traction:** 150 paying customers, $50K MRR, 25% month-over-month growth
            
            **Business Model:** SaaS subscription $99-999/month per location
            
            **Team:** CEO (10 years retail), CTO (ex-Amazon), Shopify advisor
            
            **Financials:** Seeking $2M Series A, $200 CAC, $2400 LTV
            
            **Competition:** Traditional solutions lack AI, we're 10x more accurate
            
            **Vision:** Operating system for small business inventory globally
            """)
        st.stop()
    
    # Analysis button
    if st.button("🚀 Analyze My Pitch", type="primary", use_container_width=True):
        
        with st.spinner("🧠 Analyzing your pitch..."):
            try:
                # Import here to avoid dependency issues on startup
                import sys
                sys.path.append('src')
                
                from src.pitch_analyzer import PitchAnalyzer
                
                # Analyze pitch
                analyzer = PitchAnalyzer()
                result = analyzer.analyze_pitch(pitch_content, mode.lower())
                
                # Store in session state
                st.session_state.analysis_result = result
                st.success("✅ Analysis complete!")
                
            except ImportError as e:
                st.error(f"❌ Import error: {e}")
                st.info("Run `python quick_fix.py` to fix dependencies")
                return
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                return
    
    # Display results
    if hasattr(st.session_state, 'analysis_result'):
        result = st.session_state.analysis_result
        
        # Readiness Score
        st.markdown("## 📊 Pitch Readiness Score")
        score = result.readiness_score
        
        st.progress(score / 100)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Score", f"{score:.1f}/100")
        with col2:
            if score >= 80:
                st.metric("Status", "🎉 Excellent")
            elif score >= 60:
                st.metric("Status", "👍 Good")
            else:
                st.metric("Status", "🔧 Needs Work")
        
        # Key Insights
        st.markdown("## 🧠 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Hype Level", f"{result.hype_meter:.0f}/100")
        with col2:
            st.metric("Archetype", result.startup_archetype)
        with col3:
            st.metric("Storytelling", f"{result.storytelling_score:.1f}/10")
        
        # Investor Reactions
        st.markdown("## 🎭 Investor Reactions")
        for reaction in result.investor_simulations:
            with st.expander(f"{reaction.avatar} {reaction.persona}"):
                st.write(reaction.reaction)
                st.metric("Interest Level", reaction.investment_likelihood.value)
        
        # Red Flags
        if result.pitch_flags:
            st.markdown("## 🚨 Areas for Improvement")
            for flag in result.pitch_flags:
                st.warning(f"⚠️ {flag}")
        
        # Recommendations
        st.markdown("## 💡 Recommendations")
        for rec in result.recommendations.get("next_steps", []):
            st.info(f"📋 {rec}")
        
        # Success message
        if score >= 75:
            st.success("🚀 Your pitch is looking strong! Consider reaching out to investors.")
        elif score >= 50:
            st.info("📈 Good foundation. Address the recommendations above.")
        else:
            st.warning("🔧 Focus on strengthening your core value proposition.")

if __name__ == "__main__":
    main()
