"""
Setup script for PitchOS React + Streamlit dual frontend
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status."""
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def create_missing_react_components():
    """Create remaining React components."""
    
    # Create components directory if it doesn't exist
    components_dir = Path("frontend/src/components")
    components_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a simple AnalysisResults component
    analysis_results_content = '''import React from 'react'
import { motion } from 'framer-motion'
import { AnalysisResult, AnalysisMode } from '../types'
import { formatScore, getProgressColor, downloadReport } from '../utils/api'

interface AnalysisResultsProps {
  result: AnalysisResult
  mode: AnalysisMode
  onReset: () => void
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result, mode, onReset }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-900">Analysis Results</h2>
        <div className="space-x-4">
          <button
            onClick={() => downloadReport(result)}
            className="btn-secondary"
          >
            📥 Download Report
          </button>
          <button onClick={onReset} className="btn-primary">
            🔄 New Analysis
          </button>
        </div>
      </div>

      {/* Readiness Score */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">📊 Pitch Readiness Score</h3>
        <div className="flex items-center space-x-6">
          <div className="flex-1">
            <div className="progress-bar">
              <div 
                className={`progress-fill ${getProgressColor(result.readiness_score)}`}
                style={{ width: `${result.readiness_score}%` }}
              />
            </div>
          </div>
          <div className="text-3xl font-bold text-gray-900">
            {formatScore(result.readiness_score)}/100
          </div>
        </div>
        <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="metric-card">
            <div className="text-sm text-gray-600">Storytelling</div>
            <div className="text-xl font-semibold">{formatScore(result.storytelling_score)}/10</div>
          </div>
          <div className="metric-card">
            <div className="text-sm text-gray-600">Emotional Hook</div>
            <div className="text-xl font-semibold">{formatScore(result.emotional_hook_score)}/10</div>
          </div>
          <div className="metric-card">
            <div className="text-sm text-gray-600">Hype Level</div>
            <div className="text-xl font-semibold">{formatScore(result.hype_meter)}/100</div>
          </div>
        </div>
      </div>

      {/* Startup Archetype */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">🧬 Startup Archetype</h3>
        <div className="archetype-badge text-lg">
          {result.startup_archetype}
        </div>
      </div>

      {/* Investor Reactions */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">🎭 Investor Reactions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {result.investor_simulations.map((reaction, index) => (
            <div key={index} className="investor-card">
              <div className="flex items-center space-x-2 mb-3">
                <span className="text-2xl">{reaction.avatar}</span>
                <div>
                  <div className="font-semibold">{reaction.persona}</div>
                  <div className="text-sm text-gray-600">{reaction.investment_likelihood} Interest</div>
                </div>
              </div>
              <p className="text-gray-700 text-sm">{reaction.reaction}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Red Flags */}
      {result.pitch_flags.length > 0 && (
        <div className="card">
          <h3 className="text-xl font-semibold mb-4">🚨 Areas for Improvement</h3>
          <div className="space-y-2">
            {result.pitch_flags.map((flag, index) => (
              <div key={index} className="flag-warning">
                <span className="text-yellow-600">⚠️</span>
                <span className="text-gray-700">{flag}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">💡 Recommendations</h3>
        <div className="space-y-2">
          {result.recommendations.next_steps.map((rec, index) => (
            <div key={index} className="recommendation-item">
              <span className="text-blue-600">📋</span>
              <span className="text-gray-700">{rec}</span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}

export default AnalysisResults'''
    
    with open("frontend/src/components/AnalysisResults.tsx", "w") as f:
        f.write(analysis_results_content)
    
    print("✅ Created AnalysisResults component")

def setup_react_frontend():
    """Set up React frontend."""
    print("🔧 Setting up React frontend...")
    
    # Check if Node.js is installed
    if not run_command("node --version"):
        print("❌ Node.js not found. Please install Node.js first.")
        return False
    
    # Install dependencies
    if not run_command("npm install", cwd="frontend"):
        print("❌ Failed to install React dependencies")
        return False
    
    # Create missing components
    create_missing_react_components()
    
    return True

