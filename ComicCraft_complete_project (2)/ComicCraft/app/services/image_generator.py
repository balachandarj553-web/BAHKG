import base64
from pathlib import Path

from google import genai

from app.config import settings
from app.utils.files import unique_filename


_client_instance = None


def _client():
    global _client_instance

    if _client_instance is None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        _client_instance = genai.Client(
            api_key=settings.gemini_api_key
        )

    return _client_instance


def generate_image(prompt: str, panel_number: int) -> tuple[Path, bool]:

    if not settings.gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Please configure it in .env."
        )

    output = (
        settings.panels_dir
        / unique_filename(
            f"panel-{panel_number}",
            ".png"
        )
    )

    image_prompt = f"""
Create a high-quality comic-book illustration for a college
Generative AI project.

Scene:
{prompt}

Requirements:
- detailed comic book illustration
- expressive characters
- cinematic lighting
- clear foreground and background
- visually attractive
- consistent character appearance
- no text, captions, speech bubbles, logos or watermarks
- landscape composition suitable for a comic panel
"""

    interaction = _client().interactions.create(
        model=settings.gemini_image_model,
        input=image_prompt,
        response_format={
            "type": "image",
            "aspect_ratio": "4:3",
        },
    )

    image_data = None

    # Preferred output location.
    if getattr(interaction, "output_image", None):
        image_data = interaction.output_image.data

    # Fallback: search through model output steps.
    if not image_data and getattr(interaction, "steps", None):
        for step in interaction.steps:
            if getattr(step, "type", None) != "model_output":
                continue

            for content_block in getattr(step, "content", []):
                if getattr(content_block, "type", None) == "image":
                    image_data = content_block.data
                    break

            if image_data:
                break

    if not image_data:
        raise RuntimeError(
            "Gemini returned no image for this panel."
        )

    image_bytes = base64.b64decode(image_data)

    with open(output, "wb") as f:
        f.write(image_bytes)

    return output, False