import { useMemo, useState, useEffect } from "react";
import { BLOOM_LEVELS, DIFFICULTY, LEVELS } from "../data/constants";
import { Badge, Header, SearchBar, Card, PrimaryBtn, Empty } from "../components/UI";
import AiProcessGraph from "../components/AiProcessGraph";
import {
    generateQuestionBank,
} from "../lib/questionBankApi";
const PAGE = 10;
const GEN_STAGES = [
  { title: "Syllabus map", detail: "Backend reads units and topic coverage targets." },
  { title: "Gemini generation", detail: "Questions are generated with Bloom and CO mapping." },
  { title: "Semantic scan", detail: "ML cosine checks detect repeated meaning." },
  { title: "Coverage audit", detail: "Questions are matched against syllabus topics." },
  { title: "Accuracy", detail: "Backend returns quality scores and clean questions." },
];

function normalizeBloomLevel(value) {
  const raw = String(value ?? "").trim();
  if (!raw) return "BT2";

  const compact = raw.replace(/[^A-Za-z0-9]/g, "").toUpperCase();
  const mapped = compact.replace(/^BTE/i, "BT");

  if (/^BT[1-6]$/.test(mapped)) return mapped;

  const names = {
    REMEMBER: "BT1",
    UNDERSTAND: "BT2",
    APPLY: "BT3",
    ANALYZE: "BT4",
    EVALUATE: "BT5",
    CREATE: "BT6",
  };

  return names[compact] || "BT2";
}

