import { getAuthHeaders } from './auth';

const API_BASE_URL = '/api/migration'

/**
 * Analyze uploaded Python code for migration readiness.
 * @param {File} file - The file to analyze (.py or .zip)
 * @param {Object} config - Migration configuration
 * @returns {Promise<Object>} Analysis response with report_id
 */
export async function analyzeCode(file, config) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('source_version', config.sourceVersion)
  formData.append('target_version', config.targetVersion)

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: {
      ...getAuthHeaders(),
    },
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Analysis failed')
  }

  return response.json()
}

/**
 * Get a migration report by ID.
 * @param {string} reportId - The report ID
 * @returns {Promise<Object>} The full migration report
 */
export async function getReport(reportId) {
  const response = await fetch(`${API_BASE_URL}/report/${reportId}`, {
    headers: {
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to fetch report')
  }

  return response.json()
}

/**
 * List recent migration reports.
 * @param {number} limit - Maximum reports to return
 * @param {number} skip - Number of reports to skip
 * @returns {Promise<Object>} List of reports
 */
export async function listReports(limit = 10, skip = 0) {
  const response = await fetch(`${API_BASE_URL}/reports?limit=${limit}&skip=${skip}`, {
    headers: {
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to fetch reports')
  }

  return response.json()
}

/**
 * Delete a migration report.
 * @param {string} reportId - The report ID to delete
 * @returns {Promise<Object>} Deletion confirmation
 */
export async function deleteReport(reportId) {
  const response = await fetch(`${API_BASE_URL}/report/${reportId}`, {
    method: 'DELETE',
    headers: {
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to delete report')
  }

  return response.json()
}
