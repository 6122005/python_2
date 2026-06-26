# 📄 Day 27 - PDF RAG Pipeline (PDF → ChromaDB)

## 🎯 Objective

Build the ingestion pipeline of a Retrieval-Augmented Generation (RAG) system.

Instead of searching normal text files, this project converts a PDF into searchable AI knowledge.

---

# Workflow

```
          PDF

           │

           ▼

    Extract Text

           │

           ▼

      Clean Text

           │

           ▼

     Split Chunks

           │

           ▼

 Create Embeddings

           │

           ▼

 Store in ChromaDB

===========================

 User asks Question

           │

           ▼

Question Embedding

           │

           ▼

Similarity Search

           │

           ▼

Relevant Chunks
```

---

# Technologies

- Python
- PyPDF
- Sentence Transformers
- ChromaDB

---

# Project Structure

```
day27_pdf_rag/

│

├── app.py

├── sample.pdf

├── chroma_db/

├── requirements.txt

└── README.md
```

---

# Installation

```bash
pip install pypdf
pip install chromadb
pip install sentence-transformers
```

or

```bash
pip install -r requirements.txt
```

---

# Requirements.txt

```
pypdf
chromadb
sentence-transformers
```

---

# Pipeline Explained

## 1. Read PDF

Read every page of the PDF.

Output:

```
Raw Text
```

---

## 2. Clean Text

Remove

- Extra spaces
- Empty lines
- Unwanted characters

Output:

```
Clean Text
```

---

## 3. Chunking

Split large text into smaller pieces.

Example

```
Chunk 1

Chunk 2

Chunk 3
```

---

## 4. Embeddings

Convert every chunk into vectors.

Example

```
Python is easy

↓

[0.24,0.61,0.17,...]
```

---

## 5. Store in ChromaDB

Each record contains

```
ID

Original Chunk

Embedding

Metadata
```

---

## 6. User Question

Example

```
What is Python?
```

Convert question into embedding.

---

## 7. Similarity Search

Compare

Question Vector

with

Stored Vectors

Return

Top Similar Chunks

---

# Expected Output

```
Ask:

What is Python?

----------------------

Python is a programming language.

Python supports OOP.
```

---

# Learning Outcomes

After completing Day 27 you will understand

✅ PDF Processing

✅ Text Extraction

✅ Text Cleaning

✅ Chunking

✅ Sentence Embeddings

✅ Vector Database

✅ Semantic Search

✅ Document Ingestion

✅ Foundation of RAG

---

# Difference from Day 25

Day 25

```
Text Files

↓

Embeddings

↓

Search
```

Day 27

```
PDF

↓

Extract Text

↓

Embeddings

↓

Search
```

Day 27 introduces the **Document Ingestion Pipeline**, which is one of the most important components of every modern RAG application.

---

# What's Next?

Day 28

Learn Streamlit

Build your first AI web interface.