export default function QuestionBank({ user, questions, onGenerateQBank }) {
  const isAdmin = user.role === "admin";
  const subjects = [...new Set(questions.map(q => q.subject))];
  const [search, setSearch] = useState("");
  const [fSub, setFSub] = useState("");
  const [fDiff, setFDiff] = useState("");
  const [fLevel, setFLevel] = useState("");
  const [fBloom, setFBloom] = useState("");
  const [page, setPage] = useState(0);
  const [genMode, setGenMode] = useState(false);
  const [syllabi, setSyllabi] = useState([]);
  const [selSyllabus, setSelSyllabus] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState("");
  const [selectedSubjectId,setSelectedSubjectId]=useState("");
  const [quality, setQuality] = useState(null);
  const [processStep, setProcessStep] = useState(0);
  const [aiModel, setAiModel] = useState("gemini-flash-lite-latest");
  const filtered = useMemo(() => questions.filter(q =>
    (!fSub || q.subject === fSub) &&
    (!fDiff || q.difficulty === fDiff) &&
    (!fLevel || q.level === fLevel) &&
    (!fBloom || q.bloom === fBloom) &&
    (!search || q.text.toLowerCase().includes(search.toLowerCase()) ||
      q.unit?.toLowerCase().includes(search.toLowerCase()) ||
      q.courseId?.toLowerCase().includes(search.toLowerCase()))
  ), [questions, fSub, fDiff, fLevel, fBloom, search]);

  const totalPages = Math.ceil(filtered.length / PAGE);
  const paged = filtered.slice(page * PAGE, (page + 1) * PAGE);
  useEffect(()=>{

    const storedUser = JSON.parse(
        localStorage.getItem("user")
    );

    const token = storedUser?.token;

    fetch("http://localhost:8000/upload/syllabi",{

        headers:{
            Authorization:
`Bearer ${
JSON.parse(localStorage.getItem("user"))?.token
}`
        }

    })

    .then(res=>res.json())

    .then(data=>{
        const normalized = Array.isArray(data) ? data : [];
        const unique = [...new Map(normalized.map(item => [
          `${item.subject_name || item.subject || ""}|${item.course_code || item.courseId || ""}|${item.filename || ""}`,
          item
        ])).values()];
        setSyllabi(unique);
    })

    .catch(err=>{

        console.log(
            "Syllabus fetch error:",
            err
        );

    });


},[]);
  async function generateFromBackend(subjectId){


    try{

        setGenerating(true);

        setGenError("");



        const data =
            await generateQuestionBank(
                subjectId
            );

        setProcessStep(2);

        setTimeout(() => {
            setProcessStep(3);
        }, 500);

        setTimeout(() => {
            setProcessStep(4);
        }, 1000);

        setTimeout(() => {
            setProcessStep(5);
        }, 1500);

        setQuality(data.quality || null);
        setAiModel("gemini-flash-lite-latest");

        const questions =
        data.questions || [];



        const formatted =
        questions.map((q,index)=>(

            {

                id:
                q.id ||
                Date.now()+index,


                text:
                q.question_text,


                subject:
                data.subject?.name
                || "",


                courseId:
                data.subject?.code
                || "",


                unit:
                q.unit
                || "Auto",


                marks:
                q.marks
                || 10,


                difficulty:
                q.difficulty
                || "Medium",


                bloom:
                normalizeBloomLevel(
                    q.blooms_level || q.bloom_level || q.bloom || "BT2"
                ),


                level:
                q.level || "College",


                createdBy:
                "Gemini AI"

            }

        ));



        onGenerateQBank(

            formatted,

            data.subject

        );

        setGenMode(false);
        setSelSyllabus(null);
        setSelectedSubjectId("");

    }

    catch(error){

        console.log(error);

        setGenError(
            error.message
        );

    }


    finally{

        setGenerating(false);

    }

}

  return (
    <div>
      <Header title="Question Bank" subtitle={`${questions.length} total questions${isAdmin ? " (read-only)" : ""}`} />

      {!isAdmin && (
        <div className="mb-4">
          {!genMode ? (
            <button
              onClick={() => setGenMode(true)}
              className="px-5 py-2.5 rounded-lg text-sm font-semibold"
              style={{ background: "linear-gradient(135deg,#1D4ED8,#3B82F6)", color: "white", boxShadow: "0 0 20px rgba(59,130,246,0.2)" }}>
              Generate Questions 
            </button>
          ) : (
            <Card>
              <h3 className="text-sm font-semibold mb-3" style={{ color: "#E2E8F0" }}>
                Select syllabus for backend Gemini generation
              </h3>

              {syllabi.length === 0 ? (
                <p className="text-xs" style={{ color: "#475569" }}>
                  No syllabi uploaded yet. Upload one first.
                </p>
              ) : (
                <div className="space-y-2 mb-4">

                  {syllabi.map(syl => (

                    <button
                      key={syl.id + "-" + syl.filename}
                      onClick={() => {
                        setSelectedSubjectId(syl.id);
                      }}
                      className="w-full text-left px-4 py-3 rounded-lg transition-all"
                      style={{
                        background:
                          selectedSubjectId === syl.id
                            ? "#1A2340"
                            : "#141B30",

                        border:
                          `1px solid ${
                            selectedSubjectId === syl.id
                            ? "#3B82F6"
                            : "#1E2D4A"
                          }`,
                      }}
                    >

                      <div className="flex items-center justify-between">

                        <div>

                          <p
                            className="text-sm font-medium"
                            style={{ color:"#E2E8F0" }}
                          >
                            {syl.subject_name}
                          </p>


                          <p
                            className="text-xs mt-0.5"
                            style={{ color:"#64748B" }}
                          >

                            <span
                              style={{
                                color:"#3B82F6",
                                fontFamily:"monospace"
                              }}
                            >
                              {syl.course_code}
                            </span>

                            {" / "}

                            {syl.filename}

                          </p>


                        </div>


                        {
                          selectedSubjectId === syl.id &&
                          <span style={{color:"#3B82F6"}}>
                            selected
                          </span>
                        }


                      </div>


                    </button>

                  ))}

                </div>
              )}

              {generating && <AiProcessGraph stages={GEN_STAGES} active={processStep} model={aiModel} />}
              {quality && !generating && <AiProcessGraph stages={GEN_STAGES} active={5} quality={quality} model={aiModel} />}
              {genError && <p className="text-xs mb-3" style={{ color: "#F59E0B" }}>{genError}</p>}

              <div className="flex gap-2">
                <PrimaryBtn
                  onClick={() => {
                      if(selectedSubjectId){
                          generateFromBackend(selectedSubjectId);
                      }
                  }}
                  disabled={!selectedSubjectId}
                  loading={generating}>
                  {generating ? "Generating and checking..." : "Generate Checked Questions"}
                </PrimaryBtn>
                <button
                  onClick={() => { setGenMode(false); setSelSyllabus(null); setSelectedSubjectId(""); }}
                  className="px-4 py-2 rounded-lg text-sm"
                  style={{ background: "#141B30", color: "#64748B", border: "1px solid #1E2D4A" }}>
                  Cancel
                </button>
              </div>
            </Card>
          )}
        </div>
      )}

      {quality && !genMode && (
        <AiProcessGraph stages={GEN_STAGES} active={5} quality={quality} model={aiModel} />
      )}

      <SearchBar value={search} onChange={setSearch} placeholder="Search by question, unit, or course ID..." />

      <div className="grid grid-cols-4 gap-2 mb-4">
        {[
          [fSub, setFSub, "Subject", ["", ...subjects]],
          [fDiff, setFDiff, "Difficulty", ["", ...DIFFICULTY]],
          [fLevel, setFLevel, "Level", ["", ...LEVELS]],
          [fBloom, setFBloom, "Bloom", ["", ...BLOOM_LEVELS]],
        ].map(([val, setter, label, opts]) => (
          <select
            key={label}
            value={val}
            onChange={e => { setter(e.target.value); setPage(0); }}
            className="px-3 py-2 rounded-lg text-xs outline-none"
            style={{ background: "#0F1629", border: "1px solid #1E2D4A", color: "#E2E8F0" }}>
            <option value="">{label}</option>
            {opts.slice(1).map(o => <option key={o}>{o}</option>)}
          </select>
        ))}
      </div>

      <p className="text-xs mb-3" style={{ color: "#475569" }}>
        Showing {paged.length} of {filtered.length} results
      </p>

      <div className="rounded-xl border overflow-hidden" style={{ background: "#0F1629", borderColor: "#1E2D4A" }}>
        <table className="w-full text-xs">
          <thead>
            <tr style={{ background: "#141B30" }}>
              {["#", "Question", "Subject / ID", "Unit", "Marks", "Diff", "Bloom", "By"].map(h => (
                <th key={h} className="px-3 py-3 text-left font-semibold" style={{ color: "#64748B" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map((q, i) => (
              <tr key={q.id} style={{ borderTop: "1px solid #141B30" }}>
                <td className="px-3 py-3" style={{ color: "#475569" }}>{page * PAGE + i + 1}</td>
                <td className="px-3 py-3 max-w-xs">
                  <p className="truncate" style={{ color: "#E2E8F0" }}>{q.text}</p>
                </td>
                <td className="px-3 py-3">
                  <div className="flex flex-col gap-0.5">
                    <span style={{ color: "#94A3B8" }}>{q.subject}</span>
                    {q.courseId && <span className="font-mono" style={{ color: "#3B82F6" }}>{q.courseId}</span>}
                  </div>
                </td>
                <td className="px-3 py-3" style={{ color: "#64748B" }}>{q.unit}</td>
                <td className="px-3 py-3"><Badge color="blue">{q.marks}M</Badge></td>
                <td className="px-3 py-3">
                  <Badge color={q.difficulty === "Easy" ? "green" : q.difficulty === "Medium" ? "gold" : "red"}>
                    {q.difficulty}
                  </Badge>
                </td>
                <td className="px-3 py-3"><Badge color="purple">{q.bloom}</Badge></td>
                <td className="px-3 py-3" style={{ color: "#64748B" }}>{q.createdBy}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <Empty message="No questions match your search / filters." />}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs" style={{ color: "#475569" }}>
            {page * PAGE + 1}-{Math.min((page + 1) * PAGE, filtered.length)} of {filtered.length}
          </span>
          <div className="flex gap-2">
            <button disabled={page === 0} onClick={() => setPage(p => p - 1)}
              className="px-3 py-1.5 rounded text-xs disabled:opacity-30"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#94A3B8" }}>Prev</button>
            <button disabled={page >= totalPages - 1} onClick={() => setPage(p => p + 1)}
              className="px-3 py-1.5 rounded text-xs disabled:opacity-30"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#94A3B8" }}>Next</button>
          </div>
        </div>
      )}
    </div>
  );
}
