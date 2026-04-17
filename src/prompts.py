"""Prompt templates for resume, cover letter, and cold email generation."""

SYSTEM_CAREER_AGENT = """You are a world-class career coach and personal branding expert.
You have deep knowledge of ATS systems, hiring manager psychology, and what makes
candidates stand out. You write with precision — every word earns its place.
You never use filler phrases like "I am passionate about" or "I am a team player."
You write specifically, concretely, and in the candidate's own voice."""


def resume_prompt(
    context_block: str,
    format_block: str,
    governance_block: str,
    job_description: str,
    company: str,
    role: str,
) -> str:
    return f"""You are tailoring a resume for a specific job application. Output valid LaTeX code only.

═══════════════════════════════════════
GOVERNANCE RULES — FOLLOW STRICTLY
═══════════════════════════════════════
{governance_block}

═══════════════════════════════════════
CANDIDATE RAW DATA
═══════════════════════════════════════
{context_block}

═══════════════════════════════════════
LATEX FORMAT TEMPLATE
═══════════════════════════════════════
{format_block}

═══════════════════════════════════════
TARGET ROLE: {role} at {company}
═══════════════════════════════════════

JOB DESCRIPTION:
{job_description}

═══════════════════════════════════════
OUTPUT RULES
═══════════════════════════════════════
1. Output a complete, valid LaTeX resume using EXACTLY the template structure above.

2. STRICT 1-PAGE LIMIT — section entry limits:
   - Projects:    pick 2–3 most relevant. Max 3 bullet points each.
   - Experience:  pick 2–3 most relevant. Max 3 bullet points each.
   - Leadership:  pick 1–2 most relevant. Max 2 bullet points each.
   - Education:   READ-ONLY — copy exactly from template, do not modify.
   - Skills:      READ-ONLY — copy exactly from template, do not modify.

3. For Projects:
   - Project name, date/timeline, and subtitle (italic line) are READ-ONLY — copy exactly.
   - Bullet points only: apply the Core Transformation Formula and Power Verbs from the Role-Specific Matrix.
   - Use [X]% or [Metric] placeholders if a quantifiable result is not in source data.
4. For Experience & Leadership: copy bullets as-is with light grammar cleanup only. Do NOT reframe or apply transformation verbs.

5. Do NOT change the LaTeX preamble, formatting commands, or document structure.
6. Output ONLY the LaTeX code — no explanation, no markdown fences, no extra text.
"""


def cover_letter_prompt(
    context_block: str,
    style_block: str,
    job_description: str,
    company: str,
    role: str,
    hiring_manager: str = "",
) -> str:
    style_section = (
        f"\nMY WRITING STYLE (analyze and mirror this voice):\n{style_block}\n"
        if style_block
        else ""
    )
    salutation = f"Dear {hiring_manager}," if hiring_manager else "Dear Hiring Manager,"

    return f"""You are writing a personalized cover letter for a job application.

CANDIDATE CONTEXT:
{context_block}
{style_section}
TARGET ROLE: {role} at {company}

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
1. Write a 3-paragraph cover letter that sounds like a real human, not a template.
2. Analyze my writing samples above and mirror my tone, sentence rhythm, and vocabulary.
   If no samples are provided, write in a direct, confident, slightly conversational tone.
3. Structure:
   - Para 1 ("Why This Role"): Lead with a specific, genuine reason you want THIS company.
     Reference something real about the company (mission, product, recent news if implied).
     Do NOT open with "I am writing to apply for..."
   - Para 2 ("Why Me"): Connect 2–3 specific achievements from my background to the role's
     needs. Use concrete numbers. Show you understand what success looks like here.
   - Para 3 ("Call to Action"): Short, confident, no desperation. End with a clear ask.
4. Use the salutation: {salutation}
5. Keep it under 350 words.
6. Output ONLY the cover letter. No preamble, no explanation.
"""


def founder_outreach_prompt(
    governance_block: str,
    company: str,
    founder_name: str,
    founder_research: str,
) -> str:
    return f"""You are personalizing a founder outreach email. Follow the governance rules exactly.

═══════════════════════════════════════
OUTREACH GOVERNANCE — FOLLOW STRICTLY
═══════════════════════════════════════
{governance_block}

═══════════════════════════════════════
TARGET
═══════════════════════════════════════
Company: {company}
Founder: {founder_name}

═══════════════════════════════════════
FOUNDER & COMPANY RESEARCH NOTES
═══════════════════════════════════════
{founder_research if founder_research.strip() else "No research provided — use what can be inferred from the company name only. Flag placeholders clearly."}

═══════════════════════════════════════
OUTPUT RULES
═══════════════════════════════════════
1. Use the EXACT fixed template from the governance doc — do not rewrite any lines.
2. Fill ONLY the four placeholders: [FOUNDER_FIRST_NAME], [COMPANY_NAME],
   [INSERT reason - founder], [INSERT reason - company].
3. Each reason must be specific — no generic phrases. Apply the banned phrases list.
4. Output the full message block in this format:

---
## {company}
**To:** [Full Founder Name] — [Title]
**YC:** [Yes — Batch / No]
**Recent Milestone:** [1-line summary, or "None found"]

### Message:
[complete filled message — every line, no truncation]
"""
