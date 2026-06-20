import { useMemo, useState } from "react";
import { BLOOM_LEVELS, LEVELS } from "../data/constants";
import { Badge, Header, Card, CoursePill, Flash, PrimaryBtn } from "../components/UI";
import AiProcessGraph from "../components/AiProcessGraph";
import { generatePaper } from "../lib/api";

const PAPER_STAGES = [
  { title: "Template read", detail: "Backend detects sections, marks, and question slots." },
  { title: "Bank select", detail: "Relevant checked questions and syllabus units are gathered." },
  { title: "GPT-5 sets", detail: "Set A, B, and C are generated with no repeated meaning." },
  { title: "Semantic audit", detail: "ML/NLP checks compare all questions across all sets." },
  { title: "Accuracy", detail: "Coverage and duplicate-prevention scores are returned." },
];

function parseTemplateStructure(templateContent) {
  if (!templateContent) return null;
  const lines = templateContent.split("\n");
  const sections = {};
  let currentSection = null;
  let currentMarks = 0;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const sectionMatch = trimmed.match(/^SECTION\s+([A-Z])\s*:\s*(.+?)\s*\((\d+)\s*marks?\s*each\)/i);
    if (sectionMatch) {
      const [, sectionLetter, description, marks] = sectionMatch;
      currentSection = sectionLetter.toUpperCase();
      currentMarks = parseInt(marks, 10);
      sections[currentSection] = { description, marksPerQuestion: currentMarks, questions: [] };
      continue;
    }
    if (currentSection && /^\d+\.\s/.test(trimmed)) {
      sections[currentSection].questions.push({ placeholder: trimmed, marks: currentMarks });
    }
  }

  return Object.keys(sections).length ? sections : null;
}

function syllabusFromQuestions(subject, courseId, level, questions) {
  const unitNames = [...new Set(questions.map(q => q.unit).filter(Boolean))];
  return {
    subject,
    courseId,
    level,
    units: unitNames.map(name => ({ name, topics: [name] }))
  };
}

