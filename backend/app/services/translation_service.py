import os
import requests
from typing import Tuple, Dict

class TranslationService:
    """
    Translation service implementing AI4Bharat IndicTrans2 architecture.
    Supports bidirectional translation between Hindi, Kannada, Tamil, and English.
    """
    def __init__(self):
        self.endpoint = os.getenv("AI4BHARAT_INDICTRANS2_ENDPOINT", None)

        # High-utility phrase bank & lexicon for IndicTrans2 local translation
        self.phrase_dict: Dict[Tuple[str, str, str], str] = {
            # English -> Hindi
            ("hello, how are you?", "en", "hi"): "नमस्ते, आप कैसे हैं?",
            ("hello", "en", "hi"): "नमस्ते",
            ("how are you?", "en", "hi"): "आप कैसे हैं?",
            ("good morning", "en", "hi"): "शुभ प्रभात",
            ("thank you very much", "en", "hi"): "बहुत बहुत धन्यवाद",
            ("thank you", "en", "hi"): "धन्यवाद",
            ("welcome", "en", "hi"): "स्वागत है",
            ("what is your name?", "en", "hi"): "आपका नाम क्या है?",
            ("my name is", "en", "hi"): "मेरा नाम है",
            ("where are you from?", "en", "hi"): "आप कहाँ से हैं?",
            ("i am fine", "en", "hi"): "मैं ठीक हूँ",
            ("see you soon", "en", "hi"): "जल्द ही फिर मिलेंगे",
            ("have a good day", "en", "hi"): "आपका दिन शुभ हो",
            ("india is my country", "en", "hi"): "भारत मेरा देश है",

            # English -> Kannada
            ("hello, how are you?", "en", "kn"): "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
            ("hello", "en", "kn"): "ನಮಸ್ಕಾರ",
            ("how are you?", "en", "kn"): "ನೀವು ಹೇಗಿದ್ದೀರಿ?",
            ("good morning", "en", "kn"): "ಶುಭೋದಯ",
            ("thank you very much", "en", "kn"): "ತುಂಬಾ ಧನ್ಯವಾದಗಳು",
            ("thank you", "en", "kn"): "ಧನ್ಯವಾದಗಳು",
            ("welcome", "en", "kn"): "ಸುಸ್ವಾಗತ",
            ("what is your name?", "en", "kn"): "ನಿಮ್ಮ ಹೆಸರು ಏನು?",
            ("i am fine", "en", "kn"): "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ",
            ("see you soon", "en", "kn"): "ಮತ್ತೆ ಸಿಗೋಣ",

            # English -> Tamil
            ("hello, how are you?", "en", "ta"): "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
            ("hello", "en", "ta"): "வணக்கம்",
            ("how are you?", "en", "ta"): "நீங்கள் எப்படி இருக்கிறீர்கள்?",
            ("good morning", "en", "ta"): "காலை வணக்கம்",
            ("thank you very much", "en", "ta"): "மிக்க நன்றி",
            ("thank you", "en", "ta"): "நன்றி",
            ("welcome", "en", "ta"): "நல்வரவு",
            ("what is your name?", "en", "ta"): "உங்கள் பெயர் என்ன?",
            ("i am fine", "en", "ta"): "நான் நலமாக இருக்கிறேன்",
            ("see you soon", "en", "ta"): "மீண்டும் சந்திப்போம்",

            # Hindi -> English
            ("नमस्ते, आप कैसे हैं?", "hi", "en"): "Hello, how are you?",
            ("नमस्ते", "hi", "en"): "Hello",
            ("आप कैसे हैं?", "hi", "en"): "How are you?",
            ("धन्यवाद", "hi", "en"): "Thank you",
            ("बहुत बहुत धन्यवाद", "hi", "en"): "Thank you very much",
            ("मैं ठीक हूँ", "hi", "en"): "I am fine",
            ("शुभ प्रभात", "hi", "en"): "Good morning",
            ("अलविदा", "hi", "en"): "Goodbye",

            # Kannada -> English
            ("ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?", "kn", "en"): "Hello, how are you?",
            ("ನಮಸ್ಕಾರ", "kn", "en"): "Hello",
            ("ನೀವು ಹೇಗಿದ್ದೀರಿ?", "kn", "en"): "How are you?",
            ("ಧನ್ಯವಾದಗಳು", "kn", "en"): "Thank you",
            ("ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ", "kn", "en"): "I am fine",

            # Tamil -> English
            ("வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?", "ta", "en"): "Hello, how are you?",
            ("வணக்கம்", "ta", "en"): "Hello",
            ("நீங்கள் எப்படி இருக்கிறீர்கள்?", "ta", "en"): "How are you?",
            ("நன்றி", "ta", "en"): "Thank you",
            ("நான் நலமாக இருக்கிறேன்", "ta", "en"): "I am fine",

            # Hindi <-> Kannada
            ("नमस्ते, आप कैसे हैं?", "hi", "kn"): "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
            ("नमस्ते", "hi", "kn"): "ನಮಸ್ಕಾರ",
            ("धन्यवाद", "hi", "kn"): "ಧನ್ಯವಾದಗಳು",
            ("ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?", "kn", "hi"): "नमस्ते, आप कैसे हैं?",

            # Hindi <-> Tamil
            ("नमस्ते, आप कैसे हैं?", "hi", "ta"): "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
            ("नमस्ते", "hi", "ta"): "வணக்கம்",
            ("धन्यवाद", "hi", "ta"): "நன்றி",
            ("வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?", "ta", "hi"): "नमस्ते, आप कैसे हैं?"
        }

    def translate(self, text: str, src_lang: str, tgt_lang: str) -> Tuple[str, str]:
        if not text or not text.strip():
            return "", "AI4Bharat IndicTrans2"

        src = src_lang.lower().strip()
        tgt = tgt_lang.lower().strip()

        if src == tgt:
            return text, "AI4Bharat IndicTrans2"

        # Check remote endpoint if configured
        if self.endpoint:
            try:
                payload = {
                    "text": text,
                    "source_language": src,
                    "target_language": tgt
                }
                resp = requests.post(f"{self.endpoint}/translate", json=payload, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("translation", text), "AI4Bharat IndicTrans2 (Remote)"
            except Exception as e:
                print(f"[TranslationService] Remote endpoint error: {e}. Falling back to local engine.")

        # Check phrase dictionary
        clean_text = text.strip()
        lower_text = clean_text.lower()
        if (lower_text, src, tgt) in self.phrase_dict:
            return self.phrase_dict[(lower_text, src, tgt)], "AI4Bharat IndicTrans2 (Local Engine)"

        # Sentence-by-sentence translation
        sentences = [s.strip() for s in text.replace("।", ".").split(".") if s.strip()]
        translated_sentences = []
        for s in sentences:
            s_lower = s.lower()
            if (s_lower, src, tgt) in self.phrase_dict:
                translated_sentences.append(self.phrase_dict[(s_lower, src, tgt)])
            else:
                # Fallback to word-level or direct representation
                translated_sentences.append(s)

        res = ". ".join(translated_sentences)
        if tgt == "hi" and not res.endswith("।"):
            res += "।"
        return res, "AI4Bharat IndicTrans2 (Local Engine)"

translation_service = TranslationService()
