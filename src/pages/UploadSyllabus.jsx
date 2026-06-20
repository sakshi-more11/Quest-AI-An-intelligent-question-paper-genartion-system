import { useState } from "react";
import { Header, Card, TextInput, CoursePill, LevelToggle, PrimaryBtn, Flash } from "../components/UI";
import AiProcessGraph from "../components/AiProcessGraph";
import { parseSyllabus as parseSyllabusApi } from "../lib/api";

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(",")[1]);
    reader.onerror = () => reject(new Error("File read failed"));
    reader.readAsDataURL(file);
  });
}

function getMediaType(file) {
  const ext = file.name.split(".").pop().toLowerCase();
  if (ext === "pdf") return "application/pdf";
  if (["ppt", "pptx"].includes(ext)) return "application/vnd.ms-powerpoint";
  if (["doc", "docx"].includes(ext)) return "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
  return "application/octet-stream";
}

const parseStages = [
  { title: "File intake", detail: "The uploaded syllabus is prepared for backend reading." },
  { title: "OCR / NLP", detail: "GPT-5 reads the file and extracts academic structure." },
  { title: "Topic map", detail: "Units and topics are converted into structured JSON." },
  { title: "Coverage base", detail: "Topics are prepared for syllabus coverage checks." },
  { title: "Ready", detail: "The parsed syllabus can now drive question generation." },
];

