// src/pages/Templates.jsx
// Teacher uploads .docx templates with placeholders.
// Admin sees this page as read-only (no upload/delete).

import { useState } from "react";
import { Header, Card, Flash, PrimaryBtn } from "../components/UI";
import mammoth from "mammoth";

const PLACEHOLDERS = [
  "{{subject}}", "{{courseId}}", "{{level}}", "{{date}}",
  "{{duration}}", "{{totalMarks}}", "{{examiner}}"
];

// Convert file to text content (supports .txt and .docx)
const fileToText = (file) => {
  return new Promise((resolve, reject) => {
    const fileName = file.name.toLowerCase();

    if (fileName.endsWith('.txt')) {
      // Handle plain text files
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsText(file);
    } else if (fileName.endsWith('.docx')) {
      // Handle .docx files using mammoth
      const reader = new FileReader();
      reader.onload = (event) => {
        const arrayBuffer = event.target.result;
        mammoth.extractRawText({ arrayBuffer })
          .then((result) => {
            resolve(result.value);
          })
          .catch((error) => {
            reject(new Error(`Failed to parse .docx file: ${error.message}`));
          });
      };
      reader.onerror = reject;
      reader.readAsArrayBuffer(file);
    } else {
      reject(new Error('Unsupported file format. Please upload .txt or .docx files.'));
    }
  });
};

