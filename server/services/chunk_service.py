from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(text: str):
    """
    Split cleaned text into smaller chunks for embedding.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_text(text)

    return chunks