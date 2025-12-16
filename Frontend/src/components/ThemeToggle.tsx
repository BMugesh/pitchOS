import React, { useState, useEffect } from 'react'
import { Palette } from 'lucide-react'

const ThemeToggle: React.FC = () => {
  const [theme, setTheme] = useState('pitchos')

  const themes = [
    { name: 'pitchos', label: 'PitchOS', icon: '🚀' },
    { name: 'light', label: 'Light', icon: '☀️' },
    { name: 'dark', label: 'Dark', icon: '🌙' },
    { name: 'cupcake', label: 'Cupcake', icon: '🧁' },
    { name: 'corporate', label: 'Corporate', icon: '🏢' },
    { name: 'synthwave', label: 'Synthwave', icon: '🌆' },
    { name: 'cyberpunk', label: 'Cyberpunk', icon: '🤖' },
    { name: 'valentine', label: 'Valentine', icon: '💝' },
  ]

  useEffect(() => {
    // Get saved theme from localStorage or default to 'pitchos'
    const savedTheme = localStorage.getItem('pitchos-theme') || 'pitchos'
    setTheme(savedTheme)
    document.documentElement.setAttribute('data-theme', savedTheme)
  }, [])

  const handleThemeChange = (newTheme: string) => {
    setTheme(newTheme)
    localStorage.setItem('pitchos-theme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  return (
    <div className="dropdown dropdown-end">
      <div
        tabIndex={0}
        role="button"
        className="btn btn-ghost btn-circle tooltip tooltip-bottom"
        data-tip="Change Theme"
        title="Change Theme"
        aria-label="Change Theme"
      >
        <Palette className="w-5 h-5" />
      </div>
      <ul
        tabIndex={0}
        className="dropdown-content menu bg-base-100 rounded-box z-[1000] w-56 p-2 shadow-xl border border-base-300 mt-2"
      >
        <li className="menu-title">
          <span>Choose Theme</span>
        </li>
        {themes.map((themeOption) => (
          <li key={themeOption.name}>
            <button
              type="button"
              onClick={() => handleThemeChange(themeOption.name)}
              className={`flex items-center gap-3 ${
                theme === themeOption.name ? 'active bg-primary text-primary-content' : ''
              }`}
            >
              <span className="text-lg">{themeOption.icon}</span>
              <span className="flex-1">{themeOption.label}</span>
              {theme === themeOption.name && (
                <span className="badge badge-sm">✓</span>
              )}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default ThemeToggle
