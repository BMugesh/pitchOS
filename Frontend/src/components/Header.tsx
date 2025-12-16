import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Rocket, Activity, Zap } from 'lucide-react'
import { pitchAPI } from '../utils/api'
import { HealthResponse } from '../types'
import ThemeToggle from './ThemeToggle'

const Header: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const healthData = await pitchAPI.getHealth()
        setHealth(healthData)
      } catch (error) {
        console.error('Health check failed:', error)
      } finally {
        setIsLoading(false)
      }
    }

    checkHealth()
  }, [])

  return (
    <header className="navbar bg-base-100 shadow-sm border-b border-base-300">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between w-full">
          {/* Logo and Title */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-3"
          >
            <div className="avatar placeholder">
              <div className="bg-primary text-primary-content rounded-lg w-12 h-12">
                <Rocket className="w-6 h-6" />
              </div>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-base-content">PitchOS</h1>
              <p className="text-sm text-base-content/70">AI Pitch Deck Analyzer</p>
            </div>
          </motion.div>

          {/* Status Indicators and Theme Toggle */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex items-center space-x-4"
          >
            {isLoading ? (
              <div className="flex items-center space-x-2 text-base-content/70">
                <span className="loading loading-spinner loading-sm"></span>
                <span className="text-sm">Checking status...</span>
              </div>
            ) : health ? (
              <div className="flex items-center space-x-4">
                {/* API Status */}
                <div className="flex items-center space-x-2">
                  <div className="badge badge-success badge-xs"></div>
                  <span className="text-sm text-base-content/70">API Online</span>
                </div>

                {/* Feature Status */}
                <div className="flex items-center space-x-3">
                  {/* Core Analysis */}
                  <div className="flex items-center space-x-1" title="Core Analysis">
                    <Activity className={`w-4 h-4 ${health.features.core_analysis ? 'text-success' : 'text-base-content/40'}`} />
                    <span className="text-xs text-base-content/70">Analysis</span>
                  </div>

                  {/* OCR Processing */}
                  <div className="flex items-center space-x-1" title="OCR Processing">
                    <Zap className={`w-4 h-4 ${health.features.ocr_processing ? 'text-success' : 'text-base-content/40'}`} />
                    <span className="text-xs text-base-content/70">OCR</span>
                  </div>
                </div>

                {/* Version */}
                <div className="badge badge-outline badge-sm">
                  v{health.version}
                </div>
              </div>
            ) : (
              <div className="flex items-center space-x-2 text-error">
                <div className="badge badge-error badge-xs"></div>
                <span className="text-sm">API Offline</span>
              </div>
            )}

            {/* Theme Toggle */}
            <ThemeToggle />
          </motion.div>
        </div>
      </div>
    </header>
  )
}

export default Header
