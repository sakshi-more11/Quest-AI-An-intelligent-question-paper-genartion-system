# =========================================================
# QUEST-AI — Professor Edition v2.0
# Features:
#   - Google Form for input preferences (pre-fill URL trick)
#   - Dynamic tokenization via tiktoken + LangChain splitter
#   - Adaptive chunk/question sizing based on content volume
#   - Feedback Google Form post-generation
#   - Feedback-driven regeneration loop
# =========================================================

# ── Install requirements ──────────────────────────────────
# pip install streamlit pdfplumber pandas reportlab openai tiktoken langchain langchain-community langchain-text-splitters
# ─────────────────────────────────────────────────────────

import os
import math
import re
import json
import tempfile
import time

import pandas as pd
import pdfplumber
import streamlit as st
import tiktoken
from openai import OpenAI, OpenAIError
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ModuleNotFoundError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

# ══════════════════════════════════════════════════════════
# SECTION 1 — CONSTANTS & CONFIG
# ══════════════════════════════════════════════════════════

# Token budget per chunk sent to the LLM.
# llama-3.1-8b-instant has a 128k context window and better free-tier throughput.
# These defaults intentionally stay conservative to avoid Groq rate limits.
GROQ_MODEL = "llama-3.1-8b-instant"
TOKENS_PER_CHUNK = 600          # tokens per content chunk
MAX_CHUNKS = 6                  # hard ceiling on chunks processed
MIN_Q_PER_CHUNK = 3             # floor
MAX_Q_PER_CHUNK = 4             # ceiling
MAX_TOTAL_QUESTIONS = 24        # hard ceiling on total questions
REGEN_MAX_TOTAL_QUESTIONS = 12  # feedback regeneration uses fewer calls
GROQ_MAX_RETRIES = 6            # retry transient rate limits instead of failing
GROQ_REQUEST_DELAY_SECONDS = 12 # pause between successful Groq requests

# Google Form URLs — replace the base URL with your actual form
# The `entry.XXXXXXX` parameters are field IDs from your Google Form.
# How to get them: open your form → right-click any field → Inspect → find `entry.` IDs.
#
# INPUT FORM — professor fills this BEFORE generating
INPUT_FORM_BASE_URL = (
    "https://docs.google.com/forms/d/e/YOUR_INPUT_FORM_ID/viewform"
    "?usp=pp_url"
    "&entry.111111111={complexity}"        # e.g., Low / Medium / High
    "&entry.222222222={bt_levels}"         # e.g., BT3,BT4,BT5
    "&entry.333333333={question_length}"   # e.g., Short / Medium / Detailed
    "&entry.444444444={num_co}"            # e.g., 6
    "&entry.555555555={subject_name}"      # e.g., Operating Systems
)

# FEEDBACK FORM — professor fills this AFTER generation
FEEDBACK_FORM_BASE_URL = (
    "https://docs.google.com/forms/d/e/YOUR_FEEDBACK_FORM_ID/viewform"
    "?usp=pp_url"
    "&entry.666666666={subject_name}"
    "&entry.777777777={total_questions}"
)

INPUT_FORM_CONFIGURED = "YOUR_INPUT_FORM_ID" not in INPUT_FORM_BASE_URL
FEEDBACK_FORM_CONFIGURED = "YOUR_FEEDBACK_FORM_ID" not in FEEDBACK_FORM_BASE_URL

# ══════════════════════════════════════════════════════════
# SECTION 2 — API CLIENT
# ══════════════════════════════════════════════════════════

def get_client():
    """Returns an OpenAI-compatible client pointed at Groq."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)


# ══════════════════════════════════════════════════════════
# SECTION 3 — PDF EXTRACTION
# ══════════════════════════════════════════════════════════

def extract_text_from_pdf(files) -> str:
    """Extract plain text from one or more PDF file objects."""
    text = ""
    for file in files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    return text


# ══════════════════════════════════════════════════════════
# SECTION 4 — DYNAMIC TOKENIZATION & CHUNKING
# Why tiktoken?
#   Word counts are a rough proxy. Different words tokenize
#   differently (e.g., "subconsciously" = 4 tokens).
#   tiktoken gives exact token counts matching LLM behavior,
#   so we never exceed context limits.
#
# Why RecursiveCharacterTextSplitter?
#   It splits on paragraph → sentence → word boundaries in order,
#   preserving semantic coherence instead of cutting mid-sentence.
# ══════════════════════════════════════════════════════════

@st.cache_resource
def get_tokenizer():
    """Cache the tokenizer so it's not reloaded on every rerun."""
    # cl100k_base is used by GPT-4 / llama-compatible models
    return tiktoken.get_encoding("cl100k_base")


