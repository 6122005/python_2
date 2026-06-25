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


def sentence_chunk(text):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences


def search_chunks(chunks, query):

    results = []

    for chunk in chunks:

        if query.lower() in chunk.lower():
            results.append(chunk)

    return results


if __name__ == "__main__":

    pdf_path = "tutorial.pdf"

    text = extract_text(pdf_path)

    chunks = sentence_chunk(text)

    print("=" * 60)
    print("SENTENCE BASED CHUNKING")
    print("=" * 60)

    print(f"\nTotal Chunks: {len(chunks)}")

    query = "References"

    matches = search_chunks(chunks, query)

    print(f"\nQuery: {query}")
    print(f"Matches Found: {len(matches)}")

    if matches:
        print("\nFirst Match:\n")
        print(matches[0])