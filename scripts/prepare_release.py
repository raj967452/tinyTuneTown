#!/usr/bin/env python3
"""Prepare a rights-gated original-content release package for human review."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

BLOCKED_REFERENCES = ("sunrisejunglebeat",)
REQUIRED_FIELDS = ("title", "audience", "language", "concept", "lyrics", "visual_direction", "rights")
REQUIRED_RIGHTS = ("lyrics", "music", "visuals", "samples")
ALLOWED_RIGHTS = {"original", "licensed", "none", "public-domain"}


def slugify(value: str) -> str:
    """Return a stable filesystem-safe release identifier."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "untitled-release"


def validate(brief: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if not brief.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    serialized = json.dumps(brief).lower()
    if any(reference in serialized for reference in BLOCKED_REFERENCES):
        raise ValueError("Reference-channel material is not allowed. Use an original, licensed, or public-domain brief.")

    rights = brief["rights"]
    if not isinstance(rights, dict):
        raise ValueError("rights must be an object")
    missing_rights = [item for item in REQUIRED_RIGHTS if item not in rights]
    if missing_rights:
        raise ValueError(f"Missing rights declarations: {', '.join(missing_rights)}")
    invalid = [item for item in REQUIRED_RIGHTS if rights[item] not in ALLOWED_RIGHTS]
    if invalid:
        raise ValueError(f"Unsupported rights declaration for: {', '.join(invalid)}")


def make_metadata(brief: dict[str, Any]) -> dict[str, Any]:
    hashtags = list(dict.fromkeys(brief.get("hashtags", [])))
    tags = list(dict.fromkeys(brief.get("keywords", [])))
    description = (
        f"{brief['concept']}\n\n"
        f"Made for {brief['audience']}. This is an original production.\n\n"
        f"{brief['lyrics']}\n\n"
        f"{' '.join(hashtags)}"
    )
    return {
        "title": brief["title"],
        "description": description,
        "tags": tags,
        "hashtags": hashtags,
        "thumbnail_brief": (
            f"Create an original high-contrast thumbnail for '{brief['title']}' with one clear focal "
            "character, large readable title text, and no third-party characters, logos, or copied artwork."
        ),
    }


def prepare(brief: dict[str, Any], output_root: Path) -> Path:
    validate(brief)
    release_dir = output_root / slugify(brief["title"])
    release_dir.mkdir(parents=True, exist_ok=True)
    metadata = make_metadata(brief)
    digen_job = {
        "job_type": "original_music_video",
        "title": brief["title"],
        "language": brief["language"],
        "creative_brief": {
            "concept": brief["concept"],
            "lyrics": brief["lyrics"],
            "visual_direction": brief["visual_direction"],
        },
        "rights_attestation": brief["rights"],
        "prohibited_inputs": ["third-party video", "third-party lyrics", "channel transcripts", "branded characters"],
        "submission_note": "Submit only through an authorized Digen account or documented API integration after human rights review.",
    }
    (release_dir / "digen-job.json").write_text(json.dumps(digen_job, indent=2) + "\n", encoding="utf-8")
    (release_dir / "youtube-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    checklist = """# Required release review\n\n- [ ] I own or have documented adaptation and YouTube publishing rights for all lyrics.\n- [ ] I own or have documented rights for music, vocals, visuals, samples, and thumbnail assets.\n- [ ] The Digen output does not copy another creator's footage, lyrics, branding, or distinctive characters.\n- [ ] I reviewed the title, description, tags, hashtags, and thumbnail for accuracy.\n- [ ] I will upload using my authorized YouTube account and retain rights records.\n"""
    (release_dir / "review-checklist.md").write_text(checklist, encoding="utf-8")
    return release_dir


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: prepare_release.py BRIEF.json", file=sys.stderr)
        return 2
    try:
        brief = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        output = prepare(brief, Path("out"))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Prepared original-content release package: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
