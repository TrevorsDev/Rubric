# Rubric — Job Application Intelligence

A full-stack AI application that analyzes job postings against a structured resume knowledge base and generates an honest fit report: strengths, gaps, and talking points for cover letters and interviews.

**Live demo:** https://rubric-rho-coral.vercel.app/

---

## What it does

Paste a job description. Rubric:

1. Sends the posting to OpenAI, which uses function-calling to extract structured requirements — required skills, tech stack, and years of experience
2. Queries a MongoDB Atlas knowledge base of resume chunks to retrieve relevant sections
3. Passes the requirements and retrieved context to OpenAI for synthesis, returning a structured fit report with a fit level (strong / partial / poor), fit summary, strengths, gaps, and talking points

---

## Architecture

```
Browser → Next.js frontend (Vercel)
              ↓
         /api/analyze  (Next.js server-side API route)
              ↓
         AWS Lambda  (Python 3.10)
              ↓
         ┌─────────────────────────────────┐
         │  1. OpenAI function-calling     │  extract job requirements
         │  2. MongoDB Atlas $in query     │  retrieve matching resume chunks
         │  3. OpenAI function-calling     │  synthesize fit report
         └─────────────────────────────────┘
```

The Next.js API route acts as a server-side proxy to Lambda — browser requests never hit Lambda directly, which keeps the Lambda URL out of client-side code and eliminates CORS friction.

---

## Tech stack

**Frontend**
- Next.js 15 (App Router) with TypeScript
- Tailwind CSS v4 with custom design tokens
- Deployed on Vercel

**Backend**
- Python 3.10 on AWS Lambda
- API Gateway (HTTP API, $default route)
- OpenAI API with function-calling for structured JSON extraction and synthesis
- MongoDB Atlas for resume chunk storage and retrieval (RAG pattern)

**Infrastructure**
- AWS Lambda + API Gateway
- IAM roles and execution policies
- MongoDB Atlas with network access configured for dynamic Lambda IPs

---

## RAG pattern

Resume content is stored in MongoDB as typed chunks (summary, skills, experience, project, background), each tagged with a skills array. When a job posting is analyzed, extracted skill labels are used to query MongoDB with a `$in` operator, retrieving only the chunks relevant to that role before passing them to the synthesis step. This avoids sending the full resume on every request.

---

## Local development

**Prerequisites:** Python 3.10+, Node.js 18+, MongoDB Atlas cluster, OpenAI API key

> **Note:** AWS Lambda currently runs Python 3.10 for this project. AWS has issued deprecation notices for older runtimes — a Python version upgrade (3.12+) is planned as a maintenance task.

**Backend**
```bash
python -m venv venv
source venv/bin/activate
pip install openai pymongo dnspython python-dotenv
```

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key
MONGODB_URI=your_mongodb_uri
```

Seed the resume knowledge base:
```bash
python seed_resume.py
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`

---

## Roadmap

**V2 — Resume & Cover Letter Generation**
- Multiple resume versions stored in MongoDB with selection UI
- Cover letter sample storage to preserve voice and tone
- One-click tailored resume bullets and cover letter draft output
- Batch job screening — submit multiple listings at once and get comparative fit reports to quickly prioritize which roles are worth a full application

**V3 — Eval Engineering**
- Scoring layer to evaluate fit report quality
- Structured logging of analysis outputs for quality measurement
- Exploration of eval patterns as a foundation for AI quality engineering

---

## Project background

Built as a portfolio project to develop applied AI engineering skills across serverless architecture, structured data extraction, document retrieval, and full-stack deployment. Each component was built incrementally across focused development sessions, with independent study of the underlying concepts alongside the build.
