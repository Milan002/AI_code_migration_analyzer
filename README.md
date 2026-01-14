# 🔄 AI Code Migration Analyzer

An AI-powered tool that analyzes Python code to check if it's **Python 3 compatible** or contains **Python 2 patterns**. Upload your Python files and get instant analysis with detailed reports.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## ✨ Features

- **AI-Powered Analysis** - Uses Google Gemini LLM for intelligent code analysis
- **Python 2 Detection** - Identifies Python 2 patterns like `has_key()`, `xrange()`, `print` statements, etc.
- **Detailed Reports** - Get line-by-line issue detection with fix recommendations
- **User Authentication** - Secure login/register with JWT tokens
- **Report History** - Save and view past analysis reports
- **File Upload** - Drag & drop or browse to upload `.py` files or `.zip` archives

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + Vite |
| Backend | FastAPI (Python) |
| Database | MongoDB |
| AI/LLM | Google Gemini via LangChain |
| Containerization | Docker & Docker Compose |

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose installed
- Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd migration_project1
```

### 2. Set Up Environment

```bash
# Create .env file with your Gemini API key
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 3. Run with Docker

```bash
docker-compose up --build
```

### 4. Access the Application

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:8001 |
| MongoDB | localhost:27019 |

---

## 📁 Project Structure

```
migration_project/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── config.py          # App configuration
│   │   ├── database/          # MongoDB connection
│   │   ├── models/            # Pydantic models
│   │   ├── routes/            # API endpoints
│   │   │   ├── auth.py        # Authentication routes
│   │   │   └── migration.py   # Analysis routes
│   │   └── services/
│   │       ├── auth.py        # JWT & password hashing
│   │       ├── file_processor.py
│   │       └── llm_analyzer.py # Gemini LLM integration
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── api/               # API client functions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── docker-compose.yml
├── .env                        # Environment variables (not in git)
├── .gitignore
└── README.md
```

---

## 🔍 How It Works

1. **Upload** - User uploads a Python file (`.py`) or ZIP archive
2. **Analyze** - LLM analyzes the code for Python 2 vs Python 3 compatibility
3. **Report** - Detailed report showing:
   - Whether code is Python 3 compatible
   - List of issues found with severity levels
   - Exact code snippets with problems
   - Recommended fixes

### Example Python 2 Patterns Detected

| Pattern | Issue | Fix |
|---------|-------|-----|
| `dict.has_key(x)` | Removed in Python 3 | Use `x in dict` |
| `print "hello"` | Print statement | Use `print("hello")` |
| `xrange(10)` | Removed in Python 3 | Use `range(10)` |
| `raw_input()` | Renamed | Use `input()` |
| `dict.iteritems()` | Removed | Use `dict.items()` |
| `except Error, e:` | Old syntax | Use `except Error as e:` |

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login & get JWT token |
| GET | `/api/auth/me` | Get current user info |

### Migration Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/migration/analyze` | Upload & analyze code |
| GET | `/api/migration/report/{id}` | Get report by ID |
| GET | `/api/migration/reports` | List all reports |
| DELETE | `/api/migration/report/{id}` | Delete a report |

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `MONGODB_URL` | MongoDB connection URL | No (default: mongodb://mongodb:27017) |
| `SECRET_KEY` | JWT secret key | No (has default) |

---

## 🛠️ Development

### Run Backend Locally

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

---

## 📝 License

MIT License

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
