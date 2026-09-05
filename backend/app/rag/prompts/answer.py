ANSWER_PROMPT = """Based on the following retrieved legal and regulatory context, please answer the user's query.

<context>
{context}
</context>

Target Jurisdiction: {jurisdiction}
User Query: {query}

Please format your response structured as follows:
- Jurisdiction: State the relevant jurisdiction.
- Short Answer: A brief summary of the answer.
- Detailed Explanation: The "Why", detailing the reasoning using the IRAC method if applicable.
- Applicable IP: Mention relevant IP types (e.g., Patents, TK, ABS).
- Sources: Provide a brief list of the primary sources cited in your response.
- Confidence: Note any areas where the context was ambiguous.

Remember to cite using the chunk IDs from the context, e.g., [chunk_abc123].
"""