def estimate_tokens(text: str) -> int:
    """Fallback token estimate for offline/flaky tiktoken downloads."""
    return max(1, math.ceil(len(text) / 4))


def count_tokens(text: str) -> int:
    try:
        enc = get_tokenizer()
        return len(enc.encode(text))
    except Exception as exc:
        if "tokenizer_warning_shown" not in st.session_state:
            st.session_state.tokenizer_warning_shown = True
            st.warning(
                "Could not load the exact tiktoken tokenizer, so Quest-AI is using "
                "a safe approximate token count for this run. This usually happens "
                "when the first-time tokenizer download is interrupted."
            )
        return estimate_tokens(text)


def smart_chunk(content: str, tokens_per_chunk: int = TOKENS_PER_CHUNK) -> list[str]:
    """
    Split content into semantically coherent chunks using LangChain's
    RecursiveCharacterTextSplitter, calibrated to token budget.

    The splitter works by trying to split on:
      1. Double newlines (paragraphs)
      2. Single newlines
      3. Sentence-ending punctuation
      4. Spaces (word boundary fallback)
    This order preserves context far better than raw word splitting.
    """
    # Approximate chars from tokens: 1 token ≈ 4 chars in English
    char_budget = tokens_per_chunk * 4

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=char_budget,
        chunk_overlap=char_budget // 10,          # 10% overlap keeps context at boundaries
        separators=["\n\n", "\n", ". ", "! ", "? ", " "],
        length_function=len,
    )
    return splitter.split_text(content)


