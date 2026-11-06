import os
import json
from typing import Dict, List, Any, Optional

class MetadataManager:
    """
    Manages document and chunk metadata persisted locally in JSON/SQLite.
    Maps FAISS integer vector IDs to DocumentChunkMetadata.
    """
    def __init__(self, metadata_path: str = "storage/faiss/metadata.json"):
        self.metadata_path = metadata_path
        self._ensure_dir()
        self.data: Dict[str, Any] = {
            "documents": {},
            "chunks": {},       # chunk_id -> metadata
            "id_to_chunk": {}   # str(vector_id) -> chunk_id
        }
        self.load()

    def _ensure_dir(self):
        dir_name = os.path.dirname(self.metadata_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

    def load(self):
        if os.path.exists(self.metadata_path):
            try:
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"[MetadataManager] Warning: failed to load {self.metadata_path}: {e}")
                self.save()
        else:
            self.save()

    def save(self):
        self._ensure_dir()
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_document(self, doc_id: str, doc_info: Dict[str, Any]):
        self.data["documents"][doc_id] = doc_info
        self.save()

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.data["documents"].get(doc_id)

    def list_documents(self) -> List[Dict[str, Any]]:
        return list(self.data["documents"].values())

    def remove_document(self, doc_id: str) -> List[int]:
        """
        Removes a document and all its chunks.
        Returns the list of vector IDs that were associated with this document.
        """
        if doc_id in self.data["documents"]:
            del self.data["documents"][doc_id]

        removed_vector_ids = []
        chunks_to_remove = []
        for chunk_id, chunk in self.data["chunks"].items():
            if chunk.get("doc_id") == doc_id:
                chunks_to_remove.append(chunk_id)

        # Clean id_to_chunk
        reverse_id_map = {v: k for k, v in self.data["id_to_chunk"].items()}
        for chunk_id in chunks_to_remove:
            if chunk_id in reverse_id_map:
                vid = int(reverse_id_map[chunk_id])
                removed_vector_ids.append(vid)
                del self.data["id_to_chunk"][str(vid)]
            del self.data["chunks"][chunk_id]

        self.save()
        return removed_vector_ids

    def register_chunk(self, vector_id: int, chunk_id: str, metadata: Dict[str, Any]):
        self.data["chunks"][chunk_id] = metadata
        self.data["id_to_chunk"][str(vector_id)] = chunk_id
        self.save()

    def get_chunk_by_vector_id(self, vector_id: int) -> Optional[Dict[str, Any]]:
        chunk_id = self.data["id_to_chunk"].get(str(vector_id))
        if chunk_id:
            return self.data["chunks"].get(chunk_id)
        return None

    def clear(self):
        self.data = {
            "documents": {},
            "chunks": {},
            "id_to_chunk": {}
        }
        self.save()
