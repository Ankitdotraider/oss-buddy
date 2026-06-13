# 🤝 OSS Buddy

Your AI senior engineer for open source contributions.

## What it does
Paste a GitHub issue URL and OSS Buddy explains:
1. What the bug or feature is in plain English
2. What part of the codebase is likely involved
3. Step by step course of action
4. Concepts to understand before starting

## Tech Stack
- Python
- Groq API (llama-3.3-70b-versatile)
- GitHub API
- Streamlit

## Setup
1. Clone the repo
2. Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file:
GROQ_API_KEY=your_groq_key

GITHUB_TOKEN=your_github_token
4. Run:
```bash
streamlit run app.py
```

## Demo
Paste any GitHub issue URL and get an instant breakdown from your AI senior engineer.