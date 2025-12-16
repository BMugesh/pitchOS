import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { FileText, Image, Type, Upload, X, CheckCircle, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import { pitchAPI } from '../utils/api'
import { AnalysisResult, InputMethod, AnalysisMode } from '../types'
import LoadingSpinner from './LoadingSpinner'

interface PitchInputProps {
  mode: AnalysisMode
  onAnalysisStart: () => void
  onAnalysisComplete: (result: AnalysisResult) => void
  onAnalysisError: () => void
}

const PitchInput: React.FC<PitchInputProps> = ({
  mode,
  onAnalysisStart,
  onAnalysisComplete,
  onAnalysisError,
}) => {
  const [inputMethod, setInputMethod] = useState<InputMethod>('text')
  const [pitchContent, setPitchContent] = useState('')
  const [isProcessingFiles, setIsProcessingFiles] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([])

  // File upload for documents
  const {
    getRootProps: getDocRootProps,
    getInputProps: getDocInputProps,
    isDragActive: isDocDragActive,
  } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
    onDrop: handleDocumentUpload,
  })

  // Image upload for OCR
  const {
    getRootProps: getImageRootProps,
    getInputProps: getImageInputProps,
    isDragActive: isImageDragActive,
  } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'],
    },
    maxFiles: 10,
    onDrop: handleImageUpload,
  })

  async function handleDocumentUpload(acceptedFiles: File[]) {
    if (acceptedFiles.length === 0) return

    setIsProcessingFiles(true)
    const file = acceptedFiles[0]

    try {
      const response = await pitchAPI.uploadFile(file)
      
      if (response.success && response.content) {
        setPitchContent(response.content)
        toast.success(`Successfully extracted text from ${response.filename}`)
      } else {
        toast.error(response.error || 'Failed to process file')
      }
    } catch (error) {
      console.error('File upload error:', error)
      toast.error('Failed to upload file')
    } finally {
      setIsProcessingFiles(false)
    }
  }

  async function handleImageUpload(acceptedFiles: File[]) {
    if (acceptedFiles.length === 0) return

    setIsProcessingFiles(true)
    setUploadedFiles(acceptedFiles)

    try {
      const response = await pitchAPI.uploadImages(acceptedFiles)
      
      if (response.success && response.combined_text) {
        setPitchContent(response.combined_text)
        toast.success(`Successfully extracted text from ${acceptedFiles.length} images`)
        
        // Show OCR results summary
        if (response.results) {
          const successful = response.results.filter(r => r.is_valid).length
          const failed = response.results.length - successful
          
          if (failed > 0) {
            toast.warning(`${successful}/${response.results.length} images processed successfully`)
          }
        }
      } else {
        toast.error(response.error || 'Failed to process images')
      }
    } catch (error) {
      console.error('Image upload error:', error)
      toast.error('Failed to upload images')
    } finally {
      setIsProcessingFiles(false)
    }
  }

  const handleAnalyze = async () => {
    if (!pitchContent.trim()) {
      toast.error('Please enter your pitch content')
      return
    }

    onAnalysisStart()

    try {
      const sourceType = inputMethod === 'image' ? 'ocr' : inputMethod === 'file' ? 'file' : 'text'
      
      const response = await pitchAPI.analyzePitch({
        content: pitchContent,
        mode,
        source_type: sourceType,
      })

      if (response.success && response.data) {
        onAnalysisComplete(response.data)
        toast.success('Analysis complete!')
      } else {
        throw new Error(response.error || 'Analysis failed')
      }
    } catch (error) {
      console.error('Analysis error:', error)
      toast.error('Analysis failed. Please try again.')
      onAnalysisError()
    }
  }

  const removeFile = (index: number) => {
    setUploadedFiles(files => files.filter((_, i) => i !== index))
  }

  const inputMethods = [
    { id: 'text', label: 'Text Input', icon: Type, description: 'Paste your pitch content directly' },
    { id: 'file', label: 'File Upload', icon: FileText, description: 'Upload PDF, DOC, or TXT files' },
    { id: 'image', label: 'Image OCR', icon: Image, description: 'Upload pitch deck images' },
  ]

  return (
    <div className="w-full max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="card bg-base-100 shadow-lg"
      >
        <h2 className="text-2xl font-bold text-base-content mb-6">Submit Your Pitch</h2>

        {/* Input Method Selector */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {inputMethods.map((method) => (
            <button
              key={method.id}
              onClick={() => setInputMethod(method.id as InputMethod)}
              className={`card card-compact transition-all duration-200 text-left hover:shadow-md ${
                inputMethod === method.id
                  ? 'border-2 border-primary bg-primary/10'
                  : 'border border-base-300 hover:border-base-400'
              }`}
            >
              <div className="card-body">
                <div className="flex items-center space-x-3 mb-2">
                  <method.icon className={`w-5 h-5 ${
                    inputMethod === method.id ? 'text-primary' : 'text-base-content/60'
                  }`} />
                  <span className={`font-medium ${
                    inputMethod === method.id ? 'text-primary' : 'text-base-content'
                  }`}>
                    {method.label}
                  </span>
                </div>
                <p className="text-sm text-base-content/70">{method.description}</p>
              </div>
            </button>
          ))}
        </div>

        {/* Input Content */}
        <div className="space-y-6">
          {inputMethod === 'text' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
            >
              <label className="block text-sm font-medium text-base-content mb-2">
                Pitch Content
              </label>
              <textarea
                value={pitchContent}
                onChange={(e) => setPitchContent(e.target.value)}
                placeholder="Describe your startup: problem, solution, market, traction, team, business model, financials, competition, vision..."
                className="textarea textarea-bordered w-full h-80 text-base leading-relaxed"
              />
              <p className="text-sm text-base-content/70 mt-2">
                {pitchContent.length} characters
              </p>
            </motion.div>
          )}

          {inputMethod === 'file' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
              className="w-full"
            >
              <label className="block text-sm font-medium text-base-content mb-2">
                Upload Document
              </label>
              <div
                {...getDocRootProps()}
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-300 w-full min-h-[200px] flex flex-col items-center justify-center ${
                  isDocDragActive
                    ? 'border-primary bg-primary/10 scale-105'
                    : 'border-base-300 hover:border-primary hover:bg-base-200'
                }`}
              >
                <input {...getDocInputProps()} />
                <Upload className={`w-16 h-16 mx-auto mb-4 ${isDocDragActive ? 'text-primary' : 'text-base-content/40'}`} />
                <p className={`text-xl font-medium mb-2 ${isDocDragActive ? 'text-primary' : 'text-base-content'}`}>
                  {isDocDragActive ? 'Drop your file here' : 'Upload your pitch deck'}
                </p>
                <p className="text-base-content/70 text-base">
                  Supports PDF, DOC, DOCX, and TXT files
                </p>
              </div>
              
              {pitchContent && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-base-content mb-2">
                    Extracted Content
                  </label>
                  <textarea
                    value={pitchContent}
                    onChange={(e) => setPitchContent(e.target.value)}
                    className="textarea textarea-bordered w-full h-40 text-base leading-relaxed"
                    placeholder="Extracted content will appear here..."
                  />
                </div>
              )}
            </motion.div>
          )}

          {inputMethod === 'image' && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3 }}
              className="w-full"
            >
              <label className="block text-sm font-medium text-base-content mb-2">
                Upload Images
              </label>
              <div
                {...getImageRootProps()}
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-300 w-full min-h-[200px] flex flex-col items-center justify-center ${
                  isImageDragActive
                    ? 'border-primary bg-primary/10 scale-105'
                    : 'border-base-300 hover:border-primary hover:bg-base-200'
                }`}
              >
                <input {...getImageInputProps()} />
                <Image className={`w-16 h-16 mx-auto mb-4 ${isImageDragActive ? 'text-primary' : 'text-base-content/40'}`} />
                <p className={`text-xl font-medium mb-2 ${isImageDragActive ? 'text-primary' : 'text-base-content'}`}>
                  {isImageDragActive ? 'Drop your images here' : 'Upload pitch deck images'}
                </p>
                <p className="text-base-content/70 text-base">
                  Supports PNG, JPG, JPEG, BMP, TIFF, WEBP (up to 10 files)
                </p>
              </div>

              {/* Uploaded Files */}
              {uploadedFiles.length > 0 && (
                <div className="mt-6">
                  <h4 className="text-sm font-medium text-base-content mb-3">
                    Uploaded Files ({uploadedFiles.length})
                  </h4>
                  <div className="space-y-3">
                    {uploadedFiles.map((file, index) => (
                      <div key={index} className="flex items-center justify-between bg-base-200 p-4 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <Image className="w-5 h-5 text-base-content/60" />
                          <span className="text-sm text-base-content font-medium">{file.name}</span>
                          <span className="text-xs text-base-content/70">
                            ({(file.size / 1024 / 1024).toFixed(1)} MB)
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={() => removeFile(index)}
                          className="btn btn-ghost btn-sm text-error hover:bg-error/10"
                          title="Remove file"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {pitchContent && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-base-content mb-2">
                    Extracted Text
                  </label>
                  <textarea
                    value={pitchContent}
                    onChange={(e) => setPitchContent(e.target.value)}
                    className="textarea textarea-bordered w-full h-40 text-base leading-relaxed"
                    placeholder="Extracted text from images will appear here..."
                  />
                </div>
              )}
            </motion.div>
          )}

          {/* Processing State */}
          {isProcessingFiles && (
            <div className="flex items-center justify-center py-8">
              <LoadingSpinner size="medium" text="Processing files..." />
            </div>
          )}

          {/* Analyze Button */}
          <div className="flex justify-center pt-6">
            <button
              type="button"
              onClick={handleAnalyze}
              disabled={!pitchContent.trim() || isProcessingFiles}
              className="btn btn-primary btn-lg px-8"
            >
              🚀 Analyze My Pitch
            </button>
          </div>
        </div>
      </motion.div>

      {/* Example Pitch */}
      {!pitchContent && inputMethod === 'text' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-8 card bg-base-100 shadow-lg"
        >
          <div className="card-body">
            <h3 className="card-title text-base-content mb-4">📝 Example Pitch</h3>
            <div className="bg-base-200 p-6 rounded-lg text-sm text-base-content leading-relaxed space-y-2">
              <p><strong>Problem:</strong> Small businesses lose 30% revenue from poor inventory management</p>
              <p><strong>Solution:</strong> InventoryAI - AI-powered inventory optimization platform</p>
              <p><strong>Market:</strong> $3.2B global inventory management software market, growing 15% annually</p>
              <p><strong>Traction:</strong> 150 paying customers, $50K MRR, 25% month-over-month growth</p>
              <p><strong>Business Model:</strong> SaaS subscription $99-999/month per location</p>
              <p><strong>Team:</strong> CEO (10 years retail), CTO (ex-Amazon), Shopify advisor</p>
              <p><strong>Financials:</strong> Seeking $2M Series A, $200 CAC, $2400 LTV</p>
              <p><strong>Competition:</strong> Traditional solutions lack AI, we're 10x more accurate</p>
              <p><strong>Vision:</strong> Operating system for small business inventory globally</p>
            </div>
            <div className="card-actions justify-end mt-4">
              <button
                type="button"
                onClick={() => setPitchContent(`Problem: Small businesses lose 30% revenue from poor inventory management

Solution: InventoryAI - AI-powered inventory optimization platform

Market: $3.2B global inventory management software market, growing 15% annually

Traction: 150 paying customers, $50K MRR, 25% month-over-month growth

Business Model: SaaS subscription $99-999/month per location

Team: CEO (10 years retail), CTO (ex-Amazon), Shopify advisor

Financials: Seeking $2M Series A, $200 CAC, $2400 LTV

Competition: Traditional solutions lack AI, we're 10x more accurate

Vision: Operating system for small business inventory globally`)}
                className="btn btn-secondary"
              >
                Use Example Pitch
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default PitchInput
