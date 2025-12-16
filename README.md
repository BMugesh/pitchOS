# 🚀 PitchOS - AI-Powered Startup Pitch Deck Analyzer

An omniscient AI designed to evaluate startup pitch decks like a seasoned VC, a critical founder, and an engaged tech crowd — all at once.

![PitchOS Demo](https://img.shields.io/badge/Status-Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![AI](https://img.shields.io/badge/AI-Gemini--1.5--Flash-orange)

## ✨ Features

### 🧠 Comprehensive Analysis

- **Pitch Element Extraction**: Problem, Solution, Market, Traction, Business Model, Team, Financials, Competition, Vision
- **Readiness Score**: 0-100 pitch readiness with detailed breakdown
- **Storytelling & Emotional Hook**: Narrative quality assessment

### 📸 Hybrid OCR System

- **EasyOCR Primary**: Fast, local text extraction from images
- **Google Vision Fallback**: Cloud-based OCR for difficult images
- **Image Preprocessing**: Advanced OpenCV-based image enhancement
- **Batch Processing**: Handle multiple slide images simultaneously
- **Quality Analysis**: Image quality scoring and improvement suggestions

### 🎭 Investor Persona Simulation

- **Risk-Averse VC**: Conservative, traction-focused analysis
- **Visionary Angel**: Big picture, founder-focused evaluation
- **Corporate Strategic**: Partnership and acquisition potential

### ⚔️ VC Q&A Battle

- Generates tough investor questions based on pitch weaknesses
- Provides ideal founder responses
- Categorizes by difficulty and topic area

### 📊 Advanced Scoring Systems

- **Hype Meter**: Detects buzzwords and over-promising (0-100)
- **Startup Archetype**: Builder, Visionary, Hustler, Academic, etc.
- **Team-Product-Market Fit**: Alignment analysis with radar chart
- **Idea Validation**: Logic checks and confidence scoring

### 💬 AI Crowd Feedback

- Simulates diverse community reactions
- YouTube-comment style feedback with sentiment analysis
- Technical, business, and presentation perspectives

### 🚨 Red Flag Detection

- Identifies overused jargon and hype terms
- Flags unclear monetization models
- Detects missing key elements

### 🔧 Smart Recommendations

- **Beginner Mode**: Simplified, actionable advice
- **Expert Mode**: Detailed technical and strategic guidance
- Prioritized next steps based on analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/pitchos.git
cd pitchos
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

```bash
cp .env.example .env
# Edit .env and add your Google API key:
# GOOGLE_API_KEY=your_api_key_here
```

4. **Run the application**

```bash
streamlit run app.py
```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 Usage

### Input Methods

- **Text Input**: Paste your pitch content directly
- **File Upload**: Upload PDF, TXT, or DOCX files
- **Image Upload (OCR)**: Upload pitch deck images with hybrid OCR processing

### Analysis Modes

- **Beginner**: Simplified feedback for first-time founders
- **Expert**: Detailed technical analysis for experienced entrepreneurs

### Example Pitch Format

```
Problem: [Describe the problem you're solving]
Solution: [Your product/service solution]
Market: [Target market and size]
Traction: [Current metrics and growth]
Business Model: [How you make money]
Team: [Founder and key team backgrounds]
Financials: [Revenue projections, funding needs]
Competition: [Competitive landscape]
Vision: [Long-term goals and impact]
```

## 🏗️ Architecture

```
PitchOS/
├── app.py                 # Main Streamlit application
├── src/
│   ├── pitch_analyzer.py  # Core analysis engine
│   ├── ui_components.py   # Streamlit UI components
│   ├── investor_personas.py # Investor simulation
│   ├── vc_qa_battle.py    # Q&A generation
│   ├── scoring_system.py  # Scoring algorithms
│   ├── file_processor.py  # File upload handling
│   ├── ocr_processor.py   # Hybrid OCR system
│   ├── image_preprocessor.py # Image preprocessing
│   ├── models.py          # Data models
│   └── config.py          # Configuration
├── requirements.txt       # Python dependencies
├── test_ocr_system.py     # OCR system tests
└── .env.example          # Environment template
```

## 🎯 Key Components

### PitchAnalyzer

Core engine that orchestrates the entire analysis process using Google Gemini AI.

### InvestorPersonaSimulator

Simulates reactions from different investor types with authentic personas and investment philosophies.

### VCQABattleGenerator

Identifies pitch weaknesses and generates targeted tough questions with ideal responses.

### PitchScoringSystem

Comprehensive scoring algorithms for readiness, hype detection, and validation.

### PitchOSUI

Rich Streamlit interface with interactive visualizations, progress bars, and styled components.

### HybridOCRProcessor

Advanced OCR system that uses EasyOCR as primary method with Google Cloud Vision as fallback for difficult images.

### ImagePreprocessor

OpenCV-based image preprocessing pipeline that enhances images for better OCR accuracy through denoising, contrast enhancement, and sharpening.

## 🔧 Configuration

Key settings in `src/config.py`:

```python
# Model settings
MODEL_NAME = "gemini-1.5-flash"
MAX_TOKENS = 8192
TEMPERATURE = 0.7

# Scoring thresholds
READINESS_THRESHOLDS = {
    "excellent": 90,
    "good": 75,
    "fair": 60,
    "poor": 40
}

# Investor personas
INVESTOR_PERSONAS = [...]

# Hype terms detection
HYPE_TERMS = [...]
```

## 📊 Analysis Output

PitchOS provides structured JSON output with:

```json
{
  "deck_summary": {...},
  "readiness_score": 87,
  "investor_simulations": [...],
  "vc_qa_battle": {...},
  "hype_meter": 72,
  "startup_archetype": "Visionary",
  "pitch_flags": [...],
  "crowd_feedback": [...],
  "idea_validation_report": {...},
  "recommendations": {...}
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the interactive web interface
- Powered by [Google Gemini AI](https://ai.google.dev/) for intelligent analysis
- Inspired by the startup ecosystem and VC community

## 📞 Support

- 📧 Email: mkbm1307@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/BMugesh/pitchos/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/BMugesh/pitchos/discussions)

---

**Remember**: PitchOS is an AI analysis tool. Always validate insights with real investors and customers. 🚀
