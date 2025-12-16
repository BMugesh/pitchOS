import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface UIState {
  // Theme
  theme: 'light' | 'dark' | 'auto'
  
  // Layout
  sidebarOpen: boolean
  mobileMenuOpen: boolean
  
  // Modals
  modals: {
    settings: boolean
    help: boolean
    history: boolean
    export: boolean
  }
  
  // Notifications
  notifications: Array<{
    id: string
    type: 'success' | 'error' | 'warning' | 'info'
    title: string
    message: string
    timestamp: Date
    read: boolean
  }>
  
  // User preferences
  preferences: {
    autoSave: boolean
    showTips: boolean
    animationsEnabled: boolean
    compactMode: boolean
    defaultMode: 'beginner' | 'expert'
  }
  
  // Actions
  setTheme: (theme: 'light' | 'dark' | 'auto') => void
  setSidebarOpen: (open: boolean) => void
  setMobileMenuOpen: (open: boolean) => void
  openModal: (modal: keyof UIState['modals']) => void
  closeModal: (modal: keyof UIState['modals']) => void
  closeAllModals: () => void
  addNotification: (notification: Omit<UIState['notifications'][0], 'id' | 'timestamp' | 'read'>) => void
  markNotificationRead: (id: string) => void
  clearNotifications: () => void
  updatePreferences: (preferences: Partial<UIState['preferences']>) => void
  reset: () => void
}

export const useUIStore = create<UIState>()(
  persist(
    (set, get) => ({
      // Initial state
      theme: 'auto',
      sidebarOpen: true,
      mobileMenuOpen: false,
      modals: {
        settings: false,
        help: false,
        history: false,
        export: false,
      },
      notifications: [],
      preferences: {
        autoSave: true,
        showTips: true,
        animationsEnabled: true,
        compactMode: false,
        defaultMode: 'expert',
      },

      // Actions
      setTheme: (theme) => set({ theme }),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      setMobileMenuOpen: (open) => set({ mobileMenuOpen: open }),
      
      openModal: (modal) => set((state) => ({
        modals: { ...state.modals, [modal]: true }
      })),
      
      closeModal: (modal) => set((state) => ({
        modals: { ...state.modals, [modal]: false }
      })),
      
      closeAllModals: () => set({
        modals: {
          settings: false,
          help: false,
          history: false,
          export: false,
        }
      }),
      
      addNotification: (notification) => {
        const newNotification = {
          ...notification,
          id: Date.now().toString(),
          timestamp: new Date(),
          read: false,
        }
        
        set((state) => ({
          notifications: [newNotification, ...state.notifications].slice(0, 50) // Keep last 50
        }))
      },
      
      markNotificationRead: (id) => set((state) => ({
        notifications: state.notifications.map(n => 
          n.id === id ? { ...n, read: true } : n
        )
      })),
      
      clearNotifications: () => set({ notifications: [] }),
      
      updatePreferences: (newPreferences) => set((state) => ({
        preferences: { ...state.preferences, ...newPreferences }
      })),
      
      reset: () => set({
        sidebarOpen: true,
        mobileMenuOpen: false,
        modals: {
          settings: false,
          help: false,
          history: false,
          export: false,
        },
        notifications: [],
      }),
    }),
    {
      name: 'pitchos-ui-store',
      partialize: (state) => ({
        theme: state.theme,
        preferences: state.preferences,
        notifications: state.notifications.filter(n => !n.read), // Only persist unread notifications
      }),
    }
  )
)

// Selectors for better performance
export const useTheme = () => useUIStore((state) => state.theme)
export const usePreferences = () => useUIStore((state) => state.preferences)
export const useNotifications = () => useUIStore((state) => state.notifications)
export const useModals = () => useUIStore((state) => state.modals)
