const http = require("http");
const fs = require("fs");
const path = require("path");
const { URL } = require("url");
const { runAiAction } = require("./aiBridge");
const { analyzePaperSets, analyzeQuestionBank } = require("./aiQuality");
const { callOpenAIJson, DEFAULT_MODEL } = require("./openaiClient");

const envPath = path.join(__dirname, "..", ".env");
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const match = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.+?)\s*$/);
    if (match && !process.env[match[1]]) {
      process.env[match[1]] = match[2].replace(/^["']|["']$/g, "");
    }
  }
}

const PORT = Number(process.env.BACKEND_PORT || process.env.PORT || 5000);

function sendJson(res, status, payload) {
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": process.env.CORS_ORIGIN || "http://localhost:3000",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
  });
  res.end(JSON.stringify(payload));
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.on("data", chunk => {
      body += chunk;
      if (body.length > 25 * 1024 * 1024) {
        reject(new Error("Request body is too large."));
        req.destroy();
      }
    });
    req.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch {
        reject(new Error("Invalid JSON request body."));
      }
    });
    req.on("error", reject);
  });
}

function unitsToText(syllabus) {
  return (syllabus?.units || [])
    .map(unit => `${unit.name}: ${(unit.topics || []).join(", ")}`)
    .join("\n");
}

function buildSyllabusPrompt({ subject, courseId, level, fileName }) {
  return `You are the backend AI parser for Quest-AI.
Extract the real course syllabus from the uploaded file.

Course metadata:
- Subject: ${subject}
- Course ID: ${courseId}
- Level: ${level}
- File name: ${fileName || "uploaded syllabus"}

Return ONLY valid JSON:
{
  "units": [
    { "name": "Unit 1: exact unit/module/chapter name", "topics": ["topic 1", "topic 2", "topic 3"] }
  ],
  "totalUnits": number
}

Rules:
- Use the uploaded file content if available.
- Keep unit names concise and faithful to the syllabus.
- Extract at least 3 topics per unit when possible.`;
}

function buildQuestionPrompt({ syllabus, count = 18 }) {
  return `You are Quest-AI's Gemini generationquestion generation backend.
Generate exactly ${count} exam-quality questions from this syllabus.

Subject: ${syllabus.subject}
Course ID: ${syllabus.courseId}
Level: ${syllabus.level}
Syllabus:
${unitsToText(syllabus)}

Hard requirements:
- No repeated or near-repeated questions.
- Cover every syllabus unit and as many topics as possible.
- Questions must be application-oriented, analytical, numerical, design-based, or scenario-based where suitable.
- Avoid simple recall-only questions.
- Balance marks: 6 questions of 2 marks, 6 questions of 5 marks, 6 questions of 10 marks.
- Use Bloom levels: Understand, Apply, Analyze, Evaluate, Create.
- Map CO1-CO5.

Return ONLY valid JSON:
[
  {
    "text": "question text",
    "unit": "exact unit name from syllabus",
    "marks": 2,
    "difficulty": "Easy",
    "bloom": "Understand",
    "co": "CO1"
  }
]`;
}

function defaultTemplateStructure() {
  return {
    A: { description: "Short Answer", marksPerQuestion: 2, count: 5 },
    B: { description: "Medium Answer", marksPerQuestion: 5, count: 4 },
    C: { description: "Long Answer", marksPerQuestion: 10, count: 2 }
  };
}

function parseTemplateStructure(templateContent) {
  if (!templateContent) return defaultTemplateStructure();
  const lines = templateContent.split(/\r?\n/);
  const sections = {};
  let current = null;

  for (const line of lines) {
    const trimmed = line.trim();
    const sectionMatch = trimmed.match(/^SECTION\s+([A-Z])\s*:\s*(.+?)\s*\((\d+)\s*marks?\s*each\)/i);
    if (sectionMatch) {
      const [, letter, description, marks] = sectionMatch;
      current = letter.toUpperCase();
      sections[current] = { description, marksPerQuestion: Number(marks), count: 0 };
      continue;
    }
    if (current && /^\d+\.\s/.test(trimmed)) sections[current].count += 1;
  }

  return Object.keys(sections).length ? sections : defaultTemplateStructure();
}

