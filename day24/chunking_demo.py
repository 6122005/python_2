from pypdf import PdfReader
import re


def extract_text(pdf_path, pages=15):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages[:pages]:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def fixed_chunk(text, size=500):

    return [
        text[i:i + size]
        for i in range(0, len(text), size)
    ]


def sentence_chunk(text):

    return [
        sentence.strip()
        for sentence in re.split(
            r'(?<=[.!?])\s+',
            text
        )
        if sentence.strip()
    ]


def overlap_chunk(
        text,
        chunk_size=500,
        overlap=100):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def search_chunks(chunks, query):

    results = []

    for chunk in chunks:

        if query.lower() in chunk.lower():
            results.append(chunk)

    return results


def show_results(name, chunks, query):

    matches = search_chunks(chunks, query)

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print(f"Total Chunks: {len(chunks)}")
    print(f"Matches Found: {len(matches)}")

    if matches:

        print("\nBest Match:\n")
        print(matches[0][:800])

    else:

        print("\nNo Match Found")


if __name__ == "__main__":

    pdf_path = "tutorial.pdf"

    text = extract_text(pdf_path)

    print("\nTEXT EXTRACTED")
    print(f"Characters: {len(text)}")

    query = "References"

    fixed_chunks = fixed_chunk(text)

    sentence_chunks = sentence_chunk(text)

    overlap_chunks = overlap_chunk(text)

    show_results(
        "FIXED CHUNKING",
        fixed_chunks,
        query
    )

    show_results(
        "SENTENCE CHUNKING",
        sentence_chunks,
        query
    )

    show_results(
        "OVERLAP CHUNKING",
        overlap_chunks,
        query
    )

    print("\n" + "=" * 70)
    print("COMPARISON")
    print("=" * 70)

    print("""
1. Fixed Chunking
   Fast but can break sentences.

2. Sentence Chunking
   Preserves meaning better.

3. Overlap Chunking
   Best for RAG systems.
   Used in ChatGPT-style search.
""")