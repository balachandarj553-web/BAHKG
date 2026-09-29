from app.models import ComicRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story

def test_demo_outline_has_five_panels(monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "gemini_api_key", "")
    request = ComicRequest(
        story_prompt="A fox finds a magical library.",
        character_name="Milo",
        setting="forest",
        tone="funny",
        art_style="comic book",
    )
    result = generate_outline(request)
    assert len(result) == 5
    assert result[0].panel_number == 1

def test_demo_story_has_five_panels(monkeypatch):
    from app.config import settings
    monkeypatch.setattr(settings, "gemini_api_key", "")
    request = ComicRequest(
        story_prompt="A fox finds a magical library.",
        character_name="Milo",
        setting="forest",
        tone="funny",
        art_style="comic book",
    )
    outline = generate_outline(request)
    story = generate_story(request, outline)
    assert len(story) == 5
    assert story[0].dialogue
