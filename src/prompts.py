"""Prompt templates for resume, cover letter, and cold email generation."""

SYSTEM_CAREER_AGENT = """You are a world-class career coach and personal branding expert.
You have deep knowledge of ATS systems, hiring manager psychology, and what makes
candidates stand out. You write with precision — every word earns its place.
You never use filler phrases like "I am passionate about" or "I am a team player."
You write specifically, concretely, and in the candidate's own voice."""


def resume_prompt(context_block: str, job_description: str, company: str, role: str) -> str:
    return f"""You are tailoring a resume for a specific job application.

CANDIDATE CONTEXT:
{context_block}

TARGET ROLE: {role} at {company}

JOB DESCRIPTION:
{job_description}

INSTRUCTIONS:
1. Output a complete, ATS-optimized resume in plain text (no markdown, no tables).
2. STRICT 1-PAGE LIMIT — include only what is most relevant to this role.
3. Mirror keywords from the job description naturally throughout the resume.
4. Every bullet point must be metric-driven: use numbers, percentages, or scale.
   Format: [Strong verb] + [what you did] + [result/impact].
5. Sections (in order): Contact Info | Summary (2–3 lines) | Skills | Experience | Projects | Education
6. Summary must be role-specific — not generic. Mention the company name.
7. Do NOT include irrelevant experience. Do NOT pad with soft-skill buzzwords.
8. Output ONLY the resume text. No preamble, no explanation.
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


def cold_email_prompt(
    context_block: str,
    style_block: str,
    company: str,
    role: str,
    recipient_title: str = "Head of Engineering",
) -> str:
    style_section = (
        f"\nMY WRITING STYLE (analyze and mirror this voice):\n{style_block}\n"
        if style_block
        else ""
    )

    return f"""You are writing a cold outreach email from a job seeker to a senior leader.

CANDIDATE CONTEXT:
{context_block}
{style_section}
TARGET: {recipient_title} at {company}
DESIRED ROLE: {role}

INSTRUCTIONS:
1. Write a cold email that is under 120 words total. Every sentence must earn its place.
2. Tone: hungry but not desperate. Confident but not arrogant. Direct and human.
3. Analyze my writing samples and mirror my voice. If no samples, write crisply.
4. Structure:
   - Subject line (write it as "Subject: ...")
   - Opening: One sentence on why you're reaching out to THEM specifically.
     Reference something real (their team's work, a product, a mission statement).
   - Middle: 2 sentences on who you are + your single most relevant achievement (with a number).
   - Ask: One clear, low-friction ask. A 15-minute call, not "Please review my resume."
   - Sign-off: Name, email, GitHub/LinkedIn/portfolio link.
5. Do NOT use "I hope this email finds you well" or any similar filler.
6. Output ONLY the email (subject line + body). No preamble, no explanation.
"""