export default function UploadSyllabus({ user, onUploadComplete }) {
  const [file, setFile] = useState(null);
  const [subject, setSubject] = useState("");
  const [courseId, setCourseId] = useState("");
  const [level, setLevel] = useState("College");
  const [parsing, setParsing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);
  const [processStep, setProcessStep] = useState(0);
  const [aiModel, setAiModel] = useState("gpt-5");

  const canParse = file && subject.trim() && courseId.trim();

  const parseSyllabus = async () => {
    if (!canParse) return;
    setParsing(true);
    setError("");
    setResult(null);
    setProcessStep(0);

    try {
      const b64 = await fileToBase64(file);
      setProcessStep(1);
      const parsed = await parseSyllabusApi({
        subject,
        courseId,
        level,
        fileName: file.name,
        file: {
          name: file.name,
          mediaType: getMediaType(file),
          base64: b64
        }
      });

      setProcessStep(4);
      setAiModel(parsed.model || "gpt-5");
      setResult(parsed);
    } catch (e) {
      setError(`Backend AI parsing failed: ${e.message}. Showing a sample structure based on subject name.`);
      const fallbackUnits = {
        Mathematics: [
          { name: "Unit 1: Algebra", topics: ["Linear Equations", "Polynomials", "Quadratics"] },
          { name: "Unit 2: Calculus", topics: ["Limits", "Derivatives", "Integration"] },
          { name: "Unit 3: Geometry", topics: ["Triangles", "Circles", "Vectors"] },
        ],
        Physics: [
          { name: "Unit 1: Mechanics", topics: ["Newton's Laws", "Kinematics", "Work-Energy"] },
          { name: "Unit 2: Optics", topics: ["Reflection", "Refraction", "Lenses"] },
          { name: "Unit 3: Thermodynamics", topics: ["Heat", "Entropy", "Gas Laws"] },
        ],
        "Computer Science": [
          { name: "Unit 1: Data Structures", topics: ["Arrays", "Linked Lists", "Trees"] },
          { name: "Unit 2: Algorithms", topics: ["Sorting", "Searching", "Dynamic Programming"] },
          { name: "Unit 3: OS", topics: ["Processes", "Memory", "Scheduling"] },
        ],
      };
      const units = fallbackUnits[subject] || [
        { name: `Unit 1: Introduction to ${subject}`, topics: ["Basics", "Fundamentals", "Overview"] },
        { name: "Unit 2: Core Concepts", topics: ["Key Theory", "Methods", "Applications"] },
        { name: "Unit 3: Advanced Topics", topics: ["Complex Problems", "Case Studies", "Analysis"] },
        { name: "Unit 4: Practical Applications", topics: ["Labs", "Projects", "Experiments"] },
      ];
      setResult({ units, totalUnits: units.length });
    }

    setParsing(false);
  };

  const confirmAndProceed = () => {
    if (!result) return;
    onUploadComplete({
      file,
      subject: subject.trim(),
      courseId: courseId.trim(),
      level,
      units: result.units,
    });
    setDone(true);
  };

  if (done) {
    return (
      <div>
        <Header title="Upload Syllabus" subtitle="Syllabus parsed and saved" />
        <Card>
          <div className="text-center py-6">
            <div className="text-4xl mb-3">OK</div>
            <h3 className="font-semibold mb-2" style={{ color: "#10B981" }}>Syllabus Processed</h3>
            <p className="text-sm mb-1" style={{ color: "#64748B" }}>
              <span style={{ color: "#E2E8F0" }}>{subject}</span>{" "}
              <span style={{ color: "#3B82F6", fontFamily: "monospace" }}>{courseId}</span>{" "}
              {level}
            </p>
            <p className="text-sm mb-5" style={{ color: "#475569" }}>
              {result?.units?.length} units extracted. Open Question Bank to generate checked questions.
            </p>
            <button
              onClick={() => { setDone(false); setFile(null); setSubject(""); setCourseId(""); setResult(null); }}
              className="px-5 py-2 rounded-lg text-sm font-medium"
              style={{ background: "#141B30", color: "#3B82F6", border: "1px solid #1E2D4A" }}>
              Upload Another Syllabus
            </button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <Header title="Upload Syllabus" subtitle="Upload your syllabus. Backend GPT-5 extracts units and topics." />
      <div className="space-y-4">
        <Card>
          <h3 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>Course Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <TextInput label="Subject Name" value={subject} onChange={setSubject} placeholder="e.g. Data Structures" required hint="Type the full subject name" />
            <TextInput label="Course ID" value={courseId} onChange={setCourseId} placeholder="e.g. CS301" required mono hint="e.g. CS301, MA101" />
          </div>
          <CoursePill subject={subject} courseId={courseId} level={level} />
        </Card>

        <Card>
          <label className="block text-sm font-medium mb-3" style={{ color: "#94A3B8" }}>Academic Level</label>
          <LevelToggle value={level} onChange={setLevel} />
        </Card>

        <Card>
          <label className="block text-sm font-medium mb-3" style={{ color: "#94A3B8" }}>Upload Syllabus File</label>
          <div
            className="border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all"
            style={{ borderColor: file ? "#3B82F6" : "#1E2D4A", background: "#141B30" }}
            onClick={() => document.getElementById("syllabusFile").click()}>
            <input id="syllabusFile" type="file" accept=".pdf,.ppt,.pptx,.doc,.docx" className="hidden" onChange={e => setFile(e.target.files[0])} />
            <div className="text-3xl mb-2">{file ? "PDF" : "FILE"}</div>
            <p className="text-sm font-medium" style={{ color: file ? "#3B82F6" : "#64748B" }}>
              {file ? file.name : "Click to browse or drag and drop"}
            </p>
            {!file && <p className="text-xs mt-1" style={{ color: "#475569" }}>PDF, PPT, and DOCX supported</p>}
            {file && <p className="text-xs mt-1" style={{ color: "#475569" }}>{(file.size / 1024).toFixed(1)} KB</p>}
          </div>

          <div className="mt-3 px-3 py-2.5 rounded-lg" style={{ background: "#0A1628", border: "1px solid #1E3A5F" }}>
            <p className="text-xs" style={{ color: "#475569" }}>
              Backend AI reads the syllabus, extracts units, and prepares coverage tracking for generation.
            </p>
          </div>
        </Card>

        <Flash message={error} type="warn" />

        {parsing && <AiProcessGraph stages={parseStages} active={processStep} model={aiModel} />}

        <PrimaryBtn onClick={parseSyllabus} disabled={!canParse} loading={parsing} fullWidth>
          {parsing ? "Backend GPT-5 is reading syllabus..." : "Parse Syllabus with Backend AI"}
        </PrimaryBtn>

        {!canParse && (
          <p className="text-xs text-center" style={{ color: "#475569" }}>
            Fill Subject Name, Course ID, and select a file to continue.
          </p>
        )}

        {result && (
          <Card>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-semibold" style={{ color: "#E2E8F0" }}>
                  Extracted {result.units.length} Units from Syllabus
                </h3>
                <p className="text-xs mt-0.5" style={{ color: "#64748B" }}>Review the extracted content below</p>
              </div>
              <span className="text-xs px-2 py-1 rounded-full font-medium" style={{ background: "#0B2818", border: "1px solid #065F46", color: "#6EE7B7" }}>
                AI Extracted
              </span>
            </div>

            <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
              {result.units.map((unit, i) => (
                <div key={i} className="rounded-lg p-3.5" style={{ background: "#141B30", border: "1px solid #1E2D4A" }}>
                  <p className="text-sm font-semibold mb-2" style={{ color: "#E2E8F0" }}>{unit.name}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {(unit.topics || []).map((topic, j) => (
                      <span key={j} className="text-xs px-2 py-0.5 rounded" style={{ background: "#0A1628", color: "#94A3B8", border: "1px solid #1E3A5F" }}>
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 pt-4 border-t" style={{ borderColor: "#1E2D4A" }}>
              <PrimaryBtn onClick={confirmAndProceed} fullWidth>
                Confirm and Save Syllabus
              </PrimaryBtn>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
