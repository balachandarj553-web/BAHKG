from app.config import settings
from app.models import ComicPanel, PanelOutline, PanelStory
from app.utils.files import to_static_url


def build_comic_layout(outline, stories, image_paths) -> list[ComicPanel]:
    stories_by_panel = {item.panel_number: item for item in stories}
    result = []
    for outline_item, image_path in zip(outline, image_paths):
        story = stories_by_panel[outline_item.panel_number]
        result.append(
            ComicPanel(
                panel_number=outline_item.panel_number,
                title=outline_item.title,
                scene_description=outline_item.scene_description,
                image_prompt=outline_item.image_prompt,
                narration=story.narration,
                dialogue=story.dialogue,
                caption=story.caption,
                image_url=to_static_url(image_path, settings.static_dir),
            )
        )
    return result
