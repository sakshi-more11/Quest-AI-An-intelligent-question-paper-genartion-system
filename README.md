# SecureExam AI — Setup Guide

## Project Structure

```
securexam/
├── public/
│   └── index.html               ← HTML entry point
├── src/
│   ├── index.js                 ← React entry point
│   ├── index.css                ← Global styles + Tailwind
│   ├── App.jsx                  ← Root: all state, auth, routing
│   ├── data/
│   │   └── constants.js         ← Users, seed data, enums
│   ├── components/
│   │   ├── Sidebar.jsx          ← Navigation sidebar
│   │   └── UI.jsx               ← Shared UI components (Badge, Card, etc.)
│   └── pages/
│       ├── LoginPage.jsx        ← Login screen
│       ├── Dashboard.jsx        ← Teacher & Admin dashboards
│       ├── UploadSyllabus.jsx   ← Upload + AI parse syllabus (Teacher)
│       ├── QuestionBank.jsx     ← View + generate questions (Teacher full, Admin read)
│       ├── Templates.jsx        ← Upload/manage templates (Teacher full, Admin read)
│       ├── GeneratePaper.jsx    ← Generate Set A/B/C + download PDF (Teacher only)
│       ├── Papers.jsx           ← View + download generated papers (Admin only)
│       └── ActivityLogs.jsx     ← Audit trail (Admin all, Teacher own)
├── package.json
├── tailwind.config.js
└── README.md
```

---

## Role Permissions

| Feature                   | Teacher | Admin     |
|---------------------------|---------|-----------|
| Upload Syllabus           | ✅ Yes  | ❌ No     |
| Generate Question Bank    | ✅ Yes  | ❌ No     |
| Upload Templates          | ✅ Yes  | ❌ No     |
| Generate Paper (Set A/B/C)| ✅ Yes  | ❌ No     |
| Download PDF (own papers) | ✅ Yes  | ✅ Yes    |
| View All Questions        | ✅ Yes  | ✅ Yes    |
| View Generated Papers     | ✅ Yes  | ✅ Yes    |
| View Activity Logs        | Own only| All logs |
| System Dashboard          | Own data| All data |

---

## How to Run

### Step 1 — Prerequisites

Make sure you have Node.js (v16+) installed:
```bash
node --version   # Should be v16 or higher
npm --version
```

Download Node.js from: https://nodejs.org

---

### Step 2 — Create the Project

```bash
# Create a new React app
npx create-react-app securexam
cd securexam
```

---

### Step 3 — Install Tailwind CSS

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

---

### Step 4 — Copy All Files

Copy all the files from this project into the `securexam/` folder:

- Replace `src/App.js` with `src/App.jsx`
- Replace `src/index.js` with `src/index.js`
- Replace `src/index.css` with `src/index.css`
- Create `src/data/constants.js`
- Create `src/components/Sidebar.jsx`
- Create `src/components/UI.jsx`
- Create `src/pages/LoginPage.jsx`
- Create `src/pages/Dashboard.jsx`
- Create `src/pages/UploadSyllabus.jsx`
- Create `src/pages/QuestionBank.jsx`
- Create `src/pages/Templates.jsx`
- Create `src/pages/GeneratePaper.jsx`
- Create `src/pages/Papers.jsx`
- Create `src/pages/ActivityLogs.jsx`
- Replace `tailwind.config.js`
- Replace `public/index.html`

---

### Step 5 — Update tailwind.config.js

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: { extend: {} },
  plugins: [],
};
```

---

### Step 6 — Update src/index.css (top of file)

Make sure these three lines are at the TOP of index.css:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

### Step 7 — Start the App

```bash
npm start
```

The app opens at: http://localhost:3000

---

## Demo Credentials

| Username  | Password   | Role    | Access Level     |
|-----------|------------|---------|------------------|
| teacher1  | teach123   | Teacher | Full access      |
| teacher2  | teach456   | Teacher | Full access      |
| admin     | admin123   | Admin   | Read-only viewer |

---

## Teacher Workflow

1. **Login** as teacher1 / teach123
2. **Upload Syllabus** → Upload a PDF/PPT/DOCX → AI reads and extracts units automatically (no manual unit entry)
3. **Question Bank** → Click "Generate Questions from Syllabus" → select your syllabus → AI generates 15 questions
4. **Templates** → Upload a .docx template with placeholders like `{{subject}}`, `{{sectionA}}`
5. **Generate Paper** → Select subject + template → AI generates Set A, Set B, Set C
6. **Download** → Click "⬇ Set A PDF", "⬇ Set B PDF", "⬇ Set C PDF" to print/save

---

## Admin Workflow

1. **Login** as admin / admin123
2. **Dashboard** → See system-wide stats (read-only)
3. **View Q-Bank** → Browse all questions (read-only, no generate button)
4. **Generated Papers** → See all papers teachers generated → Download any set as PDF
5. **Activity Logs** → See full audit trail of all users

---

## API Key Note

The app calls the Anthropic Claude API directly from the browser.
The API key is handled automatically by the claude.ai artifact environment.

If running standalone outside claude.ai, you need to add your API key:

In each page file that calls `fetch("https://api.anthropic.com/v1/messages", ...)`,
add this header:
```js
headers: {
  "Content-Type": "application/json",
  "x-api-key": "YOUR_API_KEY_HERE",
  "anthropic-version": "2023-06-01",
  "anthropic-dangerous-direct-browser-access": "true"
}
```

Get your API key from: https://console.anthropic.com

---

## Troubleshooting

**App won't start:**
```bash
npm install   # reinstall dependencies
npm start
```

**Tailwind styles not working:**
- Make sure `@tailwind base; @tailwind components; @tailwind utilities;` are at the TOP of `src/index.css`
- Make sure `tailwind.config.js` has `content: ["./src/**/*.{js,jsx}"]`

**AI not generating questions:**
- Check browser console for API errors
- The AI fallback will kick in automatically with sample questions

**Files not found:**
- Make sure the folder structure matches exactly: `src/pages/`, `src/components/`, `src/data/`
- React is case-sensitive — `LoginPage.jsx` not `loginpage.jsx`
