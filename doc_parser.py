# doc_parser.py
# Extracts individual requirements from uploaded PDF or DOCX files.

import re
import io

# Patterns that signal a standalone requirement line
REQ_ID_RE = re.compile(
    r"^\s*(?:REQ[-_]?[A-Z0-9]+[-_]?\d*[:.\s]|R\d+[:.]\s)",
    re.IGNORECASE,
)

# Obligation verbs
OBLIGATION_RE = re.compile(
    r"\b(must|shall|should|will|can|may|is required|is able to)\b",
    re.IGNORECASE,
)

# Numbered / bulleted list item prefixes
BULLET_RE = re.compile(
    r"^\s*(?:\d+[.)]\s+|[a-zA-Z][.)]\s+|[-•*▪▸►◆]\s+)"
)

MIN_WORDS = 6
MAX_WORDS = 150


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text.strip(".,;:\"'")


def _is_valid(text: str) -> bool:
    words = text.split()
    return MIN_WORDS <= len(words) <= MAX_WORDS


def _deduplicate(items: list) -> list:
    seen, out = set(), []
    for r in items:
        key = r.lower()[:80]
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


# ── DOCX: paragraph-level extraction ─────────────────────────────────────────

def _extract_from_paragraphs(paragraphs: list) -> list:
    """
    Smart extraction:
    1. If a paragraph starts with a REQ-ID, take it as a whole requirement.
    2. If a paragraph contains an obligation keyword and is a reasonable length,
       take it as a requirement.
    3. Ignore headings, very short lines, and non-requirement prose.
    """
    results = []
    for para in paragraphs:
        text = _clean(para)
        if not text or len(text.split()) < MIN_WORDS:
            continue
        if len(text.split()) > MAX_WORDS:
            # Try to split on REQ- boundaries inside a long paragraph
            sub = re.split(r"(?=REQ[-_]?[A-Z0-9])", text)
            for s in sub:
                s = _clean(s)
                if _is_valid(s) and OBLIGATION_RE.search(s):
                    results.append(s)
            continue
        # REQ-ID prefix → always include
        if REQ_ID_RE.match(text):
            if OBLIGATION_RE.search(text):
                results.append(text)
            continue
        # Obligation keyword → include
        if OBLIGATION_RE.search(text) and _is_valid(text):
            # Skip lines that look like headings (short, no verb object)
            if len(text.split()) >= MIN_WORDS:
                results.append(text)
    return results


# ── PDF extractor ─────────────────────────────────────────────────────────────

def extract_from_pdf(file_bytes: bytes) -> list:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required: pip install pypdf")

    reader = PdfReader(io.BytesIO(file_bytes))
    paragraphs = []
    for page in reader.pages:
        raw = page.extract_text() or ""
        # Split on newlines to get individual lines / paragraphs
        for line in raw.split("\n"):
            line = line.strip()
            if line:
                paragraphs.append(line)

    results = _extract_from_paragraphs(paragraphs)
    return _deduplicate(results)


# ── DOCX extractor ────────────────────────────────────────────────────────────

def extract_from_docx(file_bytes: bytes) -> list:
    try:
        import docx
    except ImportError:
        raise ImportError("python-docx is required: pip install python-docx")

    doc = docx.Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    results = _extract_from_paragraphs(paragraphs)
    return _deduplicate(results)


# ── Unified entry point ───────────────────────────────────────────────────────

def extract_requirements_from_file(filename: str, file_bytes: bytes) -> list:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_from_pdf(file_bytes)
    elif lower.endswith(".docx") or lower.endswith(".doc"):
        return extract_from_docx(file_bytes)
    else:
        raise ValueError(
            "Unsupported file type: '" + filename +
            "'. Please upload a .pdf or .docx file."
        )
