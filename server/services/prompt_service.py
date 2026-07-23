def build_prompt(question: str, documents: list[str]):
    """
    Build the prompt sent to the LLM.
    """

    context = "\n\n".join(documents)

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the provided context.

If the answer is not found in the context, say:
"I couldn't find the answer in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    return prompt