import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { Image, Upload, X, CheckCircle, AlertCircle, Eye, Settings } from 'lucide-react'
import toast from 'react-hot-toast'
import { pitchAPI } from '../utils/api'
import { OCRResult } from '../types'
import LoadingSpinner from './LoadingSpinner'

interface OCRProcessorProps {
  onTextExtracted: (text: string, results: OCRResult[]) => void
}

const OCRProcessor: React.FC<OCRProcessorProps> = ({ onTextExtracted }) => {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [ocrResults, setOcrResults] = useState<OCRResult[]>([])
  const [showPreprocessing, setShowPreprocessing] = useState(false)
  const [aggressiveMode, setAggressiveMode] = useState(false)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'],
    },
    maxFiles: 10,
    onDrop: handleImageUpload,
  })

  async function handleImageUpload(acceptedFiles: File[]) {
    if (acceptedFiles.length === 0) return

    setUploadedFiles(acceptedFiles)
    setOcrResults([])
  }

  const processImages = async () => {
    if (uploadedFiles.length === 0) {
      toast.error('Please upload images first')
      return
    }

    setIsProcessing(true)

    try {
      const response = await pitchAPI.uploadImages(uploadedFiles)
      
      if (response.success && response.combined_text && response.results) {
        setOcrResults(response.results)
        onTextExtracted(response.combined_text, response.results)
        
        const successful = response.results.filter(r => r.is_valid).length
        const failed = response.results.length - successful
        
        if (failed === 0) {
          toast.success(`Successfully processed all ${response.results.length} images`)
        } else {
          toast.warning(`${successful}/${response.results.length} images processed successfully`)
        }
      } else {
        toast.error(response.error || 'Failed to process images')
      }
    } catch (error) {
      console.error('OCR processing error:', error)
      toast.error('Failed to process images')
    } finally {
      setIsProcessing(false)
    }
  }

  const removeFile = (index: number) => {
    setUploadedFiles(files => files.filter((_, i) => i !== index))
    if (ocrResults.length > 0) {
      setOcrResults(results => results.filter((_, i) => i !== index))
    }
  }

  const getMethodIcon = (method: string) => {
    switch (method) {
      case 'easyocr':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'google_vision':
        return <Eye className="w-4 h-4 text-blue-500" />
      case 'failed':
        return <AlertCircle className="w-4 h-4 text-red-500" />
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />
    }
  }

  const getMethodLabel = (method: string) => {
    switch (method) {
      case 'easyocr':
        return 'EasyOCR'
      case 'google_vision':
        return 'Google Vision'
      case 'failed':
        return 'Failed'
      default:
        return 'Unknown'
    }
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        <Image className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-lg font-medium text-gray-900 mb-2">
          {isDragActive ? 'Drop your images here' : 'Upload pitch deck images'}
        </p>
        <p className="text-gray-600">
          Supports PNG, JPG, JPEG, BMP, TIFF, WEBP (up to 10 files)
        </p>
      </div>

      {/* Processing Options */}
      {uploadedFiles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-50 rounded-lg p-4"
        >
          <h4 className="font-medium text-gray-900 mb-3 flex items-center">
            <Settings className="w-4 h-4 mr-2" />
            Processing Options
          </h4>
          <div className="flex items-center space-x-6">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={aggressiveMode}
                onChange={(e) => setAggressiveMode(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="ml-2 text-sm text-gray-700">
                Aggressive preprocessing (for difficult images)
              </span>
            </label>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={showPreprocessing}
                onChange={(e) => setShowPreprocessing(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="ml-2 text-sm text-gray-700">
                Show preprocessing steps
              </span>
            </label>
          </div>
        </motion.div>
      )}

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-4"
        >
          <h4 className="font-medium text-gray-900">
            Uploaded Files ({uploadedFiles.length})
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <Image className="w-4 h-4 text-gray-500" />
                    <span className="text-sm font-medium text-gray-900 truncate">
                      {file.name}
                    </span>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
                <div className="text-xs text-gray-500 mb-2">
                  {(file.size / 1024 / 1024).toFixed(1)} MB
                </div>
                
                {/* OCR Result for this file */}
                {ocrResults[index] && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        {getMethodIcon(ocrResults[index].method)}
                        <span className="text-xs font-medium">
                          {getMethodLabel(ocrResults[index].method)}
                        </span>
                      </div>
                      {ocrResults[index].confidence > 0 && (
                        <span className="text-xs text-gray-500">
                          {Math.round(ocrResults[index].confidence * 100)}% confidence
                        </span>
                      )}
                    </div>
                    
                    {ocrResults[index].is_valid ? (
                      <div className="text-xs text-green-600">
                        ✅ {ocrResults[index].text.length} characters extracted
                      </div>
                    ) : (
                      <div className="text-xs text-red-600">
                        ❌ No valid text extracted
                      </div>
                    )}
                    
                    {ocrResults[index].issues.length > 0 && (
                      <div className="mt-2">
                        {ocrResults[index].issues.map((issue, issueIndex) => (
                          <div key={issueIndex} className="text-xs text-yellow-600">
                            ⚠️ {issue}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Process Button */}
          <div className="flex justify-center">
            <button
              onClick={processImages}
              disabled={isProcessing}
              className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? (
                <div className="flex items-center space-x-2">
                  <LoadingSpinner size="small" />
                  <span>Processing Images...</span>
                </div>
              ) : (
                <>🔍 Extract Text from Images</>
              )}
            </button>
          </div>
        </motion.div>
      )}

      {/* OCR Results Summary */}
      {ocrResults.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white border border-gray-200 rounded-lg p-6"
        >
          <h4 className="font-medium text-gray-900 mb-4">OCR Processing Summary</h4>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{ocrResults.length}</div>
              <div className="text-sm text-gray-600">Total Images</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {ocrResults.filter(r => r.is_valid).length}
              </div>
              <div className="text-sm text-gray-600">Successful</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {ocrResults.filter(r => r.method === 'easyocr' && r.is_valid).length}
              </div>
              <div className="text-sm text-gray-600">EasyOCR</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {ocrResults.filter(r => r.method === 'google_vision' && r.is_valid).length}
              </div>
              <div className="text-sm text-gray-600">Google Vision</div>
            </div>
          </div>

          {/* Success Rate */}
          <div className="mb-4">
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Success Rate</span>
              <span>
                {Math.round((ocrResults.filter(r => r.is_valid).length / ocrResults.length) * 100)}%
              </span>
            </div>
            <div className="progress-bar">
              <div 
                className="progress-fill bg-green-500"
                style={{ 
                  width: `${(ocrResults.filter(r => r.is_valid).length / ocrResults.length) * 100}%` 
                }}
              />
            </div>
          </div>

          {/* Recommendations */}
          {ocrResults.some(r => !r.is_valid) && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h5 className="font-medium text-yellow-800 mb-2">💡 Recommendations</h5>
              <ul className="text-sm text-yellow-700 space-y-1">
                <li>• Ensure images are well-lit and in focus</li>
                <li>• Use high-resolution images (at least 1080p)</li>
                <li>• Avoid shadows or glare on the slides</li>
                <li>• Take photos straight-on, not at an angle</li>
              </ul>
            </div>
          )}
        </motion.div>
      )}
    </div>
  )
}

export default OCRProcessor
