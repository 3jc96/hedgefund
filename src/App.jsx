import { useState, useEffect } from 'react'
import './App.css'

// Data Input Form Component
function DataInputForm({ currentData, onSubmit, onCancel }) {
  const [formData, setFormData] = useState(currentData)

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit(formData)
  }

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(value) || 0 }))
  }

  return (
    <form onSubmit={handleSubmit} className="data-input-form">
      <div className="form-row">
        <div className="form-group">
          <label>YTD Return (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.ytdReturn}
            onChange={(e) => handleChange('ytdReturn', e.target.value)}
            placeholder="12.4"
          />
        </div>
        <div className="form-group">
          <label>Annualized Return (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.annualizedReturn}
            onChange={(e) => handleChange('annualizedReturn', e.target.value)}
            placeholder="15.7"
          />
        </div>
        <div className="form-group">
          <label>Since Inception (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.inceptionReturn}
            onChange={(e) => handleChange('inceptionReturn', e.target.value)}
            placeholder="142"
          />
        </div>
      </div>
      
      <div className="form-row">
        <div className="form-group">
          <label>Sharpe Ratio</label>
          <input
            type="number"
            step="0.01"
            value={formData.sharpeRatio}
            onChange={(e) => handleChange('sharpeRatio', e.target.value)}
            placeholder="1.85"
          />
        </div>
        <div className="form-group">
          <label>Max Drawdown (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.maxDrawdown}
            onChange={(e) => handleChange('maxDrawdown', e.target.value)}
            placeholder="-4.2"
          />
        </div>
        <div className="form-group">
          <label>Volatility (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.volatility}
            onChange={(e) => handleChange('volatility', e.target.value)}
            placeholder="8.5"
          />
        </div>
      </div>
      
      <div className="form-row">
        <div className="form-group">
          <label>Number of Positions</label>
          <input
            type="number"
            value={formData.positions}
            onChange={(e) => handleChange('positions', e.target.value)}
            placeholder="85"
          />
        </div>
        <div className="form-group">
          <label>Net Exposure (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.netExposure}
            onChange={(e) => handleChange('netExposure', e.target.value)}
            placeholder="0"
          />
        </div>
        <div className="form-group">
          <label>Gross Exposure (%)</label>
          <input
            type="number"
            step="0.1"
            value={formData.grossExposure}
            onChange={(e) => handleChange('grossExposure', e.target.value)}
            placeholder="180"
          />
        </div>
      </div>
      
      <div className="form-actions">
        <button type="button" onClick={onCancel} className="cancel-btn">
          Cancel
        </button>
        <button type="submit" className="submit-btn">
          Update Data
        </button>
      </div>
    </form>
  )
}

