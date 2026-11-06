import React, { useState, useEffect } from 'react';
import {
  Upload,
  Database,
  Trash2,
  RefreshCw,
  Search,
  FileText,
  CheckCircle2,
  AlertCircle,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';

export default function KnowledgeBase() {
  const [documents, setDocuments] = useState([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(null);

  // RAG query state
  const [query, setQuery] = useState('What is the formal honorific rule in Hindi?');
  const [ragResult, setRagResult] = useState(null);
  const [querying, setQuerying] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  async function fetchDocuments() {
    setLoadingDocs(true);
    try {
      const data = await api.getDocuments();
      setDocuments(data.documents || []);
    } catch (err) {
      console.error('Failed to fetch documents:', err);
    } finally {
      setLoadingDocs(false);
    }
  }

  async function handleFileUpload(e) {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setUploadMessage(null);
    try {
      const res = await api.uploadDocument(file);
      setUploadMessage({ type: 'success', text: res.message });
      fetchDocuments();
    } catch (err) {
      setUploadMessage({ type: 'error', text: err.message });
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  }

  async function handleDeleteDocument(id) {
    if (!confirm('Are you sure you want to remove this document and re-index the FAISS vector database?')) return;
    try {
      await api.deleteDocument(id);
      fetchDocuments();
    } catch (err) {
      alert(`Deletion failed: ${err.message}`);
    }
  }

  async function handleReindex() {
    try {
      const res = await api.reindexKnowledge();
      alert(`FAISS Vector Index rebuilt successfully (${res.vector_count} vectors mapped).`);
      fetchDocuments();
    } catch (err) {
      alert(`Re-indexing failed: ${err.message}`);
    }
  }

  async function handleRunQuery(overrideQuery = null) {
    const q = overrideQuery || query;
    if (!q.trim()) return;

    setQuerying(true);
    try {
      const res = await api.queryKnowledge(q, 3);
      setRagResult(res);
    } catch (err) {
      console.error('RAG Query failed:', err);
    } finally {
      setQuerying(false);
    }
  }

  const sampleQuestions = [
    'What is the formal honorific rule in Hindi?',
    'What does ನೀವು mean in Kannada?',
    'What is the standard polite greeting in Tamil?',
    'How do transitive past tense verbs work in Hindi?'
  ];

  return (
    <div className="content-viewport">
      <div className="page-header">
        <h2 className="page-title">FAISS RAG Writing Knowledge Base</h2>
        <p className="page-description">
          Local vector database using FAISS IndexFlatIP (cosine similarity) and multilingual embeddings. Upload grammar references, vocabulary lists, and writing style guides.
        </p>
      </div>

      {/* Upload & Reindex Strip */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Document Ingestion & Index Management</h3>
            <p className="card-subtitle">Supports .txt, .pdf, and .docx documents with automatic chunking and vector persistence</p>
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <label className="btn btn-primary btn-sm" style={{ cursor: 'pointer' }}>
              <Upload size={14} />
              <span>{uploading ? 'Ingesting...' : 'Upload Document'}</span>
              <input
                type="file"
                accept=".txt,.pdf,.docx"
                style={{ display: 'none' }}
                onChange={handleFileUpload}
                disabled={uploading}
              />
            </label>
            <button className="btn btn-secondary btn-sm" onClick={handleReindex} title="Reconstruct FAISS index from disk">
              <RefreshCw size={14} />
              <span>Rebuild Index</span>
            </button>
          </div>
        </div>

        {uploadMessage && (
          <div className={`info-box ${uploadMessage.type === 'error' ? 'warning' : ''}`}>
            {uploadMessage.type === 'error' ? <AlertCircle size={16} /> : <CheckCircle2 size={16} />}
            <span>{uploadMessage.text}</span>
          </div>
        )}

        {/* Indexed Documents Table */}
        {loadingDocs ? (
          <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading documents...</div>
        ) : documents.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>
            No documents in knowledge base yet. Upload grammar references or vocabulary sheets.
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Document Name</th>
                <th>Type</th>
                <th>Chunks</th>
                <th>Uploaded At</th>
                <th>File Size</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((doc) => (
                <tr key={doc.id}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 600, color: 'var(--text-primary)' }}>
                      <FileText size={16} color="var(--accent-primary)" />
                      <span>{doc.name}</span>
                    </div>
                  </td>
                  <td>
                    <span style={{ textTransform: 'uppercase', fontSize: '11px', fontWeight: 600 }}>{doc.file_type}</span>
                  </td>
                  <td className="num-cell">{doc.total_chunks} vectors</td>
                  <td className="num-cell" style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{doc.uploaded_at}</td>
                  <td className="num-cell">{(doc.size_bytes / 1024).toFixed(1)} KB</td>
                  <td>
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleDeleteDocument(doc.id)}
                      title="Delete document and reindex"
                    >
                      <Trash2 size={13} color="var(--status-error)" />
                      <span>Remove</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Contextual RAG Query Workspace */}
      <div className="card">
        <div className="card-header">
          <div>
            <h3 className="card-title">Ask the Multilingual Writing Knowledge Base</h3>
            <p className="card-subtitle">Retrieves top-K semantic chunks from local FAISS and synthesizes grounded answers with citations</p>
          </div>
        </div>

        {/* Sample Questions */}
        <div className="sample-bar">
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Sample Queries:</span>
          {sampleQuestions.map((sq, idx) => (
            <button
              key={idx}
              className="sample-chip"
              onClick={() => {
                setQuery(sq);
                handleRunQuery(sq);
              }}
            >
              {sq}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
          <input
            type="text"
            style={{
              flexGrow: 1,
              padding: '10px 14px',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-surface)',
              fontSize: '14px',
              color: 'var(--text-primary)'
            }}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your uploaded writing references or grammar rules..."
            onKeyDown={(e) => e.key === 'Enter' && handleRunQuery()}
          />
          <button
            className="btn btn-primary"
            onClick={() => handleRunQuery()}
            disabled={querying || !query.trim()}
          >
            {querying ? (
              <span>Retrieving...</span>
            ) : (
              <>
                <Search size={15} />
                <span>Search & Answer</span>
              </>
            )}
          </button>
        </div>

        {/* Answer Display */}
        {ragResult && (
          <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
              <strong style={{ fontSize: '14px', color: 'var(--text-primary)' }}>Grounded Synthesis:</strong>
              <span className="meta-row" style={{ fontSize: '12px' }}>
                <span>Engine:</span>
                <strong style={{ color: 'var(--accent-primary)' }}>{ragResult.provider_used}</strong>
              </span>
            </div>

            <div style={{ fontSize: '14px', lineHeight: 1.7, color: 'var(--text-primary)', whiteSpace: 'pre-wrap', marginBottom: '18px', backgroundColor: 'var(--bg-surface-alt)', padding: '16px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
              {ragResult.answer}
            </div>

            {/* Citations */}
            {ragResult.citations && ragResult.citations.length > 0 && (
              <div>
                <strong style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Retrieved Source Citations ({ragResult.citations.length} chunks):</strong>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px', marginTop: '10px' }}>
                  {ragResult.citations.map((cite, idx) => (
                    <div key={idx} className="citation-card">
                      <div className="citation-header">
                        <span>{cite.doc_name}</span>
                        <span className="num-cell" style={{ color: 'var(--accent-primary)', fontSize: '11px' }}>
                          Cosine: {cite.similarity_score}
                        </span>
                      </div>
                      <p style={{ color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                        "{cite.snippet}"
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
