import './MigrationConfig.css'

function MigrationConfig({ config, onChange }) {
  return (
    <div className="migration-config">
      <div className="config-flow">
        <div className="version-box source">
          <label>Source Version</label>
          <select 
            value={config.sourceVersion}
            onChange={(e) => onChange({ ...config, sourceVersion: e.target.value })}
          >
            <option value="Python 2">Python 2</option>
          </select>
        </div>

        <div className="arrow">→</div>

        <div className="version-box target">
          <label>Target Version</label>
          <select 
            value={config.targetVersion}
            onChange={(e) => onChange({ ...config, targetVersion: e.target.value })}
          >
            <option value="Python 3">Python 3</option>
          </select>
        </div>
      </div>

      <p className="config-hint">
        This tool analyzes Python 3 code to detect any remaining Python 2 patterns
      </p>
    </div>
  )
}

export default MigrationConfig