def setup_fastapi_backend():
    """Set up FastAPI backend."""
    print("🔧 Setting up FastAPI backend...")
    
    # Install Python dependencies
    if not run_command("pip install -r backend/requirements.txt"):
        print("❌ Failed to install Python dependencies")
        return False
    
    return True

def create_env_files():
    """Create environment files."""
    print("🔧 Creating environment files...")
    
    # Backend .env
    backend_env = """# Backend Environment Variables
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_CLOUD_VISION_API_KEY=your_google_cloud_vision_api_key_here
DEBUG=True
LOG_LEVEL=INFO
"""
    
    with open("backend/.env", "w") as f:
        f.write(backend_env)
    
    # Frontend .env
    frontend_env = """# Frontend Environment Variables
VITE_API_URL=http://localhost:8000
"""
    
    with open("frontend/.env", "w") as f:
        f.write(frontend_env)
    
    print("✅ Created environment files")

def create_startup_scripts():
    """Create startup scripts."""
    print("🔧 Creating startup scripts...")
    
    # Start backend script
    start_backend = """#!/bin/bash
echo "🚀 Starting PitchOS FastAPI Backend..."
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
    
    with open("start_backend.sh", "w") as f:
        f.write(start_backend)
    
    # Start frontend script
    start_frontend = """#!/bin/bash
echo "🚀 Starting PitchOS React Frontend..."
cd frontend
npm run dev
"""
    
    with open("start_frontend.sh", "w") as f:
        f.write(start_frontend)
    
    # Start both script
    start_both = """#!/bin/bash
echo "🚀 Starting PitchOS Full Stack..."
echo "Starting backend..."
cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
echo "Starting frontend..."
cd frontend && npm run dev &
wait
"""
    
    with open("start_pitchos.sh", "w") as f:
        f.write(start_both)
    
    # Windows batch files
    start_backend_bat = """@echo off
echo 🚀 Starting PitchOS FastAPI Backend...
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
    
    with open("start_backend.bat", "w") as f:
        f.write(start_backend_bat)
    
    start_frontend_bat = """@echo off
echo 🚀 Starting PitchOS React Frontend...
cd frontend
npm run dev
"""
    
    with open("start_frontend.bat", "w") as f:
        f.write(start_frontend_bat)
    
    print("✅ Created startup scripts")

def main():
    """Main setup function."""
    print("🚀 PitchOS Dual Frontend Setup\n")
    
    print("This will set up both Streamlit and React frontends for PitchOS:")
    print("- Streamlit: Quick demos and prototyping")
    print("- React: Production-ready web application")
    print("- FastAPI: Backend API for React frontend\n")
    
    # Create environment files
    create_env_files()
    
    # Setup FastAPI backend
    if not setup_fastapi_backend():
        print("❌ Backend setup failed")
        return
    
    # Setup React frontend
    if not setup_react_frontend():
        print("❌ Frontend setup failed")
        return
    
    # Create startup scripts
    create_startup_scripts()
    
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Add your Google API key to backend/.env")
    print("2. Start the backend: python start_backend.py (or start_backend.bat on Windows)")
    print("3. Start the frontend: python start_frontend.py (or start_frontend.bat on Windows)")
    print("4. Or start both: python start_pitchos.py")
    
    print("\n🌐 Access Points:")
    print("- React Frontend: http://localhost:3000")
    print("- FastAPI Backend: http://localhost:8000")
    print("- Streamlit App: streamlit run app.py (port 8501)")
    
    print("\n✨ Features Available:")
    print("✅ React frontend with modern UI/UX")
    print("✅ FastAPI backend with REST API")
    print("✅ File upload (PDF, DOC, TXT)")
    print("✅ Image OCR processing")
    print("✅ Real-time analysis")
    print("✅ Responsive design")
    print("✅ Streamlit fallback for demos")

if __name__ == "__main__":
    main()
