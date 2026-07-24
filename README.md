# 🚀 QuestAI: Intelligent AI-Based Question Paper Generation Using NLP & Bloom's Taxonomy

<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/NLP-Enabled-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Integrated-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Deep%20Learning-Supported-red?style=for-the-badge" />
</p>

## 📖 Overview

**QuestAI** is an intelligent AI-powered question paper generation system that automates the traditional examination paper-setting process using **Machine Learning (ML)**, **Deep Learning (DL)**, **Natural Language Processing (NLP)**, and **Bloom's Taxonomy**.

The system analyzes syllabus content, classifies questions into cognitive levels, predicts difficulty, removes repetitive questions, and generates multiple balanced examination papers with minimal human intervention.

---

## 🎯 Project Objectives

✅ Automate question paper generation using AI and NLP techniques.

✅ Classify questions according to **Bloom's Taxonomy** levels:

* Remember
* Understand
* Apply
* Analyze
* Evaluate
* Create

✅ Ensure balanced difficulty distribution and syllabus coverage.

✅ Prevent duplicate and semantically similar questions.

✅ Generate multiple unique paper sets following university examination patterns.

---

## ✨ Key Features

### 📚 Syllabus-Based Question Generation

Generate questions directly from uploaded syllabus content.

### 🧠 Bloom's Taxonomy Classification

Automatically categorizes questions into cognitive learning levels.

### 📊 Difficulty Prediction

Classifies questions as Easy, Medium, or Hard.

### 🔍 Semantic Similarity Checking

Avoids duplicate and repetitive questions.

### 📄 Multiple Paper Set Generation

Generates:

* Set A
* Set B
* Set C

### 📑 PDF Export

Download generated question papers in printable format.

### 🎯 Balanced Paper Creation

Ensures:

* Proper syllabus coverage
* Difficulty balancing
* Non-repetition
* Examination pattern compliance

---

## 🏗️ Project Structure

```text
QuestAI/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── app.py
│   └── requirements.txt
│
├── dataset/
│   ├── syllabus_data.csv
│   └── question_bank.csv
│
├── docs/
│   └── Research_Paper.pdf
│
└── README.md
```

---

## 🛠️ Tech Stack

### Frontend

* ⚛️ React.js
* 🎨 HTML5
* 🎨 CSS3
* 🟨 JavaScript

### Backend

* 🐍 Python
* 🌐 Flask / FastAPI

### AI & Machine Learning

| Module                | Model/Technique                  |
| --------------------- | -------------------------------- |
| Question Generation   | GPT-5 / GPT-4o                   |
| Semantic Similarity   | all-MiniLM-L6-v2                 |
| Bloom Classification  | DistilBERT / Logistic Regression |
| Difficulty Prediction | Random Forest                    |
| NLP Processing        | Sentence Transformers            |

### Database

* 🗄️ MySQL / MongoDB

---

## 🤖 AI Workflow

```text
Syllabus Upload
       ↓
Topic Extraction using NLP
       ↓
Question Generation
       ↓
Bloom Classification
       ↓
Difficulty Prediction
       ↓
Duplicate Removal
       ↓
Balanced Question Selection
       ↓
Question Paper Generation
       ↓
PDF Export
```

---

## 👨‍🏫 User Workflow

### 1️⃣ Upload Syllabus

Upload syllabus or course content.

### 2️⃣ AI Processing

System extracts topics and learning outcomes automatically.

### 3️⃣ Question Generation

AI generates relevant examination questions.

### 4️⃣ Classification & Validation

Questions are:

* Bloom classified
* Difficulty scored
* Duplicate checked

### 5️⃣ Paper Generation

Generate multiple balanced paper sets.

### 6️⃣ Export

Download final question papers as PDF.

---

## 🚀 Installation & Setup

### Prerequisites

```bash
Python 3.10+
Node.js 18+
npm
```

Check versions:

```bash
python --version
node --version
npm --version
```

---

### Clone Repository

```bash
git clone https://github.com/your-username/QuestAI.git
cd QuestAI
```

---

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

python app.py
```

Backend runs at:

```text
http://localhost:5000
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm start
```

Frontend runs at:

```text
http://localhost:3000
```

---

## 📈 Expected Outcomes

✅ Fully automated question paper generation.

✅ Reduced manual effort in examination paper setting.

✅ Improved Bloom's Taxonomy classification accuracy.

✅ Better syllabus coverage and question diversity.

✅ Multiple balanced question paper sets.

✅ Enhanced reliability and consistency in examinations.

---

## 📊 Future Enhancements

🔹 Multilingual Question Generation

🔹 AI-Based Answer Key Generation

🔹 Question Quality Evaluation

🔹 Learning Management System (LMS) Integration

🔹 Advanced Analytics Dashboard

🔹 Personalized Exam Pattern Support

---


