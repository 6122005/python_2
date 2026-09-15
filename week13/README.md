# Week 13: Upgrade Product to v2 — Autonomous Agent 🚀

Welcome to Week 13! In this phase, we upgraded our static chatbot (v1) into an **Autonomous Smart Research Assistant (v2)** powered by a **LangGraph ReAct Agent**.

---

## 🌐 Live Preview

The application is deployed live on Streamlit Cloud:

👉 **[Launch Smart Research Assistant v2](https://6122005-python-2-week13app-v2-o2m1r2.streamlit.app/)**  
*(URL: `https://6122005-python-2-week13app-v2-o2m1r2.streamlit.app/`)*

---

## 💡 What's New in v2?

- **Real-Time Web Search:** Powered by DuckDuckGo to answer live questions about news, current events, and sports.
- **Accurate Live Weather:** Integrates a real-time weather tool for accurate temperatures, humidity, and wind conditions across any city.
- **Deep Historical & Entity Knowledge:** Integrated with Wikipedia for comprehensive information on people, history, science, and cricket records.
- **Transparent Reasoning UI:** Uses Streamlit expanders (`st.expander`) so users can inspect the agent's step-by-step thoughts, tool inputs, and raw observations in real-time.

---

## 📁 Week 13 Deliverables

| Day | File | Description |
|---|---|---|
| **Day 61** | [`v2_plan.md`](./v2_plan.md) | Retrospective on v1 user feedback and roadmap for the autonomous agent. |
| **Day 62** | [`core_v2.py`](./core_v2.py) | Backend LangGraph ReAct agent engine equipped with multi-tool capabilities. |
| **Day 63** | [`app_v2.py`](./app_v2.py) | Streamlit UI displaying the agent's thoughts and tool calls in real time. |
| **Day 64** | [`v2_comparison_feedback.md`](./v2_comparison_feedback.md) | Structured user comparison feedback between v1 and v2. |
| **Day 65** | [`v1_vs_v2_writeup.md`](./v1_vs_v2_writeup.md) | Case study article on agent architecture, transparency, and lessons learned. |

---

## 🛠️ Local Setup & Run

### 1. Install Dependencies
```bash
cd week13
pip install -r requirements.txt
```

### 2. Configure API Key
Create a `.env` file in the `week13/` folder (or root):
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Backend Test
```bash
python core_v2.py
```

### 4. Run the Streamlit Web Application
```bash
streamlit run app_v2.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.
