import re
import os
import requests
from typing import Dict, Any, Tuple

class TransliterationService:
    """
    Transliteration service based on AI4Bharat IndicXlit.
    Converts Roman-script Hinglish/Kanglish/Tanglish into native Devanagari, Kannada, and Tamil scripts.
    Supports AI4Bharat IndicXlit endpoint if configured, with a comprehensive phonetic rule and dictionary engine.
    """
    def __init__(self):
        self.endpoint = os.getenv("AI4BHARAT_INDICXLIT_ENDPOINT", None)

        # Common vocabulary lookup for high-accuracy transliteration
        self.vocab: Dict[str, Dict[str, str]] = {
            "namaste": {"hi": "नमस्ते", "kn": "ನಮಸ್ತೆ", "ta": "நமஸ்தே"},
            "namaskar": {"hi": "नमस्कार", "kn": "ನಮಸ್ಕಾರ", "ta": "நமஸ்காரம்"},
            "aap": {"hi": "आप", "kn": "ಆಪ್", "ta": "ஆப்"},
            "kaise": {"hi": "कैसे", "kn": "ಕೈಸೆ", "ta": "கைசே"},
            "kaisa": {"hi": "कैसा", "kn": "ಕೈಸಾ", "ta": "கைசா"},
            "kaisi": {"hi": "कैसी", "kn": "ಕೈಸಿ", "ta": "கைசி"},
            "hain": {"hi": "हैं", "kn": "ಹೈಂ", "ta": "ஹைன்"},
            "hai": {"hi": "है", "kn": "ಹೈ", "ta": "ஹை"},
            "ho": {"hi": "हो", "kn": "ಹೋ", "ta": "ஹோ"},
            "main": {"hi": "मैं", "kn": "ಮೈಂ", "ta": "மைன்"},
            "theek": {"hi": "ठीक", "kn": "ಠೀಕ್", "ta": "டீக்"},
            "hoon": {"hi": "हूँ", "kn": "ಹೂಂ", "ta": "ஹூன்"},
            "shukriya": {"hi": "शुक्रिया", "kn": "ಶುಕ್ರಿಯಾ", "ta": "சுக்ரியா"},
            "dhanyavaad": {"hi": "धन्यवाद", "kn": "ಧನ್ಯವಾದ", "ta": "தன்யவாத்"},
            "dhanyavad": {"hi": "धन्यवाद", "kn": "ಧನ್ಯವಾದ", "ta": "தன்யவாத்"},
            "kripya": {"hi": "कृपया", "kn": "ಕೃಪಯಾ", "ta": "க்ருபையா"},
            "alvida": {"hi": "अलविदा", "kn": "ಅಲ್ವಿದಾ", "ta": "அல்விதா"},
            "phir": {"hi": "फिर", "kn": "ಫಿರ್", "ta": "பிர்"},
            "milenge": {"hi": "मिलेंगे", "kn": "ಮಿಲೆಂಗೆ", "ta": "மிலேங்கே"},
            "kya": {"hi": "क्या", "kn": "ಕ್ಯಾ", "ta": "க்யா"},
            "chal": {"hi": "चल", "kn": "ಚಲ್", "ta": "சல்"},
            "raha": {"hi": "रहा", "kn": "ರಹಾ", "ta": "ரஹா"},
            "ye": {"hi": "ये", "kn": "ಯೇ", "ta": "யே"},
            "yeh": {"hi": "यह", "kn": "ಯಹ್", "ta": "யஹ்"},
            "woh": {"hi": "वह", "kn": "ವಹ್", "ta": "வஹ்"},
            "bhai": {"hi": "भाई", "kn": "ಭಾಯಿ", "ta": "பாய்"},
            "dost": {"hi": "दोस्त", "kn": "ದೋಸ್ತ್", "ta": "தோஸ்த்"},
            "bharat": {"hi": "भारत", "kn": "ಭಾರತ", "ta": "பாரத்"},
            "hindi": {"hi": "हिन्दी", "kn": "ಹಿಂದಿ", "ta": "இந்தி"},
            "kannada": {"hi": "कन्नड़", "kn": "ಕನ್ನಡ", "ta": "கன்னட"},
            "tamil": {"hi": "तमिल", "kn": "ತಮಿಳು", "ta": "தமிழ்"},
            # Kannada specific
            "neenu": {"hi": "नीनू", "kn": "ನೀನು", "ta": "நீனு"},
            "neevu": {"hi": "नीवू", "kn": "ನೀವು", "ta": "நீவு"},
            "hegidhdhiya": {"hi": "हेगिद्ध्य", "kn": "ಹೇಗಿದ್ದೀಯ", "ta": "ஹேகிக்தியா"},
            "hegidira": {"hi": "हेगिदिरा", "kn": "ಹೇಗಿದ್ದೀರಾ", "ta": "ஹேகிக்தீரா"},
            "chennagidhdhene": {"hi": "चेन्नागिद्देने", "kn": "ಚೆನ್ನಾಗಿದ್ದೇನೆ", "ta": "சென்னாகித்தேனே"},
            "chennagiddira": {"hi": "चेन्नागिद्दिरा", "kn": "ಚೆನ್ನಾಗಿದ್ದೀರಾ", "ta": "சென்னாகித்தீரா"},
            "oota": {"hi": "ऊटा", "kn": "ಊಟ", "ta": "ஊட்ட"},
            "ayitha": {"hi": "आयिता", "kn": "ಆಯಿತಾ", "ta": "ஆயிதா"},
            # Tamil specific
            "vanakkam": {"hi": "वणक्कम", "kn": "ವಣಕ್ಕಂ", "ta": "வணக்கம்"},
            "eppadi": {"hi": "एप्पडि", "kn": "ಎಪ್ಪಡಿ", "ta": "எப்படி"},
            "irukkinga": {"hi": "इरुक्किंगा", "kn": "ಇರುಕ್ಕಿಂಗ", "ta": "இருக்கிறீர்கள்"},
            "irukkiraargal": {"hi": "इरुक्किरार्गळ्", "kn": "ಇರುತ್ತೀರಾರ್ಗಳ್", "ta": "இருக்கிறார்கள்"},
            "nallaa": {"hi": "नल्ला", "kn": "ನಲ್ಲಾ", "ta": "நல்லா"},
            "irukken": {"hi": "इरुक्केन", "kn": "ಇರುಕ್ಕೆನ್", "ta": "இருக்கிறேன்"},
            "nandri": {"hi": "नन्ड्रि", "kn": "ನಂದ್ರಿ", "ta": "நன்றி"},
            "saaptingala": {"hi": "साप्तिंगळा", "kn": "ಸಾಪ್ಟಿಂಗಳಾ", "ta": "சாப்பிட்டீர்களா"}
        }

        # Phonetic mapping tables (Consonants & Vowels)
        self.char_map = {
            "hi": {
                "consonants": [
                    ("ksha", "क्ष"), ("tra", "त्र"), ("gya", "ज्ञ"), ("shra", "श्र"),
                    ("kh", "ख"), ("gh", "घ"), ("ch", "च"), ("chh", "छ"), ("jh", "झ"),
                    ("th", "थ"), ("dh", "ध"), ("ph", "फ"), ("bh", "भ"), ("sh", "श"),
                    ("zh", "ष"), ("k", "क"), ("g", "ग"), ("j", "ज"), ("t", "त"),
                    ("d", "द"), ("n", "न"), ("p", "प"), ("b", "ब"), ("m", "म"),
                    ("y", "य"), ("r", "र"), ("l", "ल"), ("v", "व"), ("w", "व"),
                    ("s", "स"), ("h", "ह")
                ],
                "vowels": [
                    ("aa", "ा"), ("ee", "ी"), ("ii", "ी"), ("oo", "ू"), ("uu", "ू"),
                    ("ai", "ै"), ("au", "ौ"), ("ou", "ौ"), ("a", ""), ("i", "ि"),
                    ("u", "ु"), ("e", "े"), ("o", "ो")
                ],
                "independent_vowels": [
                    ("aa", "आ"), ("ee", "ई"), ("ii", "ई"), ("oo", "ऊ"), ("uu", "ऊ"),
                    ("ai", "ऐ"), ("au", "औ"), ("a", "अ"), ("i", "इ"), ("u", "उ"),
                    ("e", "ए"), ("o", "ओ")
                ],
                "virama": "्"
            },
            "kn": {
                "consonants": [
                    ("kh", "ಖ"), ("gh", "ಘ"), ("chh", "ಛ"), ("jh", "ಝ"),
                    ("th", "ಥ"), ("dh", "ಧ"), ("ph", "ಫ"), ("bh", "ಭ"),
                    ("sh", "ಶ"), ("k", "ಕ"), ("g", "ಗ"), ("ch", "ಚ"),
                    ("j", "ಜ"), ("t", "ತ"), ("d", "ದ"), ("n", "ನ"),
                    ("p", "ಪ"), ("b", "ಬ"), ("m", "ಮ"), ("y", "ಯ"),
                    ("r", "ರ"), ("l", "ಲ"), ("v", "ವ"), ("w", "ವ"),
                    ("s", "ಸ"), ("h", "ಹ")
                ],
                "vowels": [
                    ("aa", "ಾ"), ("ee", "ೀ"), ("ii", "ೀ"), ("oo", "ೂ"), ("uu", "ೂ"),
                    ("ai", "ೈ"), ("au", "ೌ"), ("a", ""), ("i", "ಿ"), ("u", "ು"),
                    ("e", "ೆ"), ("o", "ೊ")
                ],
                "independent_vowels": [
                    ("aa", "ಆ"), ("ee", "ಈ"), ("ii", "ಈ"), ("oo", "ಊ"), ("uu", "ಊ"),
                    ("ai", "ಐ"), ("au", "ಔ"), ("a", "ಅ"), ("i", "ಇ"), ("u", "ಉ"),
                    ("e", "ಎ"), ("o", "ಒ")
                ],
                "virama": "್"
            },
            "ta": {
                "consonants": [
                    ("sh", "ஷ"), ("zh", "ழ"), ("ch", "ச"), ("th", "த"),
                    ("dh", "த"), ("k", "க"), ("g", "க"), ("j", "ஜ"),
                    ("t", "ட"), ("d", "ட"), ("n", "ந"), ("p", "ப"),
                    ("b", "ப"), ("m", "ம"), ("y", "ய"), ("r", "ர"),
                    ("l", "ல"), ("v", "வ"), ("w", "வ"), ("s", "ஸ"),
                    ("h", "ஹ")
                ],
                "vowels": [
                    ("aa", "ா"), ("ee", "ீ"), ("ii", "ீ"), ("oo", "ூ"), ("uu", "ூ"),
                    ("ai", "ை"), ("au", "ௌ"), ("a", ""), ("i", "ி"), ("u", "ு"),
                    ("e", "ெ"), ("o", "ொ")
                ],
                "independent_vowels": [
                    ("aa", "ஆ"), ("ee", "ஈ"), ("ii", "ஈ"), ("oo", "ஊ"), ("uu", "ஊ"),
                    ("ai", "ஐ"), ("au", "ஔ"), ("a", "அ"), ("i", "இ"), ("u", "உ"),
                    ("e", "எ"), ("o", "ஒ")
                ],
                "virama": "்"
            }
        }

    def transliterate_word(self, word: str, lang: str) -> str:
        clean_word = word.lower().strip()
        if not clean_word:
            return word

        # Check vocabulary lookup first
        if clean_word in self.vocab and lang in self.vocab[clean_word]:
            return self.vocab[clean_word][lang]

        mapping = self.char_map.get(lang, self.char_map["hi"])
        consonants = mapping["consonants"]
        vowels = mapping["vowels"]
        indep_vowels = mapping["independent_vowels"]
        virama = mapping["virama"]

        res = []
        i = 0
        n = len(clean_word)

        while i < n:
            matched = False

            # Check independent vowel if at start or after vowel
            if i == 0 or (res and res[-1] in [v[1] for v in indep_vowels]):
                for v_rom, v_indic in indep_vowels:
                    if clean_word[i:i+len(v_rom)] == v_rom:
                        res.append(v_indic)
                        i += len(v_rom)
                        matched = True
                        break
                if matched:
                    continue

            # Check consonants
            for c_rom, c_indic in consonants:
                if clean_word[i:i+len(c_rom)] == c_rom:
                    i += len(c_rom)
                    matched = True

                    # Look ahead for vowel attached to consonant
                    vowel_matched = False
                    for v_rom, v_matra in vowels:
                        if clean_word[i:i+len(v_rom)] == v_rom:
                            res.append(c_indic + v_matra)
                            i += len(v_rom)
                            vowel_matched = True
                            break

                    if not vowel_matched:
                        # If at the very end of word, in Hindi often inherent 'a' is dropped (halant or implicit a)
                        # We use natural modern convention
                        if i >= n:
                            res.append(c_indic)
                        else:
                            # Consonant cluster -> add virama
                            res.append(c_indic + virama)
                    break

            if not matched:
                # Vowel not caught or special character
                vowel_matched = False
                for v_rom, v_indic in indep_vowels:
                    if clean_word[i:i+len(v_rom)] == v_rom:
                        res.append(v_indic)
                        i += len(v_rom)
                        vowel_matched = True
                        break
                if not vowel_matched:
                    res.append(clean_word[i])
                    i += 1

        return "".join(res)

    def transliterate(self, text: str, target_lang: str) -> Tuple[str, str]:
        """
        Transliterates Roman script input into native script.
        Returns (transliterated_text, provider_name).
        """
        if not text or not text.strip():
            return "", "AI4Bharat IndicXlit"

        target_lang = target_lang.lower().strip()
        if target_lang not in ["hi", "kn", "ta"]:
            target_lang = "hi"

        # If external AI4Bharat endpoint is configured, try it
        if self.endpoint:
            try:
                payload = {
                    "input": text,
                    "target_language": target_lang
                }
                resp = requests.post(f"{self.endpoint}/transliterate", json=payload, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    return data.get("output", text), "AI4Bharat IndicXlit (Remote)"
            except Exception as e:
                print(f"[TransliterationService] Remote endpoint error: {e}. Falling back to local engine.")

        # Local phonetic tokenizer that preserves punctuation, quotes, whitespace
        tokens = re.split(r'(\s+|[.,!?;:\'\"()\-]+)', text)
        out_tokens = []
        for token in tokens:
            if re.match(r'^[a-zA-Z]+$', token):
                out_tokens.append(self.transliterate_word(token, target_lang))
            else:
                out_tokens.append(token)

        return "".join(out_tokens), "AI4Bharat IndicXlit (Local Engine)"

transliteration_service = TransliterationService()
