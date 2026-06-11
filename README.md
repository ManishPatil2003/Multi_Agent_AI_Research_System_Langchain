# AI Research Loop (Multi-Agent Research Pipeline)

ResearchMind is a small multi-agent application that produces a structured research report for any topic. It combines:

- **Search Agent** (web search)
- **Reader Agent** (scrapes and extracts key text from a selected URL)
- **Writer Chain** (drafts a full research report)
- **Critic Chain** (scores and provides improvements)

It ships with both a **Streamlit UI** and a **CLI runner**.

---

## Workflow (end-to-end)

1. **Search**: uses Tavily to find recent, relevant sources.
2. **Read/Extract**: scrapes a chosen source URL and extracts readable text.
3. **Write**: generates a report with the required sections.
4. **Critic**: evaluates the report in a strict format (score, strengths, improvements).

---

## Tech Stack

- Python
- Streamlit (UI)
- LangChain (agents + prompt chains)
- OpenAI (LLM)
- Tavily (web search)
- Requests + BeautifulSoup (scraping)

---

## Prerequisites

- Python 3.10+ (recommended)
- API keys:
  - `TAVILY_API_KEY`
  - OpenAI credentials (used by `ChatOpenAI` in `agents.py`)

---

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_key
# OpenAI key env var (choose one depending on your OpenAI setup)
OPENAI_API_KEY=your_openai_key
```

> Note: `load_dotenv()` is used in `agents.py` and `tools.py`, so the app expects these keys in a `.env` file.

---

## Run the app

### Option A: Streamlit UI

```bash
streamlit run app.py
```

1. Enter a **Research Topic**
2. Click **Run Research Pipeline**
3. Review step progress + results (including the critic feedback)

### Option B: CLI runner

```bash
python pipeline.py
```

1. Type a topic when prompted
2. The pipeline prints intermediate results and returns a final `state` dict

---

## Notes / Behavior

- The scraper in `tools.py` removes `script/style/nav/footer` and truncates extracted text to **~3000 characters**.
- The search agent returns up to **5** Tavily results (`max_results=5`).
- The **final report** is generated from:
  - raw search output
  - scraped content

---

## Troubleshooting

- **Missing API key errors**: verify you created `.env` and that `TAVILY_API_KEY` + `OPENAI_API_KEY` exist.
- **Scraping fails**: some sites block requests or require JavaScript. The scraper falls back to `Could not scrape URL: ...`.
- **Model/LLM errors**: check your OpenAI credentials and that the model name configured in `agents.py` (currently `gpt-4o-mini`) is available to your account.

---

## Project Structure

- `app.py` — Streamlit UI + rendering of pipeline steps/results
- `agents.py` — LangChain agents and prompt chains (writer + critic)
- `tools.py` — `web_search` (Tavily) and `scrape_url` (BeautifulSoup)
- `pipeline.py` — CLI pipeline runner
- `requirements.txt` — dependency list

