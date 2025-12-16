import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import './AnalysisResults.css'
import { 
  Download, 
  RefreshCw, 
  TrendingUp, 
  Users, 
  MessageSquare, 
  AlertTriangle,
  Lightbulb,
  Target,
  BarChart3,
  Zap,
  Star,
  Award,
  TrendingDown,
  CheckCircle,
  XCircle,
  ArrowRight,
  Eye,
  Heart,
  Brain,
  Rocket,
  Shield,
  DollarSign
} from 'lucide-react'
import { AnalysisResult, AnalysisMode } from '../types'
import { 
  formatScore, 
  getProgressColor, 
  getInvestmentLikelihoodColor,
  getSentimentColor,
  downloadReport 
} from '../utils/api'
import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts'

interface AnalysisResultsProps {
  result: AnalysisResult
  mode: AnalysisMode
  onReset: () => void
}

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ result, mode, onReset }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'investors' | 'qa' | 'feedback'>('overview')
  const [showDetails, setShowDetails] = useState(false)

  // Prepare radar chart data
  const radarData = [
    { subject: 'Team', score: result.team_product_market_fit.team_score, fullMark: 10 },
    { subject: 'Product', score: result.team_product_market_fit.product_score, fullMark: 10 },
    { subject: 'Market', score: result.team_product_market_fit.market_score, fullMark: 10 },
    { subject: 'Traction', score: (result.deck_summary.traction.clarity_score + result.deck_summary.traction.completeness_score) / 2, fullMark: 10 },
    { subject: 'Business Model', score: (result.deck_summary.business_model.clarity_score + result.deck_summary.business_model.completeness_score) / 2, fullMark: 10 },
  ]

  const handleDownload = async () => {
    try {
      await downloadReport(result)
    } catch (error) {
      console.error('Download failed:', error)
    }
  }

  const getScoreStatus = (score: number) => {
    if (score >= 80) return { 
      text: 'Excellent', 
      color: 'text-emerald-600', 
      bg: 'bg-gradient-to-br from-emerald-50 to-green-50', 
      border: 'border-emerald-200',
      icon: Award,
      gradient: 'from-emerald-500 to-green-600',
      ring: 'ring-emerald-500/20'
    }
    if (score >= 60) return { 
      text: 'Good', 
      color: 'text-blue-600', 
      bg: 'bg-gradient-to-br from-blue-50 to-indigo-50', 
      border: 'border-blue-200',
      icon: CheckCircle,
      gradient: 'from-blue-500 to-indigo-600',
      ring: 'ring-blue-500/20'
    }
    if (score >= 40) return { 
      text: 'Fair', 
      color: 'text-amber-600', 
      bg: 'bg-gradient-to-br from-amber-50 to-orange-50', 
      border: 'border-amber-200',
      icon: AlertTriangle,
      gradient: 'from-amber-500 to-orange-600',
      ring: 'ring-amber-500/20'
    }
    return { 
      text: 'Needs Work', 
      color: 'text-red-600', 
      bg: 'bg-gradient-to-br from-red-50 to-pink-50', 
      border: 'border-red-200',
      icon: XCircle,
      gradient: 'from-red-500 to-pink-600',
      ring: 'ring-red-500/20'
    }
  }

  const status = getScoreStatus(result.readiness_score)

  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart3, color: 'text-blue-600', bgColor: 'bg-blue-50' },
    { id: 'investors', label: 'Investors', icon: Users, color: 'text-purple-600', bgColor: 'bg-purple-50' },
    { id: 'qa', label: 'Q&A Battle', icon: MessageSquare, color: 'text-green-600', bgColor: 'bg-green-50' },
    { id: 'feedback', label: 'Feedback', icon: Zap, color: 'text-orange-600', bgColor: 'bg-orange-50' },
  ]

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5, ease: "easeOut" }
    }
  }

  const scoreVariants = {
    hidden: { scale: 0, opacity: 0 },
    visible: {
      scale: 1,
      opacity: 1,
      transition: { 
        type: "spring",
        stiffness: 200,
        damping: 15,
        delay: 0.5
      }
    }
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="w-full max-w-[1400px] mx-auto space-y-8"
    >
      {/* Enhanced Header */}
      <motion.div 
        variants={itemVariants}
        className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-slate-50 via-white to-slate-50 border border-slate-200 shadow-xl"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5" />
        <div className="relative p-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-start space-x-4">
              <motion.div
                variants={scoreVariants}
                className={`flex items-center justify-center w-16 h-16 rounded-2xl ${status.bg} ${status.border} border-2 shadow-lg ${status.ring} ring-4`}
              >
                <status.icon className={`w-8 h-8 ${status.color}`} />
              </motion.div>
              <div>
                <motion.h1 
                  variants={itemVariants}
                  className="text-4xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent"
                >
                  Analysis Complete
                </motion.h1>
                <motion.p 
                  variants={itemVariants}
                  className="text-slate-600 mt-2 text-lg"
                >
                  Your pitch has been analyzed by our AI from multiple perspectives
                </motion.p>
                <motion.div 
                  variants={itemVariants}
                  className="flex items-center space-x-4 mt-4"
                >
                  <div className={`inline-flex items-center px-4 py-2 rounded-full ${status.bg} ${status.border} border`}>
                    <span className={`text-sm font-semibold ${status.color}`}>
                      {status.text}
                    </span>
                  </div>
                  <div className="text-sm text-slate-500">
                    Mode: <span className="font-medium capitalize text-slate-700">{mode}</span>
                  </div>
                </motion.div>
              </div>
            </div>
            
            <motion.div 
              variants={itemVariants}
              className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-3 mt-6 lg:mt-0"
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="button"
                onClick={handleDownload}
                className="inline-flex items-center px-6 py-3 border border-slate-300 rounded-xl text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-sm transition-all duration-200"
              >
                <Download className="w-4 h-4 mr-2" />
                Download Report
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="button"
                onClick={onReset}
                className="inline-flex items-center px-6 py-3 border border-transparent rounded-xl text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-lg transition-all duration-200"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                New Analysis
              </motion.button>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Enhanced Key Metrics */}
      <motion.div 
        variants={itemVariants}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {/* Readiness Score */}
        <motion.div 
          variants={itemVariants}
          whileHover={{ y: -4, scale: 1.02 }}
          className="relative group"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition-opacity duration-300" />
          <div className="relative bg-white rounded-2xl p-6 shadow-lg border border-slate-200 text-center">
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-600">
              <Target className="w-6 h-6 text-white" />
            </div>
            <motion.div 
              variants={scoreVariants}
              className="text-3xl font-bold text-slate-800 mb-2"
            >
              {formatScore(result.readiness_score)}
            </motion.div>
            <div className="text-sm text-slate-600 mb-3">Readiness Score</div>
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${status.bg} ${status.color} ${status.border} border`}>
              {status.text}
            </div>
          </div>
        </motion.div>

        {/* Startup Archetype */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4, scale: 1.02 }}
          className="relative group"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition-opacity duration-300" />
          <div className="relative bg-white rounded-2xl p-6 shadow-lg border border-slate-200 text-center">
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div className="text-2xl mb-2">🧬</div>
            <div className="font-semibold text-slate-800 mb-1">{result.startup_archetype}</div>
            <div className="text-sm text-slate-600">Startup Archetype</div>
          </div>
        </motion.div>

        {/* Storytelling */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4, scale: 1.02 }}
          className="relative group"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-green-600 to-emerald-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition-opacity duration-300" />
          <div className="relative bg-white rounded-2xl p-6 shadow-lg border border-slate-200 text-center">
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-r from-green-500 to-emerald-600">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <motion.div
              variants={scoreVariants}
              className="text-3xl font-bold text-slate-800 mb-2"
            >
              {formatScore(result.storytelling_score * 10)}
            </motion.div>
            <div className="text-sm text-slate-600 mb-3">Storytelling Score</div>
            <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-green-50 to-emerald-50 text-green-700 border border-green-200">
              {result.storytelling_score >= 7 ? '📚 Compelling' : result.storytelling_score >= 5 ? '📖 Good' : '📝 Needs Work'}
            </div>
          </div>
        </motion.div>

        {/* Hype Level */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4, scale: 1.02 }}
          className="relative group"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-orange-600 to-red-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition-opacity duration-300" />
          <div className="relative bg-white rounded-2xl p-6 shadow-lg border border-slate-200 text-center">
            <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-r from-orange-500 to-red-600">
              <Rocket className="w-6 h-6 text-white" />
            </div>
            <motion.div
              variants={scoreVariants}
              className="text-3xl font-bold text-slate-800 mb-2"
            >
              {formatScore(result.hype_meter)}
            </motion.div>
            <div className="text-sm text-slate-600 mb-3">Hype Level</div>
            <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r from-orange-50 to-red-50 text-orange-700 border border-orange-200">
              {result.hype_meter >= 70 ? '🔥 Hot' : result.hype_meter >= 40 ? '📈 Rising' : '📉 Cool'}
            </div>
          </div>
        </motion.div>
      </motion.div>

      {/* Enhanced Progress Section */}
      <motion.div
        variants={itemVariants}
        className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-white to-slate-50 border border-slate-200 shadow-xl"
      >
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-purple-500/5 to-pink-500/5" />
        <div className="relative p-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className={`flex items-center justify-center w-10 h-10 rounded-xl ${status.bg} ${status.border} border`}>
                <BarChart3 className={`w-5 h-5 ${status.color}`} />
              </div>
              <h3 className="text-xl font-semibold text-slate-800">Overall Readiness</h3>
            </div>
            <motion.span
              variants={scoreVariants}
              className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent"
            >
              {formatScore(result.readiness_score)}/100
            </motion.span>
          </div>

          <div className="relative mb-6">
            <div className="h-4 bg-slate-200 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${result.readiness_score}%` }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                className={`h-full bg-gradient-to-r ${status.gradient} shadow-sm`}
              />
            </div>
            <div className="flex justify-between text-xs text-slate-500 mt-2">
              <span>0</span>
              <span>25</span>
              <span>50</span>
              <span>75</span>
              <span>100</span>
            </div>
          </div>

          <div className={`p-4 rounded-xl ${status.bg} ${status.border} border`}>
            <div className="flex items-start space-x-3">
              <status.icon className={`w-5 h-5 ${status.color} mt-0.5 flex-shrink-0`} />
              <div>
                <div className={`font-medium ${status.color} mb-1`}>
                  {status.text} - {formatScore(result.readiness_score)}%
                </div>
                <div className="text-sm text-slate-600">
                  {result.readiness_score >= 75
                    ? "🚀 Your pitch is investor-ready! Consider scheduling meetings with VCs."
                    : result.readiness_score >= 50
                    ? "📈 Good foundation. Address key recommendations before approaching investors."
                    : "🔧 Significant improvements needed before investor meetings."}
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Enhanced Tabs Section */}
      <motion.div
        variants={itemVariants}
        className="bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden"
      >
        {/* Tab Navigation */}
        <div className="border-b border-slate-200 bg-gradient-to-r from-slate-50 to-white">
          <div className="flex space-x-1 p-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-3 rounded-xl font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                    : 'text-slate-600 hover:text-slate-800 hover:bg-slate-100'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Tab Content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="p-8"
          >
            {activeTab === 'overview' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-2xl font-bold text-slate-800 mb-4 flex items-center">
                    <BarChart3 className="w-6 h-6 mr-3 text-blue-600" />
                    Executive Summary
                  </h3>
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
                    <p className="text-slate-700 leading-relaxed">
                      {result.executive_summary || "Your pitch demonstrates strong potential with clear value proposition and market opportunity. Key strengths include compelling storytelling and solid business fundamentals. Areas for improvement focus on competitive differentiation and financial projections."}
                    </p>
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-lg font-semibold text-slate-800 mb-3 flex items-center">
                      <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                      Key Strengths
                    </h4>
                    <div className="space-y-2">
                      {(result.key_strengths || [
                        "Clear value proposition",
                        "Strong market opportunity",
                        "Experienced team",
                        "Compelling storytelling"
                      ]).map((strength, index) => (
                        <div key={index} className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg border border-green-200">
                          <div className="w-2 h-2 bg-green-500 rounded-full" />
                          <span className="text-slate-700">{strength}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="text-lg font-semibold text-slate-800 mb-3 flex items-center">
                      <AlertTriangle className="w-5 h-5 mr-2 text-orange-600" />
                      Areas for Improvement
                    </h4>
                    <div className="space-y-2">
                      {(result.areas_for_improvement || [
                        "Strengthen competitive analysis",
                        "Clarify revenue model",
                        "Expand market size data",
                        "Add customer testimonials"
                      ]).map((area, index) => (
                        <div key={index} className="flex items-center space-x-3 p-3 bg-orange-50 rounded-lg border border-orange-200">
                          <div className="w-2 h-2 bg-orange-500 rounded-full" />
                          <span className="text-slate-700">{area}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'investors' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-2xl font-bold text-slate-800 mb-6 flex items-center">
                    <Users className="w-6 h-6 mr-3 text-purple-600" />
                    Investor Perspective Analysis
                  </h3>
                </div>

                <div className="grid md:grid-cols-3 gap-6">
                  {[
                    { name: "Sarah Chen", role: "Partner @ TechVentures", avatar: "👩‍💼", reaction: "🚀", sentiment: "Excited", score: 85, comment: "Strong market opportunity and experienced team. Love the traction metrics!" },
                    { name: "Michael Rodriguez", role: "GP @ Innovation Capital", avatar: "👨‍💼", reaction: "🤔", sentiment: "Interested", score: 72, comment: "Solid foundation but need more clarity on competitive differentiation." },
                    { name: "Dr. Lisa Wang", role: "Managing Director @ Future Fund", avatar: "👩‍🔬", reaction: "💡", sentiment: "Curious", score: 78, comment: "Innovative approach. Would like to see more detailed financial projections." }
                  ].map((investor, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-gradient-to-br from-white to-slate-50 rounded-xl p-6 border border-slate-200 shadow-lg"
                    >
                      <div className="flex items-center space-x-3 mb-4">
                        <div className="text-2xl">{investor.avatar}</div>
                        <div>
                          <div className="font-semibold text-slate-800">{investor.name}</div>
                          <div className="text-sm text-slate-600">{investor.role}</div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl">{investor.reaction}</span>
                          <span className="text-sm font-medium text-slate-700">{investor.sentiment}</span>
                        </div>
                        <div className="text-lg font-bold text-slate-800">{investor.score}%</div>
                      </div>

                      <p className="text-sm text-slate-600 italic">"{investor.comment}"</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'qa' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-2xl font-bold text-slate-800 mb-6 flex items-center">
                    <MessageSquare className="w-6 h-6 mr-3 text-indigo-600" />
                    Q&A Battle Preparation
                  </h3>
                  <p className="text-slate-600 mb-6">
                    Prepare for tough investor questions with our AI-generated Q&A scenarios based on your pitch analysis.
                  </p>
                </div>

                <div className="space-y-6">
                  {[
                    {
                      category: "Market & Competition",
                      questions: [
                        "How do you differentiate from existing solutions in the market?",
                        "What's your total addressable market size and how did you calculate it?",
                        "Who are your main competitors and what's your competitive advantage?"
                      ]
                    },
                    {
                      category: "Business Model & Financials",
                      questions: [
                        "What's your revenue model and how do you plan to monetize?",
                        "What are your key metrics and current traction?",
                        "How much funding do you need and what will you use it for?"
                      ]
                    },
                    {
                      category: "Team & Execution",
                      questions: [
                        "What makes your team uniquely qualified to solve this problem?",
                        "What are the biggest risks to your business and how will you mitigate them?",
                        "What's your go-to-market strategy and customer acquisition plan?"
                      ]
                    }
                  ].map((section, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-200"
                    >
                      <h4 className="text-lg font-semibold text-slate-800 mb-4">{section.category}</h4>
                      <div className="space-y-3">
                        {section.questions.map((question, qIndex) => (
                          <div key={qIndex} className="flex items-start space-x-3 p-3 bg-white rounded-lg border border-slate-200">
                            <div className="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                              <span className="text-xs font-medium text-indigo-600">Q</span>
                            </div>
                            <p className="text-slate-700">{question}</p>
                          </div>
                        ))}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'feedback' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-2xl font-bold text-slate-800 mb-6 flex items-center">
                    <RefreshCw className="w-6 h-6 mr-3 text-green-600" />
                    Detailed Feedback & Recommendations
                  </h3>
                </div>

                <div className="space-y-6">
                  {[
                    {
                      title: "Slide Structure & Flow",
                      score: 78,
                      feedback: "Your slide progression follows a logical narrative arc. Consider strengthening the problem-solution fit and adding more customer validation.",
                      recommendations: [
                        "Add customer pain point quotes",
                        "Include before/after scenarios",
                        "Strengthen the 'why now' narrative"
                      ]
                    },
                    {
                      title: "Market Analysis",
                      score: 65,
                      feedback: "Market size calculations are present but could be more detailed. Competitive analysis needs strengthening with clearer differentiation.",
                      recommendations: [
                        "Use bottom-up market sizing",
                        "Add competitive feature comparison",
                        "Include market trend analysis"
                      ]
                    },
                    {
                      title: "Financial Projections",
                      score: 72,
                      feedback: "Revenue projections are realistic but need more granular breakdown. Unit economics should be more prominent.",
                      recommendations: [
                        "Show monthly recurring revenue growth",
                        "Add customer acquisition cost details",
                        "Include sensitivity analysis"
                      ]
                    }
                  ].map((item, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-white rounded-xl p-6 border border-slate-200 shadow-lg"
                    >
                      <div className="flex items-center justify-between mb-4">
                        <h4 className="text-lg font-semibold text-slate-800">{item.title}</h4>
                        <div className="flex items-center space-x-2">
                          <div className="text-lg font-bold text-slate-800">{item.score}%</div>
                          <div className={`w-3 h-3 rounded-full ${item.score >= 75 ? 'bg-green-500' : item.score >= 50 ? 'bg-yellow-500' : 'bg-red-500'}`} />
                        </div>
                      </div>

                      <p className="text-slate-600 mb-4">{item.feedback}</p>

                      <div>
                        <h5 className="font-medium text-slate-800 mb-2">Recommendations:</h5>
                        <div className="space-y-2">
                          {item.recommendations.map((rec, recIndex) => (
                            <div key={recIndex} className="flex items-center space-x-2">
                              <div className="w-1.5 h-1.5 bg-blue-500 rounded-full" />
                              <span className="text-sm text-slate-600">{rec}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </motion.div>
    </motion.div>
  )
}

export default AnalysisResults
