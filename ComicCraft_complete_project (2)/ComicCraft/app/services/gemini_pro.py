import json
from google import genai
from google.genai import types

from app.config import settings
from app.models import ComicRequest, PanelOutline, PanelStory


# Keep one Gemini client alive for the whole application.
_client_instance = None


def _client():
    global _client_instance

    if _client_instance is None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")
        _client_instance = genai.Client(api_key=settings.gemini_api_key)

    return _client_instance


def generate_story(
    request: ComicRequest,
    outline: list[PanelOutline],
) -> list[PanelStory]:

    if not settings.gemini_api_key:
        return [
            PanelStory(
                panel_number=p.panel_number,
                narration=p.scene_description,
                dialogue=f"{request.character_name}: This is only the beginning!",
                caption=f"Panel {p.panel_number} — {request.tone.title()} adventure.",
            )
            for p in outline
        ]

    outline_json = json.dumps(
        [p.model_dump() for p in outline],
        ensure_ascii=False,
    )

    prompt = f"""
Write detailed narration and dialogue for this 5-panel comic.

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Story idea:
{request.story_prompt}

Panel outline:
{outline_json}

Return exactly one object per panel.

Each object must contain:
panel_number
narration
dialogue
caption

Keep continuity.

Dialogue should be short enough for a comic panel.

Return JSON only.
"""

    response = _client().models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelStory],
            temperature=0.9,
        ),
    )

    data = json.loads(response.text)

    stories = [
        PanelStory.model_validate(item)
        for item in data
    ]

    stories.sort(key=lambda x: x.panel_number)

    if len(stories) != 5:
        raise ValueError("Gemini returned an invalid story length.")

    return stories