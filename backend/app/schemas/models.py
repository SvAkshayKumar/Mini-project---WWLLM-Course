from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TransliterateRequest(BaseModel):
    text: str = Field(..., description="Roman-script input text (Hinglish, Kanglish, Tanglish)")
    target_language: str = Field(..., description="Target language code: 'hi', 'kn', 'ta'")
    source_language: Optional[str] = Field("en", description="Source script/lang identifier")

class TransliterateResponse(BaseModel):
    success: bool
    source_text: str
    target_language: str
    transliterated_text: str
    provider: str
    details: Optional[Dict[str, Any]] = None

class ImproveRequest(BaseModel):
    text: str = Field(..., description="Text to be improved")
    mode: str = Field(
        "grammar",
        description="Improvement mode: 'grammar', 'professional', 'simple', 'formal', 'informal', 'clarity'"
    )
    language: Optional[str] = Field("hi", description="Language of text: 'hi', 'kn', 'ta', 'en'")
    provider_preference: Optional[str] = Field(
        "bharatgen",
        description="'bharatgen' (primary) or 'gemini' (supporting)"
    )

class ImproveResponse(BaseModel):
    success: bool
    original_text: str
    improved_text: str
    mode: str
    provider_used: str
    explanation: str
    changes: List[str] = []

class TranslateRequest(BaseModel):
    text: str = Field(..., description="Source text to translate")
    source_language: str = Field(..., description="'en', 'hi', 'kn', 'ta'")
    target_language: str = Field(..., description="'en', 'hi', 'kn', 'ta'")

class TranslateResponse(BaseModel):
    success: bool
    source_text: str
    source_language: str
    target_language: str
    translated_text: str
    provider: str

class ProcessPipelineRequest(BaseModel):
    text: str = Field(..., description="Roman script input")
    transliterate_lang: str = Field("hi", description="Language for transliteration")
    improve_mode: Optional[str] = Field(None, description="Optional improvement mode")
    translate_to: Optional[str] = Field(None, description="Optional translation target language")

class ProcessPipelineResponse(BaseModel):
    success: bool
    original_input: str
    transliterated: Optional[str] = None
    improved: Optional[str] = None
    translated: Optional[str] = None
    steps: List[Dict[str, Any]] = []

class DocumentChunkMetadata(BaseModel):
    chunk_id: str
    doc_id: str
    doc_name: str
    chunk_index: int
    text: str
    char_count: int

class DocumentInfo(BaseModel):
    id: str
    name: str
    file_type: str
    total_chunks: int
    uploaded_at: str
    size_bytes: int

class KnowledgeQueryRequest(BaseModel):
    query: str = Field(..., description="User query or context question")
    top_k: int = Field(3, description="Number of context chunks to retrieve")
    language: Optional[str] = Field(None, description="Optional target language filter")

class KnowledgeCitation(BaseModel):
    doc_name: str
    chunk_index: int
    similarity_score: float
    snippet: str

class KnowledgeQueryResponse(BaseModel):
    success: bool
    query: str
    answer: str
    citations: List[KnowledgeCitation]
    provider_used: str

class SystemComponentStatus(BaseModel):
    name: str
    status: str  # 'ready', 'connected', 'fallback', 'not_configured', 'error'
    provider: str
    details: str
    is_required: bool
    env_var: Optional[str] = None
    doc_url: Optional[str] = None

class SystemStatusResponse(BaseModel):
    faiss_status: SystemComponentStatus
    embedding_status: SystemComponentStatus
    indicxlit_status: SystemComponentStatus
    indictrans2_status: SystemComponentStatus
    bharatgen_status: SystemComponentStatus
    gemini_status: SystemComponentStatus
    total_indexed_documents: int
    total_vector_chunks: int

class EvaluationTestCase(BaseModel):
    id: str
    category: str  # 'transliteration', 'translation', 'improvement', 'rag'
    language: str
    input_text: str
    expected_output: str
    actual_output: Optional[str] = None
    cer: Optional[float] = None
    word_accuracy: Optional[float] = None
    status: Optional[str] = "pending"  # 'passed', 'failed', 'pending'
    failure_reason: Optional[str] = None

class EvaluationRunResponse(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    average_cer: float
    average_word_accuracy: float
    results: List[EvaluationTestCase]
    duration_ms: float
