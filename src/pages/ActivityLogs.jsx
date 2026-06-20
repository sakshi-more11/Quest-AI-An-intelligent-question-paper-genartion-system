// src/pages/ActivityLogs.jsx
// Full audit trail. Admin sees all logs. Teachers see only their own.

import { useState, useMemo, useEffect } from "react";
import { Header, Badge, SearchBar, Stat, Empty } from "../components/UI";

const ACTION_COLOR = {
  LOGIN: "blue", QUESTION_BANK_GENERATED: "green", PAPER_GENERATED: "gold",
  TEMPLATE_UPLOADED: "purple", PAPER_DOWNLOADED: "gray", SYLLABUS_UPLOADED: "teal",
};
const ACTION_ICON = {
  LOGIN: "🔐", QUESTION_BANK_GENERATED: "⚡", PAPER_GENERATED: "📝",
  TEMPLATE_UPLOADED: "📋", PAPER_DOWNLOADED: "⬇", SYLLABUS_UPLOADED: "↑",
};

export default function ActivityLogs({ user, logs }) {
  const isAdmin = user.role === "admin";
  // Admin sees all; teacher sees only their own
  const visibleLogs = isAdmin ? logs : logs.filter(l => l.user === user.username);

  const [search,  setSearch]  = useState("");
  const [fRole,   setFRole]   = useState("");
  const [fAction, setFAction] = useState("");
  const [page,    setPage]    = useState(0);
  const PAGE = 12;

  const actions = useMemo(() => [...new Set(visibleLogs.map(l => l.action))], [visibleLogs]);

  const filtered = useMemo(() => visibleLogs.filter(l =>
    (!fRole   || l.role === fRole) &&
    (!fAction || l.action === fAction) &&
    (!search  || l.user.toLowerCase().includes(search.toLowerCase()) ||
      l.details.toLowerCase().includes(search.toLowerCase()))
  ), [visibleLogs, fRole, fAction, search]);

  const totalPages = Math.ceil(filtered.length / PAGE);
  const paged = filtered.slice(page * PAGE, (page + 1) * PAGE);
  useEffect(() => setPage(0), [fRole, fAction, search]);

  return (
    <div>
      <Header
        title="Activity Logs"
        subtitle={isAdmin ? "Complete audit trail of all system actions" : "Your personal activity history"}
      />

      <div className="grid grid-cols-3 gap-3 mb-5">
        <Stat label="Total Events"    value={visibleLogs.length}                                  color="#3B82F6" />
        <Stat label="Admin Actions"   value={visibleLogs.filter(l => l.role === "Admin").length}  color="#F59E0B" />
        <Stat label="Teacher Actions" value={visibleLogs.filter(l => l.role === "Teacher").length} color="#3B82F6" />
      </div>

      <SearchBar value={search} onChange={setSearch} placeholder="Search by user or action details…" />

      <div className="grid grid-cols-2 gap-3 mb-4">
        {isAdmin && (
          <select value={fRole} onChange={e => setFRole(e.target.value)}
            className="px-3 py-2 rounded-lg text-sm outline-none"
            style={{ background: "#0F1629", border: "1px solid #1E2D4A", color: "#E2E8F0" }}>
            <option value="">All Roles</option>
            <option>Admin</option><option>Teacher</option>
          </select>
        )}
        <select value={fAction} onChange={e => setFAction(e.target.value)}
          className="px-3 py-2 rounded-lg text-sm outline-none"
          style={{ background: "#0F1629", border: "1px solid #1E2D4A", color: "#E2E8F0" }}>
          <option value="">All Actions</option>
          {actions.map(a => <option key={a}>{a}</option>)}
        </select>
      </div>

      <p className="text-xs mb-3" style={{ color: "#475569" }}>{filtered.length} entries</p>

      <div className="rounded-xl border overflow-hidden" style={{ background: "#0F1629", borderColor: "#1E2D4A" }}>
        <table className="w-full text-xs">
          <thead>
            <tr style={{ background: "#141B30" }}>
              {["User", "Role", "Action", "Details", "Timestamp"].map(h => (
                <th key={h} className="px-3 py-3 text-left font-semibold" style={{ color: "#64748B" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paged.map(log => (
              <tr key={log.id} style={{ borderTop: "1px solid #141B30" }}>
                <td className="px-3 py-3">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0"
                      style={{ background: log.role === "Admin" ? "#2D1F00" : "#0F1D3A", color: log.role === "Admin" ? "#F59E0B" : "#3B82F6" }}>
                      {log.user[0].toUpperCase()}
                    </div>
                    <span style={{ color: "#E2E8F0" }}>{log.user}</span>
                  </div>
                </td>
                <td className="px-3 py-3">
                  <Badge color={log.role === "Admin" ? "gold" : "blue"}>{log.role}</Badge>
                </td>
                <td className="px-3 py-3">
                  <div className="flex items-center gap-1.5">
                    <span>{ACTION_ICON[log.action] || "•"}</span>
                    <Badge color={ACTION_COLOR[log.action] || "gray"}>
                      {log.action.replace(/_/g, " ")}
                    </Badge>
                  </div>
                </td>
                <td className="px-3 py-3 max-w-xs">
                  <span className="block truncate" style={{ color: "#94A3B8" }}>{log.details}</span>
                </td>
                <td className="px-3 py-3 whitespace-nowrap" style={{ color: "#64748B" }}>
                  {new Date(log.timestamp).toLocaleString()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && <Empty message="No log entries match your search." />}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-3">
          <span className="text-xs" style={{ color: "#475569" }}>
            {page * PAGE + 1}–{Math.min((page + 1) * PAGE, filtered.length)} of {filtered.length}
          </span>
          <div className="flex gap-2">
            <button disabled={page === 0} onClick={() => setPage(p => p - 1)}
              className="px-3 py-1.5 rounded text-xs disabled:opacity-30"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#94A3B8" }}>← Prev</button>
            <button disabled={page >= totalPages - 1} onClick={() => setPage(p => p + 1)}
              className="px-3 py-1.5 rounded text-xs disabled:opacity-30"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#94A3B8" }}>Next →</button>
          </div>
        </div>
      )}
    </div>
  );
}
