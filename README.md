
# 🎓 Quest-AI: Intelligent AI-Based Question Paper Generation System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![NLP](https://img.shields.io/badge/NLP-BERT-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-FAISS-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

## 📖 Overview

**Quest-AI** is an AI-powered intelligent question paper generation system developed to automate examination paper creation for educational institutions.

The system generates **Outcome-Based Education (OBE)** compliant question papers by analyzing:

- Course syllabus
- Previous year question papers
- Study materials
- Question banks
- Custom templates

using **Natural Language Processing (NLP)**, **BERT**, **Semantic Search**, and **Retrieval-Augmented Generation (RAG)**.

Unlike traditional systems, Quest-AI ensures:

- Balanced difficulty
- Bloom's Taxonomy mapping
- CO Mapping
- No duplicate questions
- Complete syllabus coverage
- Multiple unique paper sets

---

# ✨ Features

## 📚 Intelligent Question Bank Generation

- Automatic extraction from PDFs, DOCX and PPT
- OCR support for scanned documents
- Semantic chunking
- Metadata generation
- Duplicate removal

---

## 🤖 AI Question Generation

- AI-generated engineering questions
- Context-aware generation using RAG
- Bloom's taxonomy aware generation
- Difficulty prediction
- Multiple question variations

---

## 📑 Automatic Question Paper Generation

- Generate multiple paper sets
- Marks distribution
- Unit-wise coverage
- Difficulty balancing and CO mapping
- Constraint-based paper creation

---

## 🎯 Outcome Based Education (OBE)

Supports

- CO Mapping, Bloom's Levels, Difficulty Levels, Syllabus Coverage
---

## 📄 Template Learning Engine

The system can learn examination templates automatically.

Features include

- Header detection
- Footer detection
- Font analysis
- Table detection
- Pagination
- Coordinate extraction
- Layout analysis

---

## 🔍 Retrieval Augmented Generation (RAG)

Uses

- Sentence Transformers
- FAISS Vector Database
- Semantic Search
- Context Retrieval

to generate accurate and syllabus-specific questions.

---

## 🧠 AI Models

- BERT Bloom Classifier
- BERT Difficulty Classifier
- Sentence Transformers
- Engineering Prompt Generator

---

## 🛡 Quality Assurance

Every generated paper passes through

- Grammar checking
- Duplicate detection
- Bloom verification and CO verification
- Engineering terminology validation
- Readability analysis
- Paper quality analysis

---

## 🔐 Authentication & Security

- JWT Authentication
- Password Hashing
- Role-Based Access Control
- Admin Dashboard
- Teacher Dashboard

---

# 🖥 System Architecture

```
                 +----------------+
                 |     React UI   |
                 +--------+-------+
                          |
                    FastAPI Backend
                          |
     ------------------------------------------------
     |              |             |                 |
 NLP Engine    AI Engine     Template Engine    Database
     |              |             |                 |
     ------------------------------------------------
                 |
          Question Bank
                 |
        Retrieval (FAISS)
                 |
          Large Language Model
                 |
       Question Generation Engine
                 |
       Constraint Based Selection
                 |
     Question Paper Generator
                 |
      PDF / DOCX Export Engine
```

---

# 🔄 Workflow

```
Upload Syllabus
        │
        ▼
Upload Study Material
        │
        ▼
Text Extraction
(PDF/DOCX/PPT/OCR)
        │
        ▼
Preprocessing
        │
        ▼
Chunking
        │
        ▼
Embedding Generation
        │
        ▼
FAISS Index Creation
        │
        ▼
Question Bank Generation
        │
        ▼
Bloom Classification
        │
        ▼
Difficulty Prediction
        │
        ▼
CO Mapping
        │
        ▼
Constraint Solver
        │
        ▼
Generate Multiple Papers
        │
        ▼
Quality Verification
        │
        ▼
PDF / DOCX Export
```

---

# 💻 Tech Stack

## 🎨 Frontend

- ⚛️ React.js
- 🎨 Tailwind CSS
- 🟨 JavaScript (ES6+)
- 🔗 Axios
- 🌐 HTML5
- 🎭 CSS3

---

## ⚙️ Backend

- 🐍 Python
- ⚡ FastAPI
- 🔌 REST APIs
- 📦 Uvicorn

---

## 🤖 Artificial Intelligence & NLP

- 🧠 BERT
- 🔍 Sentence Transformers (SBERT)
- 📚 Natural Language Processing (NLP)
- 🔄 Retrieval-Augmented Generation (RAG)
- 📌 FAISS Vector Database
- ✍️ Prompt Engineering
- 💬 Large Language Models (LLMs)

---

## 📊 Machine Learning

- 📈 Bloom's Taxonomy Classification
- 🎯 Difficulty Prediction
- 🔗 Semantic Similarity
- 📑 Question Ranking
- 📉 Question Quality Analysis

---

## 🗄️ Database

- 🛢️ SQLite
- 🧩 SQLAlchemy ORM

---

## 📄 Document Processing

- 📕 PyMuPDF (fitz)
- 📑 pdfplumber
- 📝 python-docx
- 👁️ OCR (Optical Character Recognition)

---

## 🔐 Authentication & Security

- 🔑 JWT Authentication
- 🔒 Password Hashing
- 👤 Role-Based Access Control (RBAC)

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/sakshi-more11/Quest-AI-An-intelligent-question-paper-genartion-system.git

cd Quest-AI-An-intelligent-question-paper-genartion-system
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
pip install -r backend/requirements.txt
```

---

## Install Frontend

```bash
cd frontend

npm install
```

---

## Run Backend

```bash

uvicorn backend.api.main:app --reload   
```

---

## Run Frontend

```bash
cd frontend

npm start
```

---


## 📊 Future Enhancements

🔹 Multilingual Question Generation

🔹 LLM Fine-tuning

🔹 Question Quality Evaluation

🔹 Learning Management System (LMS) Integration

🔹 Personalized Exam Pattern Support

---


