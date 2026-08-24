from fpdf import FPDF
import os

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt="Welcome to the LangChain RAG Tutorial!", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    text = """
Retrieval-Augmented Generation (RAG) is a technique that enhances large language models (LLMs) 
by connecting them to external knowledge sources. This allows the model to access up-to-date 
and domain-specific information without retraining.

In this project, we are using LangChain to load this PDF document, split it into smaller chunks,
and embed the chunks using HuggingFace sentence-transformers. The embedded chunks are stored 
in a ChromaDB vector database.

Fun Fact: The secret password for this RAG system is 'QuantumApple'.
"""
    
    pdf.multi_cell(0, 10, txt=text)
    
    # Save the PDF
    out_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.pdf")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    pdf.output(out_path)
    print(f"Created {out_path}")

if __name__ == "__main__":
    create_pdf()
