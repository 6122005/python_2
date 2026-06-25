from pypdf import PdfReader


def extract_text(pdf_path, pages=15):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages[:pages]:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def overlap_chunk(text,
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


if __name__ == "__main__":

    pdf_path = "tutorial.pdf"

    text = extract_text(pdf_path)

    chunks = overlap_chunk(
        text,
        chunk_size=500,
        overlap=100
    )

    print("=" * 60)
    print("OVERLAP CHUNKING")
    print("=" * 60)

    print(f"\nTotal Chunks: {len(chunks)}")

    query = "References"

    matches = search_chunks(chunks, query)

    print(f"\nQuery: {query}")
    print(f"Matches Found: {len(matches)}")

    if matches:
        print("\nFirst Match:\n")
        print(matches[0][:1000])