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
  { id:1,  text:"Define the derivative of a function and state its geometric interpretation.", subject:"Mathematics",     courseId:"MA101", unit:"Calculus",          marks:2,  difficulty:"Easy",   bloom:"Remember",   co:"CO1", level:"College", createdBy:"teacher1", timestamp:"2025-01-15T10:30:00" },
  { id:2,  text:"Solve 2x² + 5x − 3 = 0 using the quadratic formula.",                        subject:"Mathematics",     courseId:"MA101", unit:"Algebra",           marks:5,  difficulty:"Medium", bloom:"Apply",      co:"CO2", level:"College", createdBy:"teacher1", timestamp:"2025-01-15T10:35:00" },
  { id:3,  text:"Evaluate the definite integral ∫₀² (x³ − 2x + 1)dx.",                        subject:"Mathematics",     courseId:"MA101", unit:"Calculus",          marks:10, difficulty:"Hard",   bloom:"Evaluate",   co:"CO3", level:"College", createdBy:"teacher1", timestamp:"2025-01-15T10:40:00" },
  { id:4,  text:"State Newton's three laws of motion with real-world examples.",                subject:"Physics",         courseId:"PH201", unit:"Mechanics",          marks:2,  difficulty:"Easy",   bloom:"Remember",   co:"CO1", level:"College", createdBy:"teacher2", timestamp:"2025-01-16T09:00:00" },
  { id:5,  text:"Explain refraction and derive Snell's law from first principles.",             subject:"Physics",         courseId:"PH201", unit:"Optics",             marks:5,  difficulty:"Medium", bloom:"Understand", co:"CO2", level:"College", createdBy:"teacher2", timestamp:"2025-01-16T09:15:00" },
  { id:6,  text:"A projectile is launched at 30° with v₀=20m/s. Find maximum height.",         subject:"Physics",         courseId:"PH201", unit:"Mechanics",          marks:10, difficulty:"Hard",   bloom:"Apply",      co:"CO3", level:"College", createdBy:"teacher2", timestamp:"2025-01-16T09:30:00" },
  { id:7,  text:"Write the IUPAC name of CH₃−CH₂−OH.",                                         subject:"Chemistry",       courseId:"CH301", unit:"Organic Chemistry",  marks:2,  difficulty:"Easy",   bloom:"Remember",   co:"CO1", level:"College", createdBy:"teacher1", timestamp:"2025-01-17T11:00:00" },
  { id:8,  text:"Compare SN1 and SN2 reactions with mechanisms and examples.",                  subject:"Chemistry",       courseId:"CH301", unit:"Organic Chemistry",  marks:5,  difficulty:"Medium", bloom:"Understand", co:"CO2", level:"College", createdBy:"teacher1", timestamp:"2025-01-17T11:15:00" },
  { id:9,  text:"What is a binary search tree? Write the insertion algorithm.",                 subject:"Computer Science", courseId:"CS401", unit:"Data Structures",   marks:5,  difficulty:"Medium", bloom:"Understand", co:"CO2", level:"College", createdBy:"teacher1", timestamp:"2025-01-18T14:00:00" },
  { id:10, text:"Implement Dijkstra's shortest path algorithm and analyse complexity.",         subject:"Computer Science", courseId:"CS401", unit:"Algorithms",         marks:10, difficulty:"Hard",   bloom:"Create",     co:"CO4", level:"College", createdBy:"teacher1", timestamp:"2025-01-18T14:30:00" },
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
