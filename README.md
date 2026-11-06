# IndicWrite AI – Multilingual Hinglish Smart Writing Assistant

> **Undergraduate CS3235 Mini-Project**  
> Based on **AI4Bharat** (IndicXlit, IndicTrans2) and **BharatGen** (Param1).  
> Features Roman-to-Indic transliteration, text improvement, translation, and a local FAISS RAG vector database.

---

## 1. Overview & Objective

**IndicWrite AI** is an intelligent writing assistant tailored for Indian languages. In everyday digital communication, users frequently type Indian languages using the Latin/Roman script (commonly known as *Hinglish*, *Kanglish*, or *Tanglish*). 

IndicWrite AI addresses this communication challenge by:
1. **Transliteration**: Faithfully converting Roman-script Indian language text into native scripts (Devanagari for Hindi, Kannada script, and Tamil script) using AI4Bharat IndicXlit models.
2. **Text Improvement**: Correcting grammar, adjusting formality registers (e.g., informal *तुम* to formal *आप*), simplifying complex vocabulary, and polishing phrasing using **BharatGen Param1** as the primary provider (with Google Gemini as a supporting LLM).
3. **Translation**: Providing high-accuracy cross-lingual translation between Indian languages and English implementing **AI4Bharat IndicTrans2**.
4. **Context-Aware Writing Knowledge Base (RAG)**: Allowing users to index personal grammar references, style guides, and vocabulary documents (PDF, DOCX, TXT) into a local **FAISS** vector store without external database credentials.
5. **Rigorous Evaluation Suite**: Benchmarking Character Error Rate (CER), Word Accuracy, and RAG Groundedness across 36 test cases with CSV export.

---

## 2. Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                            IndicWrite AI Web Frontend                             |
|         (React.js + Vite + Plain CSS + Lucide Icons + Light & Dark Themes)         |
+-----------------------------------------------------------------------------------+
                                         |
                                         | HTTP / JSON REST
                                         v
+-----------------------------------------------------------------------------------+
|                            IndicWrite Full-Stack Server                           |
|        Node/Express (Port 3000) dev proxy & Python FastAPI (Port 8000)            |
+-----------------------------------------------------------------------------------+
       |                    |                       |                   |
       v                    v                       v                   v
+--------------+   +------------------+   +-------------------+  +------------------+
| AI4Bharat    |   | BharatGen        |   | Google Gemini     |  | Local FAISS      |
| IndicXlit    |   | Param1           |   | (gemini-2.5-flash)|  | Vector Database  |
| - Hindi (hi) |   | - Grammar Fix    |   | - Supporting LLM  |  | - faiss-cpu      |
| - Kannada(kn)|   | - Tone Adapting  |   | - Server-Side API |  | - IndexFlatIP    |
| - Tamil (ta) |   | - Clarity Engine |   | - Context Synth   |  | - 384-d MiniLM   |
+--------------+   +------------------+   +-------------------+  +------------------+
                                                                        |
                                                                        v
                                                             +----------------------+
                                                             | storage/faiss/       |
                                                             | - index.faiss        |
                                                             | - metadata.json      |
                                                             +----------------------+
```

---

## 3. Technology Stack

- **Frontend**: React.js, Vite, JavaScript, Normal CSS (no Tailwind CSS), Lucide Icons, Responsive dual-theme layout.
- **Backend**: Python FastAPI, Pydantic v2 schemas, modular services, CORS middleware.
- **Vector Database**: **FAISS (Facebook AI Similarity Search)** with `faiss-cpu`. 100% local on disk; zero paid services or external cloud database accounts.
- **Multilingual Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384-dimensional dense vectors).
- **Core AI Integrations**:
  - **AI4Bharat IndicXlit**: Roman-to-Indic transliteration.
  - **AI4Bharat IndicTrans2**: Indian language to English translation.
  - **BharatGen Param1**: Primary intelligent writing and grammar improvement.
  - **Google Gemini**: Optional supporting LLM for advanced text rewriting and grounded RAG answer synthesis.

---

## 4. Quickstart & Installation

The application is designed to be **plug-and-play**.

### Method A: Automated One-Click Setup (Linux / macOS)

```bash
chmod +x setup.sh
./setup.sh
```

### Method B: Windows Setup

Double-click or run:
```cmd
start.bat
```

### Method C: Manual Setup

1. **Clone repository**:
   ```bash
   git clone https://github.com/example/indicwrite-ai.git
   cd indicwrite-ai
   ```

2. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```

3. **Install Node Dependencies & Launch Frontend**:
   ```bash
   npm install
   npm run dev
   ```

