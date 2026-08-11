import { useMemo, useState, useEffect} from "react";
import { BLOOM_LEVELS, LEVELS } from "../data/constants";
import { Badge, Header, Card, CoursePill, Flash, PrimaryBtn } from "../components/UI";
import AiProcessGraph from "../components/AiProcessGraph";
import { generatePaper } from "../lib/api";
import { getTemplates, uploadTemplate } from "../lib/templateApi";

const PAPER_STAGES = [
  { title: "Template read", detail: "Backend detects sections, marks, and question slots." },
  { title: "Bank select", detail: "Relevant checked questions and syllabus units are gathered." },
  { title: "Gemini generationsets", detail: "Set A, B, and C are generated with no repeated meaning." },
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

function sectionTitle(key) {
  const label = String(key || "").replace(/^section/i, "").replace(/([a-z])([A-Z])/g, "$1 $2").trim();
  return `SECTION ${label || "GENERAL"}`;
}

function paperTotal(paperSet) {
  const countedChoices = new Set();
  const selectedCounts = new Map();
  return Object.values(paperSet || {}).flat().reduce((sum, question) => {
    if (question.choice_group) {
      if (countedChoices.has(question.choice_group)) return sum;
      countedChoices.add(question.choice_group);
    }
    if (question.selection_group) {
      const count = selectedCounts.get(question.selection_group) || 0;
      if (count >= Number(question.required_count || 1)) return sum;
      selectedCounts.set(question.selection_group, count + 1);
    }
    return sum + Number(question.marks || 0);
  }, 0);
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>\"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[char]));
}

function normalizeModelLabel(model) {
  const value = String(model || "").trim();
  if (!value) return "gemini-flash-lite-latest";
  const lower = value.toLowerCase();
  if (lower.includes("openrouter")) return "gemini-flash-lite-latest";
  return value;
}

function isDefaultTemplate(template) {
  return Boolean(template?.builtin || template?.template_json?.template_type === "end_semester_default");
}

function getDefaultTemplateHeader(template) {
  const templateData = template?.template_json || template || {};
  const templateName = String(template?.template_name || templateData?.template_name || "").toLowerCase();
  const templateType = String(templateData?.template_type || "").toLowerCase();
  const isDkte = templateName.includes("dkte") || templateType.includes("dkte");

  const collegeName = isDkte
    ? (templateData?.college?.name || "D.K.T.E. Society's Textile & Engineering Institute")
    : "K.E.Society’s Rajarambapu Institute of Technology, Rajaramnagar";

  const examTitle = templateData?.header?.exam_title || "End Semester Examination";

  return {
    collegeName,
    examTitle
  };
}

export default function GeneratePaper({ user, questions, syllabi, templates, onGenerated }) {
  const [subject, setSubject] = useState("");
  const [courseId, setCourseId] = useState("");
  const [level, setLevel] = useState("");
  const [template, setTemplate] = useState("");
  const [generating, setGenerating] = useState(false);
  const [sets, setSets] = useState(null);
  const [activeSet, setActiveSet] = useState("A");
  const [error, setError] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [quality, setQuality] = useState(null);
  const [processStep, setProcessStep] = useState(0);
  const [aiModel, setAiModel] = useState("gemini-flash-lite-latest");
  const [date,setDate] = useState("");
  const [savedTemplates,setSavedTemplates] = useState([]);
  const [templateFile,setTemplateFile] = useState(null);

  useEffect(() => {

  const fetchTemplates = async () => {

    try {

      const data = await getTemplates();

      setSavedTemplates(data);

    } catch(error) {

      console.error(
        "Failed to load templates:",
        error
      );

    }

  };


  fetchTemplates();

}, []);

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

  // Either a faculty upload or the built-in university paper can be the
  // source of truth for sections, question slots, and marks.
  const canGenerate = subject.trim() && level.trim() && Boolean(template) && (matchedSyllabus || subjectQs.length >= 3);
  const usingDefaultTemplate = isDefaultTemplate(selectedTemplate);

  const generate = async () => {
    if (!canGenerate) return;
    setGenerating(true);
    setError("");
    setSets(null);
    setQuality(null);
    setProcessStep(0);

    const selTpl = savedTemplates.find(t => String(t.id) === String(template));
    setSelectedTemplate(selTpl);
    const syllabus = matchedSyllabus || syllabusFromQuestions(subject, courseId, level, subjectQs);

    try {
      setProcessStep(1);
      const data = await generatePaper({
        subject,
        courseId,
        date,
        level,
        questions: subjectQs,
        syllabus,
        template: selTpl ? selTpl.template_json : null
      });
      setProcessStep(4);
      setAiModel(normalizeModelLabel(data.model || "gemini-flash-lite-latest"));
      setSets(data.sets);
      setQuality(data.quality);
      if (data.fallback) setError("Backend used fallback paper generation because Gemini generationwas unavailable.");
      onGenerated({
        id: Date.now(),
        subject,
        courseId,
        level,
        sets: data.sets,
        quality: data.quality,
        template: selTpl?.template_name || "Default",
        generatedBy: user.username,
        generatedAt: new Date().toISOString()
      });
    } catch (e) {
      setError(`Backend AI failed: ${e.message}`);
    }

    setGenerating(false);
  };

  const handleTemplateUpload = async(e)=>{

  const file = e.target.files[0];

  if(!file)
    return;


  setTemplateFile(file);


  const formData = new FormData();

  formData.append(
    "file",
    file
  );


  try{


    const uploaded =
      await uploadTemplate(formData);



    setSavedTemplates(prev=>[
      ...prev,
      uploaded
    ]);
    setError("");


    setTemplate(
      uploaded.id
    );


    setSelectedTemplate(
      uploaded
    );


  }
  catch(err){

    console.error(
      "Template upload failed",
      err
    );

    setError(
      "Template upload failed"
    );

  }

};

  const downloadPDF = (setKey) => {
    const s = sets[setKey];
    if (usingDefaultTemplate) {
      const activeTemplate = selectedTemplate || savedTemplates.find(t => String(t.id) === String(template)) || null;
      const headerDetails = getDefaultTemplateHeader(activeTemplate);
      const questionBlocks = Object.entries(s || {}).map(([section, qs]) => {
        const questionNo = qs[0]?.question_no || section.replace(/^section/i, "");
        const instruction = ["Q.5", "Q.6"].includes(questionNo) ? "Answer the following (Any Two)" : "Answer the following";
        const rows = (qs || []).map((q, index) => q.or_before
          ? `<div class="or">OR</div><div class="question-row"><div class="part">${escapeHtml(q.sub_question || "B")}</div><div class="question">${escapeHtml(q.question)}</div><div>${Number(q.marks)} </div><div>${escapeHtml(q.co || "")}</div><div>${escapeHtml(q.bloom || "")}</div></div>`
          : `<div class="question-row"><div class="part">${escapeHtml(q.sub_question || String.fromCharCode(65 + index))}</div><div class="question">${escapeHtml(q.question)}</div><div>${Number(q.marks)} </div><div>${escapeHtml(q.co || "")}</div><div>${escapeHtml(q.bloom || "")}</div></div>`
        ).join("");
        return `<section><div class="question-heading"><b>${escapeHtml(questionNo)}</b><span>${instruction}</span><span>Marks &nbsp;&nbsp;&nbsp; COs &nbsp;&nbsp;&nbsp; BT Level</span></div>${rows}</section>`;
      }).join("");
      const totalMarks = paperTotal(s);
      const html = `<!DOCTYPE html><html><head><title>${escapeHtml(subject)} - Set ${setKey}</title><style>
        @page{size:A4;margin:14mm 16mm 17mm} body{font-family:"Times New Roman",serif;color:#111;font-size:12pt;line-height:1.32}.top{display:grid;grid-template-columns:115px 1fr 115px;gap:12px;align-items:center;text-align:center}.box{height:64px;border:1px solid #222;font-weight:bold;font-size:14pt;padding-top:4px}.box div{height:39px;border-top:1px solid #222;margin-top:4px}.inst{font-size:14pt;line-height:1.15}.inst strong{font-size:16pt}.course{text-align:center;font-size:14pt;margin:7px 0}.meta{display:flex;justify-content:space-between;border-bottom:1.5px solid #111;padding:4px 0 8px;font-size:13pt}.instructions{margin:18px 0 54px;display:grid;grid-template-columns:82px 1fr}.instructions b{font-size:14pt}.instructions ol{margin:0;padding-left:20px}.question-heading{display:grid;grid-template-columns:65px 1fr 235px;gap:5px;font-size:13pt;margin:18px 0 11px}.question-row{display:grid;grid-template-columns:42px 1fr 44px 58px 54px;gap:7px;margin:0 0 14px 82px;break-inside:avoid}.question{padding-right:8px;text-align:justify}.or{text-align:center;font-size:14pt;font-weight:bold;margin:0 0 10px 80px}.footer{position:fixed;bottom:0;left:0;right:0;text-align:center;font-size:11pt}.set{position:fixed;bottom:0;left:0;font-size:10pt}@media print{.footer:after{content:"Page " counter(page) " of " counter(pages)}}
      </style></head><body><div class="top"><div class="box">Enroll No<div></div></div><div class="inst"><strong>${escapeHtml(headerDetails.collegeName)}</strong><br>${escapeHtml(headerDetails.examTitle)}<br>T.Y.B.Tech. ${escapeHtml(level)}</div><div class="box">Q.P.Code<div></div></div></div><div class="course"><b>Course Code:</b> ${escapeHtml(courseId)} &nbsp;&nbsp;&nbsp;&nbsp; <b>Course Name:</b> ${escapeHtml(subject)}</div><div class="meta"><span><b>Day & Date:</b> ____________________<br><b>Time:</b> ____________________</span><span><b>Max Marks: ${totalMarks}</b></span></div><div class="instructions"><b>Instructions:</b><ol><li>All questions are compulsory.</li><li>Figures in rounded brackets within the question indicate the scheme of marking for the respective part; figures in the right columns indicate marks, COs and BT level.</li><li>CO is the index number of the Course Outcome statement.</li><li>BT Levels 1–6 are remember, understand, apply, analyze, evaluate and create respectively.</li><li>Assume suitable data if necessary.</li></ol></div>${questionBlocks}<div class="set">Set ${setKey}</div><div class="footer"></div></body></html>`;
      const win = window.open("", "_blank");
      win.document.write(html); win.document.close(); win.focus(); setTimeout(() => win.print(), 500);
      return;
    }
    const dateStr =
date ||
new Date().toLocaleDateString("en-IN", {
 day:"2-digit",
 month:"long",
 year:"numeric"
});
    const rows = questions => (questions || []).map((q, i) =>
        `<tr><td style="padding:8px 4px;vertical-align:top;color:#555;font-size:13px;">${i + 1}.</td><td style="padding:8px 8px 8px 4px;font-size:13px;">${escapeHtml(q.question)}</td><td style="padding:8px 4px;text-align:right;font-size:13px;white-space:nowrap;">[${Number(q.marks || 0)}M]</td></tr>`
      ).join("");
    const sections = Object.entries(s || {}).map(([name, questions]) =>
      `<h2>${escapeHtml(sectionTitle(name))} (${questions.reduce((total, q) => total + Number(q.marks || 0), 0)} Marks)</h2><table>${rows(questions)}</table>`
    ).join("");
    const total = paperTotal(s);
    const html = `<!DOCTYPE html><html><head><title>${escapeHtml(subject)} - Set ${setKey}</title>
<style>body{font-family:Georgia,serif;margin:0;padding:40px;color:#111;}h1{font-size:20px;text-align:center;margin:0 0 4px;}.meta{text-align:center;font-size:13px;color:#555;margin-bottom:24px;}h2{font-size:14px;border-bottom:2px solid #111;padding-bottom:4px;margin:24px 0 12px;}table{width:100%;border-collapse:collapse;}.footer{margin-top:40px;text-align:center;font-size:12px;color:#888;border-top:1px solid #ddd;padding-top:12px;}@media print{@page{margin:20mm;}}</style></head>
<body>
<p style="text-align:right;font-size:12px;color:#888;">CONFIDENTIAL - EXAMINER COPY</p>
<h1>${escapeHtml(subject)} Examination - Set ${setKey}</h1>
<div class="meta">${courseId ? `<strong>${escapeHtml(courseId)}</strong> &nbsp;|&nbsp;` : ""} Level: ${escapeHtml(level)} &nbsp;|&nbsp; Total Marks: ${total} &nbsp;|&nbsp; Duration: 3 Hours &nbsp;|&nbsp; Date: ${dateStr}</div>
<p style="font-size:13px;font-style:italic;color:#555;">Answer all sections. Write clearly and concisely.</p>
${sections}
<div class="footer">Generated by Quest-AI | ${escapeHtml(subject)} ${escapeHtml(courseId)} | Set ${setKey} | ${dateStr}</div>
</body></html>`;

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
      <Header title="Generate Question Paper" subtitle="Backend Gemini generationgenerates Set A, B, and C using your template" />

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
            <label className="block text-xs font-medium mb-1.5" style={{ color: "#94A3B8" }}>Year *</label>
            <input type="text" value={level} onChange={e => setLevel(e.target.value)} placeholder="e.g. T.Y / S.Y / F.Y"
              className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
              style={{ background: "#141B30", border: `1px solid ${level ? "#3B82F6" : "#1E2D4A"}`, color: "#E2E8F0" }} />
          </div>
          <div>
            <label className="block text-xs font-medium mb-1.5"style={{color:"#94A3B8"}}>Template *</label>
            <select value={template}onChange={e=>{const selected =savedTemplates.find(t=>String(t.id)===String(e.target.value));setTemplate(e.target.value);setSelectedTemplate(selected);}}
            className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
            style={{background:"#141B30",border:"1px solid #1E2D4A",color:"#E2E8F0"}}>
            <option value="" disabled>Select Default Template or an uploaded paper</option>


        {
        savedTemplates.map(t=>(

        <option
        key={t.id}
        value={t.id}
        >

        {t.template_name}

        </option>

        ))
        }


        </select>


        <label
        className="block text-xs font-medium mt-3 mb-1.5"
        style={{color:"#94A3B8"}}
        >

        Upload New Template

        </label>


        <input

        type="file"

        accept=".pdf,.docx"

        onChange={handleTemplateUpload}

        className="w-full text-xs"

        style={{
        color:"#E2E8F0"
        }}

        />


        </div>
        </div>

        <div className="flex items-center gap-3 p-3 rounded-lg mb-3" style={{ background: "#141B30" }}>
          <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${canGenerate ? "bg-emerald-500" : "bg-amber-500"}`} />
          <span className="text-xs" style={{ color: canGenerate ? "#10B981" : "#F59E0B" }}>
            {subject
              ? `${subjectQs.length} bank questions and ${matchedSyllabus ? "a saved syllabus" : "no matching saved syllabus"} found`
              : "Enter a subject name to check backend readiness"}
            {!level && " Enter the year (T.Y / S.Y / F.Y) to continue."}
            {!template && " Select the Default Template or an uploaded previous-year paper to use as the exact blueprint."}
            {usingDefaultTemplate && " Using the built-in fixed 100-mark examination format."}
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
                <span>Year: {level}</span>
                <span style={{ fontWeight: 600, color: "#E2E8F0" }}>{paperTotal(sets[activeSet])} Marks</span>
                <span>3 Hours</span>
                <span>{new Date().toLocaleDateString("en-IN", { day: "2-digit", month: "long", year: "numeric" })}</span>
              </div>
            </div>

            {Object.entries(sets[activeSet]).map(([name, qs], index) => (
              <SectionBlock key={name} title={sectionTitle(name)} qs={qs} col={["#3B82F6", "#F59E0B", "#EF4444"][index % 3]} />
            ))}

            <div className="border-t pt-4" style={{ borderColor: "#1E2D4A" }}>
              <p className="text-xs mb-3 font-medium" style={{ color: "#64748B" }}>Download any set as PDF:</p>
              <div className="flex gap-3">
                {["A", "B", "C"].map(s => (
                  <button key={s} onClick={() => downloadPDF(s)}
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
