from pypdf import PdfReader


def extract_text(pdf_path, pages=15):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages[:pages]:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


if __name__ == "__main__":

    pdf_path = "tutorial.pdf"

    text = extract_text(pdf_path)

    print("=" * 60)
    print("TEXT EXTRACTED")
    print("=" * 60)

    print(text[:1000])

    print("\nTotal Characters:", len(text))