"""Gemini-backed generators for resume, cover letter, and cold email."""

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, InvalidArgument
from src.prompts import (
    SYSTEM_CAREER_AGENT,
    resume_prompt,
    cover_letter_prompt,
    cold_email_prompt,
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
    job_description: str,
    company: str,
    role: str,
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = resume_prompt(context_block, job_description, company, role)
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


def generate_cold_email(
    api_key: str,
    context_block: str,
    style_block: str,
    company: str,
    role: str,
    recipient_title: str = "Head of Engineering",
    model: str = DEFAULT_MODEL,
) -> str:
    prompt = cold_email_prompt(context_block, style_block, company, role, recipient_title)
    return _call(api_key, SYSTEM_CAREER_AGENT, prompt, model)
