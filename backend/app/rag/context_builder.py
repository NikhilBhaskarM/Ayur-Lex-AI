from app.rag.retriever import RetrievedChunk

class ContextBuilder:
    def __init__(self, max_context_length: int = 4000):
        self.max_context_length = max_context_length

    def build_context(self, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "<context>\n</context>"
            
        context_parts = ["<context>"]
        
        for i, chunk in enumerate(chunks, 1):
            source = chunk.metadata.get("source_title") or chunk.metadata.get("source_name") or chunk.metadata.get("statute") or "Unknown Source"
            section = chunk.metadata.get("section", "")
            jurisdiction = chunk.metadata.get("jurisdiction", "")
            
            meta_str = f'id="{chunk.chunk_id}" source="{source}"'
            if section:
                meta_str += f' section="{section}"'
            if jurisdiction:
                meta_str += f' jurisdiction="{jurisdiction}"'
                
            chunk_xml = f'  <chunk {meta_str}>\n    {chunk.content}\n  </chunk>'
            context_parts.append(chunk_xml)
            
        context_parts.append("</context>")
        return "\n".join(context_parts)
