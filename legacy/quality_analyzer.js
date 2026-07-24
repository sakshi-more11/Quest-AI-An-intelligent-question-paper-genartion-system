const STOP_WORDS = new Set([
  "a", "an", "and", "are", "as", "at", "be", "by", "can", "for", "from",
  "has", "have", "how", "in", "into", "is", "it", "its", "of", "on", "or",
  "that", "the", "their", "then", "this", "to", "using", "was", "were",
  "what", "when", "where", "which", "why", "with", "your"
]);

function normalizeText(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function tokenize(value) {
  return normalizeText(value)
    .split(" ")
    .filter(token => token.length > 2 && !STOP_WORDS.has(token));
}

function unique(items) {
  return [...new Set(items.filter(Boolean))];
}

function cosine(a, b) {
  const keys = unique([...Object.keys(a), ...Object.keys(b)]);
  let dot = 0;
  let left = 0;
  let right = 0;

  for (const key of keys) {
    const av = a[key] || 0;
    const bv = b[key] || 0;
    dot += av * bv;
    left += av * av;
    right += bv * bv;
  }

  if (!left || !right) return 0;
  return dot / (Math.sqrt(left) * Math.sqrt(right));
}

function vectorize(text) {
  const counts = {};
  for (const token of tokenize(text)) {
    counts[token] = (counts[token] || 0) + 1;
  }
  return counts;
}

function extractTopics(syllabus) {
  const units = Array.isArray(syllabus?.units) ? syllabus.units : [];
  const topics = [];

  for (const unit of units) {
    if (unit?.name) topics.push(unit.name);
    if (Array.isArray(unit?.topics)) topics.push(...unit.topics);
  }

  return unique(topics.map(topic => String(topic).trim()).filter(topic => tokenize(topic).length > 0));
}

function similarity(a, b) {
  return cosine(vectorize(a), vectorize(b));
}

function detectDuplicates(questions, threshold = 0.72) {
  const duplicateIndexes = new Set();
  const duplicatePairs = [];

  for (let i = 0; i < questions.length; i += 1) {
    for (let j = i + 1; j < questions.length; j += 1) {
      const score = similarity(questions[i].text || questions[i].question, questions[j].text || questions[j].question);
      if (score >= threshold) {
        duplicateIndexes.add(j);
        duplicatePairs.push({ left: i, right: j, similarity: Number(score.toFixed(3)) });
      }
    }
  }

  return { duplicateIndexes, duplicatePairs };
}

function syllabusCoverage(questions, syllabus, threshold = 0.22) {
  const topics = extractTopics(syllabus);
  if (!topics.length) {
    return { topics: [], covered: [], score: 0, averageAlignment: 0 };
  }

  const covered = [];
  const questionTexts = questions.map(q => q.text || q.question || "");
  let alignmentSum = 0;

  for (const topic of topics) {
    const scores = questionTexts.map(text => similarity(text, topic));
    const best = Math.max(0, ...scores);
    alignmentSum += best;
    if (best >= threshold || questionTexts.some(text => normalizeText(text).includes(normalizeText(topic)))) {
      covered.push(topic);
    }
  }

  return {
    topics,
    covered,
    score: Number(((covered.length / topics.length) * 100).toFixed(2)),
    averageAlignment: Number((alignmentSum / topics.length).toFixed(3))
  };
}

function distributionScore(questions) {
  const units = questions.map(q => q.unit).filter(Boolean);
  const uniqueUnits = unique(units);
  if (!questions.length) return 0;
  if (uniqueUnits.length <= 1) return uniqueUnits.length ? 55 : 0;
  return Number(Math.min(100, (uniqueUnits.length / Math.max(1, questions.length / 3)) * 100).toFixed(2));
}

function analyzeQuestionBank(questions, syllabus) {
  const { duplicateIndexes, duplicatePairs } = detectDuplicates(questions);
  const uniqueQuestions = questions.filter((_, index) => !duplicateIndexes.has(index));
  const coverage = syllabusCoverage(uniqueQuestions, syllabus);
  const duplicatePreventionScore = Number(((uniqueQuestions.length / Math.max(1, questions.length)) * 100).toFixed(2));
  const unitDistributionScore = distributionScore(uniqueQuestions);
  const semanticAlignmentScore = Number(Math.min(100, (coverage.averageAlignment / 0.22) * 100).toFixed(2));
  const overallAccuracy = Number((
    duplicatePreventionScore * 0.35 +
    coverage.score * 0.35 +
    semanticAlignmentScore * 0.2 +
    unitDistributionScore * 0.1
  ).toFixed(2));

  return {
    questions: uniqueQuestions,
    removedDuplicates: questions.length - uniqueQuestions.length,
    duplicatePairs,
    accuracy: {
      duplicatePreventionScore,
      syllabusCoverageScore: coverage.score,
      semanticAlignmentScore,
      unitDistributionScore,
      overallAccuracy,
      topicsDetected: coverage.topics.length,
      topicsCovered: coverage.covered.length
    }
  };
}

function analyzePaperSets(sets, syllabus) {
  const all = [];
  for (const setName of ["A", "B", "C"]) {
    const set = sets?.[setName] || {};
    for (const section of ["sectionA", "sectionB", "sectionC"]) {
      for (const q of set[section] || []) {
        all.push({ ...q, text: q.question, set: setName, section });
      }
    }
  }
  return analyzeQuestionBank(all, syllabus);
}

module.exports = {
  analyzePaperSets,
  analyzeQuestionBank,
  detectDuplicates,
  extractTopics,
  normalizeText,
  syllabusCoverage
};
