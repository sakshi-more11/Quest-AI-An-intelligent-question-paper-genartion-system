# =========================================
# QUEST-AI — Professor Edition
# Auto-scales question count & chunks based
# on syllabus + notes size automatically.
# =========================================

# Install:
# pip install streamlit pdfplumber pandas reportlab openai

import os
import math

import pandas as pd
import pdfplumber
import streamlit as st
from openai import OpenAI, OpenAIError
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


# ==========================
# CONFIG
# ==========================
def get_api_key():
    return (
        st.secrets.get("GROQ_API_KEY")
        or os.getenv("GROQ_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )


api_key = get_api_key()
client = None

if api_key:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )


# ==========================
# PDF TEXT EXTRACTION
# ==========================
def extract_text_from_pdf(files):
    text = ""
    for file in files:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    return text


# ==========================
# AUTO SIZING LOGIC
# Decides chunks & questions per chunk
# based on content volume automatically
# ==========================
WORDS_PER_CHUNK = 300
MAX_Q_PER_CHUNK = 15
MAX_TOTAL_QUESTIONS = 120
MAX_CHUNKS = 30


def compute_chunk_params(content: str, syllabus: str):
    """
    Returns (chunk_size, num_chunks, questions_per_chunk) computed
    from the volume of content and syllabus text.
    """
    word_count = len(content.split())
    syllabus_topics = max(1, len([l for l in syllabus.splitlines() if l.strip()]))

    # Number of chunks: one per 500 words, capped at MAX_CHUNKS
    raw_chunks = math.ceil(word_count / WORDS_PER_CHUNK)
    num_chunks = min(raw_chunks, MAX_CHUNKS)

    # Questions per chunk: scale with syllabus depth
    if syllabus_topics <= 1:
        q_per_chunk = 4
    elif syllabus_topics <= 3:
        q_per_chunk = 6
    elif syllabus_topics <= 5:
        q_per_chunk = 8
    else:
        q_per_chunk = MAX_Q_PER_CHUNK

    # Cap total
    if num_chunks * q_per_chunk > MAX_TOTAL_QUESTIONS:
        num_chunks = math.ceil(MAX_TOTAL_QUESTIONS / q_per_chunk)

    return WORDS_PER_CHUNK, num_chunks, q_per_chunk


# ==========================
# TEXT CHUNKING
# ==========================
def chunk_text(text, size=WORDS_PER_CHUNK):
    words = text.split()
    return [" ".join(words[i: i + size]) for i in range(0, len(words), size)]


# ==========================
# SYSTEM PROMPT
# ==========================
SYSTEM_PROMPT = """You are an expert question paper setter for undergraduate engineering examinations.
Your task is to generate exam-quality questions STRICTLY aligned with Bloom's Taxonomy (BT) levels.

=== BLOOM'S TAXONOMY ALIGNMENT — MANDATORY RULES ===

BT2 (Understand):
  - Student must explain a mechanism, describe a process, compare two concepts, or paraphrase a principle.
  - Must NOT be a simple one-line "what is" question.
  - Allowed starter verbs: "Explain why...", "Describe how...", "Compare and contrast...", "Distinguish between...", "Summarize the working of...", "Illustrate with an example..."
  - Complexity: LOW

BT3 (Apply):
  - Student must apply a concept, formula, or algorithm to a NEW scenario or problem.
  - Must involve solving a numerical, implementing a technique, or demonstrating a procedure.
  - Allowed starter verbs: "Calculate...", "Implement...", "Solve the following...", "Use X to...", "Apply the concept of...", "Demonstrate...", "Construct..."
  - Complexity: MEDIUM

BT4 (Analyze):
  - Student must break down a system, trace execution step-by-step, diagnose a failure, or differentiate approaches with justification.
  - Must involve reasoning about WHY something happens or HOW parts relate.
  - Allowed starter verbs: "Analyze...", "Differentiate between X and Y and justify...", "Examine...", "Trace the execution of...", "Diagnose the error in...", "Compare and justify...", "Categorize..."
  - Complexity: MEDIUM

BT5 (Evaluate):
  - Student must make a judgment, critique a design or algorithm, defend a recommendation, or assess trade-offs.
  - Must require the student to take a position and justify it with reasoning.
  - Allowed starter verbs: "Evaluate...", "Critique the design of...", "Justify your choice of...", "Recommend and justify...", "Assess the trade-offs...", "Defend...", "Prioritize and justify..."
  - Complexity: HIGH

BT6 (Create):
  - Student must design a system, write an algorithm from scratch, construct a model, or propose a novel solution.
  - Must require original synthesis — not just explaining an existing design.
  - Allowed starter verbs: "Design...", "Construct...", "Develop an algorithm for...", "Propose a solution for...", "Formulate...", "Invent...", "Generate..."
  - Complexity: HIGH

=== ABSOLUTE PROHIBITIONS ===
- NEVER generate BT1 (Remember) questions. No "Define", "List", "State", "What is", "Write short note on", "Mention", "Name" starters.
- NEVER generate a question answerable in one sentence from memory.
- NEVER generate pure theory/definition questions.
- NEVER use Bloom's taxonomy names (Remember, Understand, Apply, Analyze, Evaluate, Create) in the question text.
- Every question must be at least 2 sentences long and scenario/application-specific.

=== COMPLEXITY RULES (derived from BT level) ===
- BT2 → Complexity: Low
- BT3 → Complexity: Medium
- BT4 → Complexity: Medium
- BT5 → Complexity: High
- BT6 → Complexity: High

=== CHAPTER DETECTION ===
- Read the syllabus carefully to identify all chapter/module names.
- For every question, assign it to the most relevant chapter or module from the syllabus.
- Use the EXACT chapter/module name as it appears in the syllabus (e.g., "Module 3: Memory Management").
- If a topic spans multiple chapters, pick the most specific one.

=== CO MAPPING ===
- Map each question to CO1 through CO6 based on the topic covered.
- Higher BT levels (BT5, BT6) should generally map to higher COs (CO4-CO6).
- Lower BT levels (BT2, BT3) typically map to lower COs (CO1-CO3).

=== OUTPUT FORMAT ===
Return ONLY a pipe-separated table with this EXACT header row, then one row per question:
Question | BT Level | CO | Chapter | Complexity

Rules for the table:
- No markdown formatting, no bold, no asterisks.
- No extra columns.
- BT Level values: BT2, BT3, BT4, BT5, or BT6 only.
- Complexity values: Low, Medium, or High only.
- Chapter: exact name from syllabus.
- Every row must have exactly 5 pipe-separated fields.
"""


# ==========================
# QUESTION GENERATION
# ==========================
def generate_questions(chunk, syllabus, num_questions, bt_levels, difficulty_mix):
    if client is None:
        raise RuntimeError(
            "Missing API key. Set GROQ_API_KEY in .streamlit/secrets.toml or as environment variable."
        )

    if difficulty_mix == "Mostly Hard (BT5 & BT6 dominant)":
        diff_instruction = "Generate 30% Medium complexity (BT3/BT4) and 70% High complexity (BT5/BT6) questions. No Low complexity."
    elif difficulty_mix == "Mostly Medium (BT3 & BT4 dominant)":
        diff_instruction = "Generate 20% Low (BT2), 60% Medium (BT3/BT4), 20% High (BT5/BT6) questions."
    else:
        diff_instruction = "Generate 20% Low (BT2), 40% Medium (BT3/BT4), 40% High (BT5/BT6) questions."

    prompt = f"""Generate exactly {num_questions} exam questions for an undergraduate engineering course.

ALLOWED BT LEVELS: {bt_levels}
DIFFICULTY DISTRIBUTION: {diff_instruction}

SYLLABUS (use this to detect chapter names):
{syllabus}

CHAPTER CONTENT (base your questions on this):
{chunk}

IMPORTANT REMINDERS:
- All questions must be scenario-based, application-oriented, numerical, design-based, or diagnostic.
- Each question must be specific to the content above — not generic.
- Do NOT repeat BT levels uniformly; distribute them across the allowed levels.
- Return the table with header: Question | BT Level | CO | Chapter | Complexity
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError(f"Question generation failed: {exc}") from exc

    return response.choices[0].message.content


# ==========================
# PARSE TO DATAFRAME
# ==========================
def parse_to_df(text):
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


# ==========================
# CLEAN & VALIDATE DATAFRAME
# ==========================
def clean_dataframe(df):
    df = df.drop_duplicates(subset=["Question"]).copy()
    df = df[df["Question"] != "Question"]
    df["BT Level"] = df["BT Level"].str.upper().str.strip()
    df = df[~df["BT Level"].str.contains("BT1", na=False)]

    def normalize_complexity(val, bt):
        v = str(val).strip().lower()
        if "high" in v:
            return "High"
        if "med" in v:
            return "Medium"
        if "low" in v:
            return "Low"
        bt_upper = str(bt).upper()
        if "BT5" in bt_upper or "BT6" in bt_upper:
            return "High"
        if "BT3" in bt_upper or "BT4" in bt_upper:
            return "Medium"
        return "Low"

    df["Complexity"] = df.apply(lambda r: normalize_complexity(r["Complexity"], r["BT Level"]), axis=1)
    df["CO"] = df["CO"].str.upper().str.strip()
    df = df.reset_index(drop=True)
    df.index = df.index + 1
    return df


# ==========================
# GENERATE PDF
# ==========================
def generate_pdf(df):
    file_path = "question_bank.pdf"
    doc = SimpleDocTemplate(
        file_path, pagesize=A4,
        leftMargin=1.5 * cm, rightMargin=1.5 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    question_style = ParagraphStyle("QS", parent=styles["Normal"], fontSize=8, leading=11, wordWrap="CJK")
    normal_style = ParagraphStyle("NS", parent=styles["Normal"], fontSize=8, leading=11)
    title_style = ParagraphStyle("TS", parent=styles["Heading1"], fontSize=14, spaceAfter=12)

    elements = [Paragraph("Question Bank", title_style), Spacer(1, 0.3 * cm)]
    header = ["#", "Question", "BT Level", "CO", "Chapter", "Complexity"]
    data = [header]
    for idx, row in df.iterrows():
        data.append([
            str(idx),
            Paragraph(row["Question"], question_style),
            Paragraph(row["BT Level"], normal_style),
            Paragraph(row["CO"], normal_style),
            Paragraph(row["Chapter"], normal_style),
            Paragraph(row["Complexity"], normal_style),
        ])

    col_widths = [0.8 * cm, 7.5 * cm, 1.8 * cm, 1.5 * cm, 3.5 * cm, 2.0 * cm]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E4057")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")]),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(table)
    doc.build(elements)
    return file_path


# ==========================
# STREAMLIT UI
# ==========================
st.set_page_config(page_title="Quest-AI", page_icon="📚", layout="wide")

# ── Header ──
st.markdown("""
<div style='padding:1.2rem 0 0.4rem 0;'>
    <h1 style='margin:0; font-size:2rem;'>📚 Quest-AI</h1>
    <p style='color:gray; margin-top:4px; font-size:1rem;'>
        Intelligent Question Bank Generator for Engineering Courses
    </p>
</div>
""", unsafe_allow_html=True)
st.divider()

if client is None:
    st.warning("⚠️ No API key found. Add `GROQ_API_KEY` to `.streamlit/secrets.toml` or environment variables.")

# ── Upload + Settings side by side ──
left, right = st.columns([3, 2], gap="large")

with left:
    st.subheader("📂 Upload Files")
    pdf_files = st.file_uploader(
        "Chapter Notes / Textbook PDFs",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more chapter PDFs. Quest-AI auto-decides how many questions to generate.",
    )
    syllabus_file = st.file_uploader(
        "Course Syllabus",
        type=["pdf", "txt"],
        help="Chapter/module names are auto-detected from the syllabus.",
    )
    if pdf_files:
        st.caption(f"✅ {len(pdf_files)} chapter file(s) ready")
    if syllabus_file:
        st.caption(f"✅ Syllabus: **{syllabus_file.name}**")

with right:
    st.subheader("⚙️ Question Settings")

    bt_options = st.multiselect(
        "Bloom's Taxonomy Levels to Include",
        options=["BT2", "BT3", "BT4", "BT5", "BT6"],
        default=["BT2", "BT3", "BT4", "BT5", "BT6"],
        help="BT1 (pure recall) is always excluded.",
    )

    difficulty_mix = st.radio(
        "Difficulty Distribution",
        options=[
            "Balanced (BT2–BT6 mix)",
            "Mostly Hard (BT5 & BT6 dominant)",
            "Mostly Medium (BT3 & BT4 dominant)",
        ],
        index=0,
    )

    st.info("🤖 Question count and content coverage are **set automatically** from your uploaded files.", icon=None)

    with st.expander("📖 BT Level Quick Reference"):
        st.markdown("""
| Level | Skill | Complexity |
|-------|-------|------------|
| BT2 | Understand — explain, compare, describe | 🟢 Low |
| BT3 | Apply — solve, calculate, implement | 🟡 Medium |
| BT4 | Analyze — trace, diagnose, differentiate | 🟡 Medium |
| BT5 | Evaluate — critique, justify, recommend | 🔴 High |
| BT6 | Create — design, construct, propose | 🔴 High |
""")

st.divider()

# ── Generate button ──
if st.button("🚀 Generate Question Bank", type="primary", use_container_width=True, disabled=(client is None)):

    if not pdf_files or not syllabus_file:
        st.error("Please upload at least one chapter PDF and your syllabus.")
        st.stop()
    if not bt_options:
        st.error("Please select at least one BT level.")
        st.stop()

    bt_levels_str = ", ".join(bt_options)

    # Extract text
    with st.spinner("📄 Reading uploaded files..."):
        content = extract_text_from_pdf(pdf_files)
        syllabus = (
            extract_text_from_pdf([syllabus_file])
            if syllabus_file.type == "application/pdf"
            else syllabus_file.read().decode("utf-8")
        )

    if not content.strip():
        st.error("Could not extract text from chapter PDFs. Ensure they are text-based (not scanned images).")
        st.stop()
    if not syllabus.strip():
        st.error("Could not extract text from the syllabus.")
        st.stop()

    # Auto-compute plan
    chunk_size, num_chunks, q_per_chunk = compute_chunk_params(content, syllabus)
    chunks = chunk_text(content, size=chunk_size)
    selected_chunks = chunks[:num_chunks]

    # Show auto-detected plan
    st.markdown("### 📋 Auto-detected Generation Plan")
    pc1, pc2, pc3, pc4 = st.columns(4)
    pc1.metric("Content Size", f"{len(content.split()):,} words")
    pc2.metric("Sections to Process", num_chunks)
    pc3.metric("Questions per Section", q_per_chunk)
    pc4.metric("Estimated Total", num_chunks * q_per_chunk)
    st.divider()

    # Generate
    all_dfs, raw_outputs = [], []
    progress_bar = st.progress(0, text="Starting generation...")

    for i, chunk in enumerate(selected_chunks):
        progress_bar.progress(
            i / len(selected_chunks),
            text=f"Generating questions — section {i + 1} of {len(selected_chunks)}...",
        )
        try:
            output = generate_questions(chunk, syllabus, q_per_chunk, bt_levels_str, difficulty_mix)
            raw_outputs.append(output)
            parsed = parse_to_df(output)
            if not parsed.empty:
                all_dfs.append(parsed)
        except RuntimeError as exc:
            st.error(str(exc))
            st.stop()

    progress_bar.progress(1.0, text="✅ Generation complete!")

    if not all_dfs:
        st.warning("No questions could be parsed. See raw output below.")
        for idx, out in enumerate(raw_outputs, 1):
            st.text_area(f"Section {idx} raw output", out, height=220)
        st.stop()

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df = clean_dataframe(final_df)

    if final_df.empty:
        st.warning("Questions were generated but filtered out. See raw output below.")
        for idx, out in enumerate(raw_outputs, 1):
            st.text_area(f"Section {idx} raw output", out, height=220)
        st.stop()

    st.success(f"✅ Question bank ready — **{len(final_df)} questions** generated!")

    # Summary metrics
    st.markdown("### 📊 Summary")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Questions", len(final_df))
    m2.metric("🔴 High", len(final_df[final_df["Complexity"] == "High"]))
    m3.metric("🟡 Medium", len(final_df[final_df["Complexity"] == "Medium"]))
    m4.metric("🟢 Low", len(final_df[final_df["Complexity"] == "Low"]))
    m5.metric("Chapters Covered", final_df["Chapter"].nunique())

    # Charts
    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("**BT Level Distribution**")
        st.bar_chart(final_df["BT Level"].value_counts().sort_index(), use_container_width=True)
    with ch2:
        st.markdown("**Complexity Breakdown**")
        st.bar_chart(final_df["Complexity"].value_counts(), use_container_width=True)

    # Filter & browse
    st.markdown("### 🔍 Browse & Filter Questions")
    f1, f2, f3 = st.columns(3)
    with f1:
        bt_filter = st.multiselect("BT Level", options=sorted(final_df["BT Level"].unique()))
    with f2:
        complexity_filter = st.multiselect("Complexity", options=["Low", "Medium", "High"])
    with f3:
        chapter_filter = st.multiselect("Chapter", options=sorted(final_df["Chapter"].unique()))

    display_df = final_df.copy()
    if bt_filter:
        display_df = display_df[display_df["BT Level"].isin(bt_filter)]
    if complexity_filter:
        display_df = display_df[display_df["Complexity"].isin(complexity_filter)]
    if chapter_filter:
        display_df = display_df[display_df["Chapter"].isin(chapter_filter)]

    st.dataframe(display_df, use_container_width=True, height=480)
    st.caption(f"Showing {len(display_df)} of {len(final_df)} questions")

    # Downloads
    st.markdown("### ⬇️ Download Question Bank")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            "📄 Download CSV",
            final_df.to_csv(index=True),
            file_name="question_bank.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with dl2:
        try:
            pdf_path = generate_pdf(final_df)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📑 Download PDF",
                    f,
                    file_name="question_bank.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        except Exception as e:
            st.warning(f"PDF export failed: {e}. Use CSV instead.")

    # Debug
    with st.expander("🛠️ Raw model output (debug)"):
        for idx, out in enumerate(raw_outputs, 1):
            st.text_area(f"Section {idx}", out, height=200)
