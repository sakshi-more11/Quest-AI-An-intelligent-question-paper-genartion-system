// src/pages/Dashboard.jsx
// Teacher dashboard: overview of their questions, syllabi, recent activity.
// Admin dashboard: system-wide stats, read-only view of everything.

import { BLOOM_LEVELS, BLOOM_COLORS, DIFFICULTY } from "../data/constants";
import { Header, Stat, Badge, Card } from "../components/UI";

export default function Dashboard({ user, questions, logs, syllabi, papers }) {
  const isAdmin = user.role === "admin";

  if (isAdmin) return <AdminDashboard questions={questions} logs={logs} papers={papers} />;
  return <TeacherDashboard user={user} questions={questions} syllabi={syllabi} logs={logs} />;
}

// ─── TEACHER DASHBOARD ─────────────────────────────────────────────────────────
function TeacherDashboard({ user, questions, syllabi, logs }) {
  const myQs      = questions.filter(q => q.createdBy === user.username);
  const subjects  = [...new Set(myQs.map(q => q.subject))];
  const mySyllabi = syllabi.filter(s => s.uploadedBy === user.username);
  const myLogs    = logs.filter(l => l.user === user.username);

  return (
    <div>
      <Header title={`Welcome, ${user.name.split(" ").slice(-1)[0]}`} subtitle="Your question bank overview" />

      <div className="grid grid-cols-2 gap-3 mb-5">
        <Stat label="My Questions"    value={myQs.length}        color="#3B82F6" />
        <Stat label="Subjects"        value={subjects.length}    color="#10B981" />
        <Stat label="Syllabi Uploaded" value={mySyllabi.length} color="#F59E0B" />
        <Stat label="Actions Taken"   value={myLogs.length}      color="#8B5CF6" />
      </div>

      {/* Syllabi list */}
      <Card className="mb-4">
        <h3 className="text-sm font-semibold mb-3" style={{ color: "#E2E8F0" }}>Your Syllabi</h3>
        {mySyllabi.length === 0 ? (
          <p className="text-xs text-center py-4" style={{ color: "#475569" }}>No syllabi uploaded yet.</p>
        ) : mySyllabi.map(s => (
          <div key={s.id} className="flex items-center justify-between py-2.5 border-b last:border-0"
            style={{ borderColor: "#141B30" }}>
            <div>
              <p className="text-xs font-medium" style={{ color: "#E2E8F0" }}>{s.subject}</p>
              <p className="text-xs mt-0.5" style={{ color: "#475569" }}>
                <span style={{ color: "#3B82F6", fontFamily: "monospace" }}>{s.courseId}</span> · {s.level} · {s.units.length} units
              </p>
            </div>
            <span className="text-xs" style={{ color: "#10B981" }}>
              {questions.filter(q => q.subject === s.subject).length} questions
            </span>
          </div>
        ))}
      </Card>

      {/* Subject breakdown */}
      <Card className="mb-4">
        <h3 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>Questions by Subject</h3>
        {subjects.length === 0 ? (
          <p className="text-xs text-center py-4" style={{ color: "#475569" }}>No questions yet.</p>
        ) : subjects.map(sub => {
          const subQs = myQs.filter(q => q.subject === sub);
          const cid   = subQs[0]?.courseId || "";
          const pct   = Math.round((subQs.length / Math.max(myQs.length, 1)) * 100);
          return (
            <div key={sub} className="mb-4 last:mb-0">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium" style={{ color: "#E2E8F0" }}>{sub}</span>
                  {cid && (
                    <span className="text-xs font-mono px-1.5 py-0.5 rounded"
                      style={{ background: "#0A1628", color: "#3B82F6", border: "1px solid #1E3A5F" }}>{cid}</span>
                  )}
                </div>
                <span className="text-xs" style={{ color: "#64748B" }}>{subQs.length} questions</span>
              </div>
              <div className="h-2 rounded-full" style={{ background: "#141B30" }}>
                <div className="h-full rounded-full"
                  style={{ width: `${pct}%`, background: "linear-gradient(90deg,#1D4ED8,#3B82F6)" }} />
              </div>
              <div className="flex gap-3 mt-1">
                {[["E", "Easy", "#10B981"], ["M", "Medium", "#F59E0B"], ["H", "Hard", "#EF4444"]].map(([sh, d, c]) => (
                  <span key={d} className="text-xs" style={{ color: c }}>
                    {sh}: {subQs.filter(q => q.difficulty === d).length}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </Card>

      {/* Bloom distribution */}
      <Card>
        <h3 className="text-sm font-semibold mb-3" style={{ color: "#E2E8F0" }}>Bloom's Taxonomy</h3>
        <div className="grid grid-cols-3 gap-2">
          {BLOOM_LEVELS.map((bl, i) => (
            <div key={bl} className="rounded-lg p-2.5 text-center" style={{ background: "#141B30" }}>
              <div className="text-lg font-bold" style={{ color: BLOOM_COLORS[i] }}>
                {myQs.filter(q => q.bloom === bl).length}
              </div>
              <div className="text-xs mt-0.5" style={{ color: "#64748B" }}>{bl}</div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

// ─── ADMIN DASHBOARD ───────────────────────────────────────────────────────────
function AdminDashboard({ questions, logs, papers }) {
  const subjects        = [...new Set(questions.map(q => q.subject))];
  const papersGenCount  = logs.filter(l => l.action === "PAPER_GENERATED").length;
  const teacherCount    = [...new Set(logs.filter(l => l.role === "Teacher").map(l => l.user))].length;

  return (
    <div>
      <Header title="Admin Dashboard" subtitle="System-wide read-only overview" />

      {/* Read-only notice */}
      <div className="mb-5 px-4 py-3 rounded-xl text-sm flex items-center gap-3"
        style={{ background: "#2D1F00", border: "1px solid #92400E", color: "#FCD34D" }}>
        <span>👁</span>
        <span>You have <strong>read-only access</strong>. Teachers handle all operations. You can view all data and download generated papers.</span>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-5">
        <Stat label="Total Questions"   value={questions.length}  color="#3B82F6" />
        <Stat label="Subjects in Bank"  value={subjects.length}   color="#10B981" />
        <Stat label="Papers Generated"  value={papersGenCount}    color="#F59E0B" />
        <Stat label="Active Teachers"   value={teacherCount}      color="#8B5CF6" />
      </div>

      {/* Subject readiness */}
      <Card className="mb-4">
        <h3 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>Question Bank Status</h3>
        {subjects.length === 0 ? (
          <p className="text-xs text-center py-4" style={{ color: "#475569" }}>No questions yet.</p>
        ) : subjects.map(sub => {
          const subQs = questions.filter(q => q.subject === sub);
          const cid   = subQs[0]?.courseId || "";
          const cnt   = subQs.length;
          const pct   = Math.min(100, Math.round((cnt / 300) * 100));
          const ready = cnt >= 300;
          return (
            <div key={sub} className="mb-4 last:mb-0">
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium" style={{ color: "#E2E8F0" }}>{sub}</span>
                  {cid && (
                    <span className="text-xs font-mono px-1.5 py-0.5 rounded"
                      style={{ background: "#0A1628", color: "#3B82F6", border: "1px solid #1E3A5F" }}>{cid}</span>
                  )}
                </div>
                <span className="text-xs font-medium" style={{ color: ready ? "#10B981" : "#F59E0B" }}>
                  {cnt}/300 {ready ? "✓ Ready" : "Building…"}
                </span>
              </div>
              <div className="h-2 rounded-full" style={{ background: "#141B30" }}>
                <div className="h-full rounded-full"
                  style={{ width: `${pct}%`, background: ready ? "linear-gradient(90deg,#059669,#10B981)" : "linear-gradient(90deg,#B45309,#F59E0B)" }} />
              </div>
            </div>
          );
        })}
      </Card>

      {/* Recent generated papers */}
      <Card className="mb-4">
        <h3 className="text-sm font-semibold mb-3" style={{ color: "#E2E8F0" }}>Generated Papers</h3>
        {papers.length === 0 ? (
          <p className="text-xs text-center py-4" style={{ color: "#475569" }}>No papers generated yet.</p>
        ) : papers.slice(0, 5).map((p, i) => (
          <div key={i} className="flex items-center justify-between py-2.5 border-b last:border-0"
            style={{ borderColor: "#141B30" }}>
            <div>
              <p className="text-xs font-medium" style={{ color: "#E2E8F0" }}>{p.subject}</p>
              <p className="text-xs mt-0.5" style={{ color: "#475569" }}>
                {p.courseId && <span style={{ color: "#3B82F6", fontFamily: "monospace" }}>{p.courseId} · </span>}
                {p.level} · by {p.generatedBy} · {new Date(p.generatedAt).toLocaleDateString()}
              </p>
            </div>
            <Badge color="green">Set A·B·C</Badge>
          </div>
        ))}
      </Card>

      {/* Recent logs */}
      <Card>
        <h3 className="text-sm font-semibold mb-3" style={{ color: "#E2E8F0" }}>Recent Activity</h3>
        {logs.slice(0, 6).map(log => (
          <div key={log.id} className="flex items-center gap-3 py-2.5 border-b last:border-0"
            style={{ borderColor: "#141B30" }}>
            <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0"
              style={{ background: log.role === "Admin" ? "#2D1F00" : "#0F1D3A", color: log.role === "Admin" ? "#F59E0B" : "#3B82F6" }}>
              {log.user[0].toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium truncate" style={{ color: "#E2E8F0" }}>{log.details}</p>
              <p className="text-xs mt-0.5" style={{ color: "#475569" }}>{log.user} · {new Date(log.timestamp).toLocaleString()}</p>
            </div>
            <Badge color={log.role === "Admin" ? "gold" : "blue"}>{log.action.split("_")[0]}</Badge>
          </div>
        ))}
      </Card>
    </div>
  );
}
