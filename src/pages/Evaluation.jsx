import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Download,
  Filter,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  FileSpreadsheet,
  Clock,
  Layers
} from 'lucide-react';
import { api } from '../services/api';

export default function Evaluation() {
  const [testResults, setTestResults] = useState(null);
  const [running, setRunning] = useState(false);
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    // Initial evaluation run on mount so user sees immediate results
    handleRunTests();
  }, []);

  async function handleRunTests() {
    setRunning(true);
    try {
      const data = await api.runEvaluation();
      setTestResults(data);
    } catch (err) {
      console.error('Evaluation run failed:', err);
    } finally {
      setRunning(false);
    }
  }

  function handleExportCSV() {
    if (!testResults || !testResults.results) return;

    const headers = ['ID', 'Category', 'Language', 'Input Text', 'Expected Output', 'Actual Output', 'CER', 'Word Accuracy', 'Status', 'Failure Reason'];
    const rows = testResults.results.map(r => [
      `"${r.id}"`,
      `"${r.category}"`,
      `"${r.language}"`,
      `"${(r.input_text || '').replace(/"/g, '""')}"`,
      `"${(r.expected_output || '').replace(/"/g, '""')}"`,
      `"${(r.actual_output || '').replace(/"/g, '""')}"`,
      r.cer,
      r.word_accuracy,
      `"${r.status}"`,
      `"${(r.failure_reason || '').replace(/"/g, '""')}"`
    ]);

    const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `indicwrite_evaluation_report_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  const filteredResults = testResults?.results.filter(r => {
    const matchCat = filterCategory === 'all' || r.category === filterCategory;
    const matchStatus = filterStatus === 'all' || r.status === filterStatus;
    return matchCat && matchStatus;
  }) || [];

  return (
    <div className="content-viewport">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h2 className="page-title">CS3235 Evaluation & Benchmarking Suite</h2>
          <p className="page-description">
            Standardized evaluation of 36 representative test cases across Hindi, Kannada, Tamil, and English measuring Character Error Rate (CER), Word Accuracy, and RAG Groundedness.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            className="btn btn-primary"
            onClick={handleRunTests}
            disabled={running}
          >
            <Sparkles size={15} />
            <span>{running ? 'Running Tests...' : 'Run All 36 Tests'}</span>
          </button>
          <button
            className="btn btn-secondary"
            onClick={handleExportCSV}
            disabled={!testResults}
            title="Export evaluation results to CSV"
          >
            <Download size={15} />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Aggregate Metric Cards */}
      {testResults && (
        <div className="stat-grid">
          <div className="stat-card">
            <div>
              <div className="stat-val">{testResults.total_tests}</div>
              <div className="stat-label">Total Test Cases</div>
            </div>
          </div>

          <div className="stat-card">
            <div>
              <div className="stat-val" style={{ color: 'var(--status-success)' }}>
                {testResults.passed_tests} ({((testResults.passed_tests / testResults.total_tests) * 100).toFixed(1)}%)
              </div>
              <div className="stat-label">Passed Tests</div>
            </div>
          </div>

          <div className="stat-card">
            <div>
              <div className="stat-val" style={{ color: testResults.failed_tests > 0 ? 'var(--status-error)' : 'var(--text-primary)' }}>
                {testResults.failed_tests}
              </div>
              <div className="stat-label">Failed Tests</div>
            </div>
          </div>

          <div className="stat-card">
            <div>
              <div className="stat-val num-cell">
                {(testResults.average_cer * 100).toFixed(1)}%
              </div>
              <div className="stat-label">Average CER (Lower is better)</div>
            </div>
          </div>

          <div className="stat-card">
            <div>
              <div className="stat-val num-cell">
                {(testResults.average_word_accuracy * 100).toFixed(1)}%
              </div>
              <div className="stat-label">Avg Word Accuracy</div>
            </div>
          </div>

          <div className="stat-card">
            <div>
              <div className="stat-val num-cell" style={{ fontSize: '18px' }}>
                {testResults.duration_ms} ms
              </div>
              <div className="stat-label">Execution Duration</div>
            </div>
          </div>
        </div>
      )}

      {/* Filter and Table Card */}
      <div className="card">
        <div className="card-header" style={{ flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <h3 className="card-title">Detailed Evaluation Results ({filteredResults.length} records)</h3>
            <p className="card-subtitle">Granular comparison of ground-truth reference vs. generated output</p>
          </div>

          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            {/* Category Filter */}
            <div className="segmented-tabs">
              <button
                className={`tab-btn ${filterCategory === 'all' ? 'active' : ''}`}
                onClick={() => setFilterCategory('all')}
              >
                All
              </button>
              <button
                className={`tab-btn ${filterCategory === 'transliteration' ? 'active' : ''}`}
                onClick={() => setFilterCategory('transliteration')}
              >
                Translit
              </button>
              <button
                className={`tab-btn ${filterCategory === 'translation' ? 'active' : ''}`}
                onClick={() => setFilterCategory('translation')}
              >
                Translation
              </button>
              <button
                className={`tab-btn ${filterCategory === 'improvement' ? 'active' : ''}`}
                onClick={() => setFilterCategory('improvement')}
              >
                Improvement
              </button>
              <button
                className={`tab-btn ${filterCategory === 'rag' ? 'active' : ''}`}
                onClick={() => setFilterCategory('rag')}
              >
                RAG
              </button>
            </div>

            {/* Status Filter */}
            <select
              style={{ padding: '6px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface)' }}
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="passed">Passed Only</option>
              <option value="failed">Failed Only</option>
            </select>
          </div>
        </div>

        {/* Data Table */}
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Test ID</th>
                <th>Category</th>
                <th>Language</th>
                <th>Input Text</th>
                <th>Expected Output</th>
                <th>Generated Actual Output</th>
                <th>CER</th>
                <th>Word Acc</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredResults.map((r) => (
                <tr key={r.id}>
                  <td className="num-cell" style={{ fontWeight: 600 }}>{r.id}</td>
                  <td>
                    <span style={{ textTransform: 'capitalize', fontSize: '12px' }}>{r.category}</span>
                  </td>
                  <td>{r.language}</td>
                  <td style={{ maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {r.input_text}
                  </td>
                  <td style={{ maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'var(--font-indic)' }}>
                    {r.expected_output}
                  </td>
                  <td style={{ maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontFamily: 'var(--font-indic)', color: r.status === 'passed' ? 'var(--text-primary)' : 'var(--status-error)' }}>
                    {r.actual_output || '—'}
                  </td>
                  <td className="num-cell" style={{ color: r.cer <= 0.35 ? 'var(--status-success)' : 'var(--status-error)' }}>
                    {(r.cer * 100).toFixed(1)}%
                  </td>
                  <td className="num-cell" style={{ color: r.word_accuracy >= 0.6 ? 'var(--status-success)' : 'var(--text-muted)' }}>
                    {(r.word_accuracy * 100).toFixed(1)}%
                  </td>
                  <td>
                    <span className="status-pill">
                      <span className={`status-dot ${r.status}`}></span>
                      <span style={{ textTransform: 'capitalize', fontWeight: 600 }}>{r.status}</span>
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