def compute_adaptive_params(
    content: str,
    syllabus: str,
    num_co: int,
    tokens_per_chunk: int = TOKENS_PER_CHUNK,
    regeneration: bool = False,
) -> dict:
    """
    Dynamically decide:
      - How many chunks to process
      - How many questions per chunk
    Based on: total tokens in content, syllabus topic count, and CO count.

    Returns a dict with keys: total_tokens, num_chunks, q_per_chunk, est_total
    """
    total_tokens = count_tokens(content)
    syllabus_lines = [l for l in syllabus.splitlines() if l.strip()]
    topic_count = max(1, len(syllabus_lines))

    # Raw chunk count from the selected token budget.
    tokens_per_chunk = max(1, int(tokens_per_chunk or TOKENS_PER_CHUNK))
    raw_chunks = math.ceil(total_tokens / tokens_per_chunk)
    num_chunks = min(raw_chunks, MAX_CHUNKS)

    # Questions per chunk: scale with topic & CO depth
    # More topics / COs → professor expects more varied coverage
    depth_score = topic_count + num_co
    if depth_score <= 5:
        q_per_chunk = MIN_Q_PER_CHUNK
    elif depth_score <= 10:
        q_per_chunk = 4
    elif depth_score <= 20:
        q_per_chunk = 4
    elif depth_score <= 35:
        q_per_chunk = 4
    else:
        q_per_chunk = MAX_Q_PER_CHUNK

    q_per_chunk = min(q_per_chunk, MAX_Q_PER_CHUNK)

    if regeneration:
        q_per_chunk = min(q_per_chunk, 3)

    # Cap total
    total_limit = REGEN_MAX_TOTAL_QUESTIONS if regeneration else MAX_TOTAL_QUESTIONS
    if num_chunks * q_per_chunk > total_limit:
        num_chunks = max(1, total_limit // q_per_chunk)

    return {
        "total_tokens": total_tokens,
        "num_chunks": num_chunks,
        "q_per_chunk": q_per_chunk,
        "est_total": num_chunks * q_per_chunk,
    }


# ══════════════════════════════════════════════════════════
# SECTION 5 — DYNAMIC SYSTEM PROMPT BUILDER
# The system prompt is now assembled from form responses
# rather than being hardcoded, making it fully configurable.
# ══════════════════════════════════════════════════════════

def build_system_prompt(prefs: dict) -> str:
    """
    Build a dynamic system prompt from professor's form preferences.
    prefs keys: bt_levels, difficulty_mix, question_length, num_co, subject_name, feedback_notes
    """
    bt_str = ", ".join(prefs.get("bt_levels", ["BT2","BT3","BT4","BT5","BT6"]))
    q_length = prefs.get("question_length", "Medium")
    num_co = prefs.get("num_co", 6)
    feedback_notes = prefs.get("feedback_notes", "").strip()

    length_guide = {
        "Short": "Each question should be 1–2 sentences. Concise and direct.",
        "Medium": "Each question should be 2–3 sentences. Include context and a clear task.",
        "Detailed": "Each question should be 3–5 sentences. Include scenario setup, constraints, and expected deliverable.",
    }.get(q_length, "Each question should be 2–3 sentences.")

    feedback_block = ""
    if feedback_notes:
        feedback_block = f"""
=== PROFESSOR FEEDBACK (APPLY STRICTLY) ===
The professor has reviewed previous output and provided the following feedback.
You MUST incorporate all of these points in the new questions:
{feedback_notes}
============================================
"""

    return f"""You are an expert question paper setter for undergraduate engineering examinations in {prefs.get('subject_name', 'the subject')}.
Your task is to generate exam-quality questions STRICTLY aligned with Bloom's Taxonomy (BT) levels.

{feedback_block}

=== ALLOWED BT LEVELS ===
Only generate questions for these BT levels: {bt_str}

=== BLOOM'S TAXONOMY ALIGNMENT — MANDATORY RULES ===

BT2 (Understand):
  - Explain a mechanism, compare concepts, paraphrase a principle.
  - Starters: "Explain why...", "Describe how...", "Compare and contrast...", "Distinguish between...", "Summarize..."
  - Complexity: Low

BT3 (Apply):
  - Apply a concept/formula to a NEW scenario. Solve numericals.
  - Starters: "Calculate...", "Implement...", "Solve...", "Apply...", "Demonstrate...", "Construct..."
  - Complexity: Medium

BT4 (Analyze):
  - Break down a system, trace execution, diagnose failures.
  - Starters: "Analyze...", "Differentiate and justify...", "Trace the execution...", "Diagnose...", "Examine..."
  - Complexity: Medium

BT5 (Evaluate):
  - Make a judgment, critique a design, assess trade-offs.
  - Starters: "Evaluate...", "Critique...", "Justify...", "Recommend and justify...", "Assess trade-offs..."
  - Complexity: High

BT6 (Create):
  - Design a system, write an algorithm from scratch, propose a novel solution.
  - Starters: "Design...", "Construct...", "Develop an algorithm...", "Propose...", "Formulate..."
  - Complexity: High

=== QUESTION LENGTH REQUIREMENT ===
{length_guide}

=== ABSOLUTE PROHIBITIONS ===
- NEVER generate BT1 (Remember) questions. No "Define", "List", "State", "What is", "Write short note on".
- NEVER generate a question answerable in one sentence from memory.
- NEVER use Bloom's taxonomy level names (Remember, Understand, etc.) in question text.
- Every question must be scenario/application-specific.

=== CO MAPPING ===
- Map each question to CO1 through CO{num_co}.
- Higher BT levels (BT5, BT6) → higher COs (CO{max(1,num_co-1)}, CO{num_co}).
- Lower BT levels (BT2, BT3) → lower COs (CO1, CO2, CO3).

=== CHAPTER DETECTION ===
- Read the syllabus to identify chapter/module names.
- Assign each question to the EXACT chapter name from the syllabus.
- If uncertain, pick the most specific matching chapter.

=== COMPLEXITY RULES ===
- BT2 → Low
- BT3 → Medium
- BT4 → Medium
- BT5 → High
- BT6 → High

=== OUTPUT FORMAT ===
Return ONLY a pipe-separated table with this EXACT header, then one row per question:
Question | BT Level | CO | Chapter | Complexity

Rules:
- No markdown, no bold, no asterisks, no extra columns.
- BT Level: BT2, BT3, BT4, BT5, or BT6 only.
- Complexity: Low, Medium, or High only.
- Every row must have exactly 5 pipe-separated fields.
"""


# ══════════════════════════════════════════════════════════
# SECTION 6 — QUESTION GENERATION
# ══════════════════════════════════════════════════════════

def build_user_prompt(chunk: str, syllabus: str, num_questions: int, prefs: dict) -> str:
    bt_str = ", ".join(prefs.get("bt_levels", ["BT2","BT3","BT4","BT5","BT6"]))
    difficulty_mix = prefs.get("difficulty_mix", "Balanced")

    if "Hard" in difficulty_mix:
        diff_instruction = "30% Medium (BT3/BT4) and 70% High (BT5/BT6). No Low."
    elif "Medium" in difficulty_mix:
        diff_instruction = "20% Low (BT2), 60% Medium (BT3/BT4), 20% High (BT5/BT6)."
    else:
        diff_instruction = "20% Low (BT2), 40% Medium (BT3/BT4), 40% High (BT5/BT6)."

    return f"""Generate exactly {num_questions} exam questions.

ALLOWED BT LEVELS: {bt_str}
DIFFICULTY DISTRIBUTION: {diff_instruction}

SYLLABUS (for chapter name detection):
{syllabus}

CHAPTER CONTENT (base all questions on this):
{chunk}

REMINDERS:
- Questions must be scenario-based, not generic recall.
- Distribute BT levels across the allowed set — do not repeat the same level consecutively.
- Return only the pipe-separated table with header: Question | BT Level | CO | Chapter | Complexity
"""


def get_retry_delay_seconds(error_text: str, attempt: int) -> float:
    match = re.search(r"try again in\s+(\d+(?:\.\d+)?)\s*(ms|s)", error_text, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        delay = value / 1000 if match.group(2).lower() == "ms" else value
    else:
        delay = min(2 ** attempt, 30)
    return max(delay + 0.5, 1.0)


def generate_questions(chunk: str, syllabus: str, num_questions: int,
                        prefs: dict, client) -> str:
    system_prompt = build_system_prompt(prefs)
    user_prompt = build_user_prompt(chunk, syllabus, num_questions, prefs)
    max_output_tokens = min(700, max(350, num_questions * 100))

    for attempt in range(GROQ_MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=max_output_tokens,
            )
            return response.choices[0].message.content
        except OpenAIError as exc:
            error_text = str(exc)
            is_rate_limit = "rate_limit" in error_text.lower() or "429" in error_text
            if is_rate_limit and attempt < GROQ_MAX_RETRIES:
                delay = get_retry_delay_seconds(error_text, attempt)
                st.warning(
                    f"Groq rate limit reached. Waiting {delay:.1f}s, then retrying. "
                    f"Current model: {GROQ_MODEL}. If this repeats on the first section, "
                    "your Groq key has reached its current quota and you need to wait, "
                    "change keys, or upgrade the Groq plan."
                )
                time.sleep(delay)
                continue
            raise RuntimeError(f"Generation failed: {exc}") from exc

    raise RuntimeError("Generation failed after retrying the Groq request.")


# ══════════════════════════════════════════════════════════
# SECTION 7 — PARSING & CLEANING
# ══════════════════════════════════════════════════════════

def parse_to_df(text: str) -> pd.DataFrame:
    rows = []
    for line in text.split("\n"):
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) != 5:
            continue
        if all(set(p) <= {"-", ":", "=", " "} for p in parts):
            continue
        if parts[0].lower() == "question":
            continue
        if any(parts):
            rows.append(parts)
    return pd.DataFrame(rows, columns=["Question", "BT Level", "CO", "Chapter", "Complexity"])


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["Question"]).copy()
    df = df[df["Question"] != "Question"]
    df["BT Level"] = df["BT Level"].str.upper().str.strip()
    df = df[~df["BT Level"].str.contains("BT1", na=False)]

    def normalize_complexity(val, bt):
        v = str(val).strip().lower()
        if "high" in v: return "High"
        if "med" in v: return "Medium"
        if "low" in v: return "Low"
        bt_upper = str(bt).upper()
        if "BT5" in bt_upper or "BT6" in bt_upper: return "High"
        if "BT3" in bt_upper or "BT4" in bt_upper: return "Medium"
        return "Low"

    df["Complexity"] = df.apply(
        lambda r: normalize_complexity(r["Complexity"], r["BT Level"]), axis=1
    )
    df["CO"] = df["CO"].str.upper().str.strip()
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    return df


