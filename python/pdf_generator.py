# STRAVA-ANALYSE/python/pdf_generator.py

# Bibliotek

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

from .visning import sekunder_til_tid, hent_dato_for_Norge

# Funksjoner

def hent_stiler() -> tuple[ParagraphStyle, ParagraphStyle]:
    """
    Henter nødvendige font-stiler for å bruke emojis i tekst.

    Returns:
        ParagraphStyle: Stiler for å kunne bruke emojis som font
    """
    styles = getSampleStyleSheet()
    pdfmetrics.registerFont(TTFont('EmojiFont', 'fonts/Symbola.ttf'))
    emoji_title = ParagraphStyle(
        "EmojiTitle",
        parent=styles["Title"],
        fontName="EmojiFont"
    )
    emoji_heading = ParagraphStyle(
        "EmojiHeading2",
        parent=styles["Heading2"],
        fontName="EmojiFont"
    )
    return emoji_title, emoji_heading, styles["Normal"]

def lag_aktivitetsrapport(aktivitet: dict, kartfil: str="rute.png", pdf_fil: str="rapport.pdf") -> None:
    """
    Lager en PDF med overskrift, nøkkeltall og kartet til aktiviteten.

    Args:
        aktivitet (dict): Aktuell aktivitet returnert av Strava-APIet
        kartfil (str): Filsti til der kartet er lagret som png-fil (default: "rute.png")
        pdf_fil (str): Filsti til PDFen som skal lages (default: "rapport.pdf")
    """
    doc = SimpleDocTemplate(pdf_fil, pagesize=A4)
    tittel, header, paragraf = hent_stiler()
    story = []

    # Stor overskrift øverst
    story.append(Paragraph(f"{aktivitet['name']}", tittel))
    story.append(Spacer(1, 20))

    # Litt større undertittel
    story.append(Paragraph("📊 Nøkkeldata", header))
    story.append(Spacer(1, 10))

    # Nøkkeldata
    story.append(Paragraph(f"<b>Dato</b>: {hent_dato_for_Norge(aktivitet)}", paragraf))
    story.append(Paragraph(f"<b>Distanse</b>: {aktivitet['distance']/1000:.2f} km", paragraf))
    story.append(Paragraph(f"<b>Varighet</b>: {sekunder_til_tid(aktivitet['moving_time'])}", paragraf))
    story.append(Paragraph(f"<b>Høydemeter</b>: {aktivitet['total_elevation_gain']} m", paragraf))
    story.append(Spacer(1, 20))

    # Kart
    story.append(Paragraph("🗺️ Rute", header))
    story.append(Spacer(1, 10))
    if os.path.exists(kartfil):
        story.append(Image(kartfil, width=400, height=400))
    
    doc.build(story)
    print(f"PDF generert: {pdf_fil}")
