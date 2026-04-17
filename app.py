"""Personal Career AI Agent — Streamlit UI"""

import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

from src.memory import load_user_context, format_context_block, format_style_block
from src.generators import generate_resume, generate_cover_letter, generate_cold_email, DEFAULT_MODEL

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career AI Agent",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Personal Career AI Agent")
st.caption("Tailored resume · Cover letter · Cold email — grounded in your actual story.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Configuration")

    api_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Get yours free at aistudio.google.com/app/apikey",
    )

    st.divider()

    # ── Model selector ────────────────────────────────────────────────────────
    st.subheader("🤖 Model")

    # Fetch available models when API key is entered
    if api_key:
        try:
            genai.configure(api_key=api_key)
            available_models = [
                m.name.replace("models/", "")
                for m in genai.list_models()
                if "generateContent" in m.supported_generation_methods
            ]
        except Exception:
            available_models = [DEFAULT_MODEL]
    else:
        available_models = [DEFAULT_MODEL]

    # Default to DEFAULT_MODEL if available, else first in list
    default_index = (
        available_models.index(DEFAULT_MODEL)
        if DEFAULT_MODEL in available_models
        else 0
    )

    selected_model = st.selectbox(
        "Active Model",
        options=available_models,
        index=default_index,
        help="Models are fetched live from your API key. Select one and it's used immediately.",
    )

    st.caption(f"Using: `{selected_model}`")

    st.divider()

    # ── Memory status ─────────────────────────────────────────────────────────
    st.subheader("Memory Status")

    ctx = load_user_context()
    for label, key, path in [
        ("Profile",         "profile",         "data/profile.md"),
        ("Skills",          "skills",          "data/skills.md"),
        ("Projects",        "projects",        "data/projects.md"),
        ("Stories",         "stories",         "data/stories.md"),
        ("Writing Samples", "writing_samples", "data/writing_samples/"),
    ]:
        filled = bool(ctx[key] and "[" not in ctx[key][:80])
        icon = "✅" if filled else "⚠️"
        st.write(f"{icon} `{path}`")

    st.divider()
    st.caption("Edit the files in `data/` to add your real info. The AI reads them on every run.")

# ── Main form ─────────────────────────────────────────────────────────────────
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
    recipient_title = st.text_input(
        "Cold Email Recipient Title",
        value="Head of Engineering",
        placeholder="e.g. VP of Product, Director of Data Science",
    )

job_description = st.text_area(
    "Paste the Job Description",
    height=250,
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
Medpace is a full-service clinical contract research organization (CRO). We provide Phase I-IV clinical development services to the biotechnology, pharmaceutical and medical device industries. Our mission is to accelerate the global development of safe and effective medical therapeutics through its scientific and disciplined approach. We leverage local regulatory and therapeutic expertise across all major areas including oncology, cardiology, metabolic disease, endocrinology, central nervous system, anti-viral and anti-infective. Headquartered in Cincinnati, Ohio, employing more than 5,000 people across 40+ countries.

Why Medpace?:
People. Purpose. Passion. Make a Difference Tomorrow. Join Us Today.

The work we've done over the past 30+ years has positively impacted the lives of countless patients and families who face hundreds of diseases across all key therapeutic areas. The work we do today will improve the lives of people living with illness and disease in the future.""",
)

generate_btn = st.button("Generate All Three Outputs", type="primary", use_container_width=True)

# ── Generation ────────────────────────────────────────────────────────────────
if generate_btn:
    if not api_key:
        st.error("Add your Gemini API key in the sidebar.")
        st.stop()
    if not company or not role or not job_description:
        st.error("Fill in Company, Role, and Job Description before generating.")
        st.stop()

    context_block = format_context_block(ctx)
    style_block = format_style_block(ctx)

    tab_resume, tab_cover, tab_email = st.tabs(
        ["Tailored Resume", "Cover Letter", "Cold Email"]
    )

    with tab_resume:
        try:
            with st.spinner(f"Crafting your 1-page tailored resume with {selected_model}..."):
                resume = generate_resume(
                    api_key, context_block, job_description, company, role, model=selected_model
                )
            st.text_area("Resume", value=resume, height=600, label_visibility="collapsed")
            st.download_button(
                "Download Resume (.txt)",
                data=resume,
                file_name=f"resume_{company.lower().replace(' ', '_')}.txt",
                mime="text/plain",
            )
        except RuntimeError as e:
            st.error(str(e))

    with tab_cover:
        try:
            with st.spinner("Writing your personalized cover letter..."):
                cover = generate_cover_letter(
                    api_key, context_block, style_block, job_description,
                    company, role, hiring_manager, model=selected_model
                )
            st.text_area("Cover Letter", value=cover, height=400, label_visibility="collapsed")
            st.download_button(
                "Download Cover Letter (.txt)",
                data=cover,
                file_name=f"cover_letter_{company.lower().replace(' ', '_')}.txt",
                mime="text/plain",
            )
        except RuntimeError as e:
            st.error(str(e))

    with tab_email:
        try:
            with st.spinner("Drafting your cold outreach email..."):
                email = generate_cold_email(
                    api_key, context_block, style_block, company,
                    role, recipient_title, model=selected_model
                )
            st.text_area("Cold Email", value=email, height=300, label_visibility="collapsed")
            st.download_button(
                "Download Cold Email (.txt)",
                data=email,
                file_name=f"cold_email_{company.lower().replace(' ', '_')}.txt",
                mime="text/plain",
            )
        except RuntimeError as e:
            st.error(str(e))

    st.success("Done! Review each tab, copy, and send.")

else:
    st.info(
        "Fill in the job details above and click **Generate All Three Outputs**. "
        "Make sure your `data/` files contain your real information first."
    )
