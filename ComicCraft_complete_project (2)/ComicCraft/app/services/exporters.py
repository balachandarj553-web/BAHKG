from fpdf import FPDF

from app.config import settings
from app.models import ComicPanel
from app.utils.files import unique_filename


def _safe_text(value: str) -> str:
    """Convert text to something the standard PDF font can render."""
    if value is None:
        return ""

    text = str(value)

    # Replace characters that standard Helvetica cannot render.
    text = text.encode("latin-1", "replace").decode("latin-1")

    # Remove problematic control characters.
    text = text.replace("\x00", " ")
    text = text.replace("\r", " ")

    return text


def _write_text(pdf, text, width=180, line_height=6):
    """
    Write text using character-based wrapping.

    Character wrapping prevents FPDF2 from failing when
    AI-generated text contains a very long word/string.
    """
    pdf.set_x(15)

    pdf.multi_cell(
        w=width,
        h=line_height,
        text=_safe_text(text),
        wrapmode="CHAR",
        new_x="LEFT",
        new_y="NEXT",
    )


def save_pdf(title: str, panels: list[ComicPanel]):
    output = settings.exports_dir / unique_filename(title, ".pdf")

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in panels:

        # New page for every comic panel.
        pdf.add_page()

        # -------------------------------------------------
        # PANEL TITLE
        # -------------------------------------------------

        pdf.set_xy(15, 15)

        pdf.set_font(
            "Helvetica",
            "B",
            18,
        )

        _write_text(
            pdf,
            f"Panel {panel.panel_number}: {panel.title}",
            width=180,
            line_height=9,
        )

        # -------------------------------------------------
        # PANEL IMAGE
        # -------------------------------------------------

        image_path = (
            settings.static_dir
            / panel.image_url.removeprefix("/static/")
        )

        if image_path.exists():

            # Keep image inside the A4 page.
            pdf.image(
                str(image_path),
                x=15,
                y=35,
                w=180,
            )

        # -------------------------------------------------
        # TEXT INFORMATION
        # -------------------------------------------------

        pdf.set_y(175)

        sections = [
            ("Scene", panel.scene_description),
            ("Caption", panel.caption),
            ("Narration", panel.narration),
            ("Dialogue", panel.dialogue),
        ]

        for heading, text in sections:

            # Heading
            pdf.set_x(15)

            pdf.set_font(
                "Helvetica",
                "B",
                11,
            )

            _write_text(
                pdf,
                heading,
                width=180,
                line_height=7,
            )

            # Content
            pdf.set_x(15)

            pdf.set_font(
                "Helvetica",
                "",
                10,
            )

            _write_text(
                pdf,
                text,
                width=180,
                line_height=6,
            )

            pdf.ln(2)

    pdf.output(str(output))

    return output