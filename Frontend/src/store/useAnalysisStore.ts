import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { AnalysisResult, AnalysisMode, InputMethod, OCRResult } from '../types'

interface AnalysisState {
  // Current analysis state
  isAnalyzing: boolean
  analysisResult: AnalysisResult | null
  analysisMode: AnalysisMode
  inputMethod: InputMethod
  pitchContent: string
  
  // File upload state
  uploadedFiles: File[]
  isProcessingFiles: boolean
  ocrResults: OCRResult[]
  
  // UI state
  activeTab: string
  showPreprocessing: boolean
  aggressiveMode: boolean
  
  // History
  analysisHistory: Array<{
    id: string
    timestamp: Date
    result: AnalysisResult
    mode: AnalysisMode
    inputMethod: InputMethod
    content: string
  }>
  
  // Actions
  setAnalyzing: (isAnalyzing: boolean) => void
  setAnalysisResult: (result: AnalysisResult | null) => void
  setAnalysisMode: (mode: AnalysisMode) => void
  setInputMethod: (method: InputMethod) => void
  setPitchContent: (content: string) => void
  setUploadedFiles: (files: File[]) => void
  setProcessingFiles: (isProcessing: boolean) => void
  setOcrResults: (results: OCRResult[]) => void
  setActiveTab: (tab: string) => void
  setShowPreprocessing: (show: boolean) => void
  setAggressiveMode: (aggressive: boolean) => void
  addToHistory: (result: AnalysisResult, mode: AnalysisMode, inputMethod: InputMethod, content: string) => void
  clearHistory: () => void
  reset: () => void
}

export const useAnalysisStore = create<AnalysisState>()(
  persist(
    (set, get) => ({
      // Initial state
      isAnalyzing: false,
      analysisResult: null,
      analysisMode: 'expert',
      inputMethod: 'text',
      pitchContent: '',
      uploadedFiles: [],
      isProcessingFiles: false,
      ocrResults: [],
      activeTab: 'overview',
      showPreprocessing: false,
      aggressiveMode: false,
      analysisHistory: [],

      // Actions
      setAnalyzing: (isAnalyzing) => set({ isAnalyzing }),
      
      setAnalysisResult: (result) => {
        set({ analysisResult: result })
        if (result) {
          const { analysisMode, inputMethod, pitchContent } = get()
          get().addToHistory(result, analysisMode, inputMethod, pitchContent)
        }
      },
      
      setAnalysisMode: (mode) => set({ analysisMode: mode }),
      setInputMethod: (method) => set({ inputMethod: method }),
      setPitchContent: (content) => set({ pitchContent: content }),
      setUploadedFiles: (files) => set({ uploadedFiles: files }),
      setProcessingFiles: (isProcessing) => set({ isProcessingFiles: isProcessing }),
      setOcrResults: (results) => set({ ocrResults: results }),
      setActiveTab: (tab) => set({ activeTab: tab }),
      setShowPreprocessing: (show) => set({ showPreprocessing: show }),
      setAggressiveMode: (aggressive) => set({ aggressiveMode: aggressive }),
      
      addToHistory: (result, mode, inputMethod, content) => {
        const newEntry = {
          id: Date.now().toString(),
          timestamp: new Date(),
          result,
          mode,
          inputMethod,
          content: content.substring(0, 500), // Store first 500 chars
        }
        
        set((state) => ({
          analysisHistory: [newEntry, ...state.analysisHistory].slice(0, 10) // Keep last 10
        }))
      },
      
      clearHistory: () => set({ analysisHistory: [] }),
      
      reset: () => set({
        isAnalyzing: false,
        analysisResult: null,
        pitchContent: '',
        uploadedFiles: [],
        isProcessingFiles: false,
        ocrResults: [],
        activeTab: 'overview',
      }),
    }),
    {
      name: 'pitchos-analysis-store',
      partialize: (state) => ({
        analysisMode: state.analysisMode,
        inputMethod: state.inputMethod,
        analysisHistory: state.analysisHistory,
        showPreprocessing: state.showPreprocessing,
        aggressiveMode: state.aggressiveMode,
      }),
    }
  )
)
