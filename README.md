# 🚀 CareerAdvocate — Personal Career AI Agent

A local AI tool that acts as your personal career advocate. It reads your real background from local markdown files and generates a **tailored resume**, **personalized cover letter**, and **cold email** for any job you apply to — in one click.

Built with Python + Streamlit + Gemini API.

---

## Why I Built This

Generic AI resume tools don't know who you are. This one does.

Instead of hallucinating credentials, CareerAdvocate reads your actual projects, achievements, and writing style from files you control — then uses that context to produce outputs that sound like *you*, not a template.

---

## Features

- **User Memory System** — feeds the AI your real profile, skills, projects, and STAR stories from local markdown files
- **Style Learning** — analyzes your past writing samples to mirror your tone and voice
- **ATS-Optimized Resume** — strictly 1 page, metric-driven, keyword-matched to the job description
- **Personalized Cover Letter** — role-specific "Why Company / Why Me" structure, written in your voice
- **Cold Email** — concise, direct outreach to a Head of Department (under 120 words)
- **Live Model Selector** — fetches all available Gemini models from your API key and lets you switch instantly

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| AI | Google Gemini API (`google-generativeai`) |
| Language | Python 3.10+ |
| Data | Local markdown files |
| Auth | `.env` file (API key) |

---

## Project Structure

```
career-ai/
├── app.py                  # Streamlit UI
├── requirements.txt
├── .env.example            # API key template
├── src/
│   ├── memory.py           # Loads and structures your data files
│   ├── prompts.py          # Prompt templates for all 3 outputs
│   └── generators.py       # Gemini API calls
└── data/                   # YOUR personal data (not tracked by git)
    ├── profile.md
    ├── skills.md
    ├── projects.md
    ├── stories.md
    └── writing_samples/
        └── sample1.md
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/nyle06dn/CareerAdvocate.git
cd CareerAdvocate
```

**2. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your Gemini API key**
```bash
cp .env.example .env
# open .env and add your key: GEMINI_API_KEY=AIza...
```
Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

**5. Fill in your personal data**

Create the following files in the `data/` folder:

| File | What to put in it |
|---|---|
| `data/profile.md` | Name, email, education, work experience |
| `data/skills.md` | Your tech stack and skills |
| `data/projects.md` | Projects with tech stack and metrics |
| `data/stories.md` | STAR stories and key achievements |
| `data/writing_samples/sample1.md` | A past cover letter or email (for style learning) |

**6. Run the app**
```bash
streamlit run app.py
```

Open [localhost:8501](http://localhost:8501) in your browser.

---

## How to Use

1. Paste your **Gemini API key** in the sidebar
2. Select a **model** from the dropdown (auto-fetched from your key)
3. Enter the **company name**, **role**, and paste the **job description**
4. Click **Generate All Three Outputs**
5. Review and download your resume, cover letter, and cold email

---

## Notes

- The `data/` folder is in `.gitignore` — your personal info never gets pushed to GitHub
- Switching jobs = just change the job description field. Your personal data stays the same
- To change the AI model, use the sidebar dropdown — no code edits needed

---

*Built by [Nhi Thuc Le](https://github.com/nyle06dn)*
