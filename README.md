# 🤖 AI DevOps Incident Copilot

An AI-powered incident analysis system that ingests production logs, understands system context, and automatically generates root cause analysis and fix recommendations — with real-time alerts.

> Built as a portfolio project to demonstrate DevOps, AI integration, and cloud engineering skills.

---

## 🚀 Live Demo

> > 🟢 Live at https://ai-devops-copilot-y0n0.onrender.com

---

## 🧠 What It Does

Paste any production log → AI analyzes it → get instant cause, fix, and severity → critical incidents trigger Discord alerts automatically.

**Example:**
Input:  CrashLoopBackOff: pod payment-service restarting, exit code 137
Output: Cause: OOM kill due to memory limit breach
Fix:   Increase memory limit for payment-service pod
Severity: CRITICAL → Discord alert fired

---

## 🏗️ Architecture
[Log Input - UI / API / CI Pipeline]
↓
[Log Sanitizer - strips PII]
↓
[AI Analyzer - GPT-4o-mini + System Context]
↓
[PostgreSQL - incident history]
↓
[Alert Service - Discord webhook]
↓
[React Dashboard - UI]

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| AI | OpenAI GPT-4o-mini |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Alerts | Discord Webhook |
| Deployment | Render (coming) |

---

## ⚙️ Core Features

- **Log Analysis** — paste any log, get AI-generated root cause and fix
- **System Context** — AI understands your specific stack and services
- **Incident History** — every analysis saved to PostgreSQL with timestamps
- **Smart Alerts** — high and critical severity automatically triggers Discord
- **Log Sanitizer** — strips emails, tokens, passwords before sending to AI
- **Mock Mode** — development mode that skips OpenAI calls to save credits
- **REST API** — any external system (Jenkins, K8s, CloudWatch) can POST logs

---

## 🗂️ Project Structure
ai-devops-copilot/
├── backend/
│   ├── main.py
│   ├── routes/
│   │   └── logs.py
│   ├── services/
│   │   ├── ai_analyzer.py
│   │   └── alert_service.py
│   └── db/
│       └── database.py
├── frontend/
│   └── index.html
├── data/
│   ├── sample_logs.log
│   └── system_context.txt
├── docker/
│   └── docker-compose.yml
└── .github/workflows/

---

## 🚀 How To Run

### Prerequisites
- Docker Desktop
- OpenAI API key
- Discord webhook URL

### 1. Clone the repo
```bash
git clone https://github.com/GoQueueOps/ai-devops-copilot.git
cd ai-devops-copilot
```

### 2. Create root `.env` file
OPENAI_API_KEY=your-key-here
DISCORD_WEBHOOK=your-webhook-here
MOCK_MODE=false

### 3. Start with Docker
```bash
cd docker
docker-compose up --build
```

### 4. Open the dashboard
http://localhost:8000

---

## 📡 API Reference

### Analyze a log
```bash
POST /api/analyze-log
Content-Type: application/json

{
  "log_text": "OOMKilled: container exceeded memory limit of 512Mi"
}
```

**Response:**
```json
{
  "cause": "Container hit memory limit under high load",
  "fix": "Increase memory limit or add HPA",
  "severity": "high"
}
```

### Get recent incidents
```bash
GET /api/incidents
```

---

## 🔐 Security

- Log sanitizer strips PII before sending to AI
- API keys stored in `.env` — never committed to git
- Mock mode prevents accidental API calls during development

---

## 🗺️ Roadmap

- [ ] Deploy to Render with public URL
- [ ] RAG — upload runbooks and architecture docs for smarter analysis
- [ ] Pattern detection — "this error occurred 12 times today"
- [ ] AWS Bedrock integration — replace OpenAI, keep data inside AWS
- [ ] Kubernetes API integration — auto-pull logs from crashing pods
- [ ] Real-time log streaming simulation

---

## 👨‍💻 Author

**Tejas Jee** — Packeged Application Developer Analyst

- GitHub: [@GoQueueOps](https://github.com/GoQueueOps)
- LinkedIn: [Tejas Jee](https://linkedin.com/in/your-profile)