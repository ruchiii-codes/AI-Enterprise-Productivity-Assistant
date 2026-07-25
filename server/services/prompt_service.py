def build_prompt(question: str, documents: list[str]):
    """
    Build the prompt sent to the LLM.
    """

    context = ""

    for index, document in enumerate(documents, start=1):
        context += f"Document Chunk {index}\n"
        context += "-" * 30 + "\n"
        context += document
        context += "\n\n"

    prompt = f"""
    You are an AI Enterprise Knowledge Assistant.
    
    Your job is to answer questions ONLY using the provided context.
    
    Rules:
    - Answer ONLY using the provided context.
    - Never use outside knowledge.
    - Never make up facts.
    - Never invent examples that are not present in the context.
    - If the context is incomplete, do not guess or fill in missing information.
    - If the answer is not found in the context, reply exactly:
      "I couldn't find the answer in the uploaded documents."
    - Keep answers clear, professional, and concise.
    - Explain technical concepts in simple language.
    - Do not repeat information.
    - Use Markdown formatting.
    
    Answer Format:
    1. Definition
    2. Explanation
    3. Key Points (if applicable)
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """

    return prompt