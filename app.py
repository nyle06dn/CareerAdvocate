"""Personal Career AI Agent — Streamlit UI"""

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

from src.memory import load_user_context, format_context_block, format_style_block, format_format_block
from src.generators import generate_resume, generate_cover_letter, generate_founder_outreach, DEFAULT_MODEL

FAVORITE_MODEL = "gemini-2.5-flash-lite-preview-06-17"


def fetch_models(api_key: str) -> list[str]:
    try:
        genai.configure(api_key=api_key)
        models = [
            m.name.replace("models/", "")
            for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
        return models if models else [FAVORITE_MODEL]
    except Exception as e:
        st.sidebar.warning(f"Could not fetch models: {e}")
        return [FAVORITE_MODEL]


def model_label(model: str) -> str:
    return f"⭐ {model}" if model == FAVORITE_MODEL else model


load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Career AI Agent", page_icon="🚀", layout="wide")

st.title("🚀 Personal Career AI Agent")
st.caption("Tailored resume · Cover letter · Founder outreach — grounded in your actual story.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Configuration")

    if "api_key" not in st.session_state:
        st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")

    api_key = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        help="Loaded from your .env file automatically.",
    )
    st.session_state.api_key = api_key

    st.divider()

    # ── Model selector ────────────────────────────────────────────────────────
    st.subheader("🤖 Model")

    if "model_list" not in st.session_state:
        st.session_state.model_list = [FAVORITE_MODEL]
    if "last_api_key" not in st.session_state:
        st.session_state.last_api_key = ""

    if api_key and api_key != st.session_state.last_api_key:
        with st.spinner("Fetching available models..."):
            st.session_state.model_list = fetch_models(api_key)
            st.session_state.last_api_key = api_key

    if api_key and st.button("🔄 Refresh Models", use_container_width=True):
        with st.spinner("Fetching available models..."):
            st.session_state.model_list = fetch_models(api_key)

    labeled_options = [model_label(m) for m in st.session_state.model_list]
    fav_label = model_label(FAVORITE_MODEL)
    default_index = labeled_options.index(fav_label) if fav_label in labeled_options else 0

    selected_label = st.selectbox(
        "Active Model", options=labeled_options, index=default_index,
        help="⭐ = favorite model. Click Refresh Models to reload.",
    )
    selected_model = selected_label.replace("⭐ ", "")
    st.caption(f"Using: `{selected_model}`")

    st.divider()

    # ── Memory status ─────────────────────────────────────────────────────────
    st.subheader("Memory Status")
    ctx = load_user_context()
    for _label, key, path in [
        ("Profile",              "profile",              "data/profile.md"),
        ("Skills",               "skills",               "data/skills.md"),
        ("Projects",             "projects",             "data/projects.md"),
        ("Stories",              "stories",              "data/stories.md"),
        ("Writing Samples",      "writing_samples",      "data/writing_samples/"),
        ("Resume Governance",    "resume_governance",    "data/resume_governance.md"),
        ("Outreach Governance",  "outreach_governance",  "data/outreach_governance.md"),
    ]:
        filled = bool(ctx[key])
        icon = "✅" if filled else "⚠️"
        st.write(f"{icon} `{path}`")

    st.divider()
    st.caption("Edit files in `data/` to update your info. AI reads them on every run.")

# ── Load context blocks ───────────────────────────────────────────────────────
context_block      = format_context_block(ctx)
style_block        = format_style_block(ctx)
format_block       = format_format_block(ctx)
resume_governance  = ctx.get("resume_governance", "")
outreach_governance = ctx.get("outreach_governance", "")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB LAYOUT — Resume & Cover Letter | Founder Outreach
# ═══════════════════════════════════════════════════════════════════════════════
tab_job, tab_outreach = st.tabs(["📄 Resume & Cover Letter", "📨 Founder Outreach"])

