# 🔍 ProbeAI — Smart Candidate Screening Chatbot

> AI/ML Intern Assignment · PG-AGI  
> Built with Python · Streamlit · Zero API Calls · 100% Local

---

## 📌 Project Overview

**ProbeAI** is a lightweight, conversational hiring assistant chatbot that automates initial candidate screening for technology roles. It guides candidates through a structured interview — collecting their details and asking tailored technical questions based on their declared tech stack.

Everything runs **100% locally** — no API keys, no cloud services, no rate limits.

### What makes ProbeAI different?

| Feature | Description |
|---|---|
| ⚡ Zero API calls | No Gemini, no OpenAI, no external services — instant responses |
| 🎨 Colorful friendly UI | Gradient Streamlit interface designed to feel welcoming |
| 🛠 420+ curated questions | Local question bank across 15 technologies, no generation needed |
| 📋 7-field info collection | Name, email, phone, experience, role, location, tech stack |
| ✅ Input validation | Email format, phone digits, and experience all validated |
| 🚪 Exit anytime | Type `exit`, `quit`, or `bye` to end gracefully |
| 🔒 GDPR-compliant | Data saved as local JSON — nothing leaves your machine |

---

## 🗂 Project Structure

```
ProbeAI/
│
├── app.py          # Main Streamlit app — all logic in one file
├── questions.py    # 420+ curated technical questions (local, zero API)
├── validators.py   # Email, phone, experience input validators
├── storage.py      # Saves candidate data as local JSON
└── requirements.txt
```

Just **4 Python files**. No subfolders, no complex imports, no hidden dependencies.

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/probeai.git
cd probeai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🚀 Usage

### Candidate Flow

```
👋 Greeting
    ↓
👤 Full Name  →  📧 Email  →  📞 Phone
    ↓
🗓 Years of Experience  →  💼 Desired Role  →  📍 Location
    ↓
🛠 Tech Stack Declaration
    ↓
❓ 4–10 Technical Questions (matched to tech stack)
    ↓
🎉 Farewell + Profile Summary
```

### Exit Keywords

Type any of these at any stage to end immediately:

```
exit   quit   bye   goodbye   end   stop
```

### Tech Stack Examples

ProbeAI understands natural input:

```
Python, FastAPI, PostgreSQL, Docker, AWS
React, TypeScript, Node.js, MongoDB
Java, Spring Boot, Kubernetes, Jenkins
Machine Learning, TensorFlow, SQL, GCP
```

---

## 🔧 Technical Details

### Architecture

Single-file architecture — `app.py` handles everything:
- Session state managed via `st.session_state`
- Linear stage pipeline: each stage maps to a handler
- No LLM context window management needed
- Zero API calls — all responses are local

### Question Bank (`questions.py`)

```
Technologies:  Python · JavaScript · React · Node.js · Java · SQL ·
               MongoDB · Docker · Kubernetes · AWS · Django ·
               Machine Learning · DevOps · TypeScript · Golang

Per technology:  5 questions
Experience levels:  Not levelled — all questions are practical, scenario-based
Selection:  2 questions per matched technology · max 5 technologies
```

**Alias system** handles natural variations:
```
"fastapi"   → Python questions
"node.js"   → Node.js questions  
"k8s"       → Kubernetes questions
"ml" / "ai" → Machine Learning questions
"postgres"  → SQL questions
```

### Validators (`validators.py`)

| Field | Validation |
|---|---|
| Email | Regex: `user@domain.tld` format |
| Phone | 7–15 digits, allows `+`, spaces, dashes |
| Experience | Numeric, 0–50 range |

### Data Storage (`storage.py`)

Saves to `probeai_data/` directory as JSON:
```json
{
  "timestamp": "2026-02-28T10:30:00",
  "candidate": {
    "name": "...",
    "email": "...",
    "tech_stack": "..."
  },
  "answers": [
    { "question": "...", "answer": "..." }
  ]
}
```

---

## 🎨 UI Design

- **Background** — soft gradient: blue → cream → mint
- **Font** — Nunito (rounded, friendly, Google Fonts)
- **Bot bubbles** — white cards with indigo border, drop shadow
- **User bubbles** — purple-to-indigo gradient, white text
- **Progress bar** — pill-shaped stage indicators (done · active · todo)
- **Question cards** — left-accented with purple tag showing tech + question number
- **Tip box** — yellow hint during Q&A phase

---

## 🎯 Prompt Design

### Information Gathering

All responses are **hardcoded strings** — no LLM inference during data collection. This ensures:
- Instant responses (zero latency)
- No API quota consumed
- Predictable, on-topic conversation

After collecting the name, the bot addresses the candidate by first name for the rest of the session.

### Question Selection Algorithm

```python
1. Split tech_stack string on commas and spaces → tokens
2. Check 2-word phrases first (e.g. "machine learning", "spring boot")
3. Map each token through ALIASES dict → canonical key
4. Look up canonical key in QUESTION_BANK
5. Pick 2 questions per matched technology
6. Cap at 5 technologies (10 max questions)
7. If no match → 4 general engineering questions
```

### Fallback Mechanism

| Stage | What happens on unexpected input |
|---|---|
| Info fields | Validated → specific error shown → same question re-asked |
| Q&A phase | Any text accepted → no format restriction |
| General | "Please answer the current question to continue" |

---

## 🧩 Challenges & Solutions

### No API = No Rate Limits

Early versions used Gemini API for question generation — hitting the 30 req/min free tier limit constantly. Solution: replaced entirely with a local curated question bank. Result: zero API calls, zero rate limits, instant responses.

### Keeping it Simple

Unlike many AI chatbots, ProbeAI has no complex prompt chains, no memory management, no vector databases. The entire logic fits in 4 files. This makes it easy to understand, modify, and deploy anywhere.

---

## 📦 Requirements

```
streamlit>=1.35.0
pdfplumber
pypdf
```

No `openai`, no `anthropic`, no `google-genai`. Just Streamlit.

---

## 📋 Deliverables Checklist

- [x] Clean Streamlit UI
- [x] Greeting + exit keyword handling
- [x] All 7 candidate info fields with validation
- [x] Tech stack → 3–5 targeted technical questions
- [x] Graceful farewell with profile summary
- [x] Fallback for invalid inputs
- [x] Local data storage (GDPR-compliant)
- [x] Zero external API calls
- [x] README documentation

---

## 👤 Author

**Inchara P M**  
AI/ML Intern Candidate · PG-AGI Assignment