function buildPaperPrompt({ subject, courseId, level, questions, syllabus, template }) {
  const structure = parseTemplateStructure(template?.content);
  const structureText = Object.entries(structure)
    .map(([letter, section]) =>
      `Section ${letter}: ${section.count} questions, ${section.marksPerQuestion} marks each, ${section.description}`
    )
    .join("\n");

  return `You are Quest-AI's Gemini generationpaper generation backend.
Create exactly 3 distinct question paper sets: A, B, and C.

Subject: ${subject}
Course ID: ${courseId || "N/A"}
Level: ${level}
Template name: ${template?.name || "Default"}
Template structure:
${structureText}

Syllabus:
${unitsToText(syllabus)}

Available question bank:
${JSON.stringify(questions.slice(0, 80))}

Hard requirements:
- Follow the user's template section structure exactly.
- Generate Set A, Set B, Set C.
- Do not repeat or paraphrase the same question within or across sets.
- Cover the syllabus broadly across the three sets.
- Prefer questions from the bank, but rewrite/improve them when needed for quality and uniqueness.
- Preserve marks per section.
- Include unit and Bloom level for every question.

Return ONLY valid JSON:
{
  "A": {
    "sectionA": [{"question": "text", "marks": 2, "unit": "Unit name", "bloom": "Understand"}],
    "sectionB": [{"question": "text", "marks": 5, "unit": "Unit name", "bloom": "Apply"}],
    "sectionC": [{"question": "text", "marks": 10, "unit": "Unit name", "bloom": "Evaluate"}]
  },
  "B": { "sectionA": [], "sectionB": [], "sectionC": [] },
  "C": { "sectionA": [], "sectionB": [], "sectionC": [] }
}`;
}

function fallbackQuestions(syllabus, count = 18) {
  const units = syllabus.units?.length ? syllabus.units : [{ name: `Unit 1: ${syllabus.subject}`, topics: ["Core concepts"] }];
  const marks = [2, 5, 10];
  const blooms = ["Understand", "Apply", "Analyze", "Evaluate", "Create"];
  return Array.from({ length: count }, (_, index) => {
    const unit = units[index % units.length];
    const topic = unit.topics?.[index % Math.max(1, unit.topics.length)] || unit.name;
    return {
      text: `Analyze a practical scenario involving ${topic} from ${unit.name}. Explain the method, justify the steps, and mention one limitation.`,
      unit: unit.name,
      marks: marks[Math.floor(index / 6)] || marks[index % marks.length],
      difficulty: index < 6 ? "Easy" : index < 12 ? "Medium" : "Hard",
      bloom: blooms[index % blooms.length],
      co: `CO${(index % 5) + 1}`
    };
  });
}

function fallbackSets(payload) {
  const units = payload.syllabus?.units?.length ? payload.syllabus.units : [{ name: payload.subject, topics: ["core concepts"] }];
  const makeQuestion = (set, section, index, marks) => {
    const unit = units[(index + set.charCodeAt(0) + section.length) % units.length];
    const topic = unit.topics?.[index % Math.max(1, unit.topics.length)] || unit.name;
    return {
      question: `Set ${set}: Apply ${topic} to a realistic ${payload.subject} problem and justify your answer.`,
      marks,
      unit: unit.name,
      bloom: marks === 2 ? "Understand" : marks === 5 ? "Analyze" : "Evaluate"
    };
  };

  const build = set => ({
    sectionA: Array.from({ length: 5 }, (_, i) => makeQuestion(set, "sectionA", i, 2)),
    sectionB: Array.from({ length: 4 }, (_, i) => makeQuestion(set, "sectionB", i, 5)),
    sectionC: Array.from({ length: 2 }, (_, i) => makeQuestion(set, "sectionC", i, 10))
  });

  return { A: build("A"), B: build("B"), C: build("C") };
}

async function handleParseSyllabus(req, res) {
  const payload = await readJson(req);

  try {
    console.log("===== PARSE SYLLABUS START =====");

    const parsed = await runAiAction("parse_syllabus", payload);

    console.log("AI Bridge Success");

    return sendJson(res, 200, parsed);

  } catch (pipelineError) {

    console.error("AI Bridge Failed:");
    console.error(pipelineError);

    try {

      const prompt = buildSyllabusPrompt(payload);

      const { json, model } = await callOpenAIJson({
        prompt,
        file: payload.file,
        maxOutputTokens: 2500
      });

      console.log("OpenAI Success");

      return sendJson(res, 200, {
        ...json,
        model,
        pipelineWarning: pipelineError.message
      });

    } catch (openaiError) {

      console.error("OPENAI ERROR");
      console.error(openaiError);
      console.error(openaiError.stack);

      return sendJson(res, 500, {
        error: openaiError.message,
        stack: openaiError.stack
      });

    }
  }
}

