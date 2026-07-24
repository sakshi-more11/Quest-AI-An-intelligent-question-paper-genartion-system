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
function TeacherDashboard({ user }) {

  return (

    <div>

      <Header
        title={`Welcome, ${user.name || user.email}`}
        subtitle="QuestAI Teacher Dashboard"
      />

      <div className="grid grid-cols-4 gap-4 mb-6">

        <Stat
          label="My Questions"
          value="125"
          color="#2563EB"
        />

        <Stat
          label="Syllabi Uploaded"
          value="8"
          color="#16A34A"
        />

        <Stat
          label="Generated Papers"
          value="22"
          color="#F59E0B"
        />

        <Stat
          label="Pending Actions"
          value="3"
          color="#8B5CF6"
        />

      </div>

      <Card className="mb-5">

        <h2
          className="text-xl font-semibold mb-4"
          style={{ color:"#F8FAFC" }}
        >
          Recent Activity
        </h2>

        <div className="space-y-3">

          <div className="flex justify-between">

            <span style={{color:"#CBD5E1"}}>
              Uploaded Machine Learning syllabus
            </span>

            <span style={{color:"#64748B"}}>
              Today
            </span>

          </div>

          <div className="flex justify-between">

            <span style={{color:"#CBD5E1"}}>
              Generated Question Paper Set A
            </span>

            <span style={{color:"#64748B"}}>
              Yesterday
            </span>

          </div>

          <div className="flex justify-between">

            <span style={{color:"#CBD5E1"}}>
              Added 45 new questions
            </span>

            <span style={{color:"#64748B"}}>
              2 days ago
            </span>

          </div>

        </div>

      </Card>

      <Card>

  <h2
    className="text-xl font-semibold mb-5"
    style={{ color: "#F8FAFC" }}
  >
    Performance Overview
  </h2>

  <div className="space-y-5">

    <div>

      <div className="flex justify-between mb-2">

        <span style={{ color: "#CBD5E1" }}>
          Question Bank Completion
        </span>

        <span style={{ color: "#3B82F6" }}>
          82%
        </span>

      </div>

      <div className="w-full h-3 rounded-full bg-slate-800">

        <div
          className="h-3 rounded-full bg-blue-600"
          style={{ width: "82%" }}
        />

      </div>

    </div>

    <div>

      <div className="flex justify-between mb-2">

        <span style={{ color: "#CBD5E1" }}>
          Syllabus Coverage
        </span>

        <span style={{ color: "#16A34A" }}>
          90%
        </span>

      </div>

      <div className="w-full h-3 rounded-full bg-slate-800">

        <div
          className="h-3 rounded-full bg-green-600"
          style={{ width: "90%" }}
        />

      </div>

    </div>

    <div>

      <div className="flex justify-between mb-2">

        <span style={{ color: "#CBD5E1" }}>
          Bloom's Taxonomy Mapping
        </span>

        <span style={{ color: "#F59E0B" }}>
          75%
        </span>

      </div>

      <div className="w-full h-3 rounded-full bg-slate-800">

        <div
          className="h-3 rounded-full bg-orange-500"
          style={{ width: "75%" }}
        />

      </div>

    </div>

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
      <Header title="Admin Dashboard" subtitle="Manage teachers, question bank and generated papers"/>


      <div className="grid grid-cols-2 gap-3 mb-5">
        <Stat label="Total Questions"   value={questions.length}  color="#3B82F6" />
        <Stat label="Subjects in Bank"  value={subjects.length}   color="#10B981" />
        <Stat label="Papers Generated"  value={papersGenCount}    color="#F59E0B" />
        <Stat label="Active Teachers"   value={teacherCount}      color="#8B5CF6" />
      </div>


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
