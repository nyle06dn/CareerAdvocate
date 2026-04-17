"""Gemini-backed generators for resume, cover letter, and cold email."""

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InvalidArgument
from src.prompts import (
    SYSTEM_CAREER_AGENT,
    resume_prompt,
    cover_letter_prompt,
    founder_outreach_prompt,
)
DEFAULT_MODEL = "gemini-2.5-flash-lite-preview-06-17"


def _call(api_key: str, system: str, user: str, model: str) -> str:
    genai.configure(api_key=api_key)
    gemini = genai.GenerativeModel(
        model_name=model,
        system_instruction=system,
    )
    try:
        response = gemini.generate_content(
            user,
            generation_config=genai.types.GenerationConfig(temperature=0.7),
        )
        return response.text.strip()

    except ResourceExhausted:
        raise RuntimeError(
            f"⚠️ Quota exceeded for **{model}**.\n\n"
            "**Fix:** Select a different model from the sidebar dropdown and try again.\n"
            "Common alternatives: `gemini-1.5-flash`, `gemini-2.0-flash-lite`\n\n"
            "If all models are exhausted, wait until tomorrow or add billing at aistudio.google.com."
        )

    except InvalidArgument:
        raise RuntimeError(
            f"⚠️ Model **{model}** not found or API key is invalid.\n\n"
            "**Fix:** Select a different model from the sidebar dropdown."
        )


def generate_resume(
    api_key: str,
    context_block: str,
    format_block: str,
    governance_block: str,
    job_description: str,
    company: str,
    role: str,
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = resume_prompt(context_block, format_block, governance_block, job_description, company, role)
    return _call(api_key, SYSTEM_CAREER_AGENT, prompt, model)


def generate_cover_letter(
    api_key: str,
    context_block: str,
    style_block: str,
    job_description: str,
    company: str,
    role: str,
    hiring_manager: str = "",
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = cover_letter_prompt(
        context_block, style_block, job_description, company, role, hiring_manager
    )
    return _call(api_key, SYSTEM_CAREER_AGENT, prompt, model)


def generate_founder_outreach(
    api_key: str,
    governance_block: str,
    company: str,
    founder_name: str,
    founder_research: str,
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = founder_outreach_prompt(governance_block, company, founder_name, founder_research)
    return _call(api_key, SYSTEM_CAREER_AGENT, prompt, model)
