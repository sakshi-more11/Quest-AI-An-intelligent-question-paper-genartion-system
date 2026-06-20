const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000";

async function request(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Backend request failed.");
  return data;
}

export function parseSyllabus(payload) {
  return request("/api/parse-syllabus", payload);
}

export function generateQuestions(payload) {
  return request("/api/generate-questions", payload);
}

export function generatePaper(payload) {
  return request("/api/generate-paper", payload);
}
