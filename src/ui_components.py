"""Streamlit UI components for PitchOS."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
from src.models import (
    PitchAnalysisResult, InvestorReaction, QAItem, CrowdFeedback,
    InvestmentLikelihood, TeamProductMarketFit
)
from src.config import config

class PitchOSUI:
    """Main UI component manager for PitchOS."""
    
    def __init__(self):
        """Initialize UI components."""
        self.setup_page_config()
    
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=config.PAGE_TITLE,
            page_icon=config.PAGE_ICON,
            layout=config.LAYOUT,
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for dark mode and styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-card {
            background-color: #1E1E1E;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #4ECDC4;
            margin: 0.5rem 0;
        }
        
        .investor-card {
            background-color: #2D2D2D;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            border: 1px solid #444;
        }
        
        .qa-question {
            background-color: #FF6B6B;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        
        .qa-answer {
            background-color: #4ECDC4;
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        
        .crowd-comment {
            background-color: #3D3D3D;
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.3rem 0;
            border-left: 3px solid #FFD93D;
        }
        
        .archetype-badge {
            display: inline-block;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.1rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render the main header."""
        st.markdown('<h1 class="main-header">🚀 PitchOS</h1>', unsafe_allow_html=True)
        st.markdown("### *An omniscient AI designed to evaluate startup pitch decks like a seasoned VC*")
        st.markdown("---")
    
    def render_mode_selector(self) -> str:
        """Render mode selection toggle."""
        st.sidebar.markdown("## 🧭 Analysis Mode")
        mode = st.sidebar.radio(
            "Choose your analysis depth:",
            ["Beginner", "Expert"],
            help="Beginner mode provides simplified feedback, Expert mode gives detailed technical analysis"
        )
        return mode.lower()
    
    def render_input_section(self) -> str:
        """Render pitch input section with OCR support."""
        from src.file_processor import FileProcessor
        from src.ocr_processor import HybridOCRProcessor
        from PIL import Image

        st.markdown("## 📝 Submit Your Pitch")

        input_method = st.radio(
            "How would you like to submit your pitch?",
            ["Text Input", "File Upload", "Image Upload (OCR)"],
            horizontal=True
        )

        pitch_content = ""

        if input_method == "Text Input":
            pitch_content = st.text_area(
                "Paste your pitch deck content here:",
                height=200,
                placeholder="Describe your startup, problem, solution, market, traction, team, and business model..."
            )

        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload your pitch deck",
                type=['pdf', 'txt', 'docx'],
                help="Upload a PDF, text file, or Word document containing your pitch"
            )

            if uploaded_file:
                try:
                    processor = FileProcessor()
                    pitch_content = processor.process_uploaded_file(uploaded_file)

                    if pitch_content:
                        # Clean and validate content
                        pitch_content = processor.clean_content(pitch_content)

                        if processor.validate_content(pitch_content):
                            st.success(f"✅ File processed successfully! Extracted {len(pitch_content)} characters.")

                            # Show preview
                            with st.expander("📄 Content Preview"):
                                st.text(pitch_content[:500] + "..." if len(pitch_content) > 500 else pitch_content)
                        else:
                            st.error("❌ File content doesn't appear to be a pitch deck. Please ensure it contains information about your startup's problem, solution, market, etc.")
                            pitch_content = ""
                    else:
                        st.error("❌ Could not extract text from file.")

                except Exception as e:
                    st.error(f"❌ Error processing file: {str(e)}")

        else:  # Image Upload (OCR)
            pitch_content = self._render_image_ocr_section()

        return pitch_content

    def _render_image_ocr_section(self) -> str:
        """Render image upload and OCR processing section."""
        from src.ocr_processor import HybridOCRProcessor
        from src.image_preprocessor import ImagePreprocessor
        from PIL import Image
        import time

        st.markdown("### 📸 Upload Pitch Deck Images")
        st.info("💡 Upload images of your pitch deck slides. We'll extract text using advanced OCR technology.")

        # Multiple file upload
        uploaded_images = st.file_uploader(
            "Choose pitch deck images",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp'],
            accept_multiple_files=True,
            help="Upload multiple images of your pitch deck slides"
        )

        if not uploaded_images:
            return ""

        # OCR processing options
        col1, col2 = st.columns(2)
        with col1:
            aggressive_preprocessing = st.checkbox(
                "🔧 Aggressive preprocessing",
                help="Apply more intensive image processing for difficult-to-read slides"
            )
        with col2:
            show_preprocessing = st.checkbox(
                "👁️ Show preprocessing steps",
                help="Display image preprocessing results"
            )

        # Process images
        if st.button("🚀 Extract Text from Images", type="primary"):
            return self._process_images_with_ocr(
                uploaded_images,
                aggressive_preprocessing,
                show_preprocessing
            )

        return ""

    def _process_images_with_ocr(self, uploaded_images, aggressive_preprocessing: bool, show_preprocessing: bool) -> str:
        """Process uploaded images with OCR."""
        from src.ocr_processor import HybridOCRProcessor
        from src.image_preprocessor import ImagePreprocessor
        from PIL import Image

        ocr_processor = HybridOCRProcessor()
        image_preprocessor = ImagePreprocessor()

        all_extracted_text = []

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, uploaded_image in enumerate(uploaded_images):
            status_text.text(f"Processing image {i+1}/{len(uploaded_images)}: {uploaded_image.name}")

            try:
                # Load image
                image = Image.open(uploaded_image)

                # Show original image
                with st.expander(f"📄 Slide {i+1}: {uploaded_image.name}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.image(image, caption="Original Image", use_column_width=True)

                        # Image quality analysis
                        quality_metrics = image_preprocessor.analyze_image_quality(image)
                        st.metric("Quality Score", f"{quality_metrics['overall_quality']:.2f}")

                    with col2:
                        if show_preprocessing:
                            # Show preprocessed image
                            preprocessed = image_preprocessor.preprocess_for_ocr(image, aggressive_preprocessing)
                            st.image(preprocessed, caption="Preprocessed", use_column_width=True)

                # Perform OCR
                ocr_result = ocr_processor.process_image(image, uploaded_image.name)

                # Display OCR results
                self._display_ocr_result(ocr_result, i+1)

                if ocr_result.text.strip():
                    all_extracted_text.append(f"--- Slide {i+1} ({uploaded_image.name}) ---")
                    all_extracted_text.append(ocr_result.text)
                    all_extracted_text.append("")  # Empty line separator

            except Exception as e:
                st.error(f"❌ Error processing {uploaded_image.name}: {str(e)}")

            # Update progress
            progress_bar.progress((i + 1) / len(uploaded_images))

        status_text.text("✅ OCR processing complete!")

        # Combine all extracted text
        combined_text = "\n".join(all_extracted_text)

        if combined_text.strip():
            st.success(f"🎉 Successfully extracted text from {len(uploaded_images)} images!")

            # Show combined text preview
            with st.expander("📝 Combined Extracted Text"):
                st.text_area("Extracted Content", combined_text, height=300)

            return combined_text
        else:
            st.warning("⚠️ No meaningful text could be extracted from the uploaded images.")
            return ""

    def _display_ocr_result(self, ocr_result, slide_number: int):
        """Display OCR result with method indicator."""
        method_icons = {
            "easyocr": "✔️",
            "google_vision": "☁️",
            "failed": "❌"
        }

        method_names = {
            "easyocr": "EasyOCR",
            "google_vision": "Google Vision",
            "failed": "Failed"
        }

        icon = method_icons.get(ocr_result.method, "❓")
        method_name = method_names.get(ocr_result.method, "Unknown")

        # OCR method and confidence
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("OCR Method", f"{icon} {method_name}")
        with col2:
            if ocr_result.confidence > 0:
                st.metric("Confidence", f"{ocr_result.confidence:.1%}")
        with col3:
            st.metric("Processing Time", f"{ocr_result.processing_time:.2f}s")

        # Show extracted text
        if ocr_result.text.strip():
            st.text_area(
                f"Extracted Text (Slide {slide_number})",
                ocr_result.text,
                height=150,
                key=f"ocr_text_{slide_number}"
            )
        else:
            st.warning("No text extracted from this image")

        # Show issues if any
        if ocr_result.issues:
            with st.expander("⚠️ Processing Issues"):
                for issue in ocr_result.issues:
                    st.warning(issue)

        # Show quality recommendations
        if not ocr_result.is_valid:
            st.error("❌ OCR quality is poor. Consider:")
            st.markdown("""
            - Retaking the photo with better lighting
            - Ensuring the image is in focus
            - Using higher resolution
            - Avoiding shadows or glare
            """)

    def render_ocr_quality_summary(self, ocr_results: list):
        """Render OCR quality summary and recommendations."""
        st.markdown("## 📊 OCR Processing Summary")

        total_slides = len(ocr_results)
        successful_extractions = sum(1 for result in ocr_results if result.is_valid)
        easyocr_count = sum(1 for result in ocr_results if result.method == "easyocr" and result.is_valid)
        google_vision_count = sum(1 for result in ocr_results if result.method == "google_vision" and result.is_valid)
        failed_count = total_slides - successful_extractions

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Slides", total_slides)
        with col2:
            st.metric("Successful", successful_extractions)
        with col3:
            st.metric("✔️ EasyOCR", easyocr_count)
        with col4:
            st.metric("☁️ Google Vision", google_vision_count)

        if failed_count > 0:
            st.warning(f"⚠️ {failed_count} slides had poor OCR quality")

            # Show recommendations for failed slides
            st.markdown("### 💡 Recommendations for Better OCR:")
            st.markdown("""
            - **Lighting**: Ensure even, bright lighting without shadows
            - **Focus**: Make sure text is sharp and in focus
            - **Resolution**: Use high-resolution images (at least 1080p)
            - **Angle**: Take photos straight-on, avoid skewed angles
            - **Contrast**: Ensure good contrast between text and background
            - **File Format**: Use PNG or high-quality JPEG
            """)

        # Show processing method breakdown
        if successful_extractions > 0:
            success_rate = (successful_extractions / total_slides) * 100

            if success_rate >= 90:
                st.success(f"🎉 Excellent OCR success rate: {success_rate:.1f}%")
            elif success_rate >= 70:
                st.info(f"👍 Good OCR success rate: {success_rate:.1f}%")
            else:
                st.warning(f"⚠️ OCR success rate could be improved: {success_rate:.1f}%")

        # Method usage statistics
        if easyocr_count > 0 or google_vision_count > 0:
            st.markdown("### 🔧 OCR Method Usage")

            method_data = {
                "Method": ["EasyOCR", "Google Vision", "Failed"],
                "Count": [easyocr_count, google_vision_count, failed_count],
                "Percentage": [
                    (easyocr_count / total_slides) * 100,
                    (google_vision_count / total_slides) * 100,
                    (failed_count / total_slides) * 100
                ]
            }

            import pandas as pd
            df = pd.DataFrame(method_data)
            st.dataframe(df, use_container_width=True)
    
    def render_readiness_score(self, score: float):
        """Render readiness score with progress bar."""
        st.markdown("## 📊 Pitch Readiness Score")
        
        # Color coding based on score
        if score >= config.READINESS_THRESHOLDS["excellent"]:
            color = "#4ECDC4"
            status = "Excellent"
        elif score >= config.READINESS_THRESHOLDS["good"]:
            color = "#FFD93D"
            status = "Good"
        elif score >= config.READINESS_THRESHOLDS["fair"]:
            color = "#FF9F43"
            status = "Fair"
        else:
            color = "#FF6B6B"
            status = "Needs Work"
        
        # Progress bar
        st.progress(score / 100)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{score:.1f}/100")
        with col2:
            st.metric("Status", status)
        with col3:
            st.metric("Percentile", f"{min(99, int(score))}th")
    
    def render_deck_summary(self, deck_summary):
        """Render deck summary in expandable sections."""
        st.markdown("## 🧠 Pitch Deck Analysis")
        
        elements = [
            ("Problem", deck_summary.problem, "🎯"),
            ("Solution", deck_summary.solution, "💡"),
            ("Market", deck_summary.market, "🌍"),
            ("Traction", deck_summary.traction, "📈"),
            ("Business Model", deck_summary.business_model, "💰"),
            ("Team", deck_summary.team, "👥"),
            ("Financials", deck_summary.financials, "💹"),
            ("Competition", deck_summary.competition, "⚔️"),
            ("Vision", deck_summary.vision, "🔮")
        ]
        
        for name, element, emoji in elements:
            with st.expander(f"{emoji} {name} (Clarity: {element.clarity_score:.1f}/10, Completeness: {element.completeness_score:.1f}/10)"):
                st.write(element.content)
                
                # Score visualization
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Clarity", f"{element.clarity_score:.1f}/10")
                with col2:
                    st.metric("Completeness", f"{element.completeness_score:.1f}/10")
    
    def render_investor_reactions(self, reactions: List[InvestorReaction]):
        """Render investor persona reactions."""
        st.markdown("## 🎭 Investor Reactions")
        
        for reaction in reactions:
            with st.expander(f"{reaction.avatar} {reaction.persona} - {reaction.investment_likelihood.value} Interest"):
                st.markdown(f"**Reaction:** {reaction.reaction}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Investment Likelihood", reaction.investment_likelihood.value)
                with col2:
                    st.metric("Excitement Level", f"{reaction.excitement_level:.1f}/10")
                
                if reaction.key_concerns:
                    st.markdown("**Key Concerns:**")
                    for concern in reaction.key_concerns:
                        st.markdown(f"• {concern}")
    
    def render_vc_qa_battle(self, qa_battle):
        """Render VC Q&A battle section."""
        st.markdown("## ⚔️ VC Q&A Battle")
        st.markdown("*Tough questions VCs might ask and how to answer them*")
        
        for i, qa_item in enumerate(qa_battle.questions, 1):
            st.markdown(f"### Question {i} ({qa_item.difficulty_level} - {qa_item.category})")
            
            # Question
            st.markdown(f'<div class="qa-question">❓ <strong>VC:</strong> {qa_item.question}</div>', 
                       unsafe_allow_html=True)
            
            # Answer
            st.markdown(f'<div class="qa-answer">💡 <strong>Ideal Response:</strong> {qa_item.ideal_response}</div>', 
                       unsafe_allow_html=True)
            
            st.markdown("---")
    
    def render_hype_meter(self, hype_score: float):
        """Render hype meter visualization."""
        st.markdown("## 💥 Hype Meter")
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = hype_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Hype Level"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        if hype_score < 25:
            st.success("✅ Low hype - Good balance of substance over style")
        elif hype_score < 50:
            st.info("ℹ️ Moderate hype - Some buzzwords but generally grounded")
        elif hype_score < 75:
            st.warning("⚠️ High hype - Consider reducing jargon and buzzwords")
        else:
            st.error("🚨 Extreme hype - Too much fluff, focus on concrete details")
    
    def render_startup_archetype(self, archetype: str):
        """Render startup archetype detection."""
        st.markdown("## 🧬 Startup Archetype")
        
        archetype_descriptions = {
            "Builder": "🔨 You're focused on creating and developing products",
            "Visionary": "🔮 You're driven by big picture thinking and transformation",
            "Hustler": "💪 You're all about growth, sales, and business execution",
            "Academic": "🎓 You approach problems with research and analytical rigor",
            "Disruptor": "💥 You're challenging traditional ways of doing things",
            "Optimizer": "⚡ You focus on improving efficiency and processes",
            "Connector": "🌐 You build networks, platforms, and communities",
            "Researcher": "🔍 You're driven by discovery and insights"
        }
        
        description = archetype_descriptions.get(archetype, "🚀 Unique startup approach")
        
        st.markdown(f'<div class="archetype-badge">{archetype}</div>', unsafe_allow_html=True)
        st.markdown(f"**{description}**")
        
        # Archetype-specific advice
        advice = {
            "Builder": "Focus on showcasing your technical capabilities and product roadmap.",
            "Visionary": "Balance your big vision with concrete execution steps.",
            "Hustler": "Highlight your traction and go-to-market success.",
            "Academic": "Translate your research into clear business value.",
            "Disruptor": "Show how your disruption creates sustainable value.",
            "Optimizer": "Quantify the improvements and efficiency gains.",
            "Connector": "Demonstrate network effects and community growth.",
            "Researcher": "Connect your insights to market opportunities."
        }
        
        st.info(f"💡 **Tip:** {advice.get(archetype, 'Stay focused on your unique strengths.')}")

    def render_crowd_feedback(self, crowd_feedback: List[CrowdFeedback]):
        """Render AI crowd feedback section."""
        st.markdown("## 💬 AI Crowd Feedback")
        st.markdown("*What the startup community might say about your pitch*")

        for feedback in crowd_feedback:
            sentiment_color = {
                "positive": "#4ECDC4",
                "negative": "#FF6B6B",
                "neutral": "#FFD93D"
            }.get(feedback.sentiment, "#888888")

            st.markdown(f"""
            <div class="crowd-comment" style="border-left-color: {sentiment_color}">
                {feedback.emoji} <strong>{feedback.category.title()}:</strong> {feedback.comment}
            </div>
            """, unsafe_allow_html=True)

    def render_red_flags(self, pitch_flags: List[str]):
        """Render pitch red flags and warnings."""
        st.markdown("## 🚨 Red Flags & Issues")

        if not pitch_flags:
            st.success("✅ No major red flags detected!")
            return

        for flag in pitch_flags:
            st.error(f"🚫 {flag}")

        st.markdown("### 💡 How to Fix These Issues:")

        flag_solutions = {
            "hype terms": "Replace buzzwords with specific, measurable outcomes",
            "monetization": "Clearly explain how you make money with specific pricing",
            "customer": "Define your target customer with specific demographics",
            "traction": "Provide concrete metrics: users, revenue, growth rates",
            "market": "Support market size claims with credible research sources"
        }

        for flag in pitch_flags:
            for key, solution in flag_solutions.items():
                if key in flag.lower():
                    st.info(f"💡 {solution}")
                    break

    def render_team_product_market_fit(self, tpm_fit: TeamProductMarketFit):
        """Render team-product-market fit analysis."""
        st.markdown("## ✅ Team-Product-Market Fit")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Team", f"{tpm_fit.team_score:.1f}/10")
        with col2:
            st.metric("Product", f"{tpm_fit.product_score:.1f}/10")
        with col3:
            st.metric("Market", f"{tpm_fit.market_score:.1f}/10")
        with col4:
            st.metric("Alignment", f"{tpm_fit.alignment_score:.1f}/10")

        # Visualization
        categories = ['Team', 'Product', 'Market']
        scores = [tpm_fit.team_score, tpm_fit.product_score, tpm_fit.market_score]

        fig = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Current State'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"**Analysis:** {tpm_fit.rationale}")

    def render_validation_report(self, validation_report):
        """Render idea validation report."""
        st.markdown("## 📈 Idea Validation Report")

        col1, col2, col3 = st.columns(3)

        with col1:
            status = "✅ PASS" if validation_report.logic_pass else "❌ NEEDS WORK"
            st.metric("Logic Check", status)

        with col2:
            st.metric("Confidence", f"{validation_report.confidence_score:.0%}")

        with col3:
            st.metric("Market Validation", f"{validation_report.market_validation_score:.1f}/10")

        if validation_report.issues_detected:
            st.markdown("### Issues Detected:")
            for issue in validation_report.issues_detected:
                st.warning(f"⚠️ {issue}")
        else:
            st.success("🎉 No major validation issues detected!")

    def render_recommendations(self, recommendations: Dict[str, List[str]], mode: str):
        """Render improvement recommendations."""
        st.markdown("## 🔧 Recommendations")

        if "next_steps" in recommendations:
            st.markdown("### 📋 Next Steps:")

            for i, step in enumerate(recommendations["next_steps"], 1):
                st.markdown(f"{i}. {step}")

        # Mode-specific additional recommendations
        if mode == "expert":
            st.markdown("### 🎯 Expert-Level Improvements:")
            expert_tips = [
                "Develop detailed unit economics model with cohort analysis",
                "Create competitive moat analysis and IP strategy",
                "Build investor-ready financial model with scenario planning",
                "Prepare for due diligence with organized data room"
            ]

            for tip in expert_tips:
                st.info(f"💡 {tip}")

    def render_analysis_summary(self, result: PitchAnalysisResult):
        """Render overall analysis summary."""
        st.markdown("## 📋 Analysis Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Readiness", f"{result.readiness_score:.0f}/100")

        with col2:
            st.metric("Storytelling", f"{result.storytelling_score:.1f}/10")

        with col3:
            st.metric("Emotional Hook", f"{result.emotional_hook_score:.1f}/10")

        with col4:
            investment_interest = sum(1 for r in result.investor_simulations
                                    if r.investment_likelihood in [InvestmentLikelihood.HIGH, InvestmentLikelihood.MEDIUM])
            st.metric("Investor Interest", f"{investment_interest}/{len(result.investor_simulations)}")

        # Overall recommendation
        if result.readiness_score >= 80:
            st.success("🚀 Your pitch is investor-ready! Consider scheduling meetings with VCs.")
        elif result.readiness_score >= 60:
            st.info("📈 Good foundation. Address key recommendations before approaching investors.")
        else:
            st.warning("🔧 Significant improvements needed before investor meetings.")

    def render_footer(self):
        """Render footer with additional information."""
        st.markdown("---")
        st.markdown("### About PitchOS")
        st.markdown("""
        PitchOS uses advanced AI to analyze your startup pitch from multiple perspectives:
        - **VC Analysis**: Simulates reactions from different investor types
        - **Market Validation**: Checks claims against industry standards
        - **Storytelling**: Evaluates narrative structure and emotional appeal
        - **Technical Assessment**: Reviews feasibility and execution capability

        Built with ❤️ using Streamlit and Google Gemini AI.
        """)

        st.markdown("*Remember: This is an AI analysis tool. Always validate insights with real investors and customers.*")
