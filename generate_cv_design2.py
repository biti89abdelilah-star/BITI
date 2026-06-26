from pathlib import Path
import textwrap

OUTPUT = Path("cv_fatima_ez_zine_design2.pdf")
PAGE_W, PAGE_H = 595, 842  # A4 portrait in PDF points
SIDEBAR_W = 218
BEIGE = "0.78 0.64 0.51 rg"
CREAM = "0.97 0.93 0.89 rg"
INK = "0.10 0.22 0.25 rg"
MUTED = "0.54 0.45 0.38 rg"
WHITE = "1 1 1 rg"

profile = [
    ("CIN", "IB128254"),
    ("Téléphone", "06 50 61 19 23"),
    ("Adresse", "Dakhla"),
    ("Naissance", "11/12/1974"),
    ("Situation", "Célibataire"),
]

formations = [
    "Permis de conduire catégorie B.",
    "Formation en tant qu'agent de nettoyage au sein de la société BENLHASSAN.",
]

experiences = [
    ("Agent de nettoyage", "USINE BENLHASSAN, DAKHLA", "4 années", [
        "Respect des normes d'hygiène et exécution rigoureuse des tâches de nettoyage.",
        "Organisation du travail quotidien avec sérieux, efficacité et sens des responsabilités.",
    ]),
    ("Traitement des produits de la mer", "KING PELAGIQUE", "1 année", [
        "Participation aux opérations de traitement des produits de la mer.",
        "Application des consignes de qualité, d'hygiène et de sécurité.",
    ]),
    ("Employée polyvalente", "FIRME MARTIL", "1 année", [
        "Participation aux différentes tâches confiées.",
        "Contribution au bon déroulement des activités de l'entreprise.",
    ]),
]

competences = [
    "Esprit d'équipe",
    "Grande capacité d'adaptation et de travail",
    "Sens des responsabilités",
    "Rigueur et sérieux dans l'exécution des tâches confiées",
]


def enc(text: str) -> str:
    return text.replace("\u2019", "'").encode("cp1252", "replace").decode("cp1252")