# ══════════════════════════════════════════════════════════
# SECTION 8 — PDF EXPORT
# ══════════════════════════════════════════════════════════

def generate_pdf(df: pd.DataFrame, subject_name: str = "Question Bank") -> str:
    file_path = os.path.join(tempfile.gettempdir(), "question_bank.pdf")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    doc = SimpleDocTemplate(
        file_path, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=2*cm, bottomMargin=2*cm,
    )
    styles = getSampleStyleSheet()
    q_style = ParagraphStyle("QS", parent=styles["Normal"], fontSize=8, leading=11)
    n_style = ParagraphStyle("NS", parent=styles["Normal"], fontSize=8, leading=11)
    t_style = ParagraphStyle("TS", parent=styles["Heading1"], fontSize=14, spaceAfter=12)

    elements = [Paragraph(subject_name, t_style), Spacer(1, 0.3*cm)]
    header = ["#", "Question", "BT Level", "CO", "Chapter", "Complexity"]
    data = [header]
    for idx, row in df.iterrows():
        data.append([
            str(idx),
            Paragraph(row["Question"], q_style),
            Paragraph(row["BT Level"], n_style),
            Paragraph(row["CO"], n_style),
            Paragraph(row["Chapter"], n_style),
            Paragraph(row["Complexity"], n_style),
        ])

    col_widths = [0.8*cm, 7.5*cm, 1.8*cm, 1.5*cm, 3.5*cm, 2.0*cm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1B2A41")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F0F4F8")]),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    doc.build(elements)
    return file_path