async function handleGenerateQuestions(req, res) {
  const payload = await readJson(req);
  const syllabus = payload.syllabus || {};
  let questions;
  let model = DEFAULT_MODEL;
  let fallback = false;

  try {
    const result = await runAiAction("generate_questions", payload);
    return sendJson(res, 200, {
      questions: result.questions || [],
      quality: result.quality || {},
      model: result.model || model,
      fallback: Boolean(result.fallback),
      evaluation: result.evaluation || null
    });
  } catch (error) {
    try {
      const result = await callOpenAIJson({
        prompt: buildQuestionPrompt({ syllabus, count: payload.count || 18 }),
        maxOutputTokens: 6500
      });
      questions = Array.isArray(result.json) ? result.json : result.json.questions;
      model = result.model;
    } catch {
      fallback = true;
      questions = fallbackQuestions(syllabus, payload.count || 18);
    }
  }

  const quality = analyzeQuestionBank(questions || [], syllabus);
  sendJson(res, 200, {
    questions: quality.questions,
    quality: {
      ...quality.accuracy,
      removedDuplicates: quality.removedDuplicates,
      duplicatePairs: quality.duplicatePairs
    },
    model,
    fallback
  });
}

async function handleGeneratePaper(req, res) {
  const payload = await readJson(req);
  let sets;
  let model = DEFAULT_MODEL;
  let fallback = false;

  try {
    const result = await runAiAction("generate_paper", payload);
    return sendJson(res, 200, {
      sets: result.sets,
      quality: result.quality || {},
      removedDuplicates: result.removedDuplicates || 0,
      duplicatePairs: result.duplicatePairs || [],
      model: result.model || model,
      fallback: Boolean(result.fallback)
    });
  } catch (error) {
    try {
      const result = await callOpenAIJson({
        prompt: buildPaperPrompt(payload),
        maxOutputTokens: 9000
      });
      sets = result.json;
      model = result.model;
    } catch {
      fallback = true;
      sets = fallbackSets(payload);
    }
  }

  const quality = analyzePaperSets(sets, payload.syllabus || {});
  sendJson(res, 200, {
    sets,
    quality: {
      ...quality.accuracy,
      removedDuplicates: quality.removedDuplicates,
      duplicatePairs: quality.duplicatePairs
    },
    model,
    fallback
  });
}

async function handleExport(req, res, action) {
  const payload = await readJson(req);
  const result = await runAiAction(action, payload);
  sendJson(res, 200, result);
}

const server = http.createServer(async (req, res) => {
  console.log(req.method, req.url);
  if (req.method === "OPTIONS") return sendJson(res, 204, {});

  const url = new URL(req.url, `http://${req.headers.host}`);
  try {
    if (req.method === "GET" && url.pathname === "/api/health") {
      return sendJson(res, 200, { ok: true, model: DEFAULT_MODEL });
    }
    if (req.method === "POST" && url.pathname === "/api/parse-syllabus") {
      return handleParseSyllabus(req, res);
    }
    if (req.method === "POST" && url.pathname === "/api/generate-questions") {
      return handleGenerateQuestions(req, res);
    }
    if (req.method === "POST" && url.pathname === "/api/generate-paper") {
      return handleGeneratePaper(req, res);
    }
    if (req.method === "POST" && url.pathname === "/api/export-docx") {
      return handleExport(req, res, "export_docx");
    }
    if (req.method === "POST" && url.pathname === "/api/export-pdf") {
      return handleExport(req, res, "export_pdf");
    }
    return sendJson(res, 404, { error: "Not found" });
  } catch (error) {
    return sendJson(res, 500, { error: error.message || "Backend error" });
  }
});

server.listen(PORT, () => {
  console.log(`Quest-AI backend running on http://localhost:${PORT}`);
  console.log(`OpenAI model: ${DEFAULT_MODEL}`);
});
