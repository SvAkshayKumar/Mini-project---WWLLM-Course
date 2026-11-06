import React, { useState, useEffect } from 'react';
import {
  Server,
  Database,
  Layers,
  Cpu,
  Key,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  Copy,
  Check
} from 'lucide-react';
import { api } from '../services/api';

export default function SystemStatus() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copiedEnv, setCopiedEnv] = useState(false);

  useEffect(() => {
    async function loadStatus() {
      try {
        const data = await api.getSystemStatus();
        setStatus(data);
      } catch (err) {
        console.error('Failed to load system status:', err);
      } finally {
        setLoading(false);
      }
    }
    loadStatus();
  }, []);

  const sampleEnvText = `# IndicWrite AI Environment Configuration
# Save as .env in the project root directory

# Gemini API (Supporting LLM)
# Get key from: https://aistudio.google.com
GEMINI_API_KEY=""
GEMINI_MODEL="gemini-2.5-flash"

# BharatGen Param1 (Primary Writing Improvement)
# Model reference: https://huggingface.co/bharatgenai
BHARATGEN_API_KEY=""
BHARATGEN_MODEL_ENDPOINT=""

# AI4Bharat Integrations (Transliteration & Translation)
AI4BHARAT_INDICXLIT_ENDPOINT=""
AI4BHARAT_INDICTRANS2_ENDPOINT=""

# Application Ports & Local FAISS Vector Store
APP_ENV="development"
BACKEND_PORT=8000
FRONTEND_PORT=3000
FAISS_INDEX_PATH="storage/faiss/index.faiss"
FAISS_METADATA_PATH="storage/faiss/metadata.json"
EMBEDDING_MODEL="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"`;

  function handleCopyEnv() {
    navigator.clipboard.writeText(sampleEnvText);
    setCopiedEnv(true);
    setTimeout(() => setCopiedEnv(false), 2000);
  }

  const components = status ? [
    status.faiss_status,
    status.embedding_status,
    status.indicxlit_status,
    status.indictrans2_status,
    status.bharatgen_status,
    status.gemini_status
  ] : [];

  return (
    <div className="content-viewport">
      <div className="page-header">
        <h2 className="page-title">System Architecture & Model Status</h2>
        <p className="page-description">
          Transparent configuration health, provider credentials guidance, and local FAISS vector store status.
        </p>
      </div>

      {/* Component Status Grid */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Active AI Services & Vector Storage Components</h3>
            <p className="card-subtitle">Verified on backend server initialization</p>
          </div>
        </div>

        {loading ? (
          <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-muted)' }}>
            Inspecting system components...
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
            {components.map((comp, idx) => (
              <div
                key={idx}
                style={{
                  padding: '18px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-surface-alt)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between'
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                    <strong style={{ fontSize: '14px', color: 'var(--text-primary)' }}>{comp.name}</strong>
                    <span className="status-pill">
                      <span className={`status-dot ${comp.status}`}></span>
                      <span style={{ textTransform: 'capitalize', fontSize: '11px', fontWeight: 600 }}>
                        {comp.status === 'ready' ? 'Initialized' : comp.status === 'connected' ? 'Connected' : comp.status === 'fallback' ? 'Local Fallback' : 'Not Configured'}
                      </span>
                    </span>
                  </div>

                  <div style={{ fontSize: '12px', color: 'var(--accent-primary)', fontWeight: 600, marginBottom: '6px' }}>
                    {comp.provider}
                  </div>

                  <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '14px' }}>
                    {comp.details}
                  </p>
                </div>

                <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11px', color: 'var(--text-muted)' }}>
                  <span>Var: <code>{comp.env_var || 'N/A'}</code></span>
                  {comp.doc_url && (
                    <a
                      href={comp.doc_url}
                      target="_blank"
                      rel="noreferrer"
                      style={{ color: 'var(--accent-primary)', display: 'inline-flex', alignItems: 'center', gap: '3px' }}
                    >
                      Official Docs <ExternalLink size={11} />
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Provider Credentials & .env Instructions */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Configuration & Provider Credentials Guide</h3>
            <p className="card-subtitle">How to customize model endpoints or attach external credentials</p>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={handleCopyEnv}>
            {copiedEnv ? <Check size={14} color="var(--status-success)" /> : <Copy size={14} />}
            <span>{copiedEnv ? 'Copied .env' : 'Copy .env Template'}</span>
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <h4 style={{ fontSize: '13px', fontWeight: 600, marginBottom: '10px' }}>Official Provider Links & Variables</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <div>
                <strong>1. FAISS (Local Vector Database):</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  Works 100% locally on disk at <code>storage/faiss/index.faiss</code>. Does NOT require any API key, external account, or paid cloud service.
                </p>
              </div>

              <div>
                <strong>2. BharatGen Param1:</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  Primary writing improvement provider. Available on HuggingFace at <a href="https://huggingface.co/bharatgenai" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-primary)' }}>huggingface.co/bharatgenai</a>. To configure an inference server, set <code>BHARATGEN_MODEL_ENDPOINT</code>.
                </p>
              </div>

              <div>
                <strong>3. AI4Bharat IndicXlit & IndicTrans2:</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  Developed by IIT Madras / AI4Bharat (<a href="https://github.com/AI4Bharat" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-primary)' }}>github.com/AI4Bharat</a>). Runs locally without external credentials, or connects to your hosted IndicXlit / IndicTrans2 service via <code>AI4BHARAT_INDICXLIT_ENDPOINT</code>.
                </p>
              </div>

              <div>
                <strong>4. Google Gemini API (Supporting LLM):</strong>
                <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                  Optional supporting provider for text improvement and RAG synthesis. Obtain an API key from Google AI Studio (<a href="https://aistudio.google.com" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-primary)' }}>aistudio.google.com</a>) and add <code>GEMINI_API_KEY</code>.
                </p>
              </div>
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '13px', fontWeight: 600, marginBottom: '10px' }}>Baseline .env Template</h4>
            <pre className="code-block" style={{ height: '240px' }}>
              {sampleEnvText}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
