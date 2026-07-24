// src/components/Sidebar.jsx
// Navigation sidebar — teacher gets full feature nav, admin gets read-only nav

export default function Sidebar({ user, activeTab, setActiveTab, onLogout }) {
  const teacherNav = [
    { id:"dashboard", label:"Dashboard📊"},
    { id:"upload-syllabus", label:"Upload Syllabus📚"},
    { id:"upload-center", label:"Upload Materials 📂"},
    { id:"question-bank", label:"Question Bank🗂️"},
    { id:"generate-paper", label:"Generate Paper📝"},
    { id:"papers", label:"Generated Papers📄"},

  ];

  const adminNav = [
    { id:"dashboard", label:"Dashboard📊"},
    { id:"teachers", label:"Teachers Management👨‍🏫"},
    { id:"question-bank", label:"Question Bank🗂️"},
    { id:"papers", label:"Generated Papers📄"},
    { id:"history", label:"Activity Logs📜"}
  ];

  const nav = user.role === "admin" ? adminNav : teacherNav;
  const isAdmin = user.role === "admin";

  return (
    <aside className="flex flex-col h-full shrink-0" style={{ width: 240, background: "#0D1726", borderRight: "1px solid rgba(148,163,184,0.12)" }}>
      <div className="px-5 py-6 border-b" style={{ borderColor: "rgba(148,163,184,0.1)" }}>
        <div className="inline-flex items-center gap-3 rounded-3xl px-4 py-3 bg-slate-950/80 border border-slate-800">
          <div className="w-11 h-11 rounded-3xl flex items-center justify-center text-lg font-bold text-white" style={{ background: "#2563EB" }}>
            SE
          </div>
          <div>
            <div className="text-sm font-semibold" style={{ color: "#F8FAFC" }}>SecureExam</div>
            <div className="text-[11px] uppercase tracking-[0.18em]" style={{ color: "#94A3B8" }}>Question Paper System</div>
          </div>
        </div>
      </div>

      <div className="mx-5 my-4 rounded-3xl p-4 bg-slate-950/70 border border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold text-white" style={{ background: isAdmin ? "#F59E0B" : "#2563EB" }}>
            {(user?.name || user?.email || "U")[0].toUpperCase()}
          </div>
          <div className="min-w-0">
            <div className="text-xs font-semibold truncate" style={{ color: "#F8FAFC" }}>{user?.name ? user.name : user.email}</div>
            <div className="text-[11px] text-slate-400 truncate">
              {isAdmin ? "Admin — Full Access" : "Teacher — Full Access"}
            </div>
          </div>
        </div>
      </div>

      <nav className="flex-1 px-3 py-2 space-y-2 overflow-y-auto">
        {nav.map(item => {
          const active = activeTab === item.id;
          return (
            <button key={item.id} onClick={() => setActiveTab(item.id)}
              className="w-full text-left flex items-center gap-3 px-4 py-3 rounded-3xl transition"
              style={{
                background: active ? "rgba(37,99,235,0.14)" : "transparent",
                color: active ? "#F8FAFC" : "#CBD5E1",
                border: active ? "1px solid rgba(37,99,235,0.24)" : "1px solid transparent",
              }}>
              <span className="text-base leading-none">{item.icon}</span>
              <span className="text-sm font-medium truncate">{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="px-5 py-4 border-t" style={{ borderColor: "rgba(148,163,184,0.1)" }}>
        <button onClick={onLogout}
          className="w-full flex items-center justify-center gap-2 px-4 py-3 rounded-3xl text-sm font-semibold transition"
          style={{ background: "#0F172A", color: "#F8FAFC", border: "1px solid #1E293B" }}>
          ⇤ Sign Out
        </button>
      </div>
    </aside>
  );
}