function App() {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [isLoading, setIsLoading] = useState(true)
  const [performanceData, setPerformanceData] = useState({
    ytdReturn: 12.4,
    annualizedReturn: 15.7,
    inceptionReturn: 142,
    sharpeRatio: 1.85,
    maxDrawdown: -4.2,
    volatility: 8.5,
    positions: 85,
    netExposure: 0,
    grossExposure: 180,
    lastUpdated: new Date().toLocaleDateString()
  })
  const [showDataInput, setShowDataInput] = useState(false)

  useEffect(() => {
    // Update time every second
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)

    // Simulate loading
    const loadingTimer = setTimeout(() => {
      setIsLoading(false)
    }, 1500)

    return () => {
      clearInterval(timer)
      clearTimeout(loadingTimer)
    }
  }, [])

  const handleDataUpdate = (newData) => {
    setPerformanceData({ ...performanceData, ...newData, lastUpdated: new Date().toLocaleDateString() })
    setShowDataInput(false)
  }

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading Quantum Capital...</p>
      </div>
    )
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <nav className="navbar">
          <div className="logo">
            <span className="logo-icon">⚡</span>
            <span className="logo-text">Quantum Capital</span>
          </div>
          <div className="nav-links">
            <a href="#about">About</a>
            <a href="#strategy">Strategy</a>
            <a href="#team">Team</a>
            <a href="#performance">Performance</a>
            <a href="#contact">Contact</a>
          </div>
        </nav>
        
        <div className="hero">
          <div className="hero-content">
            <h1>Quantum Capital</h1>
            <p className="hero-subtitle">Systematic Delta-Neutral Trading</p>
            <p className="hero-description">
              A Singapore-based hedge fund leveraging advanced quantitative strategies 
              and systematic approaches to deliver consistent alpha generation.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-number">2</span>
                <span className="stat-label">Founders</span>
              </div>
              <div className="stat">
                <span className="stat-number">Singapore</span>
                <span className="stat-label">Headquarters</span>
              </div>
              <div className="stat">
                <span className="stat-number">Delta-Neutral</span>
                <span className="stat-label">Strategy</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* About Section */}
      <section id="about" className="section">
        <div className="container">
          <h2>About Quantum Capital</h2>
          <div className="about-content">
            <div className="about-text">
              <p>
                Quantum Capital is a boutique hedge fund founded by two quantitative finance 
                professionals from UC Berkeley and Columbia University. Based in Singapore, 
                we specialize in systematic trading strategies with a focus on delta-neutral 
                portfolios and long/short equity positions.
              </p>
              <p>
                Our approach combines rigorous academic research with cutting-edge technology 
                to identify and exploit market inefficiencies across global markets. We maintain 
                a disciplined risk management framework while seeking consistent, uncorrelated returns.
              </p>
            </div>
            <div className="about-features">
              <div className="feature">
                <div className="feature-icon">📊</div>
                <h3>Systematic Trading</h3>
                <p>Algorithm-driven strategies based on quantitative research</p>
              </div>
              <div className="feature">
                <div className="feature-icon">⚖️</div>
                <h3>Delta-Neutral</h3>
                <p>Market-neutral positioning to reduce directional risk</p>
              </div>
              <div className="feature">
                <div className="feature-icon">🌏</div>
                <h3>Global Markets</h3>
                <p>Diversified exposure across multiple asset classes</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Strategy Section */}
      <section id="strategy" className="section strategy-section">
        <div className="container">
          <h2>Investment Strategy</h2>
          <div className="strategy-grid">
            <div className="strategy-card">
              <h3>Long/Short Equity</h3>
              <p>
                Systematic identification of alpha opportunities through fundamental 
                and technical analysis, maintaining balanced long and short positions 
                to capture relative value.
              </p>
              <ul>
                <li>Multi-factor stock selection models</li>
                <li>Risk-adjusted position sizing</li>
                <li>Dynamic portfolio rebalancing</li>
              </ul>
            </div>
            
            <div className="strategy-card">
              <h3>Delta-Neutral Portfolio</h3>
              <p>
                Sophisticated hedging strategies to neutralize market direction risk 
                while preserving alpha generation from stock selection and timing.
              </p>
              <ul>
                <li>Options-based hedging strategies</li>
                <li>Futures and ETF overlays</li>
                <li>Real-time risk monitoring</li>
              </ul>
            </div>
            
            <div className="strategy-card">
              <h3>Systematic Approach</h3>
              <p>
                Technology-driven execution with minimal human intervention, 
                ensuring consistency and eliminating emotional biases from trading decisions.
              </p>
              <ul>
                <li>Algorithmic execution systems</li>
                <li>Real-time market data analysis</li>
                <li>Automated risk management</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="section">
        <div className="container">
          <h2>Our Team</h2>
          <div className="team-grid">
            <div className="team-member">
              <div className="member-photo">👨‍💼</div>
              <h3>Yur mudder</h3>
              <p className="member-title">Co-Founder & CIO</p>
              <p className="member-education">UC Berkeley, Bachelor in Financial Engineering</p>
              <p className="member-bio">
                Specializes in systematic equity strategies and risk management.
              </p>
            </div>
            
            <div className="team-member">
              <div className="member-photo">👨‍💼</div>
              <h3>Yur fadder</h3>
              <p className="member-title">Co-Founder & CTO</p>
              <p className="member-education">Columbia University, Bachelor in Computer Science</p>
              <p className="member-bio">
                Expert in algorithmic trading systems and machine learning applications in finance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Section */}
      <section id="performance" className="section performance-section">
        <div className="container">
          <div className="performance-header">
            <h2>Performance Overview</h2>
            <button 
              className="update-data-btn"
              onClick={() => setShowDataInput(true)}
            >
              Update Data
            </button>
          </div>
          
          {showDataInput && (
            <div className="data-input-modal">
              <div className="data-input-content">
                <h3>Update Performance Data</h3>
                <p>Enter your Interactive Brokers portfolio data:</p>
                <DataInputForm 
                  currentData={performanceData}
                  onSubmit={handleDataUpdate}
                  onCancel={() => setShowDataInput(false)}
                />
              </div>
            </div>
          )}
          
          <div className="performance-grid">
            <div className="performance-card">
              <h3>Risk Metrics</h3>
              <div className="metric">
                <span className="metric-label">Sharpe Ratio</span>
                <span className="metric-value">{performanceData.sharpeRatio}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Max Drawdown</span>
                <span className="metric-value">{performanceData.maxDrawdown}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Volatility</span>
                <span className="metric-value">{performanceData.volatility}%</span>
              </div>
            </div>
            
            <div className="performance-card">
              <h3>Returns</h3>
              <div className="metric">
                <span className="metric-label">YTD Return</span>
                <span className="metric-value positive">+{performanceData.ytdReturn}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Annualized</span>
                <span className="metric-value positive">+{performanceData.annualizedReturn}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Since Inception</span>
                <span className="metric-value positive">+{performanceData.inceptionReturn}%</span>
              </div>
            </div>
            
            <div className="performance-card">
              <h3>Portfolio Stats</h3>
              <div className="metric">
                <span className="metric-label">Positions</span>
                <span className="metric-value">{performanceData.positions}</span>
              </div>
              <div className="metric">
                <span className="metric-label">Net Exposure</span>
                <span className="metric-value">{performanceData.netExposure}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Gross Exposure</span>
                <span className="metric-value">{performanceData.grossExposure}%</span>
              </div>
            </div>
          </div>
          
          <div className="data-source">
            <p>Last updated: {performanceData.lastUpdated}</p>
            <p>Data source: Interactive Brokers Portfolio Analyst</p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="section">
        <div className="container">
          <h2>Contact Information</h2>
          <div className="contact-content">
            <div className="contact-info">
              <div className="contact-item">
                <span className="contact-icon">📍</span>
                <div>
                  <h4>Office</h4>
                  <p>Marina Bay Financial Centre<br />Singapore 018956</p>
                </div>
              </div>
              
              <div className="contact-item">
                <span className="contact-icon">📧</span>
                <div>
                  <h4>Email</h4>
                  <p>info@quantumcapital.sg</p>
                </div>
              </div>
              
              <div className="contact-item">
                <span className="contact-icon">📱</span>
                <div>
                  <h4>Phone</h4>
                  <p>+65 6789 0123</p>
                </div>
              </div>
            </div>
            
            <div className="disclaimer">
              <h4>Important Disclaimers</h4>
              <p>
                This website is for informational purposes only. Past performance does not 
                guarantee future results. Investment in hedge funds involves substantial risk 
                and may result in the loss of your entire investment. Please consult with 
                your financial advisor before making any investment decisions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h4>Quantum Capital</h4>
              <p>Systematic Delta-Neutral Trading</p>
            </div>
            
            <div className="footer-section">
              <h4>Current Time</h4>
              <p>{currentTime.toLocaleTimeString()}</p>
            </div>
            
            <div className="footer-section">
              <h4>Regulatory</h4>
              <p>Licensed by MAS Singapore</p>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>&copy; 2024 Quantum Capital. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
