const OPENAI_API_URL = "https://api.openai.com/v1/responses";
const DEFAULT_MODEL = process.env.OPENAI_MODEL || "gpt-5";

function extractOutputText(response) {
  if (response.output_text) return response.output_text;

  const chunks = [];
  for (const item of response.output || []) {
    for (const content of item.content || []) {
      if (content.type === "output_text" && content.text) chunks.push(content.text);
      if (content.text && typeof content.text === "string") chunks.push(content.text);
    }
  }
  return chunks.join("\n");
}

function parseJsonText(text) {
  const cleaned = String(text || "")
    .replace(/```json/g, "")
    .replace(/```/g, "")
    .trim();

  try {
    return JSON.parse(cleaned);
  } catch {
    const firstObject = cleaned.indexOf("{");
    const firstArray = cleaned.indexOf("[");
    const start = firstArray >= 0 && (firstArray < firstObject || firstObject < 0) ? firstArray : firstObject;
    const end = cleaned.lastIndexOf(cleaned[start] === "[" ? "]" : "}");
    if (start >= 0 && end > start) return JSON.parse(cleaned.slice(start, end + 1));
    throw new Error("AI response was not valid JSON.");
  }
}

async function callOpenAI({ prompt, file, maxOutputTokens = 5000 }) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    throw new Error("OPENAI_API_KEY is not set on the backend.");
  }

  const content = [{ type: "input_text", text: prompt }];
  if (file?.base64 && file?.mediaType) {
    content.unshift({
      type: "input_file",
      filename: file.name || "uploaded-file",
      file_data: `data:${file.mediaType};base64,${file.base64}`
    });
  }

  const body = {
    model: DEFAULT_MODEL,
    input: [{ role: "user", content }],
    max_output_tokens: maxOutputTokens,
    reasoning: { effort: "medium" }
  };

  const response = await fetch(OPENAI_API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify(body)
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data?.error?.message || `OpenAI request failed with HTTP ${response.status}`;
    throw new Error(message);
  }

  return {
    raw: data,
    text: extractOutputText(data),
    model: data.model || DEFAULT_MODEL
  };
}

async function callOpenAIJson(options) {
  const result = await callOpenAI(options);
  return { json: parseJsonText(result.text), text: result.text, model: result.model };
}

module.exports = {
  callOpenAI,
  callOpenAIJson,
  DEFAULT_MODEL,
  parseJsonText
};
