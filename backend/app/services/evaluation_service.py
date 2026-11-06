import time
from typing import List, Dict, Any, Tuple

from app.services.transliteration_service import transliteration_service
from app.services.translation_service import translation_service
from app.services.improvement_service import improvement_service

def calculate_cer(reference: str, hypothesis: str) -> float:
    """
    Computes Character Error Rate (CER) via Levenshtein distance:
    CER = (S + D + I) / N
    """
    ref = reference.strip()
    hyp = hypothesis.strip()
    if not ref:
        return 0.0 if not hyp else 1.0

    r_len, h_len = len(ref), len(hyp)
    dp = [[0] * (h_len + 1) for _ in range(r_len + 1)]

    for i in range(r_len + 1):
        dp[i][0] = i
    for j in range(h_len + 1):
        dp[0][j] = j

    for i in range(1, r_len + 1):
        for j in range(1, h_len + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    dist = dp[r_len][h_len]
    return min(1.0, dist / max(1, r_len))

def calculate_word_accuracy(reference: str, hypothesis: str) -> float:
    """
    Computes exact word match accuracy between tokenized strings.
    """
    ref_words = reference.strip().split()
    hyp_words = hypothesis.strip().split()
    if not ref_words:
        return 1.0 if not hyp_words else 0.0

    matches = sum(1 for r, h in zip(ref_words, hyp_words) if r == h)
    return matches / max(len(ref_words), len(hyp_words))

class EvaluationService:
    """
    Evaluation suite for IndicWrite AI with 36 curated test cases across Hindi, Kannada, Tamil.
    Evaluates CER, word accuracy, translation fidelity, and RAG groundedness.
    """
    def __init__(self):
        # 36 Ground-Truth Evaluation Test Cases
        self.test_cases: List[Dict[str, Any]] = [
            # === Hindi Transliteration Test Cases ===
            {
                "id": "TC-HI-01",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Namaste, aap kaise hain?",
                "expected_output": "नमस्ते, आप कैसे हैं?"
            },
            {
                "id": "TC-HI-02",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Main theek hoon, dhanyavaad.",
                "expected_output": "मैं ठीक हूँ, धन्यवाद।"
            },
            {
                "id": "TC-HI-03",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Bharat mera pyara desh hai.",
                "expected_output": "भारत मेरा प्यारा देश है।"
            },
            {
                "id": "TC-HI-04",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Aapka shubh naam kya hai?",
                "expected_output": "आपका शुभ नाम क्या है?"
            },
            {
                "id": "TC-HI-05",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Shukriya dost, phir milenge.",
                "expected_output": "शुक्रिया दोस्त, फिर मिलेंगे।"
            },
            {
                "id": "TC-HI-06",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Kripya yahan aaiye aur baithiye.",
                "expected_output": "कृपया यहाँ आइए और बैठिए।"
            },
            {
                "id": "TC-HI-07",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Yeh pustak bahut acchi hai.",
                "expected_output": "यह पुस्तक बहुत अच्छी है।"
            },
            {
                "id": "TC-HI-08",
                "category": "transliteration",
                "language": "hi",
                "input_text": "Subah ka samay suhavana hota hai.",
                "expected_output": "सुबह का समय सुहावना होता है।"
            },

            # === Kannada Transliteration Test Cases ===
            {
                "id": "TC-KN-01",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Namaskara, neevu hegidira?",
                "expected_output": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಾ?"
            },
            {
                "id": "TC-KN-02",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Naanu chennagiddene, dhanyavadagalu.",
                "expected_output": "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ, ಧನ್ಯವಾದಗಳು."
            },
            {
                "id": "TC-KN-03",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Ninna hesaru enu?",
                "expected_output": "ನಿನ್ನ ಹೆಸರು ಏನು?"
            },
            {
                "id": "TC-KN-04",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Oota ayitha?",
                "expected_output": "ಊಟ ಆಯಿತಾ?"
            },
            {
                "id": "TC-KN-05",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Banni, banni, kootkoli.",
                "expected_output": "ಬನ್ನಿ, ಬನ್ನಿ, ಕೂತ್ಕೊಳ್ಳಿ."
            },
            {
                "id": "TC-KN-06",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Matte sigona.",
                "expected_output": "ಮತ್ತೆ ಸಿಗೋಣ."
            },
            {
                "id": "TC-KN-07",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Kannada nanna matrubhashe.",
                "expected_output": "ಕನ್ನಡ ನನ್ನ ಮಾತೃಭಾಷೆ."
            },
            {
                "id": "TC-KN-08",
                "category": "transliteration",
                "language": "kn",
                "input_text": "Bengaluru sundara nagara.",
                "expected_output": "ಬೆಂಗಳೂರು ಸುಂದರ ನಗರ."
            },

            # === Tamil Transliteration Test Cases ===
            {
                "id": "TC-TA-01",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Vanakkam, eppadi irukkinga?",
                "expected_output": "வணக்கம், எப்படி இருக்கிறீர்கள்?"
            },
            {
                "id": "TC-TA-02",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Naan nallaa irukken, nandri.",
                "expected_output": "நான் நல்லா இருக்கேன், நன்றி."
            },
            {
                "id": "TC-TA-03",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Unga peyar enna?",
                "expected_output": "உங்கள் பெயர் என்ன?"
            },
            {
                "id": "TC-TA-04",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Saaptingala?",
                "expected_output": "சாப்பிட்டீர்களா?"
            },
            {
                "id": "TC-TA-05",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Meendum santhippom.",
                "expected_output": "மீண்டும் சந்திப்போம்."
            },
            {
                "id": "TC-TA-06",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Romba nandri thozhar.",
                "expected_output": "ரொம்ப நன்றி தோழர்."
            },
            {
                "id": "TC-TA-07",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Tamil semmozhi aagum.",
                "expected_output": "தமிழ் செம்மொழி ஆகும்."
            },
            {
                "id": "TC-TA-08",
                "category": "transliteration",
                "language": "ta",
                "input_text": "Kaalai vanakkam anbarghaley.",
                "expected_output": "காலை வணக்கம் அன்பர்களே."
            },

            # === Translation Test Cases ===
            {
                "id": "TC-TR-01",
                "category": "translation",
                "language": "en -> hi",
                "input_text": "Hello, how are you?",
                "expected_output": "नमस्ते, आप कैसे हैं?"
            },
            {
                "id": "TC-TR-02",
                "category": "translation",
                "language": "en -> kn",
                "input_text": "Hello, how are you?",
                "expected_output": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?"
            },
            {
                "id": "TC-TR-03",
                "category": "translation",
                "language": "en -> ta",
                "input_text": "Hello, how are you?",
                "expected_output": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?"
            },
            {
                "id": "TC-TR-04",
                "category": "translation",
                "language": "hi -> en",
                "input_text": "नमस्ते, आप कैसे हैं?",
                "expected_output": "Hello, how are you?"
            },
            {
                "id": "TC-TR-05",
                "category": "translation",
                "language": "kn -> en",
                "input_text": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
                "expected_output": "Hello, how are you?"
            },
            {
                "id": "TC-TR-06",
                "category": "translation",
                "language": "ta -> en",
                "input_text": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
                "expected_output": "Hello, how are you?"
            },

            # === Text Improvement Test Cases ===
            {
                "id": "TC-IMP-01",
                "category": "improvement",
                "language": "hi (formal)",
                "input_text": "तुम यहाँ आओ और बैठो",
                "expected_output": "आप यहाँ आइए और बैठिए"
            },
            {
                "id": "TC-IMP-02",
                "category": "improvement",
                "language": "hi (grammar)",
                "input_text": "हम जाएगा और काम करेगा",
                "expected_output": "हम जाएंगे और काम करेंगे"
            },
            {
                "id": "TC-IMP-03",
                "category": "improvement",
                "language": "hi (simple)",
                "input_text": "अविलंब वार्तालाप प्रारंभ करें",
                "expected_output": "तुरंत बातचीत प्रारंभ करें"
            },

            # === RAG Groundedness Test Cases ===
            {
                "id": "TC-RAG-01",
                "category": "rag",
                "language": "hi",
                "input_text": "What is the formal honorific rule in Hindi?",
                "expected_output": "Use 'आप' (Aap) with plural verb endings such as 'हैं' (hain) or 'करते हैं'."
            },
            {
                "id": "TC-RAG-02",
                "category": "rag",
                "language": "kn",
                "input_text": "What does 'ನೀವು' mean in Kannada?",
                "expected_output": "Formal address meaning you (respectful/plural), while 'ನೀನು' is informal singular."
            },
            {
                "id": "TC-RAG-03",
                "category": "rag",
                "language": "ta",
                "input_text": "What is the standard Tamil polite greeting?",
                "expected_output": "Formal greeting is 'வணக்கம்' (Vanakkam)."
            }
        ]

    def run_all(self) -> Dict[str, Any]:
        """
        Executes all evaluation test cases against the live AI services.
        Computes real CER, Word Accuracy, and pass/fail thresholds.
        """
        start_time = time.time()
        results = []
        total_cer = 0.0
        total_word_acc = 0.0
        passed = 0
        failed = 0

        for tc in self.test_cases:
            cat = tc["category"]
            input_t = tc["input_text"]
            exp = tc["expected_output"]
            actual = ""
            fail_reason = None

            try:
                if cat == "transliteration":
                    lang = tc["language"]
                    actual, _ = transliteration_service.transliterate(input_t, lang)
                elif cat == "translation":
                    parts = tc["language"].split(" -> ")
                    src, tgt = parts[0], parts[1]
                    actual, _ = translation_service.translate(input_t, src, tgt)
                elif cat == "improvement":
                    lang_tag = tc["language"].split()[0]
                    mode = "formal" if "formal" in tc["language"] else "grammar" if "grammar" in tc["language"] else "simple"
                    res = improvement_service.improve_text(input_t, mode=mode, language=lang_tag)
                    actual = res.get("improved_text", "")
                elif cat == "rag":
                    # Evaluate RAG groundedness
                    from app.services.rag_service import rag_service
                    res = rag_service.query(input_t, top_k=2)
                    actual = res.get("answer", "")
            except Exception as e:
                actual = ""
                fail_reason = f"Execution exception: {str(e)}"

            cer = calculate_cer(exp, actual)
            w_acc = calculate_word_accuracy(exp, actual)

            # Transliteration/translation passing threshold: CER <= 0.35 or word acc >= 0.65
            # For RAG, grounded keyword presence
            is_pass = False
            if cat == "rag":
                # Check for expected substring keywords
                keywords = [w for w in exp.split() if len(w) > 3]
                matched_kws = sum(1 for kw in keywords if kw.lower() in actual.lower())
                is_pass = (matched_kws >= 1) or cer <= 0.65
            else:
                is_pass = (cer <= 0.35) or (w_acc >= 0.60)

            if is_pass:
                status = "passed"
                passed += 1
            else:
                status = "failed"
                failed += 1
                if not fail_reason:
                    fail_reason = f"Output divergence: CER={cer:.3f}, WordAcc={w_acc:.3f}"

            total_cer += cer
            total_word_acc += w_acc

            results.append({
                "id": tc["id"],
                "category": cat,
                "language": tc["language"],
                "input_text": input_t,
                "expected_output": exp,
                "actual_output": actual,
                "cer": round(cer, 4),
                "word_accuracy": round(w_acc, 4),
                "status": status,
                "failure_reason": fail_reason
            })

        duration = round((time.time() - start_time) * 1000, 2)
        n = max(1, len(self.test_cases))

        return {
            "total_tests": len(self.test_cases),
            "passed_tests": passed,
            "failed_tests": failed,
            "average_cer": round(total_cer / n, 4),
            "average_word_accuracy": round(total_word_acc / n, 4),
            "results": results,
            "duration_ms": duration
        }

evaluation_service = EvaluationService()
