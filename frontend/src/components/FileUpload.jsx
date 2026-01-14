import { useCallback, useRef } from 'react'
import './FileUpload.css'

function FileUpload({ onFileSelect, selectedFile }) {
  const fileInputRef = useRef(null)

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && isValidFile(file)) {
      onFileSelect(file)
    }
  }, [onFileSelect])

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      onFileSelect(file)
    }
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const isValidFile = (file) => {
    const validExtensions = ['.py', '.zip']
    return validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <div 
      className={`file-upload ${selectedFile ? 'has-file' : ''}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      {selectedFile ? (
        <div className="selected-file">
          <div className="file-icon">📄</div>
          <div className="file-info">
            <span className="file-name">{selectedFile.name}</span>
            <span className="file-size">{formatFileSize(selectedFile.size)}</span>
          </div>
          <button 
            className="remove-file"
            onClick={() => onFileSelect(null)}
          >
            ✕
          </button>
        </div>
      ) : (
        <div className="upload-prompt">
          <div className="upload-icon">📁</div>
          <p className="upload-text">
            Drag and drop a <strong>.py</strong> file or <strong>.zip</strong> archive
          </p>
          <p className="upload-or">or</p>
          <button type="button" className="browse-button" onClick={handleBrowseClick}>
            Browse Files
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept=".py,.zip"
            onChange={handleFileInput}
            style={{ display: 'none' }}
          />
        </div>
      )}
    </div>
  )
}

export default FileUpload
