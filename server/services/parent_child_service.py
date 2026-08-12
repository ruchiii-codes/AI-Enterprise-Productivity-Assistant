from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_parent_child_chunks(text: str):
    """
    Split a document into larger parent chunks and smaller child chunks.

    Parents provide broader context.
    Children are used for precise retrieval.
    """

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=400,
        separators=["\n\n", "\n", " ", ""],
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
    )

    parent_chunks = parent_splitter.split_text(text)

    parent_child_pairs = []

    for parent_id, parent in enumerate(parent_chunks):
        child_chunks = child_splitter.split_text(parent)

        for child_id, child in enumerate(child_chunks):
            parent_child_pairs.append(
                {
                    "parent_id": parent_id,
                    "child_id": child_id,
                    "parent": parent,
                    "child": child,
                }
            )

    return parent_child_pairs