4. **Launch Python FastAPI Backend (Optional standalone mode)**:
   ```bash
   pip install -r backend/requirements.txt
   cd backend
   uvicorn app.main:app --port 8000 --reload
   ```

Open your browser at **`http://localhost:3000`**.

---

## 5. Environment Variables (`.env`)

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Optional supporting LLM API key | Obtain from [Google AI Studio](https://aistudio.google.com) |
| `GEMINI_MODEL` | Gemini model variant | `gemini-2.5-flash` |
| `BHARATGEN_API_KEY` | Optional BharatGen inference key | [HuggingFace BharatGen](https://huggingface.co/bharatgenai) |
| `BHARATGEN_MODEL_ENDPOINT`| BharatGen inference endpoint | Optional URL |
| `AI4BHARAT_INDICXLIT_ENDPOINT`| Remote IndicXlit server endpoint | Optional URL |
| `AI4BHARAT_INDICTRANS2_ENDPOINT`| Remote IndicTrans2 server endpoint | Optional URL |
| `BACKEND_PORT` | FastAPI backend port | `8000` |
| `FRONTEND_PORT` | Web preview port | `3000` |
| `FAISS_INDEX_PATH` | Local FAISS index file path | `storage/faiss/index.faiss` |
| `FAISS_METADATA_PATH` | Local metadata JSON file path | `storage/faiss/metadata.json` |
| `EMBEDDING_MODEL` | Hugging Face embedding model | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |

---

## 6. API Documentation

### 1. Transliteration
- **`POST /api/transliterate`**
  ```json
  // Request
  {
    "text": "Namaste, aap kaise hain?",
    "target_language": "hi"
  }
  // Response
  {
    "success": true,
    "source_text": "Namaste, aap kaise hain?",
    "target_language": "hi",
    "transliterated_text": "नमस्ते, आप कैसे हैं?",
    "provider": "AI4Bharat IndicXlit"
  }
  ```

### 2. Text Improvement
- **`POST /api/improve`**
  ```json
  // Request
  {
    "text": "हम जाएगा और काम करेगा",
    "mode": "grammar",
    "language": "hi",
    "provider_preference": "bharatgen"
  }
  // Response
  {
    "success": true,
    "original_text": "हम जाएगा और काम करेगा",
    "improved_text": "हम जाएंगे और काम करेंगे",
    "mode": "grammar",
    "provider_used": "BharatGen Param1 (Local Engine)",
    "explanation": "Corrected first-person plural verb agreement.",
    "changes": ["Corrected agreement (जाएगा -> जाएंगे)"]
  }
  ```

### 3. Translation
- **`POST /api/translate`**
  ```json
  // Request
  {
    "text": "Hello, how are you?",
    "source_language": "en",
    "target_language": "kn"
  }
  // Response
  {
    "success": true,
    "translated_text": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
    "provider": "AI4Bharat IndicTrans2"
  }
  ```

### 4. Knowledge Base & RAG
- **`POST /api/knowledge/upload`**: Uploads `.txt`, `.pdf`, or `.docx` document to chunk and index in FAISS.
- **`GET /api/knowledge/documents`**: Lists all indexed documents.
- **`DELETE /api/knowledge/documents/{id}`**: Removes document and reconstructs the FAISS index.
- **`POST /api/knowledge/query`**: Executes cosine similarity search and returns grounded answers with source citations.

### 5. Evaluation & System Status
- **`POST /api/evaluation/run`**: Executes all 36 test cases and computes real Character Error Rate (CER) and Word Accuracy.
- **`GET /api/system/status`**: Detailed health status of FAISS, Embeddings, AI4Bharat, BharatGen, and Gemini.
- **`GET /api/health`**: Simple health check.

---

## 7. Evaluation Methodology & Metrics

IndicWrite AI incorporates a dedicated evaluation module for academic assessment:

1. **Character Error Rate (CER)**:
   $$\text{CER} = \frac{S + D + I}{N}$$
   Where $S$ is substitutions, $D$ is deletions, $I$ is insertions, and $N$ is reference character count. Computed via Levenshtein dynamic programming.
2. **Word Accuracy**: Exact token-level match between reference and hypothesis tokens.
3. **RAG Groundedness**: Keyword and semantic overlap between the retrieved citations and the synthesized response to ensure zero hallucination.

The evaluation suite includes 36 ground-truth cases across Hindi, Kannada, Tamil, and English, with interactive CSV export.

---

## 8. Academic Context

- **Course**: CS3235 Undergraduate Mini-Project
- **Frameworks**: AI4Bharat IndicNLP, BharatGen LLM initiative, FAISS by Meta Research
- **License**: Apache-2.0
