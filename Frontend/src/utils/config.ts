// Configuration utilities for React frontend

interface Config {
  apiUrl: string
  appName: string
  appVersion: string
  environment: 'development' | 'production' | 'staging'
  features: {
    ocr: boolean
    analytics: boolean
    debug: boolean
  }
  analytics?: {
    gaTrackingId?: string
    hotjarId?: string
  }
}

const config: Config = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  appName: import.meta.env.VITE_APP_NAME || 'PitchOS',
  appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',
  environment: (import.meta.env.VITE_ENVIRONMENT as Config['environment']) || 'development',
  features: {
    ocr: import.meta.env.VITE_ENABLE_OCR === 'true',
    analytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
    debug: import.meta.env.VITE_ENABLE_DEBUG === 'true',
  },
  analytics: {
    gaTrackingId: import.meta.env.VITE_GA_TRACKING_ID,
    hotjarId: import.meta.env.VITE_HOTJAR_ID,
  },
}

export default config

// Utility functions
export const isDevelopment = () => config.environment === 'development'
export const isProduction = () => config.environment === 'production'
export const isStaging = () => config.environment === 'staging'

export const getApiUrl = (endpoint: string = '') => {
  const baseUrl = config.apiUrl.endsWith('/') ? config.apiUrl.slice(0, -1) : config.apiUrl
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  return `${baseUrl}${cleanEndpoint}`
}

export const logConfig = () => {
  if (config.features.debug) {
    console.group('🔧 PitchOS Configuration')
    console.log('Environment:', config.environment)
    console.log('API URL:', config.apiUrl)
    console.log('App Version:', config.appVersion)
    console.log('Features:', config.features)
    console.groupEnd()
  }
}

// Initialize config logging in development
if (isDevelopment()) {
  logConfig()
}
