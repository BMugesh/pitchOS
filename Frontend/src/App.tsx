import React, { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Header from './components/Header'
import PitchInput from './components/PitchInput'
import AnalysisResults from './components/AnalysisResults'
import LoadingSpinner from './components/LoadingSpinner'
import { AnalysisResult } from './types'
import './index.css'

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisMode, setAnalysisMode] = useState<'beginner' | 'expert'>('expert')

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result)
    setIsAnalyzing(false)
  }

  const handleAnalysisStart = () => {
    setIsAnalyzing(true)
    setAnalysisResult(null)
  }

  const handleAnalysisError = () => {
    setIsAnalyzing(false)
  }

  const handleReset = () => {
    setAnalysisResult(null)
    setIsAnalyzing(false)
  }

  return (
    <div className="min-h-screen bg-base-200">
      <Header />
      
      <main className="container mx-auto px-4 py-8 max-w-none">
        <Routes>
          <Route path="/" element={
            <div className="max-w-[1400px] mx-auto w-full">
              {/* Hero Section */}
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="text-center mb-12"
              >
                <h1 className="text-5xl font-bold text-primary mb-4">
                  🚀 PitchOS
                </h1>
                <p className="text-xl text-base-content/70 mb-8 max-w-3xl mx-auto">
                  An omniscient AI designed to evaluate startup pitch decks like a seasoned VC,
                  a critical founder, and an engaged tech crowd — all at once.
                </p>
                
                {/* Mode Selector */}
                <div className="flex justify-center mb-8">
                  <div className="join">
                    <button
                      onClick={() => setAnalysisMode('beginner')}
                      className={`btn join-item ${
                        analysisMode === 'beginner'
                          ? 'btn-primary'
                          : 'btn-outline'
                      }`}
                    >
                      Beginner Mode
                    </button>
                    <button
                      onClick={() => setAnalysisMode('expert')}
                      className={`btn join-item ${
                        analysisMode === 'expert'
                          ? 'btn-primary'
                          : 'btn-outline'
                      }`}
                    >
                      Expert Mode
                    </button>
                  </div>
                </div>
              </motion.div>

              {/* Main Content */}
              {isAnalyzing ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex flex-col items-center justify-center py-20"
                >
                  <LoadingSpinner size="large" />
                  <h2 className="text-2xl font-semibold text-base-content mt-6 mb-2">
                    Analyzing Your Pitch
                  </h2>
                  <p className="text-base-content/70 text-center max-w-md">
                    Our AI is evaluating your pitch from multiple perspectives.
                    This may take a few moments...
                  </p>
                </motion.div>
              ) : analysisResult ? (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6 }}
                >
                  <AnalysisResults 
                    result={analysisResult} 
                    mode={analysisMode}
                    onReset={handleReset}
                  />
                </motion.div>
              ) : (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: 0.2 }}
                >
                  <PitchInput
                    mode={analysisMode}
                    onAnalysisStart={handleAnalysisStart}
                    onAnalysisComplete={handleAnalysisComplete}
                    onAnalysisError={handleAnalysisError}
                  />
                </motion.div>
              )}
            </div>
          } />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="footer footer-center bg-base-100 border-t border-base-300 mt-20 p-8">
        <div className="text-center text-base-content/70">
          <p className="mb-2">
            Built with ❤️ using React, FastAPI, and Google Gemini AI
          </p>
          <p className="text-sm">
            Remember: This is an AI analysis tool. Always validate insights with real investors and customers.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