export default function GeneratePaper({ user, questions, syllabi, templates, onGenerated }) {
  const [subject, setSubject] = useState("");
  const [courseId, setCourseId] = useState("");
  const [level, setLevel] = useState("College");
  const [template, setTemplate] = useState("");
  const [generating, setGenerating] = useState(false);
  const [sets, setSets] = useState(null);
  const [activeSet, setActiveSet] = useState("A");
  const [error, setError] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [quality, setQuality] = useState(null);
  const [processStep, setProcessStep] = useState(0);
  const [aiModel, setAiModel] = useState("gpt-5");

  const availableSubjects = useMemo(() => [
    ...new Set([...questions.map(q => q.subject), ...syllabi.map(s => s.subject)])
  ], [questions, syllabi]);

  const subjectQs = useMemo(() => questions.filter(q =>
    q.subject.toLowerCase() === subject.toLowerCase() && q.level === level
  ), [questions, subject, level]);

  const matchedSyllabus = useMemo(() => {
    return syllabi.find(s =>
      s.subject.toLowerCase() === subject.toLowerCase() &&
      (!courseId || s.courseId.toLowerCase() === courseId.toLowerCase())
    );
  }, [syllabi, subject, courseId]);

  const canGenerate = subject.trim() && (matchedSyllabus || subjectQs.length >= 3);

  const generate = async () => {
    if (!canGenerate) return;
    setGenerating(true);
    setError("");
    setSets(null);
    setQuality(null);
    setProcessStep(0);

    const selTpl = templates.find(t => String(t.id) === String(template));
    setSelectedTemplate(selTpl);
    const syllabus = matchedSyllabus || syllabusFromQuestions(subject, courseId, level, subjectQs);

    try {
      setProcessStep(1);
      const data = await generatePaper({
        subject,
        courseId,
        level,
        questions: subjectQs,
        syllabus,
        template: selTpl || null
      });
      setProcessStep(4);
      setAiModel(data.model || "gpt-5");
      setSets(data.sets);
      setQuality(data.quality);
      if (data.fallback) setError("Backend used fallback paper generation because GPT-5 was unavailable.");
      onGenerated({
        id: Date.now(),
        subject,
        courseId,
        level,
        sets: data.sets,
        quality: data.quality,
        template: selTpl?.name || "Default",
        generatedBy: user.username,
        generatedAt: new Date().toISOString()
      });
    } catch (e) {
      setError(`Backend AI failed: ${e.message}`);
    }

    setGenerating(false);
  };

  const downloadPDF = (setKey, selTpl) => {
    const s = sets[setKey];
    const dateStr = new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "long", year: "numeric" });
    let html;

    if (selTpl?.content) {
      const templateStructure = parseTemplateStructure(selTpl.content);
      let templateText = selTpl.content;

      if (templateStructure) {
        Object.entries(templateStructure).forEach(([sectionLetter, sectionData]) => {
          const sectionKey = `section${sectionLetter.toLowerCase()}`;
          sectionData.questions.forEach((placeholder, index) => {
            const question = s[sectionKey]?.[index];
            if (question) {
              const replacement = placeholder.placeholder.replace(/Question \d+/i, question.question);
              templateText = templateText.replace(placeholder.placeholder, replacement);
            }
          });
        });
      }

      templateText = templateText.replace(/\{\{subject\}\}/g, subject);
      templateText = templateText.replace(/\{\{courseId\}\}/g, courseId || "N/A");
      templateText = templateText.replace(/\{\{date\}\}/g, dateStr);
      templateText = templateText.replace(/\{\{duration\}\}/g, "3 Hours");
      templateText = templateText.replace(/\{\{totalMarks\}\}/g, "50");
      templateText = templateText.replace(/\{\{examiner\}\}/g, user.name);
      templateText = templateText.replace(/\{\{level\}\}/g, level);

      html = `<!DOCTYPE html><html><head><title>${subject} - Set ${setKey}</title><style>body{font-family:monospace;white-space:pre-wrap;margin:40px;color:#111;}</style></head><body>${templateText.replace(/\n/g, "<br>")}</body></html>`;
    } else {
      const rows = section => (s[section] || []).map((q, i) =>
        `<tr><td style="padding:8px 4px;vertical-align:top;color:#555;font-size:13px;">${i + 1}.</td><td style="padding:8px 8px 8px 4px;font-size:13px;">${q.question}</td><td style="padding:8px 4px;text-align:right;font-size:13px;white-space:nowrap;">[${q.marks}M]</td></tr>`
      ).join("");

      html = `<!DOCTYPE html><html><head><title>${subject} - Set ${setKey}</title>
<style>body{font-family:Georgia,serif;margin:0;padding:40px;color:#111;}h1{font-size:20px;text-align:center;margin:0 0 4px;}.meta{text-align:center;font-size:13px;color:#555;margin-bottom:24px;}h2{font-size:14px;border-bottom:2px solid #111;padding-bottom:4px;margin:24px 0 12px;}table{width:100%;border-collapse:collapse;}.footer{margin-top:40px;text-align:center;font-size:12px;color:#888;border-top:1px solid #ddd;padding-top:12px;}@media print{@page{margin:20mm;}}</style></head>
<body>
<p style="text-align:right;font-size:12px;color:#888;">CONFIDENTIAL - EXAMINER COPY</p>
<h1>${subject} Examination - Set ${setKey}</h1>
<div class="meta">${courseId ? `<strong>${courseId}</strong> &nbsp;|&nbsp;` : ""} Level: ${level} &nbsp;|&nbsp; Total Marks: 50 &nbsp;|&nbsp; Duration: 3 Hours &nbsp;|&nbsp; Date: ${dateStr}</div>
<p style="font-size:13px;font-style:italic;color:#555;">Answer all sections. Write clearly and concisely.</p>
<h2>SECTION A - Short Answer (2 x 5 = 10 Marks)</h2><table>${rows("sectionA")}</table>
<h2>SECTION B - Medium Answer (5 x 4 = 20 Marks)</h2><table>${rows("sectionB")}</table>
<h2>SECTION C - Long Answer (10 x 2 = 20 Marks)</h2><table>${rows("sectionC")}</table>
<div class="footer">Generated by Quest-AI | ${subject} ${courseId} | Set ${setKey} | ${dateStr}</div>
</body></html>`;
    }

    const win = window.open("", "_blank");
    win.document.write(html);
    win.document.close();
    win.focus();
    setTimeout(() => win.print(), 500);
  };

  const SectionBlock = ({ title, qs = [], col }) => (
    <div className="mb-5">
      <div className="flex items-center justify-between mb-3 pb-2 border-b" style={{ borderColor: "#1E2D4A" }}>
        <h4 className="text-sm font-bold" style={{ color: "#E2E8F0" }}>{title}</h4>
        <span className="text-xs px-2 py-0.5 rounded font-semibold" style={{ background: col + "18", color: col, border: `1px solid ${col}35` }}>
          {qs.reduce((a, q) => a + Number(q.marks || 0), 0)} marks
        </span>
      </div>
      {qs.map((q, i) => (
        <div key={i} className="flex gap-3 py-3 border-b last:border-0" style={{ borderColor: "#141B30" }}>
          <span className="text-xs font-bold w-5 shrink-0 mt-0.5" style={{ color: col }}>{i + 1}.</span>
          <div className="flex-1">
            <p className="text-sm leading-relaxed" style={{ color: "#E2E8F0" }}>{q.question}</p>
            <div className="flex gap-1.5 mt-1.5">
              <Badge color="teal">{q.unit}</Badge>
              <Badge color="purple">{q.bloom}</Badge>
            </div>
          </div>
          <span className="text-xs font-bold shrink-0 mt-0.5" style={{ color: col }}>[{q.marks}M]</span>
        </div>
      ))}
    </div>
  );

  return (
    <div>
      <Header title="Generate Question Paper" subtitle="Backend GPT-5 generates Set A, B, and C using your template" />

      <Card className="mb-4">
        <h3 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>Paper Configuration</h3>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: "#94A3B8" }}>Subject Name *</label>
            <input type="text" value={subject} onChange={e => setSubject(e.target.value)} list="subjectList" placeholder="Type or pick from bank"
              className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
              style={{ background: "#141B30", border: `1px solid ${subject ? "#3B82F6" : "#1E2D4A"}`, color: "#E2E8F0" }} />
            <datalist id="subjectList">{availableSubjects.map(s => <option key={s} value={s} />)}</datalist>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: "#94A3B8" }}>Course ID</label>
            <input type="text" value={courseId} onChange={e => setCourseId(e.target.value.toUpperCase())} placeholder="e.g. MA101"
              className="w-full px-3 py-2.5 rounded-lg text-sm outline-none font-mono"
              style={{ background: "#141B30", border: `1px solid ${courseId ? "#3B82F6" : "#1E2D4A"}`, color: "#E2E8F0", letterSpacing: "0.06em" }} />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: "#94A3B8" }}>Level</label>
            <select value={level} onChange={e => setLevel(e.target.value)}
              className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#E2E8F0" }}>
              {LEVELS.map(l => <option key={l}>{l}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium mb-1.5" style={{ color: "#94A3B8" }}>Template</label>
            <select value={template} onChange={e => setTemplate(e.target.value)}
              className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#E2E8F0" }}>
              <option value="">Default Template</option>
              {templates.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-3 p-3 rounded-lg mb-3" style={{ background: "#141B30" }}>
          <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${canGenerate ? "bg-emerald-500" : "bg-amber-500"}`} />
          <span className="text-xs" style={{ color: canGenerate ? "#10B981" : "#F59E0B" }}>
            {subject
              ? `${subjectQs.length} bank questions and ${matchedSyllabus ? "a saved syllabus" : "no matching saved syllabus"} found`
              : "Enter a subject name to check backend readiness"}
          </span>
        </div>

        <CoursePill subject={subject} courseId={courseId} level={level} />

        {generating && <AiProcessGraph stages={PAPER_STAGES} active={processStep} model={aiModel} />}
        {quality && !generating && <AiProcessGraph stages={PAPER_STAGES} active={5} quality={quality} model={aiModel} />}

        <div className="mt-4">
          <PrimaryBtn onClick={generate} disabled={!canGenerate} loading={generating} fullWidth>
            {generating ? "Generating and auditing 3 sets..." : "Generate Set A / B / C"}
          </PrimaryBtn>
        </div>
      </Card>

      <Flash message={error} type="warn" />

      {sets && (
        <div>
          <div className="flex gap-2 mb-4">
            {["A", "B", "C"].map(s => (
              <button key={s} onClick={() => setActiveSet(s)}
                className="flex-1 py-2.5 rounded-xl text-sm font-bold transition-all"
                style={{
                  background: activeSet === s ? "linear-gradient(135deg,#1D4ED8,#3B82F6)" : "#0F1629",
                  color: activeSet === s ? "white" : "#64748B",
                  border: `1px solid ${activeSet === s ? "#3B82F6" : "#1E2D4A"}`,
                  boxShadow: activeSet === s ? "0 0 16px rgba(59,130,246,0.2)" : "none",
                }}>
                Set {s}
              </button>
            ))}
          </div>

          <Card>
            <div className="text-center mb-6 pb-5 border-b" style={{ borderColor: "#1E2D4A" }}>
              <p className="text-xs font-semibold tracking-widest mb-1" style={{ color: "#475569" }}>CONFIDENTIAL - EXAMINER COPY</p>
              <h2 className="text-lg font-bold mb-1.5" style={{ color: "#E2E8F0" }}>{subject} Examination - Set {activeSet}</h2>
              <div className="flex items-center justify-center gap-4 text-xs flex-wrap" style={{ color: "#64748B" }}>
                {courseId && <span style={{ color: "#3B82F6", fontFamily: "monospace", fontWeight: 600 }}>{courseId}</span>}
                <span>Level: {level}</span>
                <span style={{ fontWeight: 600, color: "#E2E8F0" }}>50 Marks</span>
                <span>3 Hours</span>
                <span>{new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "long", year: "numeric" })}</span>
              </div>
            </div>

            <SectionBlock title="SECTION A - Short Answer (2 x 5 = 10 M)" qs={sets[activeSet].sectionA} col="#3B82F6" />
            <SectionBlock title="SECTION B - Medium Answer (5 x 4 = 20 M)" qs={sets[activeSet].sectionB} col="#F59E0B" />
            <SectionBlock title="SECTION C - Long Answer (10 x 2 = 20 M)" qs={sets[activeSet].sectionC} col="#EF4444" />

            <div className="border-t pt-4" style={{ borderColor: "#1E2D4A" }}>
              <p className="text-xs mb-3 font-medium" style={{ color: "#64748B" }}>Download any set as PDF:</p>
              <div className="flex gap-3">
                {["A", "B", "C"].map(s => (
                  <button key={s} onClick={() => downloadPDF(s, selectedTemplate)}
                    className="flex-1 py-2.5 rounded-xl text-sm font-semibold"
                    style={{ background: activeSet === s ? "#059669" : "#1D4ED8", color: "white" }}>
                    Set {s} PDF
                  </button>
                ))}
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
