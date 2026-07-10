import re
from pathlib import Path


SPEC_PATH = Path(__file__).parents[1] / "references" / "generation-spec.md"
FENCE_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def headings_outside_fences(markdown: str) -> set[str]:
    headings: set[str] = set()
    fence_character: str | None = None
    fence_length = 0

    for line in markdown.splitlines():
        match = FENCE_PATTERN.match(line)
        if fence_character is None:
            if match:
                marker = match.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
            elif line.startswith("## "):
                headings.add(line)
            continue

        if not match:
            continue

        marker, suffix = match.groups()
        if (
            marker[0] == fence_character
            and len(marker) >= fence_length
            and not suffix.strip()
        ):
            fence_character = None
            fence_length = 0

    assert fence_character is None, "generation-spec.md has an unclosed code fence"
    return headings


def test_generation_steps_render_outside_code_fences():
    markdown = SPEC_PATH.read_text(encoding="utf-8")

    headings = headings_outside_fences(markdown)

    assert "## Step 8 — Generate supporting files" in headings
    assert "## Step 9 — Generate the master SKILL.md" in headings
