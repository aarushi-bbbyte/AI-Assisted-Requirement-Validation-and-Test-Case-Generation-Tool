# AI-Assisted Requirement Tool v2

A final-year academic project that validates software requirements and auto-generates
test cases using smart rule-based NLP — no API keys or ML models required.

## Features

| Feature | Description |
|---|---|
| **Requirement Validator** | Checks obligation keywords, actor, measurability, ambiguous language, length |
| **Quality Score (0–100)** | Weighted scoring with letter grade (A/B/C/D/F) |
| **Smart Test Case Generator** | 10–15 deeply requirement-aware positive + negative test cases |
| **Document Upload** | Upload a PDF or DOCX containing requirements — all extracted & analysed automatically |
| **Requirement History** | Sidebar shows all requirements validated this session |
| **Traceability Matrix** | Live table linking every requirement to its test cases |
| **CSV Export** | Export test cases or traceability matrix as CSV |

## 📁 Project Structure

```
tuleap_v2/
├── app.py           ← Streamlit UI (entry point)
├── requirement.py   ← Domain model
├── validator.py     ← Quality checker (score + ambiguity + completeness)
├── ai_generator.py  ← Smart rule-based NLP test case generator
├── doc_parser.py    ← PDF / DOCX requirement extractor
├── repository.py    ← In-memory storage
├── controllers.py   ← Orchestration layer
├── exporter.py      ← CSV export
├── requirements.txt ← Python dependencies
└── README.md
```

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

Opens at http://localhost:8501

## How Test Cases Are Generated

The `AITestCaseGenerator` extracts from each requirement:
- **Actors** (user, admin, system…)
- **Action verbs** (what must happen)
- **Objects** (password, file, report…)
- **Numeric boundaries** (within 60 seconds, at most 10 MB…)
- **Conditional clauses** (if, when, unless…)
- **Format types** (PDF, CSV, email address…)
- **Feature flags** (auth, upload, email, report, search, delete, concurrency)

Each detected entity generates **specific, targeted test cases** rather than generic templates.

## Document Upload

Supports `.pdf` and `.docx` files.  
Requirements are detected by:
1. Numbered / bulleted list items
2. Sentences containing obligation keywords (must/shall/should/will/can/may)
