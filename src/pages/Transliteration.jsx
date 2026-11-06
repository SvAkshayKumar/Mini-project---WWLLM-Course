import React, { useState } from 'react';
import {
  Copy,
  Download,
  Trash2,
  ArrowRight,
  Check,
  Languages,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';

export default function Transliteration({ onLogActivity }) {
  const [inputText, setInputText] = useState('Namaste, aap kaise hain?');
  const [targetLang, setTargetLang] = useState('hi');
  const [outputText, setOutputText] = useState('नमस्ते, आप कैसे हैं?');
  const [provider, setProvider] = useState('AI4Bharat IndicXlit');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [details, setDetails] = useState({ char_count: 21, word_count: 4 });

  const samplePrompts = [
    { label: 'Hindi Greeting', text: 'Namaste, aap kaise hain?', lang: 'hi' },
    { label: 'Hindi Gratitude', text: 'Main theek hoon, dhanyavaad dost.', lang: 'hi' },
    { label: 'Kannada Inquiry', text: 'Namaskara, neevu hegidira?', lang: 'kn' },
    { label: 'Kannada Food', text: 'Oota ayitha? Banni kootkoli.', lang: 'kn' },
    { label: 'Tamil Greeting', text: 'Vanakkam, eppadi irukkinga?', lang: 'ta' },
    { label: 'Tamil Gratitude', text: 'Naan nallaa irukken, romba nandri.', lang: 'ta' }
  ];

  async function handleConvert(overrideText = null, overrideLang = null) {
    const textToConvert = overrideText !== null ? overrideText : inputText;
    const langToUse = overrideLang !== null ? overrideLang : targetLang;

    if (!textToConvert.trim()) return;

    setLoading(true);
    try {
      const res = await api.transliterate(textToConvert, langToUse);
      setOutputText(res.transliterated_text);
      setProvider(res.provider);
      if (res.details) setDetails(res.details);

      onLogActivity({
        type: 'transliteration',
        input: textToConvert,
        output: res.transliterated_text,
        language: langToUse.toUpperCase(),
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });
    } catch (err) {
      console.error('Transliteration failed:', err);
    } finally {
      setLoading(false);
    }
  }

  function handleSelectSample(sample) {
    setInputText(sample.text);
    setTargetLang(sample.lang);
    handleConvert(sample.text, sample.lang);
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
    link.download = `indicwrite_${targetLang}_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  }

  function handleClear() {
    setInputText('');
    setOutputText('');
  }

  const langNames = {
    hi: 'Hindi (हिन्दी · Devanagari)',
    kn: 'Kannada (ಕನ್ನಡ · Kannada Script)',
    ta: 'Tamil (தமிழ் · Tamil Script)'
  };

  return (
    <div className="content-viewport">
      <div className="page-header">
        <h2 className="page-title">Roman-to-Indic Transliteration Workspace</h2>
        <p className="page-description">
          Converts Roman-script Hinglish, Kanglish, and Tanglish into native scripts using AI4Bharat IndicXlit.
        </p>
      </div>

      {/* Target Language Tabs */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div className="segmented-tabs">
          <button
            className={`tab-btn ${targetLang === 'hi' ? 'active' : ''}`}
            onClick={() => {
              setTargetLang('hi');
              if (inputText.trim()) handleConvert(inputText, 'hi');
            }}
          >
            Hindi (हिन्दी)
          </button>
          <button
            className={`tab-btn ${targetLang === 'kn' ? 'active' : ''}`}
            onClick={() => {
              setTargetLang('kn');
              if (inputText.trim()) handleConvert(inputText, 'kn');
            }}
          >
            Kannada (ಕನ್ನಡ)
          </button>
          <button
            className={`tab-btn ${targetLang === 'ta' ? 'active' : ''}`}
            onClick={() => {
              setTargetLang('ta');
              if (inputText.trim()) handleConvert(inputText, 'ta');
            }}
          >
            Tamil (தமிழ்)
          </button>
        </div>

        <div className="meta-row">
          <span>Engine:</span>
          <strong style={{ color: 'var(--text-primary)' }}>{provider}</strong>
          <span className="meta-divider">·</span>
          <span>Target: {targetLang.toUpperCase()}</span>
        </div>
      </div>

      {/* Sample Chips */}
      <div className="sample-bar">
        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Quick Prompts:</span>
        {samplePrompts.map((s, idx) => (
          <button
            key={idx}
            className="sample-chip"
            onClick={() => handleSelectSample(s)}
          >
            {s.label} ({s.text})
          </button>
        ))}
      </div>

      {/* 2-Column Side-by-Side Editor Grid */}
      <div className="workspace-grid">
        {/* Left Column: Roman Script Input */}
        <div className="editor-pane">
          <div className="pane-toolbar">
            <span>Roman-script Input (English alphabet)</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleClear}
                title="Clear input"
              >
                <Trash2 size={13} />
                <span>Clear</span>
              </button>
            </div>
          </div>
          <textarea
            className="textarea-field"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type in Roman script (e.g. 'Namaste, aap kaise hain?' or 'Neenu hegidhdhiya?')..."
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              {inputText.length} characters · {inputText.trim() ? inputText.trim().split(/\s+/).length : 0} words
            </span>
            <button
              className="btn btn-primary"
              onClick={() => handleConvert()}
              disabled={loading || !inputText.trim()}
            >
              {loading ? (
                <span>Transliterating...</span>
              ) : (
                <>
                  <Languages size={15} />
                  <span>Convert to {targetLang.toUpperCase()}</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Column: Native Script Output */}
        <div className="editor-pane">
          <div className="pane-toolbar">
            <span>Native Indic Output ({langNames[targetLang]})</span>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleCopy}
                disabled={!outputText}
                title="Copy to clipboard"
              >
                {copied ? <Check size={13} color="var(--status-success)" /> : <Copy size={13} />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
              <button
                className="btn btn-secondary btn-sm"
                onClick={handleDownload}
                disabled={!outputText}
                title="Download text file"
              >
                <Download size={13} />
                <span>Download</span>
              </button>
            </div>
          </div>
          <textarea
            className="textarea-field indic-text"
            value={outputText}
            readOnly
            placeholder="Converted native script output will appear here..."
          />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
              {outputText.length} characters · {outputText.trim() ? outputText.trim().split(/\s+/).length : 0} words
            </span>
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              AI4Bharat IndicXlit Phonetic Accuracy: <strong>High</strong>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
