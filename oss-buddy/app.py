import os
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

groq_client = Groq(api_key=GROQ_API_KEY)

def fetch_issue(url):
    # Validate URL format first
    import re
    if not re.match(r"https://github\.com/[\w.-]+/[\w.-]+/issues/\d+", url):
        raise ValueError("Invalid URL. Use format: github.com/owner/repo/issues/123")
    
    parts = url.strip("/").split("/")
    owner = parts[3]
    repo = parts[4]
    issue_number = parts[6]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(api_url, headers=headers)
    
    data = response.json()
    
    # Check it's actually an issue
    if "title" not in data:
        raise ValueError("That URL doesn't point to a GitHub issue.")
    
    return data

def explain_issue(issue_data):
    title = issue_data["title"]
    body = issue_data["body"]
    
    prompt = f"""
You are a senior engineer helping a beginner open source contributor.

GitHub Issue Title: {title}
GitHub Issue Description: {body}

Explain the following in simple terms:
1. What is the bug or feature being asked for?
2. What part of the codebase is likely involved?
3. What should the contributor do step by step?
4. Any concepts the contributor should understand before starting?

Be friendly, clear, and teach as you explain.
"""
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# UI
st.set_page_config(page_title="OSS Buddy", page_icon="🤝")

st.title("🤝 OSS Buddy")
st.subheader("Your AI senior engineer for open source contributions")

url = st.text_input("Paste a GitHub Issue URL", placeholder="https://github.com/owner/repo/issues/123")

if st.button("Explain Issue"):
    if url:
        with st.spinner("Fetching issue and analyzing..."):
            try:
                issue = fetch_issue(url)
                st.markdown(f"### 📌 {issue['title']}")
                with st.expander("View Original Issue"):
                    st.markdown(issue["body"])
                explanation = explain_issue(issue)
                st.markdown("### 🧠 Senior Engineer Breakdown")
                st.markdown(explanation)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please paste a GitHub issue URL first.")