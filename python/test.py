import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# 1. Lag en graf
x = [1, 2, 3, 4, 5]
y = [3, 5, 7, 10, 15]
plt.plot(x, y, marker="o")
plt.title("Treningsfremgang - Knebøy")
plt.xlabel("Uker")
plt.ylabel("kg")
plt.savefig("graf.png")
plt.close()

# 2. Sett opp PDF
doc = SimpleDocTemplate("treningsrapport.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = []

# Tittel
story.append(Paragraph("🏋️ Treningsrapport - September", styles["Title"]))
story.append(Spacer(1, 20))

# Tekst
story.append(Paragraph("Fremgang i knebøy de siste 5 ukene:", styles["Normal"]))
story.append(Spacer(1, 10))

# Bilde (graf)
story.append(Image("graf.png", width=400, height=300))

# Generer PDF
doc.build(story)
