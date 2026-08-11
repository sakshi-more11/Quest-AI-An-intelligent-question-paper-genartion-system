// src/App.jsx
// Root component: holds ALL global state, handles auth, routes between pages.

import { useState, useEffect } from "react";
import { SEED_QUESTIONS, SEED_LOGS, SEED_TEMPLATES, SEED_PAPERS } from "./data/constants";

import LoginPage      from "./pages/LoginPage";
import Dashboard      from "./pages/Dashboard";
import UploadSyllabus from "./pages/teacher/UploadSyllabus";
import UploadMaterial from "./pages/teacher/UploadMaterial";
import QuestionBank   from "./pages/QuestionBank";
import Templates      from "./pages/Templates";
import GeneratePaper  from "./pages/GeneratePaper";
import Papers         from "./pages/Papers";
import ActivityLogs   from "./pages/ActivityLogs";
import Sidebar        from "./components/Sidebar";
import TeacherManagement from "./pages/TeacherManagement";
import AccessDenied from "./components/AccessDenied";
import UploadCenter from "./pages/UploadCenter";

const dedupeByKey = (items, keyFn) => {
  const seen = new Map();
  items.forEach(item => {
    const key = keyFn(item);
    if (key && !seen.has(key)) seen.set(key, item);
  });
  return [...seen.values()];
};