export default function Templates({ user, templates, onUpload, onDelete }) {
  const isAdmin = user.role === "admin";
  const [file,      setFile]      = useState(null);
  const [name,      setName]      = useState("");
  const [uploading, setUploading] = useState(false);
  const [flash,     setFlash]     = useState("");
  const [templateText, setTemplateText] = useState("");
  const [useTextArea, setUseTextArea] = useState(false);

  const handle = async () => {
    if (!name) return;
    if (!useTextArea && !file) return;
    if (useTextArea && !templateText.trim()) return;

    setUploading(true);
    try {
      let content;
      if (useTextArea) {
        content = templateText;
      } else {
        content = await fileToText(file);
      }

      onUpload({
        id: Date.now(), name, filename: useTextArea ? `${name}.txt` : file.name,
        uploadedAt: new Date().toISOString(),
        placeholders: PLACEHOLDERS,
        uploadedBy: user.username,
        content, // Store the text content
      });
      setFile(null); setName(""); setTemplateText(""); setUploading(false);
      setFlash("Template uploaded and activated successfully!");
      setTimeout(() => setFlash(""), 3000);
    } catch (e) {
      setFlash("Failed to upload template.");
      setUploading(false);
    }
  };

  return (
    <div>
      <Header
        title="Templates"
        subtitle={isAdmin ? "View available question paper templates (read-only)" : "Upload and manage question paper templates"}
      />

      <Flash message={flash} type="success" />

      {/* Upload panel — teacher only */}
      {!isAdmin && (
        <Card className="mb-4">
          <h3 className="text-sm font-semibold mb-4" style={{ color: "#E2E8F0" }}>Upload New Template</h3>

          {/* Input method toggle */}
          <div className="flex gap-3 mb-4">
            <button onClick={() => setUseTextArea(false)}
              className="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all"
              style={{
                background: !useTextArea ? "#3B82F6" : "#141B30",
                color: !useTextArea ? "white" : "#64748B",
                border: `1px solid ${!useTextArea ? "#3B82F6" : "#1E2D4A"}`
              }}>
              📁 Upload File
            </button>
            <button onClick={() => setUseTextArea(true)}
              className="flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-all"
              style={{
                background: useTextArea ? "#3B82F6" : "#141B30",
                color: useTextArea ? "white" : "#64748B",
                border: `1px solid ${useTextArea ? "#3B82F6" : "#1E2D4A"}`
              }}>
              ✏️ Write Template
            </button>
          </div>

          <div className="space-y-3">
            <input type="text" value={name} onChange={e => setName(e.target.value)}
              placeholder="Template name (e.g. College Final Exam — 50 Marks)"
              className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
              style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#E2E8F0" }} />

            {useTextArea ? (
              <textarea value={templateText} onChange={e => setTemplateText(e.target.value)}
                placeholder="Paste or write your template here (or upload .docx/.txt file)...

Example:
{{subject}} Examination Paper

Course: {{courseId}}
Date: {{date}}

SECTION A: Short Answer (2 marks each)
1. Question 1
2. Question 2
3. Question 3

SECTION B: Medium Answer (5 marks each)
1. Question 1
2. Question 2"
                rows={12}
                className="w-full px-3 py-2.5 rounded-lg text-sm outline-none font-mono"
                style={{ background: "#141B30", border: "1px solid #1E2D4A", color: "#E2E8F0", resize: "vertical" }} />
            ) : (
              <div className="border-2 border-dashed rounded-xl p-6 text-center cursor-pointer"
                style={{ borderColor: file ? "#3B82F6" : "#1E2D4A", background: "#141B30" }}
                onClick={() => document.getElementById("tplInput").click()}>
                <input id="tplInput" type="file" accept=".docx,.txt" className="hidden"
                  onChange={e => setFile(e.target.files[0])} />
                <div className="text-2xl mb-1">{file ? "📄" : "📋"}</div>
                <p className="text-sm" style={{ color: file ? "#3B82F6" : "#64748B" }}>
                  {file ? file.name : "Click to upload .docx or .txt template"}
                </p>
                {!file && <p className="text-xs mt-0.5" style={{ color: "#475569" }}>Microsoft Word .docx or plain text .txt files</p>}
              </div>
            )}

            {/* Placeholder reference */}
            <div className="rounded-lg p-3" style={{ background: "#141B30", border: "1px solid #1E2D4A" }}>
              <p className="text-xs font-medium mb-2" style={{ color: "#64748B" }}>
                Available placeholders (use in your .docx or .txt file):
              </p>
              <div className="flex flex-wrap gap-1.5">
                {PLACEHOLDERS.map(p => (
                  <span key={p} className="text-xs px-2 py-0.5 rounded font-mono"
                    style={{ background: "#0A1628", color: "#8B5CF6", border: "1px solid #2D1D5A" }}>{p}</span>
                ))}
              </div>
              <p className="text-xs mt-2" style={{ color: "#475569" }}>
                For question sections, use numbered questions like "1. Question 1" under each SECTION header
              </p>
            </div>

            <PrimaryBtn onClick={handle}
              disabled={!name || (!useTextArea && !file) || (useTextArea && !templateText.trim())}
              loading={uploading} fullWidth>
              {useTextArea ? "Save Template" : "Upload Template"}
            </PrimaryBtn>
          </div>
        </Card>
      )}

      {/* Template list */}
      <div className="space-y-3">
        {templates.length === 0 ? (
          <div className="text-center py-12" style={{ color: "#475569" }}>
            {isAdmin ? "No templates available." : "No templates uploaded yet."}
          </div>
        ) : templates.map(tpl => (
          <Card key={tpl.id}>
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-sm font-semibold" style={{ color: "#E2E8F0" }}>{tpl.name}</p>
                <p className="text-xs mt-0.5" style={{ color: "#64748B" }}>
                  {tpl.filename} · {new Date(tpl.uploadedAt).toLocaleDateString()}
                  {tpl.uploadedBy && ` · by ${tpl.uploadedBy}`}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs px-2 py-0.5 rounded border"
                  style={{ background: "#0B2818", borderColor: "#065F46", color: "#6EE7B7" }}>Active</span>
                {!isAdmin && (
                  <button onClick={() => onDelete(tpl.id)}
                    className="text-xs px-2 py-1 rounded"
                    style={{ background: "#2D1B1B", color: "#EF4444", border: "1px solid #7F1D1D" }}>
                    Delete
                  </button>
                )}
              </div>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {tpl.placeholders.map(p => (
                <span key={p} className="text-xs px-2 py-0.5 rounded font-mono"
                  style={{ background: "#141B30", color: "#8B5CF6", border: "1px solid #2D1D5A" }}>{p}</span>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
