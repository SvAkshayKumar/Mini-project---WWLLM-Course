import React, { useState } from 'react';
import {
  PenTool,
  Copy,
  Download,
  Trash2,
  Check,
  Sparkles,
  Info,
  CheckCircle2
} from 'lucide-react';
import { api } from '../services/api';

export default function Improvement({ onLogActivity }) {
  const [inputText, setInputText] = useState('हम जाएगा और वो आया था और वो बोला कि काम करो');
  const [mode, setMode] = useState('grammar');
  const [language, setLanguage] = useState('hi');
  const [providerPref, setProviderPref] = useState('bharatgen');
  const [improvedText, setImprovedText] = useState('हम जाएंगे और वह आया और उसने कहा कि काम करो।');
  const [explanation, setExplanation] = useState('Corrected first-person plural verb agreement (जाएगा -> जाएंगे) and normalized third-person pronoun/past transitive construction.');
  const [changes, setChanges] = useState([
    'Corrected first-person plural verb agreement (जाएगा -> जाएंगे)',
    'Normalized third-person pronoun and past tense transitive verb agreement'
  ]);
  const [providerUsed, setProviderUsed] = useState('BharatGen Param1 (Local Engine)');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const modes = [
    { id: 'grammar', label: 'Grammar Correction', desc: 'Fixes agreement, orthography, and verbal inflections' },
    { id: 'professional', label: 'Professional Writing', desc: 'Polished corporate tone suitable for formal communication' },
    { id: 'simple', label: 'Simple Language', desc: 'Replaces complex vocabulary with accessible everyday words' },
    { id: 'formal', label: 'Formal Register', desc: 'Elevates honorific address (आप / ನೀವು / நீங்கள்)' },
    { id: 'informal', label: 'Informal / Friendly', desc: 'Converts to peer conversational tone (तुम / ನೀನು / நீ)' },
    { id: 'clarity', label: 'Sentence Clarity', desc: 'Removes verbal filler and reorganizes phrasing' }
  ];

  const sampleInputs = [
    { label: 'Grammar Fault', text: 'हम जाएगा और काम करेगा', mode: 'grammar', lang: 'hi' },
    { label: 'Informal to Formal', text: 'तुम यहाँ आओ और यह फाइल देखो', mode: 'formal', lang: 'hi' },
    { label: 'High Vocabulary', text: 'अविलंब वार्तालाप प्रारंभ करने की कृपा करें', mode: 'simple', lang: 'hi' },
    { label: 'Greeting Polishing', text: 'aap kaise hain sab theek hai', mode: 'professional', lang: 'hi' },
    { label: 'Filler Removal', text: 'मतलब कि यानी कि प्रोजेक्ट आज पूरा हो जाएगा', mode: 'clarity', lang: 'hi' }
  ];

  async function handleImprove(overrideText = null, overrideMode = null) {
    const textToUse = overrideText !== null ? overrideText : inputText;
    const modeToUse = overrideMode !== null ? overrideMode : mode;

    if (!textToUse.trim()) return;

    setLoading(true);
    try {
      const res = await api.improve(textToUse, modeToUse, language, providerPref);
      setImprovedText(res.improved_text);
      setExplanation(res.explanation);
      setChanges(res.changes || []);
      setProviderUsed(res.provider_used);

      onLogActivity({
        type: 'improvement',
        input: textToUse,
        output: res.improved_text,
        language: `${language.toUpperCase()} (${modeToUse})`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    } catch (err) {
      console.error('Improvement failed:', err);
    } finally {
      setLoading(false);
    }
  }

  function handleSelectSample(s) {
    setInputText(s.text);
    setMode(s.mode);
    setLanguage(s.lang);
    handleImprove(s.text, s.mode);
  }

  function handleCopy() {
    if (!improvedText) return;
    navigator.clipboard.writeText(improvedText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function handleDownload() {
    if (!improvedText) return;
    const blob = new Blob([improvedText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `improved_${mode}_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="content-viewport">
      <div className="page-header">
        <h2 className="page-title">Intelligent Text Improvement Workspace</h2>
        <p className="page-description">
          Linguistic optimization, grammar correction, and tone rewriting powered primarily by BharatGen Param1, with Google Gemini as an optional supporting provider.
        </p>
      </div>

      {/* Mode Selector Ribbon */}
      <div style={{ marginBottom: '16px' }}>
        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '12px' }}>
          {modes.map(m => (
            <button
              key={m.id}
              className={`btn ${mode === m.id ? 'btn-primary' : 'btn-secondary'} btn-sm`}
              onClick={() => {
                setMode(m.id);
                if (inputText.trim()) handleImprove(inputText, m.id);
              }}
            >
              <span>{m.label}</span>
            </button>
          ))}
        </div>

        {/* Provider Selector and Metadata */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Provider Engine:</span>
            <div className="segmented-tabs">
              <button
                className={`tab-btn ${providerPref === 'bharatgen' ? 'active' : ''}`}
                onClick={() => setProviderPref('bharatgen')}
                title="Designated primary provider"
              >
                BharatGen Param1 (Primary)
              </button>
              <button
                className={`tab-btn ${providerPref === 'gemini' ? 'active' : ''}`}
                onClick={() => setProviderPref('gemini')}
                title="Optional supporting LLM"
              >
                Google Gemini (Supporting)
              </button>
            </div>
          </div>

          <div className="meta-row">
            <span>Provider Active:</span>
            <strong style={{ color: 'var(--text-primary)' }}>{providerUsed}</strong>
          </div>
        </div>
      </div>

      {/* Sample Inputs */}
      <div className="sample-bar">
        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Sample Cases:</span>
        {sampleInputs.map((s, idx) => (
          <button
            key={idx}
            className="sample-chip"
            onClick={() => handleSelectSample(s)}
          >
            {s.label} ({s.text.substring(0, 24)}...)
          </button>
        ))}
      </div>

      {/* 2-Column Side-by-Side Editor Grid */}
      <div className="workspace-grid">
        {/* Left Column: Original Text */}
        <div className="editor-pane">
          <div className="pane-toolbar">
            <span>Original Draft Text</span>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => { setInputText(''); setImprovedText(''); }}
            >
              <Trash2 size={13} />
              <span>Clear</span>
            </button>
          </div>
          <textarea
            className="textarea-field indic-text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter draft text to improve or correct..."
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Mode: <strong>{modes.find(m => m.id === mode)?.label}</strong>
            </span>
            <button
              className="btn btn-primary"
              onClick={() => handleImprove()}
              disabled={loading || !inputText.trim()}
            >
              {loading ? (
                <span>Improving Text...</span>
              ) : (
                <>
                  <PenTool size={15} />
                  <span>Improve Text</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Improved Text */}
        <div className="editor-pane">
          <div className="pane-toolbar">
            <span>Improved Text ({providerUsed})</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleCopy}
                disabled={!improvedText}
              >
                {copied ? <Check size={13} color="var(--status-success)" /> : <Copy size={13} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleDownload}
                disabled={!improvedText}
              >
                <Download size={13} />
                <span>Download</span>
              </button>
            </div>
          </div>
          <textarea
            className="textarea-field indic-text"
            value={improvedText}
            readOnly
            placeholder="Improved output will appear here..."
          />
          <div style={{ marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              Target Mode: <strong>{mode}</strong> · Length: {improvedText.length} chars
            </span>
          </div>
        </div>
      </div>

      {/* Explanation of Changes Card */}
      <div className="card" style={{ marginTop: '20px' }}>
        <div className="card-header">
          <div>
            <h3 className="card-title">Linguistic Rationale & Explanation of Changes</h3>
            <p className="card-subtitle">Transparent justification generated by {providerUsed}</p>
          </div>
        </div>

        <div style={{ marginBottom: '14px', fontSize: '14px', color: 'var(--text-primary)', lineHeight: 1.6 }}>
          {explanation}
        </div>

        {changes.length > 0 && (
          <div>
            <strong style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Specific modifications:</strong>
            <ul style={{ marginTop: '8px', paddingLeft: '20px', fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px' }}>
              {changes.map((c, i) => (
                <li key={i}>{c}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
