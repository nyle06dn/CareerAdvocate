"""
Space Optimizer — ensures the LaTeX resume fits within 1 page.

Strategy:
  1. Parse sections from the generated LaTeX.
  2. Enforce hard limits: 2–3 projects, 2–3 experiences, 1–2 leadership entries.
  3. Trim bullet points per entry to a max of 3.
  4. Estimate line count using a heuristic and remove \vspace padding if over budget.

This runs as a post-processing step after the AI generates the LaTeX.
"""

import re

# ── Hard limits ───────────────────────────────────────────────────────────────
MAX_BULLETS_PER_ENTRY = 3
SECTION_LIMITS = {
    "projects":    3,
    "experience":  3,
    "leadership":  2,
}

# Heuristic: estimated lines per LaTeX construct on a 10pt letterpaper page
LINES_PER_HEADER      = 4
LINES_PER_EDUCATION   = 5
LINES_PER_SKILLS      = 3
LINES_PER_ENTRY_BASE  = 2   # title + org line
LINES_PER_BULLET      = 1.2
LINES_PER_VSPACE      = 0.5
PAGE_LINE_BUDGET      = 58  # ~1 page at 10pt, 0.5in margins


# ── Helpers ───────────────────────────────────────────────────────────────────

def _trim_bullets(block: str, max_bullets: int = MAX_BULLETS_PER_ENTRY) -> str:
    """Keep only the first `max_bullets` \\item lines in an itemize block."""
    def _trim_itemize(m):
        content = m.group(1)
        items = re.findall(r'(    \\item .+)', content)
        kept = items[:max_bullets]
        new_content = "\n".join(kept) + "\n"
        return f"\\begin{{itemize}}[leftmargin=*,itemsep=1pt]\n{new_content}\\end{{itemize}}"
    return re.sub(
        r'\\begin\{itemize\}\[leftmargin=\*,itemsep=1pt\](.*?)\\end\{itemize\}',
        _trim_itemize,
        block,
        flags=re.DOTALL,
    )


def _split_entries(section_body: str) -> list[str]:
    """
    Split a section body into individual entries.
    Each entry starts with \\noindent\\textbf or \\textbf at line start.
    """
    pattern = r'(?=(?:\\noindent)?\\textbf\{)'
    parts = re.split(pattern, section_body)
    return [p.strip() for p in parts if p.strip()]


def _count_lines(latex: str) -> float:
    """Rough line estimate for a LaTeX resume string."""
    lines = 0.0
    lines += latex.count(r'\item ')       * LINES_PER_BULLET
    lines += latex.count(r'\vspace')      * LINES_PER_VSPACE
    lines += latex.count(r'\section')     * 1.5
    lines += latex.count(r'\\ ')          * 1.0
    lines += latex.count(r'\\[')          * 1.0
    # base structural lines
    lines += LINES_PER_HEADER + LINES_PER_EDUCATION + LINES_PER_SKILLS
    return lines


def _extract_section(latex: str, section_name: str):
    """Return (before, section_content, after) for a named section."""
    pattern = (
        r'(\\section\{' + re.escape(section_name) + r'\})'
        r'(.*?)'
        r'(?=\\section\{|\\end\{document\})'
    )
    m = re.search(pattern, latex, re.IGNORECASE | re.DOTALL)
    if not m:
        return None, None, None
    start = m.start()
    end   = m.end()
    before  = latex[:start]
    content = m.group(0)
    after   = latex[end:]
    return before, content, after


def _enforce_section_limit(section_content: str, section_title: str, max_entries: int) -> str:
    """Keep only `max_entries` entries in a section."""
    header_match = re.match(
        r'(\\section\{[^}]+\}\s*\n?)', section_content, re.IGNORECASE
    )
    if not header_match:
        return section_content
    header = header_match.group(1)
    body   = section_content[len(header):]
    entries = _split_entries(body)
    kept    = entries[:max_entries]
    return header + "\n" + "\n\n".join(kept) + "\n"


# ── Main optimizer ────────────────────────────────────────────────────────────

def optimize(latex: str) -> str:
    """
    Run all space optimization passes on the LaTeX string.
    Returns the optimized LaTeX.
    """
    # Pass 1 — trim bullets in every itemize block to MAX_BULLETS_PER_ENTRY
    latex = _trim_bullets(latex, MAX_BULLETS_PER_ENTRY)

    # Pass 2 — enforce entry limits per section
    for section_title, max_entries in SECTION_LIMITS.items():
        before, content, after = _extract_section(latex, section_title)
        if content is None:
            continue
        trimmed = _enforce_section_limit(content, section_title, max_entries)
        latex = before + trimmed + after

    # Pass 3 — if still over budget, reduce bullets to 2
    if _count_lines(latex) > PAGE_LINE_BUDGET:
        latex = _trim_bullets(latex, max_bullets=2)

    # Pass 4 — if still over budget, remove \vspace lines
    if _count_lines(latex) > PAGE_LINE_BUDGET:
        latex = re.sub(r'\\vspace\{[^}]+\}\s*\n?', '', latex)

    return latex