def esc(text: str) -> str:
    return enc(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


ops = []

def raw(s): ops.append(s)
def rect(x, y, w, h, color): raw(f"q {color} {x} {y} {w} {h} re f Q")
def stroke_rect(x, y, w, h, color="0.10 0.22 0.25 RG", width=1): raw(f"q {color} {width} w {x} {y} {w} {h} re S Q")
def line(x1, y1, x2, y2, color="0.78 0.64 0.51 RG", width=0.8): raw(f"q {color} {width} w {x1} {y1} m {x2} {y2} l S Q")
def text(x, y, value, size=10, font="F1", color=INK): raw(f"BT /{font} {size} Tf {color} {x} {y} Td ({esc(value)}) Tj ET")
def wrap(value, chars): return textwrap.wrap(enc(value), width=chars, break_long_words=False)

def circle(cx, cy, r, fill=None, stroke="1 1 1 RG", width=1.4):
    # Four cubic Bézier curves approximate a circle.
    k = 0.5522847498 * r
    parts = [
        f"{cx+r} {cy} m",
        f"{cx+r} {cy+k} {cx+k} {cy+r} {cx} {cy+r} c",
        f"{cx-k} {cy+r} {cx-r} {cy+k} {cx-r} {cy} c",
        f"{cx-r} {cy-k} {cx-k} {cy-r} {cx} {cy-r} c",
        f"{cx+k} {cy-r} {cx+r} {cy-k} {cx+r} {cy} c",
        "h",
    ]
    style = ""
    if fill and stroke:
        style = f"{fill} {stroke} {width} w " + " ".join(parts) + " B"
    elif fill:
        style = f"{fill} " + " ".join(parts) + " f"
    else:
        style = f"{stroke} {width} w " + " ".join(parts) + " S"
    raw(f"q {style} Q")

# Background and sidebar
rect(0, 0, PAGE_W, PAGE_H, CREAM)
rect(0, 0, SIDEBAR_W, PAGE_H, BEIGE)

# Decorative dots similar to the sample design
for row in range(5):
    for col in range(7):
        circle(22 + col * 28, PAGE_H - 30 - row * 27, 2.4, fill=WHITE, stroke=None)
for row in range(6):
    for col in range(6):
        circle(420 + col * 26, 210 - row * 23, 2.1, fill="0.88 0.80 0.72 rg", stroke=None)

# Empty photo placeholder for later insertion
circle(109, 675, 76, fill="0.94 0.86 0.78 rg", stroke="1 1 1 RG", width=2)
text(81, 674, "PHOTO", 13, "F2", "0.65 0.52 0.42 rg")
text(67, 654, "à ajouter plus tard", 8.5, "F1", "0.65 0.52 0.42 rg")

# Sidebar content
x = 48
y = 540
text(x, y, "COORDONNÉES", 14, "F2", INK)
y -= 34
for label, value in profile:
    text(x, y, label.upper(), 7.8, "F2", MUTED)
    text(x, y - 14, value, 9.4, "F1", INK)
    y -= 40

y -= 6
text(x, y, "LANGUES", 14, "F2", INK)
y -= 31
text(x, y, "Arabe", 9.5, "F2", INK)
text(x + 68, y, "Langue maternelle", 9.3, "F1", INK)

y -= 60
text(x, y, "FORMATION", 14, "F2", INK)
y -= 28
for item in formations:
    for ln in wrap(item, 25):
        text(x, y, ln, 8.8, "F1", INK)
        y -= 12
    y -= 7

# Main column header
mx = SIDEBAR_W + 48
text(mx, 745, "FATIMA EZ-ZINE", 30, "F3", INK)
text(mx, 711, "AGENT DE NETTOYAGE  |  EMPLOYÉE POLYVALENTE", 11.5, "F2", MUTED)

summary = "Professionnelle sérieuse, rigoureuse et polyvalente, avec une expérience confirmée dans le nettoyage, l'hygiène, le traitement des produits de la mer et les tâches opérationnelles en entreprise."
sy = 674
for ln in wrap(summary, 56):
    text(mx, sy, ln, 9.4, "F1", INK)
    sy -= 13

# Experience section
section_y = 575
text(mx, section_y, "EXPÉRIENCE PROFESSIONNELLE", 15, "F2", MUTED)
line(mx, section_y - 11, PAGE_W - 45, section_y - 11)
y = section_y - 43
for role, company, period, bullets in experiences:
    text(mx, y, role, 12, "F2", INK)
    text(mx, y - 17, company, 9.8, "F2", MUTED)
    text(PAGE_W - 112, y - 17, period, 8.8, "F2", INK)
    y -= 39
    for bullet in bullets:
        lines = wrap(bullet, 50)
        text(mx + 8, y, "•", 8.8, "F2", INK)
        for j, ln in enumerate(lines):
            text(mx + 21, y - j * 12, ln, 8.6, "F1", INK)
        y -= max(1, len(lines)) * 12 + 7
    y -= 13

# Skills section
text(mx, y, "COMPÉTENCES", 15, "F2", MUTED)
line(mx, y - 11, PAGE_W - 45, y - 11)
y -= 40
left_skills = competences[:2]
right_skills = competences[2:]
for i, item in enumerate(left_skills):
    text(mx + 8, y - i * 35, "•", 9, "F2", INK)
    for j, ln in enumerate(wrap(item, 26)):
        text(mx + 22, y - i * 35 - j * 12, ln, 8.8, "F1", INK)
for i, item in enumerate(right_skills):
    text(mx + 162, y - i * 35, "•", 9, "F2", INK)
    for j, ln in enumerate(wrap(item, 27)):
        text(mx + 176, y - i * 35 - j * 12, ln, 8.8, "F1", INK)

# Footer line
line(mx, 40, PAGE_W - 45, 40, "0.86 0.77 0.68 RG", 0.6)
text(mx, 25, "Curriculum Vitae — FATIMA EZ-ZINE", 8.2, "F1", MUTED)

content = "\n".join(ops).encode("cp1252", "replace")
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R /F3 6 0 R >> >> /Contents 7 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic /Encoding /WinAnsiEncoding >>",
    b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream",
]

pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets = [0]
for idx, obj in enumerate(objects, 1):
    offsets.append(len(pdf))
    pdf.extend(f"{idx} 0 obj\n".encode())
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")
xref = len(pdf)
pdf.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
for off in offsets[1:]:
    pdf.extend(f"{off:010d} 00000 n \n".encode())
pdf.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
OUTPUT.write_bytes(pdf)
print(f"Created {OUTPUT} ({len(pdf)} bytes)")
