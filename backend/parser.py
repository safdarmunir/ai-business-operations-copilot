from pypdf import PdfReader
from docx import Document
from pathlib import Path


def extract_pdf_text(file_path):
    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(file_path):
    doc = Document(file_path)

    return "\n".join(
        para.text for para in doc.paragraphs
        if para.text.strip()
    )


def extract_text(file_path):
    file_path = Path(file_path)

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf_text(file_path)

    elif suffix == ".docx":
        return extract_docx_text(file_path)

    elif suffix == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError(f"Unsupported file type: {suffix}")