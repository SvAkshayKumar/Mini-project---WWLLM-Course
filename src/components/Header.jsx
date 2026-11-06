import React from 'react';
import { Sun, Moon, Sparkles, CheckCircle2 } from 'lucide-react';

export default function Header({ currentTab, theme, onToggleTheme, onNavigate }) {
  const tabTitles = {
    dashboard: 'Dashboard Overview',
    transliteration: 'Roman-to-Indic Transliteration',
    improvement: 'Intelligent Text Improvement',
    translation: 'Multilingual Translation',
    knowledge: 'FAISS Writing Knowledge Base',
    evaluation: 'CS3235 Evaluation Suite',
    settings: 'System Architecture & Status'
  };

  return (
    <header className="top-header">
      <div className="header-breadcrumbs">
        <span>IndicWrite AI</span>
        <span>/</span>
        <span className="breadcrumb-active">{tabTitles[currentTab] || 'Workspace'}</span>
      </div>

      <div className="header-actions">
        <div className="meta-row" style={{ marginRight: '8px' }}>
          <span className="status-pill">
            <span className="status-dot ready"></span>
            <span>FAISS Ready</span>
          </span>
          <span className="meta-divider">·</span>
          <span>AI4Bharat + BharatGen</span>
        </div>

        <button
          className="btn btn-secondary btn-sm"
          onClick={() => onNavigate('evaluation')}
          title="Run CS3235 Evaluation Suite"
        >
          <Sparkles size={14} />
          <span>Run Evaluation</span>
        </button>

        <button
          className="theme-toggle-btn"
          onClick={onToggleTheme}
          title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          aria-label="Toggle Theme"
        >
          {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
        </button>
      </div>
    </header>
  );
}
