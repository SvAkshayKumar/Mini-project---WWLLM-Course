import React, { useState, useEffect } from 'react';
import {
  Languages,
  ArrowLeftRight,
  PenTool,
  Database,
  ArrowRight,
  CheckCircle2,
  Clock,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';

export default function Dashboard({ onNavigate, stats, recentActivity }) {
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchStatus() {
      try {
        const data = await api.getSystemStatus();
        setSystemStatus(data);
      } catch (err) {
        console.error('Failed to load status:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchStatus();
  }, []);

  return (
    <div className="content-viewport">
      <div className="page-header">
        <h2 className="page-title">IndicWrite AI Dashboard</h2>
        <p className="page-description">
          Undergraduate CS3235 mini-project: Multilingual Hinglish smart writing assistant based on AI4Bharat and BharatGen.
        </p>
      </div>

      {/* KPI Metric Strip */}
      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Languages size={22} />
          </div>
          <div>
            <div className="stat-val">{stats.transliterations}</div>
            <div className="stat-label">Total Transliterations</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <PenTool size={22} />
          </div>
          <div>
            <div className="stat-val">{stats.improvements}</div>
            <div className="stat-label">Text Improvements</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <ArrowLeftRight size={22} />
          </div>
          <div>
            <div className="stat-val">{stats.translations}</div>
            <div className="stat-label">Translations</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Database size={22} />
          </div>
          <div>
            <div className="stat-val">{systemStatus?.total_vector_chunks || 3}</div>
            <div className="stat-label">FAISS Vector Chunks</div>
          </div>
        </div>
      </div>

      {/* Model Status & Architecture Card */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">AI Engine & Model Configuration Status</h3>
            <p className="card-subtitle">Real-time connectivity to AI4Bharat, BharatGen, and local FAISS vector store</p>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={() => onNavigate('settings')}>
            View Full System Details
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '14px' }}>
          <div style={{ padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface-alt)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <strong style={{ fontSize: '13px' }}>AI4Bharat IndicXlit</strong>
              <span className="status-pill">
                <span className="status-dot ready"></span>
                <span>Active</span>
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Roman Hinglish/Kanglish/Tanglish transliteration into Devanagari, Kannada, and Tamil.
            </p>
          </div>

          <div style={{ padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface-alt)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <strong style={{ fontSize: '13px' }}>BharatGen Param1</strong>
              <span className="status-pill">
                <span className="status-dot ready"></span>
                <span>Primary</span>
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Grammar correction, clarity, formal/informal tone adaptation.
            </p>
          </div>

          <div style={{ padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface-alt)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <strong style={{ fontSize: '13px' }}>AI4Bharat IndicTrans2</strong>
              <span className="status-pill">
                <span className="status-dot ready"></span>
                <span>Active</span>
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Bidirectional translation between Hindi, Kannada, Tamil, and English.
            </p>
          </div>

          <div style={{ padding: '14px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface-alt)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <strong style={{ fontSize: '13px' }}>FAISS (Vector DB)</strong>
              <span className="status-pill">
                <span className="status-dot ready"></span>
                <span>Local Disk</span>
              </span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Zero external DB dependency. Stored at storage/faiss/index.faiss.
            </p>
          </div>
        </div>
      </div>

      {/* Quick Launch Workspaces */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Quick Action Workspaces</h3>
            <p className="card-subtitle">Launch core language modules</p>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '14px' }}>
          <div
            style={{ padding: '16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', cursor: 'pointer', transition: 'all 0.15s ease' }}
            onClick={() => onNavigate('transliteration')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <Languages size={18} color="var(--accent-primary)" />
              <strong>Transliterate Hinglish</strong>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Type in Roman alphabet ("Namaste, aap kaise hain?") and get native Indic script.
            </p>
            <span style={{ fontSize: '12px', color: 'var(--accent-primary)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
              Open Workspace <ArrowRight size={13} />
            </span>
          </div>

          <div
            style={{ padding: '16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', cursor: 'pointer', transition: 'all 0.15s ease' }}
            onClick={() => onNavigate('improvement')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <PenTool size={18} color="var(--accent-primary)" />
              <strong>Improve Writing</strong>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Grammar correction, professional rewriting, formal and informal tone via BharatGen Param1.
            </p>
            <span style={{ fontSize: '12px', color: 'var(--accent-primary)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
              Open Workspace <ArrowRight size={13} />
            </span>
          </div>

          <div
            style={{ padding: '16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', cursor: 'pointer', transition: 'all 0.15s ease' }}
            onClick={() => onNavigate('knowledge')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <Database size={18} color="var(--accent-primary)" />
              <strong>FAISS Knowledge Base</strong>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Upload writing guides (PDF/DOCX/TXT) and query with context-aware RAG citations.
            </p>
            <span style={{ fontSize: '12px', color: 'var(--accent-primary)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
              Open Workspace <ArrowRight size={13} />
            </span>
          </div>

          <div
            style={{ padding: '16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', cursor: 'pointer', transition: 'all 0.15s ease' }}
            onClick={() => onNavigate('evaluation')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <Sparkles size={18} color="var(--accent-primary)" />
              <strong>Run Evaluation Suite</strong>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '12px' }}>
              Evaluate CER, Word Accuracy, and RAG Groundedness over 36 test cases with CSV export.
            </p>
            <span style={{ fontSize: '12px', color: 'var(--accent-primary)', display: 'inline-flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
              Open Workspace <ArrowRight size={13} />
            </span>
          </div>
        </div>
      </div>

      {/* Recent Activity List */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Recent Session Activity</h3>
            <p className="card-subtitle">Live log of processed texts in this browser session</p>
          </div>
        </div>

        {recentActivity.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)', fontSize: '13px' }}>
            No texts processed yet in this session. Start by transliterating or improving text!
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Input Text</th>
                <th>Output / Result</th>
                <th>Language</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {recentActivity.slice(0, 6).map((item, idx) => (
                <tr key={idx}>
                  <td>
                    <span style={{ fontWeight: 600, textTransform: 'capitalize' }}>{item.type}</span>
                  </td>
                  <td style={{ maxWidth: '240px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {item.input}
                  </td>
                  <td style={{ maxWidth: '280px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'var(--font-indic)' }}>
                    {item.output}
                  </td>
                  <td>{item.language}</td>
                  <td className="num-cell" style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{item.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
