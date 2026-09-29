from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models import ComicRequest, ComicResponse
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf
from app.utils.files import to_static_url

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def create_comic(data: ComicRequest) -> ComicResponse:
    outline = generate_outline(data)
    stories = generate_story(data, outline)

    image_paths = []
    demo_mode = False
    for panel in outline:
        path, demo = generate_image(panel.image_prompt, panel.panel_number)
        image_paths.append(path)
        demo_mode = demo_mode or demo

    layout = build_comic_layout(outline, stories, image_paths)
    title = f"{data.character_name}'s Adventure"
    pdf_path = save_pdf(title, layout)

    return ComicResponse(
        title=title,
        panels=layout,
        pdf_url=to_static_url(pdf_path, settings.static_dir),
        demo_mode=demo_mode,
    )


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name, "ai_enabled": settings.ai_enabled},
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        result = create_comic(data)
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context=result.model_dump(),
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={"error": str(exc), "ai_enabled": settings.ai_enabled},
            status_code=500,
        )


@router.post("/generate-comic/json", response_model=ComicResponse)
async def generate_json(payload: ComicRequest):
    try:
        return create_comic(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"app_name": settings.app_name, "ai_enabled": settings.ai_enabled},
    )


@router.get("/test-image")
async def test_image(prompt: str = "A friendly robot in a colorful comic book city"):
    try:
        path, demo = generate_image(prompt, 0)
        return {"image_url": to_static_url(path, settings.static_dir), "demo_mode": demo}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
