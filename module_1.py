# =========================================
# QUEST-AI IMPROVED
# PDF -> Structured Question Bank (CSV + PDF)
# Key improvements:
#   - Proper Bloom's Taxonomy system prompting with verb banks
#   - Complexity derived from BT level (consistent)
#   - Chapter detection from syllabus
#   - No BT1 questions ever generated
#   - All questions are multi-line, application-based
# =========================================

# Install:
# pip install streamlit pdfplumber pandas reportlab openai

import os
import re

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
# TEXT CHUNKING
# ==========================
def chunk_text(text, size=500):
    words = text.split()
    return [" ".join(words[i: i + size]) for i in range(0, len(words), size)]


# ==========================
# SYSTEM PROMPT (Core BT alignment logic)
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
- Higher BT levels (BT5, BT6) should generally map to higher COs (CO4–CO6).
- Lower BT levels (BT2, BT3) typically map to lower COs (CO1–CO3).

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

    if difficulty_mix == "Mostly Hard (30% Medium / 70% High)":
        diff_instruction = "Generate 30% Medium complexity (BT3/BT4) and 70% High complexity (BT5/BT6) questions. No Low complexity."
    elif difficulty_mix == "Mostly Medium":
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
    lines = text.split("\n")

    for line in lines:
        if "|" not in line:
            continue

        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) != 5:
            continue

        # Skip separator lines (---, ===, etc.)
        if all(set(p) <= {"-", ":", "=", " "} for p in parts):
            continue

        # Skip header row
        if parts[0].lower() == "question":
            continue

        if any(parts):
            rows.append(parts)

    return pd.DataFrame(
        rows,
        columns=["Question", "BT Level", "CO", "Chapter", "Complexity"],
    )


# ==========================
# CLEAN & VALIDATE DATAFRAME
# ==========================
def clean_dataframe(df):
    df = df.drop_duplicates(subset=["Question"]).copy()
    df = df[df["Question"] != "Question"]

    # Normalize BT level column
    df["BT Level"] = df["BT Level"].str.upper().str.strip()

    # Remove any BT1 that slipped through
    df = df[~df["BT Level"].str.contains("BT1", na=False)]

    # Normalize complexity: ensure it's one of Low/Medium/High
    def normalize_complexity(val, bt):
        v = str(val).strip().lower()
        if "high" in v:
            return "High"
        if "med" in v:
            return "Medium"
        if "low" in v:
            return "Low"
        # Derive from BT level as fallback
        bt_upper = str(bt).upper()
        if "BT5" in bt_upper or "BT6" in bt_upper:
            return "High"
        if "BT3" in bt_upper or "BT4" in bt_upper:
            return "Medium"
        return "Low"

    df["Complexity"] = df.apply(
        lambda r: normalize_complexity(r["Complexity"], r["BT Level"]), axis=1
    )

    # Normalize CO column
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
        file_path,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    question_style = ParagraphStyle(
        "QuestionStyle",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        wordWrap="CJK",
    )
    normal_style = ParagraphStyle(
        "NormalSmall",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
    )

    elements = []

    # Title
    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"], fontSize=14, spaceAfter=12
    )
    elements.append(Paragraph("Question Bank", title_style))
    elements.append(Spacer(1, 0.3 * cm))

    # Build table data
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

    # Column widths (total ~17cm)
    col_widths = [0.8 * cm, 7.5 * cm, 1.8 * cm, 1.5 * cm, 3.5 * cm, 2.0 * cm]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle([
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
        ])
    )

    elements.append(table)
    doc.build(elements)
    return file_path


# ==========================
# STREAMLIT UI
# ==========================
st.set_page_config(page_title="Quest-AI", page_icon="📚", layout="wide")

st.title("📚 Quest-AI: Question Bank Generator")
st.caption("Generates BT-aligned engineering exam questions with CO mapping, chapter tagging & complexity levels")

if client is None:
    st.warning(
        "⚠️ No API key found. Add `GROQ_API_KEY` to `.streamlit/secrets.toml` or your environment variables."
    )

# ── Sidebar settings ──
with st.sidebar:
    st.header("⚙️ Settings")

    num_questions = st.slider("Questions to generate per chunk", min_value=4, max_value=20, value=8)

    bt_options = st.multiselect(
        "Allowed BT Levels",
        options=["BT2", "BT3", "BT4", "BT5", "BT6"],
        default=["BT2", "BT3", "BT4", "BT5", "BT6"],
        help="BT1 is always excluded — it only tests recall."
    )

    difficulty_mix = st.selectbox(
        "Difficulty Distribution",
        options=[
            "Balanced (20% Low / 40% Medium / 40% High)",
            "Mostly Hard (30% Medium / 70% High)",
            "Mostly Medium",
        ],
        index=0,
    )

    max_chunks = st.slider("Max chunks to process", min_value=1, max_value=10, value=3,
                           help="Each chunk is ~500 words. More chunks = more questions but slower.")

    st.markdown("---")
    st.markdown("**BT Level Guide**")
    st.markdown("🟢 BT2 → Low (Understand)")
    st.markdown("🟡 BT3/BT4 → Medium (Apply/Analyze)")
    st.markdown("🔴 BT5/BT6 → High (Evaluate/Create)")

