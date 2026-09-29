from pydantic import BaseModel, Field


class ComicRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=60)
    art_style: str = Field(min_length=1, max_length=80)


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    image_prompt: str


class PanelStory(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    narration: str
    dialogue: str
    caption: str


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    narration: str
    dialogue: str
    caption: str
    image_url: str = ""


class ComicResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_url: str | None = None
    demo_mode: bool = False
