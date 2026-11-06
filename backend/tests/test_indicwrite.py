import os
import pytest
from app.services.transliteration_service import transliteration_service
from app.services.translation_service import translation_service
from app.services.improvement_service import improvement_service
from app.services.embedding_service import embedding_service
from app.services.rag_service import rag_service
from app.services.evaluation_service import evaluation_service, calculate_cer, calculate_word_accuracy

def test_transliteration_hindi():
    text = "Namaste, aap kaise hain?"
    out, provider = transliteration_service.transliterate(text, "hi")
    assert "नमस्ते" in out or "न" in out
    assert provider is not None

def test_transliteration_kannada():
    text = "Namaskara, neevu hegidira?"
    out, provider = transliteration_service.transliterate(text, "kn")
    assert "ನಮಸ್ಕಾರ" in out or "ನ" in out

def test_transliteration_tamil():
    text = "Vanakkam, eppadi irukkinga?"
    out, provider = transliteration_service.transliterate(text, "ta")
    assert "வணக்கம்" in out or "வ" in out

def test_translation_en_to_hi():
    text = "Hello, how are you?"
    out, provider = translation_service.translate(text, "en", "hi")
    assert "नमस्ते" in out or "आप कैसे हैं" in out

def test_translation_hi_to_en():
    text = "नमस्ते, आप कैसे हैं?"
    out, provider = translation_service.translate(text, "hi", "en")
    assert "Hello" in out or "how are you" in out.lower()

def test_improvement_formal_tone():
    text = "तुम यहाँ आओ"
    res = improvement_service.improve_text(text, mode="formal", language="hi")
    assert "आप" in res["improved_text"]

def test_improvement_grammar():
    text = "हम जाएगा"
    res = improvement_service.improve_text(text, mode="grammar", language="hi")
    assert "जाएंगे" in res["improved_text"]

def test_embedding_generation():
    texts = ["नमस्ते", "Hello world", "ನಮಸ್ಕಾರ"]
    embs = embedding_service.embed_texts(texts)
    assert len(embs) == 3
    assert embs.shape[1] == 384

def test_faiss_indexing_and_search():
    doc_info = rag_service.ingest_text(
        filename="test_guide.txt",
        text_content="Hindi honorific uses 'Aap' for respectful conversation with elders.",
        file_type="txt"
    )
    assert doc_info["id"] is not None
    assert rag_service.faiss_manager.count() > 0

    res = rag_service.query("What pronoun is used for respectful Hindi conversation?", top_k=2)
    assert len(res["citations"]) > 0

    # Test document deletion
    deleted = rag_service.delete_document(doc_info["id"])
    assert deleted is True

def test_cer_calculation():
    ref = "नमस्ते"
    hyp = "नमस्ते"
    assert calculate_cer(ref, hyp) == 0.0

    hyp_diff = "नमस्तेजी"
    assert calculate_cer(ref, hyp_diff) > 0.0

def test_word_accuracy():
    ref = "aap kaise hain"
    hyp = "aap kaise hain"
    assert calculate_word_accuracy(ref, hyp) == 1.0

def test_evaluation_suite():
    res = evaluation_service.run_all()
    assert res["total_tests"] >= 30
    assert "average_cer" in res
    assert "results" in res
