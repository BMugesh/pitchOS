// API utilities for PitchOS React Frontend

import axios from 'axios'
import {
  PitchAnalysisRequest,
  PitchAnalysisResponse,
  FileUploadResponse,
  ImageUploadResponse,
  HealthResponse
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes for analysis
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const pitchAPI = {
  // Health check
  async getHealth(): Promise<HealthResponse> {
    const response = await api.get('/')
    return response.data
  },

  // Analyze pitch content
  async analyzePitch(request: PitchAnalysisRequest): Promise<PitchAnalysisResponse> {
    const response = await api.post('/api/analyze', request)
    return response.data
  },

  // Upload file (PDF, DOC, TXT)
  async uploadFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/upload-file', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Upload images for OCR
  async uploadImages(files: File[]): Promise<ImageUploadResponse> {
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })

    const response = await api.post('/api/upload-images', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 180000, // 3 minutes for OCR processing
    })
    return response.data
  },
}

// Utility functions
export const formatScore = (score: number, decimals: number = 1): string => {
  return score.toFixed(decimals)
}

export const getScoreColor = (score: number): string => {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-yellow-600'
  if (score >= 40) return 'text-orange-600'
  return 'text-red-600'
}

export const getScoreBgColor = (score: number): string => {
  if (score >= 80) return 'bg-green-100'
  if (score >= 60) return 'bg-yellow-100'
  if (score >= 40) return 'bg-orange-100'
  return 'bg-red-100'
}

export const getProgressColor = (score: number): string => {
  if (score >= 80) return 'bg-green-500'
  if (score >= 60) return 'bg-yellow-500'
  if (score >= 40) return 'bg-orange-500'
  return 'bg-red-500'
}

export const getInvestmentLikelihoodColor = (likelihood: string): string => {
  switch (likelihood) {
    case 'High':
      return 'text-green-600 bg-green-100'
    case 'Medium':
      return 'text-yellow-600 bg-yellow-100'
    case 'Low':
      return 'text-orange-600 bg-orange-100'
    case 'Very Low':
      return 'text-red-600 bg-red-100'
    default:
      return 'text-gray-600 bg-gray-100'
  }
}

export const getSentimentColor = (sentiment: string): string => {
  switch (sentiment) {
    case 'positive':
      return 'text-green-600 bg-green-50 border-green-200'
    case 'negative':
      return 'text-red-600 bg-red-50 border-red-200'
    case 'neutral':
      return 'text-gray-600 bg-gray-50 border-gray-200'
    default:
      return 'text-gray-600 bg-gray-50 border-gray-200'
  }
}

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

export const formatPercentage = (value: number): string => {
  return `${Math.round(value * 100)}%`
}

export const downloadReport = (result: any, filename: string = 'pitchos-analysis-report.json') => {
  const dataStr = JSON.stringify(result, null, 2)
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)
  
  const exportFileDefaultName = filename
  
  const linkElement = document.createElement('a')
  linkElement.setAttribute('href', dataUri)
  linkElement.setAttribute('download', exportFileDefaultName)
  linkElement.click()
}

export default api
