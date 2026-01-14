import { useState, useEffect } from 'react'
import { listReports, deleteReport } from '../api/migration'
import './ReportHistory.css'

function ReportHistory({ onViewReport }) {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      setLoading(true)
      const data = await listReports()
      setReports(data.reports || [])
    } catch (err) {
      setError('Failed to load reports')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (reportId) => {
    if (!window.confirm('Are you sure you want to delete this report?')) {
      return
    }

    try {
      await deleteReport(reportId)
      setReports(reports.filter(r => r.id !== reportId))
    } catch (err) {
      setError('Failed to delete report')
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'Complete': return 'success'
      case 'Partially Complete': return 'warning'
      case 'Not Started': return 'error'
      default: return 'neutral'
    }
  }

  if (loading) {
    return (
      <div className="report-history">
        <div className="loading">Loading reports...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="report-history">
        <div className="error">{error}</div>
        <button onClick={fetchReports} className="retry-button">
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="report-history">
      <div className="history-header">
        <h2>Report History</h2>
        <button onClick={fetchReports} className="refresh-button">
          🔄 Refresh
        </button>
      </div>

      {reports.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <p>No reports yet. Upload and analyze some code to get started!</p>
        </div>
      ) : (
        <div className="reports-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Files</th>
                <th>Status</th>
                <th>Issues</th>
                <th>Risks</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((report) => (
                <tr key={report.id}>
                  <td>{formatDate(report.created_at)}</td>
                  <td>
                    <span className="files-count">
                      {report.total_files_analyzed} file(s)
                    </span>
                  </td>
                  <td>
                    <span className={`status-pill ${getStatusColor(report.migration_status)}`}>
                      {report.migration_status}
                    </span>
                  </td>
                  <td className="count">{report.issues_count}</td>
                  <td className="count">{report.risks_count}</td>
                  <td>
                    <div className="actions">
                      <button 
                        className="view-button"
                        onClick={() => onViewReport(report.id)}
                      >
                        View
                      </button>
                      <button 
                        className="delete-button"
                        onClick={() => handleDelete(report.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default ReportHistory
