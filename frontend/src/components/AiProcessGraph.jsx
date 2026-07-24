const STAGE_COLORS = {
  done: "#10B981",
  active: "#38BDF8",
  pending: "#334155"
};

export default function AiProcessGraph({ stages = [], active = 0, quality, model = "gpt-5" }) {
  return (
    <div className="ai-arena rounded-2xl border p-4 mb-4" style={{ background: "#07111F", borderColor: "#1F2A44" }}>
      <div className="flex items-center justify-between mb-4 gap-3">
        <div>
          <p className="text-xs font-semibold tracking-wide" style={{ color: "#7DD3FC" }}>
            AI BACKEND ARENA
          </p>
          <h3 className="text-sm font-semibold mt-1" style={{ color: "#E2E8F0" }}>
            Gemini generationtask pipeline
          </h3>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full font-mono" style={{ background: "#0F172A", color: "#93C5FD", border: "1px solid #1D4ED8" }}>
          {model}
        </span>
      </div>

      <div className="relative grid gap-3 md:grid-cols-5">
        <div className="hidden md:block absolute left-6 right-6 top-5 h-px ai-flow-line" />
        {stages.map((stage, index) => {
          const state = index < active ? "done" : index === active ? "active" : "pending";
          return (
            <div key={stage.title} className="relative rounded-xl p-3 min-h-[92px]" style={{ background: "#0B1628", border: `1px solid ${state === "active" ? "#38BDF8" : "#1E293B"}` }}>
              <div className="flex items-center gap-2 mb-2">
                <span className={state === "active" ? "ai-node active" : "ai-node"} style={{ background: STAGE_COLORS[state] }} />
                <span className="text-[11px] font-semibold" style={{ color: state === "pending" ? "#64748B" : "#E2E8F0" }}>
                  {stage.title}
                </span>
              </div>
              <p className="text-[11px] leading-relaxed" style={{ color: "#7C8EA3" }}>
                {stage.detail}
              </p>
            </div>
          );
        })}
      </div>

      {quality && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-4">
          {[
            ["No repetition", quality.duplicatePreventionScore],
            ["Syllabus cover", quality.syllabusCoverageScore],
            ["Semantic match", quality.semanticAlignmentScore],
            ["Accuracy", quality.overallAccuracy]
          ].map(([label, value]) => (
            <div key={label} className="rounded-xl px-3 py-2" style={{ background: "#0F172A", border: "1px solid #1E293B" }}>
              <p className="text-[10px]" style={{ color: "#64748B" }}>{label}</p>
              <p className="text-lg font-bold" style={{ color: value >= 70 ? "#10B981" : value >= 45 ? "#F59E0B" : "#F87171" }}>
                {Number(value || 0).toFixed(1)}%
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
