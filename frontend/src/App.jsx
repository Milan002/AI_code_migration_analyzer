import { useState, useEffect } from 'react'
import Header from './components/Header'
import FileUpload from './components/FileUpload'
import MigrationConfig from './components/MigrationConfig'
import AnalysisResults from './components/AnalysisResults'
import ReportHistory from './components/ReportHistory'
import AuthPage from './components/Auth/AuthPage'
import { analyzeCode, getReport } from './api/migration'
import { isAuthenticated, logoutUser, getCurrentUser } from './api/auth'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(isAuthenticated())
  const [user, setUser] = useState(null)
  const [file, setFile] = useState(null)
  const [config, setConfig] = useState({
    sourceVersion: 'Python 2',
    targetVersion: 'Python 3'
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [report, setReport] = useState(null)
  const [activeTab, setActiveTab] = useState('analyze')

  // Fetch user info on auth
  useEffect(() => {
    if (isLoggedIn) {
      getCurrentUser()
        .then(setUser)
        .catch(() => {
          // Token expired or invalid
          handleLogout()
        })
    }
  }, [isLoggedIn])

  const handleAuthSuccess = () => {
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    logoutUser()
    setIsLoggedIn(false)
    setUser(null)
    setReport(null)
    setFile(null)
  }

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile)
    setError(null)
    setReport(null)
  }

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a file to analyze')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await analyzeCode(file, config)
      const fullReport = await getReport(response.report_id)
      setReport(fullReport)
    } catch (err) {
      if (err.message === 'Session expired' || err.message.includes('401')) {
        handleLogout()
        return
      }
      setError(err.message || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleViewReport = async (reportId) => {
    setLoading(true)
    try {
      const fullReport = await getReport(reportId)
      setReport(fullReport)
      setActiveTab('analyze')
    } catch (err) {
      if (err.message === 'Session expired') {
        handleLogout()
        return
      }
      setError('Failed to load report')
    } finally {
      setLoading(false)
    }
  }

  // Show auth page if not logged in
  if (!isLoggedIn) {
    return <AuthPage onAuthSuccess={handleAuthSuccess} />
  }

  return (
    <div className="app">
      <Header user={user} onLogout={handleLogout} />
      
      <nav className="tabs">
        <button 
          className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
          onClick={() => setActiveTab('analyze')}
        >
          Analyze Code
        </button>
        <button 
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          Report History
        </button>
      </nav>

      <main className="main-content">
        {activeTab === 'analyze' ? (
          <>
            <div className="analysis-panel">
              <div className="upload-section">
                <h2>Upload Python Code</h2>
                <FileUpload onFileSelect={handleFileSelect} selectedFile={file} />
              </div>

              <div className="config-section">
                <h2>Migration Configuration</h2>
                <MigrationConfig config={config} onChange={setConfig} />
              </div>

              <button 
                className={`analyze-button ${loading ? 'loading' : ''}`}
                onClick={handleAnalyze}
                disabled={loading || !file}
              >
                {loading ? 'Analyzing...' : 'Analyze Code'}
              </button>

              {error && <div className="error-message">{error}</div>}
            </div>

            {report && <AnalysisResults report={report} />}
          </>
        ) : (
          <ReportHistory onViewReport={handleViewReport} />
        )}
      </main>

      <footer className="footer">
        <p>AI Code Migration Analyzer v1.0</p>
      </footer>
    </div>
  )
}

export default App
