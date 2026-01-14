import './Header.css'

function Header({ user, onLogout }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <div className="logo">
            <span className="logo-icon">🔍</span>
            <h1>AI Code Migration Readiness Analyzer</h1>
          </div>
          <p className="tagline">
            Verify Python 2 → Python 3 migration completeness
          </p>
        </div>
        {user && (
          <div className="header-right">
            <span className="user-info">
              <span className="user-icon">👤</span>
              {user.username || user.email}
            </span>
            <button className="logout-btn" onClick={onLogout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  )
}

export default Header
