from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Chunk:
    content: str
    chunk_index: int
    metadata: dict

class TextChunker:
    def chunk_text(self, text: str, chunk_size: int = 512, chunk_overlap: int = 50, metadata: Optional[dict] = None) -> List[Chunk]:
        # Simplistic recursive character splitting
        # In a real scenario, use langchain text splitter or similar
        chunks = []
        start = 0
        text_len = len(text)
        index = 0
        
        while start < text_len:
            end = min(start + chunk_size, text_len)
            chunks.append(Chunk(
                content=text[start:end],
                chunk_index=index,
                metadata=metadata or {}
            ))
            start += (chunk_size - chunk_overlap)
            index += 1
            
        return chunks
