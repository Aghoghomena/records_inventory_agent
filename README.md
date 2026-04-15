# RetroGroove Records — VinylBot

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/LLM-Gemini-4285F4?logo=google&logoColor=white)
![LangSmith](https://img.shields.io/badge/Observability-LangSmith-FF6B35?logo=langchain&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![uv](https://img.shields.io/badge/Package_Manager-uv-DE5FE9?logo=astral&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

**VinylBot** is an AI-powered email assistant for a vinyl record shop. Drop a CSV of customer enquiries in, and it reads every message, figures out what each customer is asking for, queries the store's catalogue, and writes back a formatted response — all without a human touching it.

---

## What it does

Customers email questions like *"Do you have any Bowie albums?"* or *"What jazz records came out in the late 70s?"* VinylBot reads the inbox (a CSV of email bodies), understands each question in plain English, searches a local catalogue of thousands of albums, and generates a friendly, formatted reply — then saves every response back to a CSV for the team to send.

No manual searching. No copy-pasting. The agent handles the full loop.

---

## Why it matters

Small independent record shops run on thin margins and lean staff. Answering customer emails about stock takes real time — especially when someone asks for "early 90s grunge" or "anything by Fela Kuti." Staff either spend hours manually searching a spreadsheet, or customers wait days for a reply.

VinylBot collapses that to seconds. It gives a small shop the same responsive customer experience as a big e-commerce platform, without the headcount.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT                                │
│              resources/emails.csv                           │
│        (raw customer email enquiries)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     AGENT LAYER                             │
│                                                             │
│   workflowagent.py          reactagent.py                   │
│   (multi-turn loop)         (ReAct loop)                    │
│                                                             │
│   Reads CSV → iterates      Reads CSV in one shot,          │
│   enquiry by enquiry,        uses tool calls to             │
│   maintains full             process all queries            │
│   conversation state         in a single pass               │
└──────────────────────┬──────────────────────────────────────┘
                       │  LLM decides which tool to call
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     TOOL ROUTER                             │
│                                                             │
│  get_album_by_artists     ──▶  artist name(s) → LIKE query  │
│  get_album_by_genre       ──▶  genre / subgenre → LIKE      │
│  get_album_by_year        ──▶  year or date range → BETWEEN │
│  get_album_by_generated_query ▶ LLM-generated raw SQL       │
│  read_csv_file            ──▶  load customer emails         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│              resources/music.db  (SQLite)                   │
│   Schema: number | year | album | artist | genre |          │
│           subgenre | price                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                       OUTPUT                                │
│   resources/email_responses.csv  (workflow agent)           │
│   resources/email_responses_2.csv  (react agent)           │
│   Columns: enquiry | formatted response                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini (via OpenAI-compatible API) |
| Agent patterns | ReAct loop · Workflow (multi-turn) |
| Tool calling | OpenAI function-calling spec |
| Database | SQLite — local `music.db` |
| Input / Output | CSV (pandas-free, stdlib `csv` module) |
| Observability | LangSmith (`@traceable` decorators) |
| Config / secrets | `python-dotenv` |
| Package manager | [uv](https://docs.astral.sh/uv/) |
| Runtime | Python 3.13 |

---

## What I learned / challenges

### 1. Designing a reliable tool router without fine-tuning
The hardest part was writing tool descriptions that make the LLM consistently pick the *right* search function. An enquiry like "rock albums from the early 70s" involves both a genre and a date range — neither `get_album_by_genre` nor `get_album_by_year` alone handles it. The fix was adding a `get_album_by_generated_query` fallback that lets the LLM write raw SQL for anything multi-dimensional, while keeping the simple tools for the common cases. Getting the description boundaries right so the model didn't over-route to the SQL generator took several iterations.

### 2. Managing conversation state across a tool-calling loop
The workflow agent maintains a running `conversation_history` list that grows with every turn: system prompt → user message → assistant tool call → function response → assistant reply → next user message. Keeping this structure valid for the Gemini API (which uses the OpenAI message format) required separate helper functions (`add_system`, `append_tool_response`, `append_function_response`) rather than ad-hoc dict construction. A single misplaced role field breaks the entire chain silently.

### 3. Two agent architectures for the same problem
Building both a ReAct agent (`reactagent.py`) and a workflow agent (`workflowagent.py`) on the same toolset exposed a real trade-off: the workflow agent preserves full conversational context (useful for follow-up questions) but accumulates a large message window; the ReAct agent processes the whole CSV in one structured pass, which is faster and cheaper but loses per-enquiry conversational nuance. Neither is universally better — the right choice depends on whether the use case needs memory across turns.

### 4. LangSmith tracing for async debugging
Adding `@traceable` to agent functions meant every tool call, argument, and response was captured in the LangSmith dashboard without changing business logic. This was essential for debugging — instead of reading interleaved print statements, I could inspect the exact JSON sent to and returned from each function call, in order, across a full run. The key lesson: instrument *before* you hit hard bugs, not after.

### 5. SQL injection via LLM-generated queries
`get_album_by_generated_query` executes a raw SQL string produced by the model directly against the database. In a production system this is a serious security risk — a prompt injection could exfiltrate or corrupt data. The current implementation is acceptable for a local, read-only demo database, but the fix would be to parse and validate the LLM output (allow only `SELECT`, restrict to the `music` table, use parameterised queries for any user-supplied values) before execution.

---

## Demo

> Live demo link coming soon — will be updated on deployment.

---

## How to run

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- A Google Gemini API key

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd records_inventory
uv sync
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_API_BASE=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_API_MODEL=gemini-2.0-flash

# Optional — for LangSmith tracing
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=records-inventory
```

### 3. Add customer enquiries

Edit `resources/emails.csv`. The file expects an `email` column:

```csv
email
Do you have any David Bowie albums?
What rock records do you have from the early 70s?
Any jazz albums in stock?
```

### 4. Run the agent

**Workflow agent** (multi-turn, conversational):
```bash
uv run python workflowagent.py
```
Responses written to `resources/email_responses.csv`.

**ReAct agent** (single-pass batch processing):
```bash
uv run python reactagent.py
```
Responses written to `resources/email_responses_2.csv`.


Built by Aghogho Joy Olokpa — connect with me on LinkedIn https://www.linkedin.com/in/aghogho-olokpa-1b0b11115.