// src/pages/LoginPage.jsx
import { useState } from "react";
import { USERS } from "../data/constants";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const attempt = () => {
    setLoading(true);
    setError("");
    setTimeout(() => {
      const u = USERS[username];
      if (u && u.password === password) {
        onLogin({ username, role: u.role, name: u.name });
      } else {
        setError("Invalid credentials. Try teacher1/teach123 or admin/admin123");
      }
      setLoading(false);
    }, 700);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "#08121F" }}>
      <div className="w-full max-w-4xl overflow-hidden rounded-[32px] border border-slate-800 bg-slate-950/90 shadow-[0_32px_70px_rgba(15,23,42,0.35)]">
        <div className="grid md:grid-cols-[1.2fr_1fr]">
          <div className="p-10 md:p-14" style={{ background: "linear-gradient(180deg, rgba(15,23,42,1), rgba(15,23,42,0.86))" }}>
            <div className="mb-8">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-3xl bg-slate-800 text-white text-lg font-semibold mb-4">
                SE
              </div>
              <h1 className="text-3xl font-semibold" style={{ color: "#F8FAFC" }}>SecureExam</h1>
              <p className="mt-3 max-w-sm text-sm leading-6" style={{ color: "#94A3B8" }}>
                A clean, modern exam management interface designed for teachers and admins. Sign in to manage syllabi, questions, templates and papers.
              </p>
            </div>
          </div>

          <div className="p-10 md:p-14">
            <div className="mb-8">
              <h2 className="text-2xl font-semibold" style={{ color: "#F8FAFC" }}>Welcome back</h2>
              <p className="mt-2 text-sm text-slate-400">Enter your credentials to continue to SecureExam.</p>
            </div>

            {error && (
              <div className="mb-6 rounded-3xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-200">
                {error}
              </div>
            )}

            <div className="space-y-5">
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-2">Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && attempt()}
                  className="w-full rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-sky-500"
                  placeholder="Enter username"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-400 mb-2">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && attempt()}
                  className="w-full rounded-2xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-sky-500"
                  placeholder="••••••••"
                />
              </div>

              <button
                onClick={attempt}
                disabled={loading}
                className="w-full rounded-2xl bg-sky-600 px-4 py-3 text-sm font-semibold text-white transition hover:bg-sky-500 disabled:cursor-not-allowed disabled:bg-slate-700"
              >
                {loading ? "Signing in..." : "Sign in"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
