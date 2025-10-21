# STRAVA-ANALYSE/python/pdf_generator.py

# Bibliotek

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle

from .geo import lag_rutekart
from .visning import hent_dato_for_Norge, sekunder_til_tid

# Funksjoner

def hent_stiler() -> tuple[ParagraphStyle, ParagraphStyle, ParagraphStyle]:
    """
    Henter nødvendige font-stiler for å bruke emojis i tekst.

    Returns:
        ParagraphStyle: Font-stiler som kan brukes i PDFen, inkludert støtte for emojier
    """
    styles = getSampleStyleSheet()
    font = "EmojiFont"
    pdfmetrics.registerFont(TTFont('EmojiFont', 'fonts/Symbola.ttf'))
    emoji_title = ParagraphStyle(
        "EmojiTitle",
        parent=styles["Title"],
        fontName=font,
        textColor=colors.HexColor("#FF6F00"),
        fontSize=24,
        leading=28,
        alignment=1
    )
    emoji_heading = ParagraphStyle(
        "EmojiHeading2",
        parent=styles["Heading2"],
        fontName=font
    )
    return emoji_title, emoji_heading, font

def footer(canvas: Canvas, font: str, doc) -> None:
    """
    Tegner en fast bunntekst på hver side i PDF-en.

    Args:
        canvas (Canvas): ReportLab Canvas-objektet som brukes til å tegne innhold på siden
        font (str): Font som skal brukes på teksten
        doc (BaseDocTemplate): Dokumentobjektet som inneholder layout og metadata for PDF-en
    """
    canvas.saveState()
    canvas.setFont(font, 8)
    canvas.drawString(40, 20, "Generert med Strava API 🚴")
    canvas.restoreState()

def lag_aktivitetsrapport(aktivitet: dict, pdf_fil: str="rapport.pdf") -> None:
    """
    Lager en PDF med overskrift, nøkkeltall og kartet til aktiviteten.

    Args:
        aktivitet (dict): Aktuell aktivitet returnert av Strava-APIet
        pdf_fil (str): Filsti til PDFen som skal lages (default: "rapport.pdf")
    """
    doc = BaseDocTemplate(pdf_fil, pagesize=A4)
    kart_bredde = doc.width * 0.95
    kart_img = lag_rutekart(aktivitet, kart_bredde)

    if kart_img:
        tittel, header, paragraf = hent_stiler()
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
        template = PageTemplate(id="footer", frames=frame, onPage=lambda canvas, doc: footer(canvas, paragraf, doc))
        doc.addPageTemplates([template])
        story = []

        # Stor overskrift øverst
        tittel_tabell = Table(
            [[Paragraph(f"{aktivitet['name']}", tittel)]],
            colWidths=[doc.width]
        )
        tittel_tabell.setStyle(TableStyle([
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("BOTTOMPADDING", (0,0), (-1,-1), 16),
            ("TOPPADDING", (0,0), (-1,-1), 16)
        ]))
        story.append(tittel_tabell)
        story.append(Spacer(1, 15))

        # Litt større undertittel
        story.append(Paragraph("📊 Nøkkeldata", header))
        story.append(Spacer(1, 10))

        # Nøkkeldata
        data = [
            ["📅 Dato", hent_dato_for_Norge(aktivitet)],
            ["📏 Distanse", f"{aktivitet['distance']/1000:.2f} km"],
            ["⏱️ Varighet", sekunder_til_tid(aktivitet['moving_time'])],
            ["⛰️ Høydemeter", f"{aktivitet['total_elevation_gain']} m"]
        ]
        tabell = Table(data, colWidths=[100, doc.width-100])
        tabell.setStyle(TableStyle([
            ("TEXTCOLOR", (0,0), (-1,-1), colors.black),
            ("ALIGN", (0,0), (0,-1), "RIGHT"),
            ("ALIGN", (1,0), (1,-1), "LEFT"),
            ("FONTNAME", (0,0), (-1,-1), paragraf),
            ("FONTSIZE", (0,0), (-1,-1), 11),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
        ]))
        story.append(tabell)
        story.append(Spacer(1, 25))

        # Kart
        story.append(Paragraph("🗺️ Rute", header))
        story.append(Spacer(1, 10))
        
        kart_tabell = Table([[kart_img]], colWidths=[kart_bredde])
        kart_tabell.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 2.5, colors.HexColor("#FF6F00")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("BACKGROUND", (0,0), (-1,-1), colors.whitesmoke)
        ]))
        story.append(kart_tabell)

        doc.build(story)
        print(f"PDF generert: {pdf_fil}")
    else:
        print("Kartet kunne ikke genereres på rett måte.")
