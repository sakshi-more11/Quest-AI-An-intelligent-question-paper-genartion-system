// src/components/UI.jsx
// Shared reusable UI primitives used across all pages

export function Badge({ children, color = "blue" }) {
  const map = {
    blue:   "bg-sky-500/10 text-sky-300 border-sky-400/30",
    gold:   "bg-amber-500/10 text-amber-300 border-amber-400/30",
    green:  "bg-emerald-500/10 text-emerald-300 border-emerald-400/30",
    red:    "bg-red-500/10 text-red-300 border-red-400/30",
    purple: "bg-violet-500/10 text-violet-300 border-violet-400/30",
    gray:   "bg-slate-500/10 text-slate-300 border-slate-400/30",
    teal:   "bg-teal-500/10 text-teal-300 border-teal-400/30",
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold border ${map[color]}`}>
      {children}
    </span>
  );
}

export function Stat({ label, value, color }) {
  return (
    <div className="rounded-3xl border p-5 text-center" style={{ background: "#111827", borderColor: "#1F2937" }}>
      <div className="text-2xl font-semibold tracking-tight" style={{ color: color || "#3B82F6" }}>{value}</div>
      <div className="text-xs mt-1.5" style={{ color: "#94A3B8" }}>{label}</div>
    </div>
  );
}

export function Header({ title, subtitle }) {
  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between mb-6">
      <div>
        <h1 className="text-3xl font-semibold" style={{ color: "#F8FAFC", letterSpacing: "-0.03em" }}>{title}</h1>
        {subtitle && <p className="text-sm mt-1" style={{ color: "#94A3B8" }}>{subtitle}</p>}
      </div>
      <div className="flex items-center gap-2 text-xs px-4 py-2 rounded-full" style={{ background: "#111827", border: "1px solid #1F2937", color: "#7DD3FC" }}>
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        Online
      </div>
    </div>
  );
}

export function TextInput({ label, value, onChange, placeholder, mono, required, hint, list }) {
  return (
    <div>
      {label && (
        <label className="block text-xs font-medium mb-2" style={{ color: "#94A3B8" }}>
          {label}{required && <span style={{ color: "#EF4444" }}> *</span>}
        </label>
      )}
      <input
        type="text"
        value={value}
        list={list}
        onChange={e => onChange(mono ? e.target.value.toUpperCase() : e.target.value)}
        placeholder={placeholder}
        className="w-full px-4 py-3 rounded-2xl text-sm outline-none transition-all"
        style={{
          background: "#0F172A",
          border: `1px solid ${value ? "#3B82F6" : "#1F2937"}`,
          color: "#E2E8F0",
          fontFamily: mono ? "monospace" : "inherit",
          letterSpacing: mono ? "0.05em" : "inherit",
        }}
      />
      {hint && <p className="text-xs mt-2" style={{ color: "#7C8EA3" }}>{hint}</p>}
    </div>
  );
}

export function SearchBar({ value, onChange, placeholder }) {
  return (
    <div className="relative mb-4">
      <input
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder || "Search…"}
        className="w-full pl-12 pr-4 py-3 rounded-2xl text-sm outline-none"
        style={{ background: "#0F172A", border: "1px solid #1F2937", color: "#E2E8F0" }}
      />
      <span className="absolute left-4 top-1/2 -translate-y-1/2" style={{ color: "#64748B", fontSize: 14 }}>🔍</span>
    </div>
  );
}

export function CoursePill({ subject, courseId, level }) {
  if (!subject && !courseId) return null;
  return (
    <div className="mt-3 px-3 py-2 rounded-2xl flex flex-wrap items-center gap-2" style={{ background: "#0E1729", border: "1px solid #1F2937" }}>
      <span className="w-2 h-2 rounded-full bg-sky-500 shrink-0" />
      <span className="text-xs" style={{ color: "#94A3B8" }}>
        {subject && <span style={{ color: "#F8FAFC" }}>{subject}</span>}
        {subject && courseId && <span> · </span>}
        {courseId && <span style={{ color: "#60A5FA", fontFamily: "monospace" }}>{courseId}</span>}
        {level && (subject || courseId) && <span style={{ color: "#7C8EA3" }}> · {level}</span>}
      </span>
    </div>
  );
}

export function Card({ children, className = "" }) {
  return (
    <div className={`rounded-3xl border p-6 ${className}`} style={{ background: "#0E1729", borderColor: "#1F2937", boxShadow: "0 14px 40px rgba(15,23,42,0.18)" }}>
      {children}
    </div>
  );
}

export function SectionTitle({ children }) {
  return (
    <h3 className="text-xs font-semibold mb-3" style={{ color: "#94A3B8", textTransform: "uppercase", letterSpacing: "0.12em" }}>
      {children}
    </h3>
  );
}

export function LevelToggle({ value, onChange }) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {['School', 'College'].map(l => {
        const active = value === l;
        return (
          <button key={l} onClick={() => onChange(l)}
            className="py-3 rounded-2xl text-sm font-semibold transition-all"
            style={{
              background: active ? "#2563EB" : "#0F172A",
              color: active ? "white" : "#94A3B8",
              border: `1px solid ${active ? "#2563EB" : "#1F2937"}`,
            }}>
            {l}
          </button>
        );
      })}
    </div>
  );
}

export function Flash({ message, type = "success" }) {
  if (!message) return null;
  const styles = {
    success: { bg: "#062F1C", border: "#0F766E", color: "#6EE7B7" },
    warn:    { bg: "#3F2507", border: "#92400E", color: "#FCD34D" },
    error:   { bg: "#2B181D", border: "#7F1D1D", color: "#FCA5A5" },
  };
  const s = styles[type];
  return (
    <div className="mb-4 px-4 py-3 rounded-3xl text-sm" style={{ background: s.bg, border: `1px solid ${s.border}`, color: s.color }}>
      {message}
    </div>
  );
}

export function PrimaryBtn({ children, onClick, disabled, loading, fullWidth }) {
  return (
    <button onClick={onClick} disabled={disabled || loading}
      className={`${fullWidth ? "w-full" : "inline-flex"} py-3 px-5 rounded-2xl font-semibold text-sm flex items-center justify-center gap-2 transition-all`}
      style={{
        background: (disabled && !loading) ? "#111827" : "#2563EB",
        color: (disabled && !loading) ? "#94A3B8" : "white",
        boxShadow: (disabled && !loading) ? "none" : "0 16px 30px rgba(37,99,235,0.25)",
        opacity: loading ? 0.92 : 1,
      }}>
      {loading && <span className="spin">⟳</span>}
      {children}
    </button>
  );
}

export function Empty({ message }) {
  return <div className="text-center py-12 text-sm" style={{ color: "#94A3B8" }}>{message}</div>;
}
