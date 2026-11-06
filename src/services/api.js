/**
 * IndicWrite AI - API Client Service
 */

const BASE_URL = '';

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const headers = options.headers || {};
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
  }

  try {
    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      let errMsg = `Request failed (${res.status})`;
      try {
        const errJson = await res.json();
        errMsg = errJson.detail || errJson.error || errMsg;
      } catch {}
      throw new Error(errMsg);
    }
    return await res.json();
  } catch (error) {
    console.error(`API Error on ${endpoint}:`, error);
    throw error;
  }
}

export const api = {
  // Transliteration
  async transliterate(text, targetLanguage = 'hi') {
    return request('/api/transliterate', {
      method: 'POST',
      body: JSON.stringify({
        text,
        target_language: targetLanguage
      })
    });
  },

  // Multi-stage pipeline
  async processPipeline(text, transliterateLang = 'hi', improveMode = null, translateTo = null) {
    return request('/api/process', {
      method: 'POST',
      body: JSON.stringify({
        text,
        transliterate_lang: transliterateLang,
        improve_mode: improveMode,
        translate_to: translateTo
      })
    });
  },

  // Text Improvement
  async improve(text, mode = 'grammar', language = 'hi', providerPreference = 'bharatgen') {
    return request('/api/improve', {
      method: 'POST',
      body: JSON.stringify({
        text,
        mode,
        language,
        provider_preference: providerPreference
      })
    });
  },

  // Translation
  async translate(text, sourceLanguage, targetLanguage) {
    return request('/api/translate', {
      method: 'POST',
      body: JSON.stringify({
        text,
        source_language: sourceLanguage,
        target_language: targetLanguage
      })
    });
  },

  // Knowledge Base & RAG
  async getDocuments() {
    return request('/api/knowledge/documents');
  },

  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    return request('/api/knowledge/upload', {
      method: 'POST',
      body: formData
    });
  },

  async deleteDocument(id) {
    return request(`/api/knowledge/documents/${encodeURIComponent(id)}`, {
      method: 'DELETE'
    });
  },

  async reindexKnowledge() {
    return request('/api/knowledge/reindex', {
      method: 'POST'
    });
  },

  async queryKnowledge(query, topK = 3) {
    return request('/api/knowledge/query', {
      method: 'POST',
      body: JSON.stringify({ query, top_k: topK })
    });
  },

  // System Status
  async getSystemStatus() {
    return request('/api/system/status');
  },

  // Evaluation
  async runEvaluation() {
    return request('/api/evaluation/run', {
      method: 'POST'
    });
  },

  async getEvaluationResults() {
    return request('/api/evaluation/results');
  }
};
