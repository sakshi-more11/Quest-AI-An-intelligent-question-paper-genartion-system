// ─── AUTH ──────────────────────────────────────────────────────────────────────
export const USERS = {
  teacher1: { password: "teach123", role: "teacher", name: "Prof. Priya Sharma" },
  teacher2: { password: "teach456", role: "teacher", name: "Prof. Arjun Verma" },
  admin:    { password: "admin123", role: "admin",   name: "Dr. Raj Mehta" },
};

// ─── ENUMS ─────────────────────────────────────────────────────────────────────
export const BLOOM_LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"];
export const DIFFICULTY   = ["Easy", "Medium", "Hard"];
export const LEVELS       = ["School", "College"];
export const BLOOM_COLORS = ["#3B82F6","#8B5CF6","#10B981","#F59E0B","#EF4444","#EC4899"];

export const CO_OPTIONS  = ["CO1","CO2","CO3","CO4","CO5"];

// ─── SEED DATA ─────────────────────────────────────────────────────────────────
export const SEED_QUESTIONS = [

{
id:1,
text:"Explain the architecture of a Feed Forward Neural Network.",
subject:"Machine Learning",
courseId:"AI601",
unit:"Neural Networks",
marks:5,
difficulty:"Easy",
bloom:"Understand",
co:"CO1",
level:"College",
createdBy:"teacher1",
timestamp:"2025-01-15"
},

{
id:2,
text:"Train a Logistic Regression model and explain the cost function.",
subject:"Machine Learning",
courseId:"AI601",
unit:"Regression",
marks:10,
difficulty:"Medium",
bloom:"Apply",
co:"CO2",
level:"College",
createdBy:"teacher1",
timestamp:"2025-01-15"
},

{
id:3,
text:"Compare Decision Tree and Random Forest algorithms.",
subject:"Machine Learning",
courseId:"AI601",
unit:"Tree Models",
marks:10,
difficulty:"Hard",
bloom:"Evaluate",
co:"CO3",
level:"College",
createdBy:"teacher1",
timestamp:"2025-01-15"
},

{
id:4,
text:"Explain Merge Sort with suitable example.",
subject:"Data Structures & Algorithms",
courseId:"CS501",
unit:"Sorting",
marks:5,
difficulty:"Easy",
bloom:"Remember",
co:"CO1",
level:"College",
createdBy:"teacher2",
timestamp:"2025-01-16"
},

{
id:5,
text:"Write DFS and BFS algorithms with complexity analysis.",
subject:"Data Structures & Algorithms",
courseId:"CS501",
unit:"Graphs",
marks:10,
difficulty:"Medium",
bloom:"Apply",
co:"CO2",
level:"College",
createdBy:"teacher2",
timestamp:"2025-01-16"
},

{
id:6,
text:"Design an AVL Tree insertion algorithm.",
subject:"Data Structures & Algorithms",
courseId:"CS501",
unit:"Trees",
marks:10,
difficulty:"Hard",
bloom:"Create",
co:"CO3",
level:"College",
createdBy:"teacher2",
timestamp:"2025-01-16"
},

{
id:7,
text:"Explain the Agile Software Development Life Cycle.",
subject:"Software Engineering",
courseId:"SE401",
unit:"SDLC",
marks:5,
difficulty:"Easy",
bloom:"Understand",
co:"CO1",
level:"College",
createdBy:"teacher1",
timestamp:"2025-01-17"
},

{
id:8,
text:"Compare Scrum and Waterfall models.",
subject:"Software Engineering",
courseId:"SE401",
unit:"Development Models",
marks:7,
difficulty:"Medium",
bloom:"Analyze",
co:"CO2",
level:"College",
createdBy:"teacher1",
timestamp:"2025-01-17"
},

{
id:9,
text:"Explain normalization up to BCNF with examples.",
subject:"Database Management System",
courseId:"DB301",
unit:"Normalization",
marks:5,
difficulty:"Easy",
bloom:"Understand",
co:"CO1",
level:"College",
createdBy:"teacher2",
timestamp:"2025-01-18"
},

{
id:10,
text:"Write SQL queries for JOIN, GROUP BY and HAVING clauses.",
subject:"Database Management System",
courseId:"DB301",
unit:"SQL",
marks:10,
difficulty:"Medium",
bloom:"Apply",
co:"CO2",
level:"College",
createdBy:"teacher2",
timestamp:"2025-01-18"
}

];

export const SEED_LOGS = [
  { id:1, user:"admin",    role:"Admin",   action:"LOGIN",                   timestamp:"2025-01-20T08:00:00", details:"Successful login" },
  { id:2, user:"teacher1", role:"Teacher", action:"SYLLABUS_UPLOADED",       timestamp:"2025-01-20T09:00:00", details:"math_syllabus.pdf — Mathematics MA101" },
  { id:3, user:"teacher1", role:"Teacher", action:"QUESTION_BANK_GENERATED", timestamp:"2025-01-20T09:15:00", details:"Generated 15 questions — Mathematics MA101" },
  { id:4, user:"teacher1", role:"Teacher", action:"PAPER_GENERATED",         timestamp:"2025-01-20T10:30:00", details:"Set A, B, C — Mathematics MA101 — College" },
  { id:5, user:"admin",    role:"Admin",   action:"PAPER_DOWNLOADED",        timestamp:"2025-01-20T11:00:00", details:"Downloaded Mathematics MA101 Set A — PDF" },
  { id:6, user:"teacher2", role:"Teacher", action:"SYLLABUS_UPLOADED",       timestamp:"2025-01-21T09:00:00", details:"physics_syllabus.pptx — Physics PH201" },
];

export const SEED_TEMPLATES = [
  { id:1, name:"College Standard — 50 Marks", filename:"college_exam_v2.docx", uploadedAt:"2025-01-10T10:00:00",
    placeholders:["{{subject}}","{{courseId}}","{{sectionA}}","{{sectionB}}","{{sectionC}}","{{date}}","{{duration}}","{{totalMarks}}"] },
];

export const SEED_PAPERS = [];
