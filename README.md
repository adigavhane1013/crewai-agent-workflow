# 🤖 Multi-Agent Research & Review System

A fully automated research pipeline built with **CrewAI** where three AI agents collaborate to produce source-grounded, fact-checked documentation from live web search results — with zero hallucinations tolerated.

---

## 🧠 How It Works

```
User Input (Topic)
       ↓
  [Tavily Search] — fetches live web results
       ↓
  [Research Agent] — extracts structured facts with verbatim quotes
       ↓
  [Writer Agent] — writes cited Markdown documentation
       ↓
  [Validator Agent] — audits every claim, scores output, issues PASS/FAIL
       ↓
  Saved Report + Metrics JSON
```

---

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| Agent Framework | CrewAI |
| LLMs | Gemini 2.5 Flash, DeepSeek-R1 (via OpenRouter) |
| Local LLM (dev) | Ollama (phi3) |
| Web Search | Tavily API |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
multi-research-agent/
├── agents.py          # Defines Research, Writer, Validator agents
├── tasks.py           # Task prompts and strict citation rules
├── crew_runner.py     # Assembles and runs the CrewAI crew
├── llms.py            # LLM initialization (Gemini / DeepSeek / Ollama)
├── search.py          # Tavily deep web search integration
├── config.py          # API keys, model settings, flags
├── metrics.py         # Per-run metrics calculation and JSON logging
├── main.py            # Entry point with retry logic and report saving
├── utils/
│   └── file_utils.py  # Report saving helpers
├── output/            # Generated Markdown reports
├── metrics/           # Per-run and historical JSON metrics
└── .env               # API keys (not committed)
```

---

## ⚙️ Setup

**1. Clone the repo**
```bash
git clone https://github.com/adigavhane1013/crewai-agent-workflow.git
cd crewai-agent-workflow
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create your `.env` file**
```env
GOOGLE_API_KEY=your_gemini_key
TAVILY_API_KEY=your_tavily_key
OPENROUTER_API_KEY=your_openrouter_key
```

**4. Run**
```bash
python main.py
```

---

## 📊 Metrics Tracked Per Run

- Total Claims extracted
- Verified Claims (source-backed)
- Unsupported Claims (hallucinations caught)
- Citation Coverage %
- Verification Rate %
- Final Verdict: `PASS` / `FAIL`

All metrics are saved as JSON in the `metrics/` folder and appended to a `history_log.json` for tracking across runs.

---

## 🔒 Anti-Hallucination Design

- Every written sentence must include a verbatim `[CITE: "..."]` tag
- Validator agent audits each claim independently against source quotes
- Any unsupported claim triggers a `FAIL` verdict
- A single controlled retry is attempted before the run is abandoned

---

## 📄 Sample Output Format

```markdown
# TOPIC NAME

## Overview
Some fact about the topic. [CITE: "exact quote from source"]

## Key Concepts
- Feature X [CITE: "exact quote"]

## Real-World Use Cases
- Used in Y industry [CITE: "exact quote"]

## Limitations
- Known drawback Z [CITE: "exact quote"]
```

---

## 🙋 Author

**Aditya Gavhane**  
[GitHub](https://github.com/adigavhane1013)