# ── Tab 1: Resume & Cover Letter ──────────────────────────────────────────────
with tab_job:
    st.subheader("Job Target")

    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company Name", value="Medpace, Inc.")
        role = st.text_input("Role / Job Title", value="Data Engineer Intern - Summer 2026")
    with col2:
        hiring_manager = st.text_input(
            "Hiring Manager Name (optional)",
            placeholder="e.g. Sarah Chen — used in cover letter salutation",
        )

    job_description = st.text_area(
        "Paste the Job Description", height=220,
        value="""Job Summary:
Our corporate activities are growing rapidly, and we are currently seeking a full-time, office-based Data Engineer Intern to join our Information Technology team. This position will work on a team to accomplish tasks and projects that are instrumental to the company's success.

Responsibilities:
Utilize skills in development areas including data warehousing, business intelligence, and databases (Snowflake, SQL Server, Azure Sql);
Support programming/software development using Extract, Transform, and Load (ETL) and Extract, Load and Transform (ELT) tools, (dbt, Azure Data Factory, SSIS);
Design, develop, enhance and support business intelligence reporting primarily using Microsoft Power BI;
Collect, analyze and document user requirements;
Participate in software validation process through development, review, and/or execution of test plan/cases/scripts;
Create software applications by following software development lifecycle process, which includes requirements gathering, design, development, testing, release, and maintenance;
Communicate with team members regarding projects, development, tools, and procedures; and
Provide end-user support including setup, installation, and maintenance for applications.

Qualifications:
Working towards a Bachelor's Degree in Computer Science, Data Science, or a related field;
Excellent communication skills; and
Excellent analytical and problem solving skills.

Medpace Overview:
Medpace is a full-service clinical contract research organization (CRO). We provide Phase I-IV clinical development services to the biotechnology, pharmaceutical and medical device industries. Our mission is to accelerate the global development of safe and effective medical therapeutics through its scientific and disciplined approach. Headquartered in Cincinnati, Ohio, employing more than 5,000 people across 40+ countries.

Why Medpace?:
People. Purpose. Passion. Make a Difference Tomorrow. Join Us Today.

The work we've done over the past 30+ years has positively impacted the lives of countless patients and families who face hundreds of diseases across all key therapeutic areas. The work we do today will improve the lives of people living with illness and disease in the future.""",
    )

    gen_job_btn = st.button("Generate Resume & Cover Letter", type="primary", use_container_width=True)

    if gen_job_btn:
        if not api_key:
            st.error("Add your Gemini API key in the sidebar.")
            st.stop()
        if not company or not role or not job_description:
            st.error("Fill in Company, Role, and Job Description.")
            st.stop()

        out_resume, out_cover = st.tabs(["Tailored Resume (LaTeX)", "Cover Letter"])

        with out_resume:
            try:
                with st.spinner(f"Crafting resume with {selected_model}..."):
                    resume = generate_resume(
                        api_key, context_block, format_block, resume_governance,
                        job_description, company, role, model=selected_model
                    )
                st.caption("📋 Copy and paste into Overleaf to render.")
                st.code(resume, language="latex")
                st.download_button(
                    "Download Resume (.tex)", data=resume,
                    file_name=f"resume_{company.lower().replace(' ', '_')}.tex",
                    mime="text/plain",
                )
            except RuntimeError as e:
                st.error(str(e))

        with out_cover:
            try:
                with st.spinner("Writing cover letter..."):
                    cover = generate_cover_letter(
                        api_key, context_block, style_block, job_description,
                        company, role, hiring_manager, model=selected_model
                    )
                st.text_area("Cover Letter", value=cover, height=400, label_visibility="collapsed")
                st.download_button(
                    "Download Cover Letter (.txt)", data=cover,
                    file_name=f"cover_letter_{company.lower().replace(' ', '_')}.txt",
                    mime="text/plain",
                )
            except RuntimeError as e:
                st.error(str(e))

# ── Tab 2: Founder Outreach ───────────────────────────────────────────────────
with tab_outreach:
    st.subheader("Founder Outreach")
    st.caption("Uses your fixed message template from outreach_governance.md — only fills in the placeholders.")

    col1, col2 = st.columns(2)
    with col1:
        out_company = st.text_input("Company Name", key="out_company", placeholder="e.g. Invert")
        out_founder = st.text_input("Founder Full Name", key="out_founder", placeholder="e.g. Evan Conrad")
    with col2:
        st.write("")  # spacer

    founder_research = st.text_area(
        "Founder & Company Research Notes",
        height=200,
        placeholder="""Paste what you found about the founder and company:
- YC batch (if any): e.g. W22
- What the company does (be specific, not generic)
- Founder background: previous job, school, anything public
- Recent milestone: funding round, product launch, blog post
- Any personal detail: a talk they gave, a tweet, a quote

The more specific, the better the email.""",
    )

    gen_outreach_btn = st.button("Generate Founder Outreach", type="primary", use_container_width=True, key="gen_outreach")

    if gen_outreach_btn:
        if not api_key:
            st.error("Add your Gemini API key in the sidebar.")
            st.stop()
        if not out_company or not out_founder:
            st.error("Fill in Company Name and Founder Name.")
            st.stop()
        if not outreach_governance:
            st.error("outreach_governance.md not found in data/.")
            st.stop()

        try:
            with st.spinner(f"Personalizing outreach for {out_founder} at {out_company}..."):
                outreach = generate_founder_outreach(
                    api_key, outreach_governance, out_company, out_founder,
                    founder_research, model=selected_model
                )
            st.text_area("Founder Outreach", value=outreach, height=500, label_visibility="collapsed")
            st.download_button(
                "Download Outreach (.txt)", data=outreach,
                file_name=f"outreach_{out_company.lower().replace(' ', '_')}.txt",
                mime="text/plain",
            )
        except RuntimeError as e:
            st.error(str(e))

    if not gen_outreach_btn:
        st.info(
            "Fill in the founder details and paste your research notes, "
            "then click **Generate Founder Outreach**."
        )
