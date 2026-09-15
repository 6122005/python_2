# ResumeFit AI 🚀

See how well your resume fits a job — before you spend an hour tailoring it by hand.

---

## 🌐 Live Preview

The application is deployed live on Streamlit Cloud:

👉 **[Launch ResumeFit AI](https://6122005-python-2-week16-18app-rbe83z.streamlit.app/)**  
*(URL: `https://6122005-python-2-week16-18app-rbe83z.streamlit.app/`)*

🔑 **App Password:** `admin`

---

## 🧪 Demo Data for Testing (ટેસ્ટ કરવા માટે ડેમો ડેટા)

You can copy and paste the following sample data directly into the app to test it:

### 📋 1. "Your resume" બોક્સમાં આ પેસ્ટ કરો:
```text
Jenish Bhesaniya
Full Stack AI Developer | Python & LangChain Specialist

SUMMARY:
Passionate Software Engineer with 2+ years of experience building AI-powered applications, ReAct agents, and RAG systems using LangChain, Groq, and Streamlit. Strong background in Python, REST APIs, and vector databases.

SKILLS:
- Languages: Python, JavaScript, SQL
- AI / LLM Frameworks: LangChain, LangGraph, ChromaDB, Groq, Llama 3
- Web & Tools: Streamlit, Flask, Docker, Git, Linux
- Concepts: Retrieval-Augmented Generation (RAG), Prompt Engineering, ReAct Planning, Sentence Chunking

PROJECTS:
1. Autonomous Research Assistant: Built a LangGraph agent equipped with live weather, DuckDuckGo search, and Wikipedia tools deployed on Streamlit Cloud.
2. AI PDF Question Answering: Developed an end-to-end RAG pipeline using ChromaDB, HuggingFace embeddings, and Gemini to answer queries over complex PDFs.
```

### 💼 2. "Job description" બોક્સમાં આ પેસ્ટ કરો:
```text
Job Title: Junior AI Engineer / Python Developer
Company: TechNova Solutions
Location: Remote

ABOUT THE ROLE:
We are looking for an ambitious AI Engineer to join our core product team. You will build intelligent agentic workflows and LLM-driven features for enterprise clients.

RESPONSIBILITIES:
- Develop conversational agents and RAG pipelines using LangChain or LangGraph.
- Integrate vector databases (like ChromaDB or Pinecone) for document search.
- Build clean, interactive demo interfaces using Streamlit or FastAPI.
- Optimize prompts and monitor latency across modern LLM providers (Groq, OpenAI).

REQUIREMENTS:
- Proficient in Python with hands-on experience in LangChain.
- Familiarity with Vector Stores, Embeddings, and Chunking strategies.
- Experience deploying web apps (Streamlit or cloud platforms).
- Good to have: Experience with FastAPI and Docker.
```

---

## What it does

Paste your resume and a job description. In a few seconds you get:

- A **fit score** (0–100)
- What in your background **matches** the role
- What's **missing or weak**
- A plain-English summary of the gap

If the fit looks reasonable, generate a **tailored cover letter** in one of three tones (Professional / Friendly / Direct) — one click, using the same resume and job description you already pasted in.

## Who it's for

Anyone applying to multiple roles who wants an honest, fast read on fit before hand-tailoring a resume for a posting that might not even be a match. Built by a job seeker, for job seekers — see `docs/spec.md` for the full scope and what's deliberately *not* included in this version.

## How to use it

1. Open the live app: [ResumeFit AI](https://6122005-python-2-week16-18app-rbe83z.streamlit.app/)
2. Enter the password: `admin`
3. Paste your resume text and the job description (use the sample demo data above).
4. Click **Analyze Fit**.
5. Optionally, click **Generate Cover Letter** once you've seen the fit results.
6. Use the **Give Feedback** button at the bottom of the app to share your experience.

## Running it locally

```bash
cd week16_18
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run offline unit tests (all 19 pass in < 0.5s):
python3 -m pytest tests/ -v

# Run the app locally:
streamlit run app.py
```

## Project structure

```
week16_18/
├── app.py                   Streamlit UI — wires everything together
├── core.py                  Fit analysis + cover letter generation logic
├── llm_client.py            Retry-safe Groq & Anthropic API wrapper
├── auth.py                  Simple shared-password gate
├── errors.py                Input validation + "never show a raw traceback" handling
├── usage_logger.py          Appends usage events to data/usage_log.csv
├── ui_text.py               All user-facing copy, in one place
├── .streamlit/config.toml   UI theme (colors, fonts, layout)
├── docs/                    Spec, testing notes, deployment + feedback guides
└── tests/                   Offline unit tests (19 tests, pytest, no API key needed)
```

## Development notes

- **Zero Unhandled Exceptions:** `errors.py`'s `safe_run` wrapper ensures no raw traceback ever reaches the user.
- **Privacy First:** Usage logging never stores what users paste in — only a timestamp and feature usage count (`usage_logger.py`).
- **Comprehensive Unit Testing:** 19 offline unit tests cover parsing, validation, auth, and logging logic.

---

## Built by

Jenish Bhesaniya — [GitHub](https://github.com/6122005)
