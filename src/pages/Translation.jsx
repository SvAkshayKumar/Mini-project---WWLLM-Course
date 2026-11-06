import React, { useState } from 'react';
import {
  ArrowLeftRight,
  Copy,
  Download,
  Trash2,
  Check,
  Languages
} from 'lucide-react';
import { api } from '../services/api';

export default function Translation({ onLogActivity }) {
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('hi');
  const [inputText, setInputText] = useState('Hello, how are you?');
  const [outputText, setOutputText] = useState('नमस्ते, आप कैसे हैं?');
  const [provider, setProvider] = useState('AI4Bharat IndicTrans2');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi (हिन्दी)' },
    { code: 'kn', name: 'Kannada (ಕನ್ನಡ)' },
    { code: 'ta', name: 'Tamil (தமிழ்)' }
  ];

  const samplePairs = [
    { label: 'English -> Hindi', src: 'en', tgt: 'hi', text: 'Hello, how are you?' },
    { label: 'English -> Kannada', src: 'en', tgt: 'kn', text: 'Hello, how are you?' },
    { label: 'English -> Tamil', src: 'en', tgt: 'ta', text: 'Hello, how are you?' },
    { label: 'Hindi -> English', src: 'hi', tgt: 'en', text: 'नमस्ते, आप कैसे हैं?' },
    { label: 'Kannada -> English', src: 'kn', tgt: 'en', text: 'ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?' },
    { label: 'Tamil -> English', src: 'ta', tgt: 'en', text: 'வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?' }
  ];

  async function handleTranslate(overrideText = null, overrideSrc = null, overrideTgt = null) {
    const textToUse = overrideText !== null ? overrideText : inputText;
    const srcToUse = overrideSrc !== null ? overrideSrc : sourceLang;
    const tgtToUse = overrideTgt !== null ? overrideTgt : targetLang;

    if (!textToUse.trim()) return;

    setLoading(true);
    try {
      const res = await api.translate(textToUse, srcToUse, tgtToUse);
      setOutputText(res.translated_text);
      setProvider(res.provider);

      onLogActivity({
        type: 'translation',
        input: textToUse,
        output: res.translated_text,
        language: `${srcToUse.toUpperCase()} -> ${tgtToUse.toUpperCase()}`,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    } catch (err) {
      console.error('Translation failed:', err);
    } finally {
      setLoading(false);
    }
  }

  function handleSwap() {
    const tempLang = sourceLang;
    const tempText = inputText;
    setSourceLang(targetLang);
    setTargetLang(tempLang);
    setInputText(outputText);
    setOutputText(tempText);
    if (outputText.trim()) {
      handleTranslate(outputText, targetLang, tempLang);
    }
  }

  function handleSelectSample(s) {
    setSourceLang(s.src);
    setTargetLang(s.tgt);
    setInputText(s.text);
    handleTranslate(s.text, s.src, s.tgt);
  }

  function handleCopy() {
    if (!outputText) return;
    navigator.clipboard.writeText(outputText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  function handleDownload() {
    if (!outputText) return;
    const blob = new Blob([outputText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `translation_${sourceLang}_${targetLang}_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="content-viewport">
      <div className="page-header">
        <h2 className="page-title">Multilingual Translation Workspace</h2>
        <p className="page-description">
          Cross-lingual translation between Indian languages and English implementing AI4Bharat IndicTrans2.
        </p>
      </div>

      {/* Language Selector Header Strip */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div>
            <label style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Source Language</label>
            <select
              style={{ padding: '6px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface)' }}
              value={sourceLang}
              onChange={(e) => setSourceLang(e.target.value)}
            >
              {languages.map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>

          <button
            className="btn btn-secondary btn-sm"
            onClick={handleSwap}
            title="Swap Source and Target Languages"
            style={{ marginTop: '16px' }}
          >
            <ArrowLeftRight size={14} />
            <span>Swap</span>
          </button>

          <div>
            <label style={{ fontSize: '11px', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Target Language</label>
            <select
              style={{ padding: '6px 12px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)', backgroundColor: 'var(--bg-surface)' }}
              value={targetLang}
              onChange={(e) => setTargetLang(e.target.value)}
            >
              {languages.map(l => (
                <option key={l.code} value={l.code}>{l.name}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="meta-row">
          <span>Engine:</span>
          <strong style={{ color: 'var(--text-primary)' }}>{provider}</strong>
        </div>
      </div>

      {/* Sample Pairs Bar */}
      <div className="sample-bar">
        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Quick Phrases:</span>
        {samplePairs.map((s, idx) => (
          <button
            key={idx}
            className="sample-chip"
            onClick={() => handleSelectSample(s)}
          >
            {s.label}
          </button>
        ))}
      </div>

      {/* 2-Column Side-by-Side Editor Grid */}
      <div className="workspace-grid">
        {/* Source Text Pane */}
        <div className="editor-pane">
          <div className="pane-toolbar">
            <span>Source Text ({languages.find(l => l.code === sourceLang)?.name})</span>
            <button
              className="btn btn-secondary btn-sm"
              onClick={() => { setInputText(''); setOutputText(''); }}
            >
              <Trash2 size={13} />
              <span>Clear</span>
            </button>
          </div>
          <textarea
            className={`textarea-field ${sourceLang !== 'en' ? 'indic-text' : ''}`}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type or paste source text to translate..."
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              {inputText.length} characters
            </span>
            <button
              className="btn btn-primary"
              onClick={() => handleTranslate()}
              disabled={loading || !inputText.trim()}
            >
              {loading ? (
                <span>Translating...</span>
              ) : (
                <>
                  <Languages size={15} />
                  <span>Translate Text</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Target Translation Pane */}
        <div className="editor-pane">
          <div className="pane-toolbar">
            <span>Translated Output ({languages.find(l => l.code === targetLang)?.name})</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleCopy}
                disabled={!outputText}
              >
                {copied ? <Check size={13} color="var(--status-success)" /> : <Copy size={13} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleDownload}
                disabled={!outputText}
              >
                <Download size={13} />
                <span>Download</span>
              </button>
            </div>
          </div>
          <textarea
            className={`textarea-field ${targetLang !== 'en' ? 'indic-text' : ''}`}
            value={outputText}
            readOnly
            placeholder="Translation will appear here..."
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              {outputText.length} characters
            </span>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Direction: <strong>{sourceLang.toUpperCase()} → {targetLang.toUpperCase()}</strong>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