# ══════════════════════════════════════════════════════════
# SECTION 9 — GOOGLE FORM URL BUILDER
# We use Google Forms' pre-fill URL feature.
# The form is EMBEDDED as an iframe so professors fill it
# inside the app. On submit, responses go to your Google Sheet.
# We read their choices back via session state (manual entry
# fallback since Forms don't return data to Streamlit directly).
# ══════════════════════════════════════════════════════════

def build_feedback_form_url(subject_name: str, total_questions: int) -> str:
    return FEEDBACK_FORM_BASE_URL.format(
        subject_name=subject_name.replace(" ", "+"),
        total_questions=total_questions,
    )


# ══════════════════════════════════════════════════════════
# SECTION 10 — STREAMLIT UI
# ══════════════════════════════════════════════════════════

st.set_page_config(page_title="Quest-AI", page_icon="📚", layout="wide")

# ── Custom CSS ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
.main { background: #0f1117; }

.hero {
    background: linear-gradient(135deg, #1B2A41 0%, #0f1117 60%, #162032 100%);
    border: 1px solid #2a3f5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
}
.hero h1 { font-size: 2.4rem; margin: 0; color: #e8f4fd; letter-spacing: -1px; }
.hero p { color: #7a9cc4; margin-top: 6px; font-size: 1rem; }

.step-badge {
    background: #162032;
    border: 1px solid #2a3f5f;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 0.78rem;
    color: #7a9cc4;
    font-family: 'JetBrains Mono', monospace;
    display: inline-block;
    margin-bottom: 1rem;
}

.form-embed-note {
    background: #162032;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.2rem;
    color: #a0c4e8;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

.metric-card {
    background: #162032;
    border: 1px solid #2a3f5f;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    border: none;
    color: white;
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    border-radius: 8px;
    padding: 0.6rem 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📚 Quest-AI</h1>
    <p>Intelligent Question Bank Generator · Bloom's Taxonomy · CO Mapping · Feedback Loop</p>
</div>
""", unsafe_allow_html=True)

# ── Init session state ───────────────────────────────────
for key in ["prefs_confirmed", "final_df", "raw_outputs", "feedback_submitted",
            "feedback_notes", "regen_requested", "content_text", "syllabus_text"]:
    if key not in st.session_state:
        st.session_state[key] = None if key in ["final_df", "raw_outputs", "feedback_notes", "content_text", "syllabus_text"] else False

client = get_client()
if client is None:
    st.warning("⚠️ No Groq API key found. Add `GROQ_API_KEY` to `.streamlit/secrets.toml`.")

# ══════════════════════════════════════════════════════════
# STEP 1 — INPUT PREFERENCES FORM
# We embed the Google Form as an iframe.
# After submission, professor manually confirms their choices
# in the sidebar so Streamlit knows the preferences.
# (Google Forms don't send data back to Streamlit directly —
#  this is the standard workaround for embedded Forms.)
# ══════════════════════════════════════════════════════════

st.markdown('<div class="step-badge">STEP 1 of 4 — Professor Preferences</div>', unsafe_allow_html=True)

if INPUT_FORM_CONFIGURED:
    with st.expander("📋 Fill Preference Form (Google Form)", expanded=not st.session_state.prefs_confirmed):
        st.markdown("""
<div class="form-embed-note">
    Fill the form below to configure your question bank. After submitting the form,
    confirm your choices in the sidebar on the left so the system can use them.
</div>
""", unsafe_allow_html=True)

        st.components.v1.html(f"""
<iframe
    src="{INPUT_FORM_BASE_URL.split('?')[0]}?embedded=true"
    width="100%"
    height="520"
    frameborder="0"
    marginheight="0"
    marginwidth="0"
    style="border-radius:8px; border:1px solid #2a3f5f; background:#0f1117;">
    Loading form…
</iframe>
""", height=540)
else:
    st.info("Set the professor preferences in the sidebar, then click Confirm & Proceed to Upload.")

# ── Sidebar: Preference confirmation ────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Confirm Preferences")
    st.caption("Set the values the generator should use.")

    subject_name = st.text_input("Subject Name", value="Operating Systems")

    bt_options = st.multiselect(
        "Bloom's Taxonomy Levels",
        options=["BT2", "BT3", "BT4", "BT5", "BT6"],
        default=["BT2", "BT3", "BT4", "BT5", "BT6"],
    )

    difficulty_mix = st.selectbox(
        "Difficulty Distribution",
        ["Balanced (BT2–BT6 mix)", "Mostly Hard (BT5 & BT6 dominant)", "Mostly Medium (BT3 & BT4 dominant)"],
    )

    question_length = st.selectbox(
        "Question Length",
        ["Short", "Medium", "Detailed"],
        index=1,
        help="Short: 1-2 sentences · Medium: 2-3 sentences · Detailed: 3-5 sentences with scenario",
    )

    num_co = st.number_input(
        "Number of Course Outcomes (COs)",
        min_value=1, max_value=12, value=6,
    )

    tokens_per_chunk = st.slider(
        "Token Budget per Chunk",
        min_value=400, max_value=2000, value=TOKENS_PER_CHUNK, step=100,
        help="Higher = fewer but larger chunks. Lower = more granular chunking. Default 800 works well for most syllabi.",
    )

    if st.button("✅ Confirm & Proceed to Upload", type="primary", use_container_width=True):
        st.session_state.prefs_confirmed = True
        st.session_state.prefs = {
            "subject_name": subject_name,
            "bt_levels": bt_options,
            "difficulty_mix": difficulty_mix,
            "question_length": question_length,
            "num_co": num_co,
            "tokens_per_chunk": tokens_per_chunk,
            "feedback_notes": "",
        }
        st.session_state.final_df = None
        st.session_state.raw_outputs = None
        st.session_state.feedback_notes = None
        st.session_state.regen_requested = False
        st.session_state.content_text = None
        st.session_state.syllabus_text = None
        st.success("Preferences saved!")

# ══════════════════════════════════════════════════════════
# STEP 2 — FILE UPLOAD
# ══════════════════════════════════════════════════════════

if st.session_state.prefs_confirmed:
    st.divider()
    st.markdown('<div class="step-badge">STEP 2 of 4 — Upload Course Material</div>', unsafe_allow_html=True)

    ul1, ul2 = st.columns(2)
    with ul1:
        pdf_files = st.file_uploader(
            "📂 Chapter Notes / Textbook PDFs",
            type="pdf", accept_multiple_files=True,
        )
    with ul2:
        syllabus_file = st.file_uploader(
            "📋 Course Syllabus",
            type=["pdf", "txt"],
        )

    if pdf_files:
        st.caption(f"✅ {len(pdf_files)} chapter file(s) uploaded")
    if syllabus_file:
        st.caption(f"✅ Syllabus: **{syllabus_file.name}**")

# ══════════════════════════════════════════════════════════
# STEP 3 — GENERATION
# ══════════════════════════════════════════════════════════

    has_uploaded_inputs = bool(pdf_files and syllabus_file)
    has_saved_inputs = bool(st.session_state.content_text and st.session_state.syllabus_text)

    if has_uploaded_inputs or (st.session_state.regen_requested and has_saved_inputs):
        st.divider()
        st.markdown('<div class="step-badge">STEP 3 of 4 — Generate Question Bank</div>', unsafe_allow_html=True)

        # Show adaptive plan preview
        with st.spinner("Analyzing content volume..."):
            prefs = st.session_state.prefs
            if has_uploaded_inputs:
                content_preview = extract_text_from_pdf(pdf_files)
                syllabus_preview = (
                    extract_text_from_pdf([syllabus_file])
                    if syllabus_file.type == "application/pdf"
                    else syllabus_file.read().decode("utf-8")
                )
                syllabus_file.seek(0)  # reset for later reads
            else:
                content_preview = st.session_state.content_text
                syllabus_preview = st.session_state.syllabus_text
            st.session_state.content_text = content_preview
            st.session_state.syllabus_text = syllabus_preview

            params = compute_adaptive_params(
                content_preview,
                syllabus_preview,
                prefs["num_co"],
                tokens_per_chunk=prefs["tokens_per_chunk"],
                regeneration=bool(st.session_state.regen_requested),
            )

        st.markdown("#### 🔍 Auto-Detected Generation Plan")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Tokens", f"{params['total_tokens']:,}")
        c2.metric("Chunk Budget", f"{prefs['tokens_per_chunk']} tokens")
        c3.metric("Sections", params["num_chunks"])
        c4.metric("Q / Section", params["q_per_chunk"])
        c5.metric("Est. Total Q", params["est_total"])

        should_generate = st.button(
            "🚀 Generate Question Bank", type="primary",
            use_container_width=True,
            disabled=(client is None),
        )

        if should_generate or st.session_state.regen_requested:
            is_regeneration = st.session_state.regen_requested

            # If this is a feedback-driven regen, update prefs
            if st.session_state.feedback_notes:
                prefs["feedback_notes"] = st.session_state.feedback_notes

            content = st.session_state.content_text
            syllabus = st.session_state.syllabus_text

            if not content or not syllabus:
                with st.spinner("📄 Extracting text..."):
                    content = extract_text_from_pdf(pdf_files)
                    syllabus_file.seek(0)
                    syllabus = (
                        extract_text_from_pdf([syllabus_file])
                        if syllabus_file.type == "application/pdf"
                        else syllabus_file.read().decode("utf-8")
                    )
                    st.session_state.content_text = content
                    st.session_state.syllabus_text = syllabus

            if not content.strip():
                st.error("Could not extract text from PDFs. Ensure they are text-based, not scanned images.")
                st.session_state.regen_requested = False
                st.stop()

            # Smart chunking via LangChain + tiktoken
            spinner_text = "🔄 Regenerating with feedback..." if is_regeneration else "✂️ Tokenizing and chunking content..."
            with st.spinner(spinner_text):
                all_chunks = smart_chunk(content, tokens_per_chunk=prefs["tokens_per_chunk"])
                params = compute_adaptive_params(
                    content,
                    syllabus,
                    prefs["num_co"],
                    tokens_per_chunk=prefs["tokens_per_chunk"],
                    regeneration=is_regeneration,
                )
                selected_chunks = all_chunks[:params["num_chunks"]]

            st.info(f"📊 Processing **{len(selected_chunks)} sections** × **{params['q_per_chunk']} questions** = ~**{len(selected_chunks) * params['q_per_chunk']} questions**")

            all_dfs, raw_outputs = [], []
            progress_bar = st.progress(0, text="Starting...")

            for i, chunk in enumerate(selected_chunks):
                progress_bar.progress(
                    i / len(selected_chunks),
                    text=f"Section {i+1}/{len(selected_chunks)} — generating questions..."
                )
                try:
                    output = generate_questions(
                        chunk, syllabus, params["q_per_chunk"], prefs, client
                    )
                    raw_outputs.append(output)
                    parsed = parse_to_df(output)
                    if not parsed.empty:
                        all_dfs.append(parsed)
                    if i < len(selected_chunks) - 1:
                        time.sleep(GROQ_REQUEST_DELAY_SECONDS)
                except RuntimeError as exc:
                    st.error(str(exc))
                    st.session_state.regen_requested = False
                    st.stop()

            progress_bar.progress(1.0, text="✅ Done!")

            if not all_dfs:
                st.warning("No questions parsed. See raw output in debug section.")
                st.session_state.regen_requested = False
                st.stop()

            final_df = pd.concat(all_dfs, ignore_index=True)
            final_df = clean_dataframe(final_df)

            st.session_state.final_df = final_df
            st.session_state.raw_outputs = raw_outputs
            st.session_state.feedback_submitted = False
            st.session_state.regen_requested = False
            if is_regeneration:
                st.success("Regenerated the question bank using your feedback.")

# ── Display Results ──────────────────────────────────────
        if st.session_state.final_df is not None:
            final_df = st.session_state.final_df

            st.success(f"✅ **{len(final_df)} questions** generated!")

            # Summary
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Total", len(final_df))
            m2.metric("🔴 High", len(final_df[final_df["Complexity"]=="High"]))
            m3.metric("🟡 Medium", len(final_df[final_df["Complexity"]=="Medium"]))
            m4.metric("🟢 Low", len(final_df[final_df["Complexity"]=="Low"]))
            m5.metric("Chapters", final_df["Chapter"].nunique())

            # Charts
            ch1, ch2 = st.columns(2)
            with ch1:
                st.markdown("**BT Level Distribution**")
                st.bar_chart(final_df["BT Level"].value_counts().sort_index())
            with ch2:
                st.markdown("**Complexity Breakdown**")
                st.bar_chart(final_df["Complexity"].value_counts())

            # Filter & browse
            st.markdown("#### 🔍 Browse & Filter")
            f1, f2, f3 = st.columns(3)
            bt_filter = f1.multiselect("BT Level", sorted(final_df["BT Level"].unique()))
            cx_filter = f2.multiselect("Complexity", ["Low","Medium","High"])
            ch_filter = f3.multiselect("Chapter", sorted(final_df["Chapter"].unique()))

            display_df = final_df.copy()
            if bt_filter: display_df = display_df[display_df["BT Level"].isin(bt_filter)]
            if cx_filter: display_df = display_df[display_df["Complexity"].isin(cx_filter)]
            if ch_filter: display_df = display_df[display_df["Chapter"].isin(ch_filter)]

            st.dataframe(display_df, use_container_width=True, height=420)
            st.caption(f"Showing {len(display_df)} of {len(final_df)} questions")

            # Downloads
            st.markdown("#### ⬇️ Download")
            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button(
                    "📄 Download CSV", final_df.to_csv(index=True),
                    file_name="question_bank.csv", mime="text/csv",
                    use_container_width=True,
                )
            with dl2:
                try:
                    pdf_path = generate_pdf(final_df, prefs.get("subject_name","Question Bank"))
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📑 Download PDF", f,
                            file_name="question_bank.pdf", mime="application/pdf",
                            use_container_width=True,
                        )
                except Exception as e:
                    st.warning(f"PDF export failed: {e}")

            # Debug
            with st.expander("🛠️ Raw model output (debug)"):
                for idx, out in enumerate(st.session_state.raw_outputs or [], 1):
                    st.text_area(f"Section {idx}", out, height=200)

# ══════════════════════════════════════════════════════════
# STEP 4 — FEEDBACK FORM & REGENERATION LOOP
# After generation, embed the feedback Google Form.
# Professor submits quality ratings and suggestions.
# Those suggestions are captured in the sidebar and used
# to regenerate the question bank with improved prompting.
# ══════════════════════════════════════════════════════════

            st.divider()
            st.markdown('<div class="step-badge">STEP 4 of 4 — Quality Feedback & Regeneration</div>', unsafe_allow_html=True)

            if FEEDBACK_FORM_CONFIGURED:
                st.markdown("""
<div class="form-embed-note">
    Review the generated questions above, then fill the feedback form below.
    If you request improvements, enter your specific feedback in the box below the form
    and click <strong>Regenerate</strong> — the system will incorporate your feedback.
</div>
""", unsafe_allow_html=True)
            else:
                st.markdown("""
<div class="form-embed-note">
    Review the generated questions above. If you want improvements, enter specific feedback below
    and click <strong>Regenerate</strong> — the system will incorporate your suggestions.
</div>
""", unsafe_allow_html=True)

            if FEEDBACK_FORM_CONFIGURED:
                feedback_form_url = build_feedback_form_url(
                    prefs.get("subject_name",""), len(final_df)
                )
                st.components.v1.html(f"""
<iframe
    src="{feedback_form_url.split('?')[0]}?embedded=true"
    width="100%"
    height="600"
    frameborder="0"
    style="border-radius:8px; border:1px solid #2a3f5f;">
    Loading feedback form…
</iframe>
""", height=620)
            # Feedback capture for regeneration
            st.markdown("#### 💬 Enter Improvement Suggestions for Regeneration")
            st.caption(
                "Type any specific feedback here (e.g., 'Add more numerical problems', "
                "'Questions are too easy for BT5', 'Focus more on Chapter 3'). "
                "Leave blank if the quality is acceptable."
            )
            feedback_text = st.text_area(
                "Feedback / Suggestions",
                value=st.session_state.feedback_notes or "",
                height=120,
                placeholder="e.g., Generate more design-based BT6 questions for the Memory Management chapter. Reduce BT2 questions.",
            )

            regen_col1, regen_col2 = st.columns([2, 1])
            with regen_col1:
                if st.button("🔄 Regenerate with Feedback", type="primary", use_container_width=True,
                             disabled=(client is None or not feedback_text.strip())):
                    st.session_state.feedback_notes = feedback_text.strip()
                    st.session_state.prefs["feedback_notes"] = feedback_text.strip()
                    st.session_state.regen_requested = True
                    st.session_state.final_df = None
                    st.session_state.raw_outputs = None
                    st.session_state.feedback_submitted = False
                    st.rerun()
            with regen_col2:
                if st.button("✅ Accept & Finalize", use_container_width=True):
                    st.session_state.feedback_submitted = True
                    st.balloons()
                    st.success("Question bank finalized! Download your files above.")

            if st.session_state.feedback_submitted:
                st.info("🎉 Done! Your question bank has been finalized. You can upload new files to start again.")