export default function App() {
  // ── Auth ──────────────────────────────────────────────────────────────────
  const [user,      setUser]      = useState(null);
  const [activeTab, setActiveTab] = useState("dashboard");

  // ── Global state ──────────────────────────────────────────────────────────
  const [questions,  setQuestions]  = useState(SEED_QUESTIONS);
  const [logs,       setLogs]       = useState(SEED_LOGS);
  const [templates,  setTemplates]  = useState(SEED_TEMPLATES);
  const [papers,     setPapers]     = useState(SEED_PAPERS);
  const [syllabi,    setSyllabi]    = useState([]);  // parsed syllabi from upload

  // ── Load persisted app data on mount ─────────────────────────────────────
  useEffect(() => {
    try {
      const storedPapers = localStorage.getItem("securexam_papers");
      const storedSyllabi = localStorage.getItem("securexam_syllabi");
      const storedLogs = localStorage.getItem("securexam_logs");

      if (storedPapers) {
        const parsed = JSON.parse(storedPapers);
        if (Array.isArray(parsed) && parsed.length) setPapers(parsed);
      }
      if (storedSyllabi) {
        const parsed = JSON.parse(storedSyllabi);
        if (Array.isArray(parsed)) setSyllabi(dedupeByKey(parsed, s => `${s.subject_name || s.subject || ""}|${s.course_code || s.courseId || ""}|${s.filename || ""}`));
      }
      if (storedLogs) {
        const parsed = JSON.parse(storedLogs);
        if (Array.isArray(parsed)) setLogs(parsed);
      }
    } catch (e) {
      console.error("Failed to load persisted app data from localStorage", e);
    }
  }, []);

  // ── Save app data to localStorage whenever they change ───────────────────
  useEffect(() => {
    localStorage.setItem("securexam_papers", JSON.stringify(papers));
  }, [papers]);

  useEffect(() => {
    localStorage.setItem("securexam_syllabi", JSON.stringify(syllabi));
  }, [syllabi]);

  useEffect(() => {
    localStorage.setItem("securexam_logs", JSON.stringify(logs));
  }, [logs]);

  // ── Logging helper ────────────────────────────────────────────────────────
  const addLog = (action, details) => {
    if (!user) return;
    setLogs(prev => [{
      id: Date.now(),
      user: user.username,
      role: user.role === "admin" ? "Admin" : "Teacher",
      action, details,
      timestamp: new Date().toISOString(),
    }, ...prev]);
  };

  // ── Auth handlers ─────────────────────────────────────────────────────────
  const handleLogin = (u) => {
    try {
      const storedPapers = JSON.parse(localStorage.getItem("securexam_papers") || "[]");
      const storedSyllabi = JSON.parse(localStorage.getItem("securexam_syllabi") || "[]");
      const storedLogs = JSON.parse(localStorage.getItem("securexam_logs") || "[]");
      if (Array.isArray(storedPapers) && storedPapers.length) setPapers(storedPapers);
      if (Array.isArray(storedSyllabi) && storedSyllabi.length) setSyllabi(dedupeByKey(storedSyllabi, s => `${s.subject_name || s.subject || ""}|${s.course_code || s.courseId || ""}|${s.filename || ""}`));
      if (Array.isArray(storedLogs) && storedLogs.length) setLogs(storedLogs);
    } catch (e) {
      console.error("Failed to rehydrate app data on login", e);
    }

    setUser(u);
    setActiveTab("dashboard");
    setLogs(prev => [{
      id: Date.now(), user: u.username,
      role: u.role === "admin" ? "Admin" : "Teacher",
      action: "LOGIN", details: "Successful login",
      timestamp: new Date().toISOString(),
    }, ...prev]);
  };

  const handleLogout = () => { setUser(null); setActiveTab("dashboard"); };

  // ── Feature handlers ──────────────────────────────────────────────────────
  // Called when teacher confirms a parsed syllabus
  const handleSyllabusUploaded = ({ file, subject, courseId, level, units }) => {
    const syl = { id: Date.now(), subject, courseId, level, units, filename: file.name, uploadedBy: user.username, uploadedAt: new Date().toISOString() };
    setSyllabi(prev => dedupeByKey([...prev, syl], item => `${item.subject || item.subject_name || ""}|${item.courseId || item.course_code || ""}|${item.filename || ""}`));
    addLog("SYLLABUS_UPLOADED", `${file.name} — ${subject} ${courseId} — ${units.length} units extracted`);
  };

  // Called when AI generates questions from a syllabus
  const handleGenerateQBank = (newQs, syl) => {
    setQuestions(prev => [...prev, ...newQs]);
    addLog("QUESTION_BANK_GENERATED", `Generated ${newQs.length} questions — ${syl.subject} ${syl.courseId}`);
  };

  // Called when teacher uploads a template
  const handleTemplateUpload = (tpl) => {
    setTemplates(prev => [...prev, tpl]);
    addLog("TEMPLATE_UPLOADED", `${tpl.filename} uploaded`);
  };

  // Called when teacher deletes a template
  const handleTemplateDelete = (id) => {
    setTemplates(prev => prev.filter(t => t.id !== id));
  };

  // Called when teacher generates a paper (Set A/B/C)
  const handlePaperGenerated = (paperData) => {
    setPapers(prev => [...prev, paperData]);
    addLog("PAPER_GENERATED", `Set A, B, C — ${paperData.subject} ${paperData.courseId || ""} — ${paperData.level}`);
  };

  // Called when teacher deletes a generated paper
  const handlePaperDelete = (paperId) => {
    setPapers(prev => prev.filter(p => p.id !== paperId));
    addLog("PAPER_DELETED", `Paper deleted`);
  };

  // ── Route render ──────────────────────────────────────────────────────────
  const renderPage = () => {
    const isAdmin   = user.role === "admin";
    const isTeacher = user.role === "teacher";

    switch (activeTab) {
      case "dashboard":
        return (<Dashboard user={user} questions={questions} logs={logs} syllabi={syllabi} papers={papers}/>);

      case "upload-syllabus":
        if (isAdmin) return <Dashboard user={user} />;
        return <UploadSyllabus user={user} onUploadComplete={handleSyllabusUploaded} />;

      case "upload-material":

    if(isAdmin)
        return <Dashboard user={user}/>;


    return (
        <UploadMaterial
            user={user}
        />
    );  

      case "upload-center":
        if (isAdmin) return <AccessDenied />;
        return (<UploadCenter user={user}/>);  

      case "question-bank":
        return (
          <QuestionBank
            user={user}
            questions={questions}
            syllabi={syllabi.filter(s => s.uploadedBy === user.username || isAdmin)}
            onGenerateQBank={handleGenerateQBank}
          />
        );

      case "templates":
        if (isAdmin) return <AccessDenied />;
        return (
          <Templates
            user={user}
            templates={templates}
            onUpload={handleTemplateUpload}
            onDelete={handleTemplateDelete}
          />
        );

      case "generate-paper":
        if (isAdmin) return <Dashboard user={user} />;
        return (
          <GeneratePaper
            user={user}
            questions={questions}
            syllabi={syllabi.filter(s => s.uploadedBy === user.username)}
            templates={templates}
            onGenerated={handlePaperGenerated}
          />
        );

      case "papers":
        return <Papers user={user} papers={papers} onDelete={handlePaperDelete} />;

      case "history":
        if (!isAdmin) {
          return <AccessDenied />;
        }
        return <ActivityLogs
          user={user}
          logs={logs}
        />;

      case "teachers":

          if (!isAdmin) {
              return <AccessDenied />;
          }

        return <TeacherManagement user={user} />;
  

      default:
        return <Dashboard user={user} questions={questions} logs={logs} syllabi={syllabi} papers={papers} />;
    }
  };

  // ── Not logged in ─────────────────────────────────────────────────────────
  if (!user) return <LoginPage onLogin={handleLogin} />;

  // ── Main layout ───────────────────────────────────────────────────────────
  return (
    <div className="flex h-screen overflow-hidden" style={{ background: "#080F1A" }}>
      <Sidebar user={user} activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
      <main className="flex-1 overflow-y-auto p-6" style={{ background: "#0B1320" }}>
        <div className="max-w-6xl mx-auto px-2 sm:px-4 pb-6">
          {renderPage()}
        </div>
      </main>
    </div>
  );
}


