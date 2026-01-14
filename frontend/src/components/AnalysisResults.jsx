import './AnalysisResults.css'

function AnalysisResults({ report }) {
  const getSeverityClass = (severity) => {
    return `severity-${severity}`
  }

  const getStatusBadge = () => {
    if (report.is_valid_python3) {
      return { class: 'success', text: '✅ Valid Python 3' }
    }
    const issueCount = report.issues?.length || 0
    if (issueCount === 0) {
      return { class: 'success', text: 'No Issues Found' }
    }
    if (issueCount <= 3) {
      return { class: 'warning', text: 'Minor Issues Found' }
    }
    return { class: 'error', text: 'Issues Found' }
  }

  const status = getStatusBadge()

  return (
    <div className="analysis-results">
      {/* Summary Section */}
      <div className="results-header">
        <div className={`status-badge ${status.class}`}>
          {status.text}
        </div>
        <div className="stats">
          <div className="stat">
            <span className="stat-value">{report.files_analyzed?.length || 0}</span>
            <span className="stat-label">Files Analyzed</span>
          </div>
          <div className="stat">
            <span className="stat-value">{report.issues?.length || 0}</span>
            <span className="stat-label">Issues Found</span>
          </div>
          <div className="stat">
            <span className="stat-value">
              {report.issues?.filter(i => i.severity === 'high').length || 0}
            </span>
            <span className="stat-label">High Severity</span>
          </div>
        </div>
      </div>

      {/* Summary Text */}
      <div className="summary-section">
        <h3>Summary</h3>
        <p>{report.summary || 'Analysis complete.'}</p>
      </div>

      {/* Issues Section */}
      {report.issues && report.issues.length > 0 && (
        <div className="issues-section">
          <h3>Detected Issues</h3>
          <div className="issues-list">
            {report.issues.map((issue, index) => (
              <div key={index} className={`issue-card ${getSeverityClass(issue.severity)}`}>
                <div className="issue-header">
                  <span className="issue-type">Issue #{index + 1}</span>
                  <span className={`issue-severity ${issue.severity}`}>{issue.severity}</span>
                </div>
                <div className="issue-description">{issue.issue}</div>
                {issue.line_hint && (
                  <div className="issue-code">
                    <code>{issue.line_hint}</code>
                  </div>
                )}
                {issue.fix && (
                  <div className="issue-fix">
                    💡 <strong>Fix:</strong> {issue.fix}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Issues Message */}
      {(!report.issues || report.issues.length === 0) && (
        <div className="no-issues">
          <div className="no-issues-icon">🎉</div>
          <p>No compatibility issues found! Your code appears to be Python 3 compatible.</p>
        </div>
      )}

      {/* Files Analyzed */}
      {report.files_analyzed && report.files_analyzed.length > 0 && (
        <div className="files-section">
          <h3>Files Analyzed</h3>
          <div className="files-list">
            {report.files_analyzed.map((file, index) => (
              <span key={index} className="file-tag">📄 {file}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default AnalysisResults
