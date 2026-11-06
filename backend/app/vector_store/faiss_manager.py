import os
import json
import numpy as np
from typing import List, Tuple, Dict, Any, Optional

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False
    print("[FAISSManager] Notice: faiss-cpu not installed in Python environment, using high-performance NumPy IndexFlatIP fallback.")

class FAISSManager:
    """
    Manages FAISS vector indexing with disk persistence and mapping.
    Uses IndexFlatIP with L2 normalized vectors for exact cosine similarity search.
    """
    def __init__(self, index_path: str = "storage/faiss/index.faiss", dimension: int = 384):
        self.index_path = index_path
        self.dimension = dimension
        self.index = None
        # In-memory vector array for fallback when faiss C library is loading or not installed
        self._vectors: Optional[np.ndarray] = None
        self._ensure_dir()
        self.initialize_index()

    def _ensure_dir(self):
        dir_name = os.path.dirname(self.index_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

    def initialize_index(self):
        if HAS_FAISS:
            if os.path.exists(self.index_path) and os.path.getsize(self.index_path) > 0:
                try:
                    self.index = faiss.read_index(self.index_path)
                    print(f"[FAISSManager] Loaded existing FAISS index from {self.index_path} with {self.index.ntotal} vectors.")
                    return
                except Exception as e:
                    print(f"[FAISSManager] Could not read index from {self.index_path}: {e}. Creating new index.")
            self.index = faiss.IndexFlatIP(self.dimension)
            self.save()
        else:
            # NumPy fallback persistence
            npy_path = self.index_path.replace(".faiss", ".npy")
            if os.path.exists(npy_path):
                try:
                    self._vectors = np.load(npy_path)
                    print(f"[FAISSManager-Fallback] Loaded {len(self._vectors)} vectors from {npy_path}.")
                    return
                except Exception as e:
                    print(f"[FAISSManager-Fallback] Error loading {npy_path}: {e}")
            self._vectors = np.empty((0, self.dimension), dtype=np.float32)

    def count(self) -> int:
        if HAS_FAISS and self.index is not None:
            return self.index.ntotal
        elif self._vectors is not None:
            return len(self._vectors)
        return 0

    def add_vectors(self, vectors: np.ndarray) -> List[int]:
        """
        Normalizes vectors to unit L2 norm and adds them to the FAISS index.
        Returns the assigned vector IDs [start_id, ..., end_id].
        """
        if len(vectors) == 0:
            return []

        vectors = np.array(vectors, dtype=np.float32)
        # L2 normalize for cosine similarity via inner product
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        normalized_vectors = vectors / norms

        start_id = self.count()
        count = len(normalized_vectors)

        if HAS_FAISS and self.index is not None:
            self.index.add(normalized_vectors)
            self.save()
        else:
            if self._vectors is None or len(self._vectors) == 0:
                self._vectors = normalized_vectors
            else:
                self._vectors = np.vstack([self._vectors, normalized_vectors])
            self._save_numpy()

        return list(range(start_id, start_id + count))

    def search(self, query_vector: np.ndarray, top_k: int = 3) -> List[Tuple[int, float]]:
        """
        Returns list of (vector_id, similarity_score) sorted by descending similarity.
        """
        if self.count() == 0:
            return []

        query = np.array(query_vector, dtype=np.float32).reshape(1, -1)
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        top_k = min(top_k, self.count())

        if HAS_FAISS and self.index is not None:
            distances, indices = self.index.search(query, top_k)
            results = []
            for idx, score in zip(indices[0], distances[0]):
                if idx != -1:
                    results.append((int(idx), float(score)))
            return results
        else:
            # NumPy inner product
            scores = np.dot(self._vectors, query.T).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            return [(int(idx), float(scores[idx])) for idx in top_indices]

    def reset(self):
        if HAS_FAISS:
            self.index = faiss.IndexFlatIP(self.dimension)
            self.save()
        else:
            self._vectors = np.empty((0, self.dimension), dtype=np.float32)
            self._save_numpy()

    def save(self):
        self._ensure_dir()
        if HAS_FAISS and self.index is not None:
            try:
                faiss.write_index(self.index, self.index_path)
            except Exception as e:
                print(f"[FAISSManager] Warning: failed to save index to {self.index_path}: {e}")

    def _save_numpy(self):
        self._ensure_dir()
        npy_path = self.index_path.replace(".faiss", ".npy")
        try:
            if self._vectors is not None:
                np.save(npy_path, self._vectors)
        except Exception as e:
            print(f"[FAISSManager-Fallback] Warning: failed to save {npy_path}: {e}")
