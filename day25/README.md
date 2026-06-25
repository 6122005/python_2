# Day 25 - Search My Notes (Semantic Search)

## Project Overview

This project demonstrates a simple AI-powered semantic search system.

The application:

1. Reads a PDF file.
2. Extracts text from the PDF.
3. Splits text into chunks.
4. Creates embeddings using Sentence Transformers.
5. Stores embeddings in ChromaDB.
6. Allows users to ask questions.
7. Retrieves the most relevant chunks using semantic similarity search.

---

## Technologies Used

* Python
* PyPDF
* Sentence Transformers
* ChromaDB

---

## Project Structure

```text
day25/
│
├── tutorial.pdf
├── extract.py
├── embed_store.py
├── search.py
├── note_search.py
├── chroma_db/
└── README.md
```

---

## Installation

Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install pypdf
pip install sentence-transformers
pip install chromadb
```

---

## Running The Project

Run the final application:

```bash
python3 note_search.py
```

Example:

```text
Ask Question:
What is Transformer?
```

The system returns the most relevant text chunks from the PDF.

---

## Concepts Learned

* PDF Text Extraction
* Chunking
* Embeddings
* Vector Databases
* Semantic Search
* Retrieval-Augmented Generation (RAG) Basics

---

## Learning Outcome

This project combines concepts from:

* Day 21: Embeddings
* Day 22: ChromaDB
* Day 23: Sentence Transformers
* Day 24: Chunking

and builds a complete semantic search application.