# ── Main inputs ──
col1, col2 = st.columns(2)

with col1:
    pdf_files = st.file_uploader(
        "Upload Chapter PDFs / Notes",
        type="pdf",
        accept_multiple_files=True,
    )

with col2:
    syllabus_file = st.file_uploader(
        "Upload Syllabus",
        type=["pdf", "txt"],
    )

if st.button("🚀 Generate Question Bank", type="primary", use_container_width=True):

    if not pdf_files or not syllabus_file:
        st.error("Please upload both chapter PDFs and the syllabus.")
        st.stop()

    if client is None:
        st.error("Missing API key. Cannot generate questions.")
        st.stop()

    if not bt_options:
        st.error("Select at least one BT level.")
        st.stop()

    bt_levels_str = ", ".join(bt_options)

    with st.spinner("Extracting text from PDFs..."):
        content = extract_text_from_pdf(pdf_files)

        if syllabus_file.type == "application/pdf":
            syllabus = extract_text_from_pdf([syllabus_file])
        else:
            syllabus = syllabus_file.read().decode("utf-8")

    if not content.strip():
        st.error("No text could be extracted from chapter PDFs.")
        st.stop()

    if not syllabus.strip():
        st.error("No text could be extracted from the syllabus.")
        st.stop()

    chunks = chunk_text(content)
    selected_chunks = chunks[:max_chunks]

    st.info(f"Processing {len(selected_chunks)} chunk(s) from {len(pdf_files)} file(s)...")

    all_dfs = []
    raw_outputs = []
    progress = st.progress(0)

    for i, chunk in enumerate(selected_chunks):
        try:
            with st.spinner(f"Generating questions for chunk {i + 1}/{len(selected_chunks)}..."):
                output = generate_questions(
                    chunk, syllabus, num_questions, bt_levels_str, difficulty_mix
                )
                raw_outputs.append(output)
                parsed = parse_to_df(output)
                if not parsed.empty:
                    all_dfs.append(parsed)
        except RuntimeError as exc:
            st.error(str(exc))
            st.stop()

        progress.progress((i + 1) / len(selected_chunks))

    if not all_dfs:
        st.warning("No questions could be parsed. Showing raw model output below.")
        for idx, out in enumerate(raw_outputs, 1):
            st.text_area(f"Chunk {idx} raw output", out, height=220)
        st.stop()

    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df = clean_dataframe(final_df)

    if final_df.empty:
        st.warning("Parsed empty dataframe after cleaning. See raw output below.")
        for idx, out in enumerate(raw_outputs, 1):
            st.text_area(f"Chunk {idx} raw output", out, height=220)
        st.stop()

    st.success(f"✅ Generated {len(final_df)} questions!")

    # ── Summary stats ──
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Questions", len(final_df))
    col_b.metric("High Complexity", len(final_df[final_df["Complexity"] == "High"]))
    col_c.metric("Medium Complexity", len(final_df[final_df["Complexity"] == "Medium"]))
    col_d.metric("Chapters Covered", final_df["Chapter"].nunique())

    # ── BT distribution chart ──
    with st.expander("📊 BT Level Distribution", expanded=True):
        bt_counts = final_df["BT Level"].value_counts().sort_index()
        st.bar_chart(bt_counts)

    # ── Filter & display ──
    st.subheader("Question Bank")
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        bt_filter = st.multiselect(
            "Filter by BT Level", options=sorted(final_df["BT Level"].unique()), default=[]
        )
    with filter_col2:
        complexity_filter = st.multiselect(
            "Filter by Complexity", options=["Low", "Medium", "High"], default=[]
        )
    with filter_col3:
        chapter_filter = st.multiselect(
            "Filter by Chapter", options=sorted(final_df["Chapter"].unique()), default=[]
        )

    display_df = final_df.copy()
    if bt_filter:
        display_df = display_df[display_df["BT Level"].isin(bt_filter)]
    if complexity_filter:
        display_df = display_df[display_df["Complexity"].isin(complexity_filter)]
    if chapter_filter:
        display_df = display_df[display_df["Chapter"].isin(chapter_filter)]

    st.dataframe(display_df, use_container_width=True, height=500)

    # ── Downloads ──
    st.subheader("Downloads")
    dl_col1, dl_col2 = st.columns(2)

    with dl_col1:
        csv_data = final_df.to_csv(index=True)
        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            file_name="question_bank.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with dl_col2:
        try:
            pdf_path = generate_pdf(final_df)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "⬇️ Download PDF",
                    f,
                    file_name="question_bank.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        except Exception as e:
            st.warning(f"PDF generation failed: {e}. Use CSV download instead.")

    # ── Raw output expander ──
    with st.expander("🔍 Raw model output (debug)"):
        for idx, out in enumerate(raw_outputs, 1):
            st.text_area(f"Chunk {idx}", out, height=200)
