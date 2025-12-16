import React from 'react'
import { motion } from 'framer-motion'

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large'
  text?: string
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  text
}) => {
  const sizeClasses = {
    small: 'loading-sm',
    medium: 'loading-md',
    large: 'loading-lg'
  }

  const textSizeClasses = {
    small: 'text-sm',
    medium: 'text-base',
    large: 'text-lg'
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <span className={`loading loading-spinner loading-primary ${sizeClasses[size]}`}></span>
      {text && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className={`mt-2 text-base-content/70 ${textSizeClasses[size]}`}
        >
          {text}
        </motion.p>
      )}
    </div>
  )
}

export default LoadingSpinner
