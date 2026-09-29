# ComicCraft — AI Comic Story Creator

A complete FastAPI + Jinja2 Generative AI comic application.

## Features
- 5-panel comic outline generation with Gemini structured JSON
- Narration/dialogue generation with Gemini
- Comic illustration generation through Hugging Face Inference Providers
- Automatic demo mode when API keys are absent
- PDF export
- Browser UI
- JSON API
- Image test endpoint
- Automated tests

The original documentation uses older `google-generativeai`, Gemini 1.5 names and local Diffusers. This implementation keeps the requested architecture while using the current `google-genai` SDK and Hugging Face Inference Providers. Hugging Face's provider layer can run diffusion models remotely, so a large local PyTorch model is not required.

## Structure
```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_flash.py
│   │   ├── gemini_pro.py
│   │   ├── image_generator.py
│   │   ├── layout_builder.py
│   │   └── exporters.py
│   └── utils/
│       ├── __init__.py
│       └── files.py
├── templates/
├── static/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows / VS Code

Install Python 3.11+ and open this folder in VS Code.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```

For real AI:
```env
GEMINI_API_KEY=your_google_ai_studio_key
HF_TOKEN=your_huggingface_token
```

## Demo mode

No API keys are required to verify the application.

```powershell
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

Demo mode generates placeholder images but exercises the complete web → backend → layout → PDF pipeline.

## Real AI mode

Set both keys in `.env`, restart Uvicorn, then create a comic.

Pipeline:
```text
Form → FastAPI → Gemini outline → Gemini story → HF image generation
     → layout builder → PDF exporter → preview/download
```

## API

`POST /generate-comic/json`

Example:
```json
{
  "story_prompt": "A brave fox discovers a hidden library in an enchanted forest.",
  "character_name": "Milo",
  "setting": "enchanted forest",
  "tone": "adventurous",
  "art_style": "comic book"
}
```

Interactive docs:
http://127.0.0.1:8000/docs

## Tests
```powershell
pytest -q
```

## Troubleshooting

`ModuleNotFoundError`:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

AI authentication errors: check `.env` and restart Uvicorn.

If a Hugging Face image model/provider is unavailable, change:
```env
HF_PROVIDER=auto
HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell
```

Never commit `.env`.
