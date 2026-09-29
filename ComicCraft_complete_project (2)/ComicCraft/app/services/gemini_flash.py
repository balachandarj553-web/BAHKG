import json
from google import genai
from google.genai import types

from app.config import settings
from app.models import ComicRequest, PanelOutline


# Keep one Gemini client alive for the whole application.
_client_instance = None


def _client():
    global _client_instance

    if _client_instance is None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        _client_instance = genai.Client(api_key=settings.gemini_api_key)

    return _client_instance


def generate_outline(request: ComicRequest) -> list[PanelOutline]:
    if not settings.gemini_api_key:
        data = [
            (
                "The Idea",
                f"{request.character_name} begins an unexpected adventure in the {request.setting}.",
            ),
            (
                "The Discovery",
                f"{request.character_name} discovers something unusual in the {request.setting}.",
            ),
            (
                "The Challenge",
                f"A difficult problem tests {request.character_name}'s courage.",
            ),
            (
                "The Turning Point",
                f"{request.character_name} finds a clever way to overcome the challenge.",
            ),
            (
                "A New Beginning",
                f"The adventure ends with a hopeful new beginning.",
            ),
        ]

        return [
            PanelOutline(
                panel_number=i,
                title=title,
                scene_description=description,
                image_prompt=(
                    f"{request.art_style}, {description}, "
                    "cinematic comic illustration, expressive characters, clean composition"
                ),
            )
            for i, (title, description) in enumerate(data, 1)
        ]

    prompt = f"""
Create exactly 5 connected comic panels.

Story idea:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Return only a JSON array.

Every item must contain:
panel_number (1-5)
title
scene_description
image_prompt

Keep the character appearance, setting, lighting and visual style
consistent across all panels.
"""

    response = _client().models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelOutline],
            temperature=0.8,
        ),
    )

    data = json.loads(response.text)

    panels = [
        PanelOutline.model_validate(item)
        for item in data
    ]

    panels.sort(key=lambda x: x.panel_number)

    if len(panels) != 5:
        raise ValueError("Gemini returned an invalid number of panels.")

    return panels