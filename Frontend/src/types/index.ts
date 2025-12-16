// PitchOS React Frontend Types

export interface PitchElement {
  content: string
  clarity_score: number
  completeness_score: number
}

export interface DeckSummary {
  problem: PitchElement
  solution: PitchElement
  market: PitchElement
  traction: PitchElement
  business_model: PitchElement
  team: PitchElement
  financials: PitchElement
  competition: PitchElement
  vision: PitchElement
}

export interface InvestorReaction {
  persona: string
  avatar: string
  reaction: string
  investment_likelihood: 'High' | 'Medium' | 'Low' | 'Very Low'
  key_concerns: string[]
  excitement_level: number
}

export interface QAItem {
  question: string
  ideal_response: string
  difficulty_level: string
  category: string
}

export interface VCQABattle {
  questions: QAItem[]
}

export interface CrowdFeedback {
  comment: string
  sentiment: 'positive' | 'negative' | 'neutral'
  emoji: string
  category: string
}

export interface IdeaValidationReport {
  logic_pass: boolean
  issues_detected: string[]
  confidence_score: number
  market_validation_score: number
  technical_feasibility_score: number
}

export interface TeamProductMarketFit {
  team_score: number
  product_score: number
  market_score: number
  alignment_score: number
  rationale: string
}

export interface AnalysisResult {
  deck_summary: DeckSummary
  readiness_score: number
  hype_meter: number
  startup_archetype: string
  storytelling_score: number
  emotional_hook_score: number
  investor_simulations: InvestorReaction[]
  vc_qa_battle: VCQABattle
  pitch_flags: string[]
  crowd_feedback: CrowdFeedback[]
  idea_validation_report: IdeaValidationReport
  team_product_market_fit: TeamProductMarketFit
  recommendations: {
    next_steps: string[]
  }
}

export interface PitchAnalysisRequest {
  content: string
  mode: 'beginner' | 'expert'
  source_type: 'text' | 'file' | 'ocr'
}

export interface PitchAnalysisResponse {
  success: boolean
  data?: AnalysisResult
  error?: string
}

export interface FileUploadResponse {
  success: boolean
  content?: string
  filename?: string
  error?: string
}

export interface OCRResult {
  filename: string
  text: string
  method: 'easyocr' | 'google_vision' | 'failed'
  confidence: number
  is_valid: boolean
  issues: string[]
  processing_time: number
}

export interface ImageUploadResponse {
  success: boolean
  combined_text?: string
  results?: OCRResult[]
  error?: string
}

export interface HealthResponse {
  status: string
  version: string
  features: {
    core_analysis: boolean
    file_upload: boolean
    ocr_processing: boolean
  }
}

export type InputMethod = 'text' | 'file' | 'image'
export type AnalysisMode = 'beginner' | 'expert'
