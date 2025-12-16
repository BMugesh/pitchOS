import { useState, useEffect } from 'react'

interface BreakpointConfig {
  mobile: number
  tablet: number
  desktop: number
}

const defaultBreakpoints: BreakpointConfig = {
  mobile: 768,
  tablet: 1024,
  desktop: 1280,
}

export type ScreenSize = 'mobile' | 'tablet' | 'desktop' | 'wide'

export const useResponsive = (breakpoints: BreakpointConfig = defaultBreakpoints) => {
  const [screenSize, setScreenSize] = useState<ScreenSize>('desktop')
  const [windowSize, setWindowSize] = useState({
    width: typeof window !== 'undefined' ? window.innerWidth : 1024,
    height: typeof window !== 'undefined' ? window.innerHeight : 768,
  })

  useEffect(() => {
    const handleResize = () => {
      const width = window.innerWidth
      const height = window.innerHeight

      setWindowSize({ width, height })

      if (width < breakpoints.mobile) {
        setScreenSize('mobile')
      } else if (width < breakpoints.tablet) {
        setScreenSize('tablet')
      } else if (width < breakpoints.desktop) {
        setScreenSize('desktop')
      } else {
        setScreenSize('wide')
      }
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [breakpoints])

  const isMobile = screenSize === 'mobile'
  const isTablet = screenSize === 'tablet'
  const isDesktop = screenSize === 'desktop' || screenSize === 'wide'
  const isMobileOrTablet = isMobile || isTablet

  return {
    screenSize,
    windowSize,
    isMobile,
    isTablet,
    isDesktop,
    isMobileOrTablet,
    breakpoints,
  }
}

export const useMediaQuery = (query: string): boolean => {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    if (media.matches !== matches) {
      setMatches(media.matches)
    }

    const listener = () => setMatches(media.matches)
    media.addEventListener('change', listener)
    return () => media.removeEventListener('change', listener)
  }, [matches, query])

  return matches
}

// Predefined media queries
export const useBreakpoints = () => {
  const isMobile = useMediaQuery('(max-width: 767px)')
  const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1023px)')
  const isDesktop = useMediaQuery('(min-width: 1024px)')
  const isWide = useMediaQuery('(min-width: 1280px)')

  return {
    isMobile,
    isTablet,
    isDesktop,
    isWide,
    isMobileOrTablet: isMobile || isTablet,
  }
}
