import React from 'react';
import {
  LayoutDashboard,
  Languages,
  PenTool,
  ArrowLeftRight,
  Database,
  BarChart3,
  Settings2,
  BookOpen
} from 'lucide-react';

export default function Sidebar({ currentTab, onNavigate }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'transliteration', label: 'Transliteration', icon: Languages },
    { id: 'improvement', label: 'Text Improvement', icon: PenTool },
    { id: 'translation', label: 'Translation', icon: ArrowLeftRight },
    { id: 'knowledge', label: 'Knowledge Base (FAISS)', icon: Database },
    { id: 'evaluation', label: 'Evaluation Suite', icon: BarChart3 },
    { id: 'settings', label: 'System & Status', icon: Settings2 }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="brand-icon">
          <span>आ</span>
        </div>
        <div>
          <h1 className="brand-title">IndicWrite AI</h1>
          <p className="brand-tagline">AI4Bharat & BharatGen</p>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map(item => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onNavigate(item.id)}
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="footer-meta">
          <strong>CS3235 Mini-Project</strong>
          <div>Hindi · Kannada · Tamil · English</div>
          <div style={{ marginTop: '4px', fontSize: '10px' }}>v1.0.0 · Local FAISS Index</div>
        </div>
      </div>
    </aside>
  );
}
