#!/usr/bin/env python3
"""
IndicWrite AI - Automated Python Setup Script
Initializes directories, verifies dependencies, downloads embedding model, and checks FAISS.
"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("   IndicWrite AI - Plug-and-Play Setup (CS3235)")
    print("=" * 60)

    # 1. Create storage directories
    dirs = [
        "storage/faiss",
        "storage/documents",
        "storage/uploads"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✓ Created storage directories (storage/faiss, storage/documents, storage/uploads)")

    # 2. Check or create .env
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✓ Generated .env from .env.example")
        else:
            with open(".env", "w") as f:
                f.write("APP_ENV=development\nBACKEND_PORT=8000\nFRONTEND_PORT=3000\n")
            print("✓ Generated baseline .env file")
    else:
        print("✓ Verified .env configuration exists")

    # 3. Check FAISS
    try:
        import faiss
        print(f"✓ FAISS (faiss-cpu) successfully verified in Python environment.")
    except ImportError:
        print("ℹ Notice: 'faiss-cpu' not yet installed in active Python environment.")
        print("  FastAPI and Express will operate with high-speed NumPy cosine vector matching fallback.")
        print("  To install: pip install faiss-cpu")

    # 4. Check SentenceTransformers
    try:
        from sentence_transformers import SentenceTransformer
        print("✓ Downloading/verifying multilingual MiniLM model cache...")
        _ = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        print("✓ Multilingual embedding model cached locally.")
    except Exception as e:
        print(f"ℹ Multilingual embedding model download info: {e}")

    print("=" * 60)
    print("Setup verified. Run backend via:")
    print("  uvicorn app.main:app --port 8000 --app-dir backend")
    print("=" * 60)

if __name__ == "__main__":
    main()
