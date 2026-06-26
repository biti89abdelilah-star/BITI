from pathlib import Path
import textwrap

OUTPUT = Path("cv_fatima_ez_zine.pdf")
PAGE_W, PAGE_H = 595, 842  # A4 in points
MARGIN = 48
BLUE = "0.08 0.22 0.40 rg"
DARK = "0.10 0.10 0.10 rg"
GREY = "0.35 0.35 0.35 rg"
LIGHT = "0.92 0.95 0.98 rg"

profile = [
    ("Adresse", "Dakhla"),
    ("CIN", "IB128254"),
    ("Téléphone", "06 50 61 19 23"),
    ("Date de naissance", "11/12/1974"),
    ("Situation familiale", "Célibataire"),
]

sections = [
    ("FORMATION ET DIPLÔMES", [
        "Permis de conduire catégorie B.",
        "Formation en tant qu’agent de nettoyage au sein de la société BENLHASSAN.",
    ]),
    ("EXPÉRIENCE PROFESSIONNELLE", [
        "4 années d’expérience en qualité d’agent de nettoyage au sein de l’usine BENLHASSAN à Dakhla, avec respect des normes d’hygiène et exécution des tâches de nettoyage de manière rigoureuse et efficace.",
        "1 année d’expérience dans le domaine du traitement des produits de la mer au sein de la société KING PELAGIQUE.",
        "Employée polyvalente au sein de la FIRME MARTIL pendant 1 année, avec participation aux différentes tâches confiées et contribution au bon déroulement des activités de l’entreprise.",
    ]),
    ("COMPÉTENCES", [
        "Esprit d’équipe.",
        "Grande capacité d’adaptation et de travail.",
        "Sens des responsabilités.",
        "Rigueur et sérieux dans l’exécution des tâches confiées.",
    ]),
    ("LANGUES", [
        "Arabe : Langue maternelle.",
    ]),
]


def enc(text: str) -> str:
    return text.replace("\u2019", "'").encode("cp1252", "replace").decode("cp1252")


def esc(text: str) -> str:
    return enc(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


ops = []

def raw(s): ops.append(s)
def fill_rect(x, y, w, h, color): raw(f"q {color} {x} {y} {w} {h} re f Q")
def line(x1, y1, x2, y2, color="0.70 0.70 0.70 RG", width=0.8): raw(f"q {color} {width} w {x1} {y1} m {x2} {y2} l S Q")
def text(x, y, value, size=10, font="F1", color=DARK): raw(f"BT /{font} {size} Tf {color} {x} {y} Td ({esc(value)}) Tj ET")

def wrapped(text_value, width_chars):
    return textwrap.wrap(enc(text_value), width=width_chars, break_long_words=False)

# Header: professional, feminine-neutral, no photo
fill_rect(0, PAGE_H - 142, PAGE_W, 142, LIGHT)
fill_rect(0, PAGE_H - 142, 14, 142, BLUE)
text(MARGIN, PAGE_H - 70, "FATIMA EZ-ZINE", 25, "F2", BLUE)
text(MARGIN, PAGE_H - 96, "Agent de nettoyage | Employée polyvalente", 12, "F1", GREY)
line(MARGIN, PAGE_H - 116, PAGE_W - MARGIN, PAGE_H - 116, "0.08 0.22 0.40 RG", 1.2)

# Personal information block
x1, x2 = MARGIN, 318
y = PAGE_H - 165
text(x1, y, "INFORMATIONS PERSONNELLES", 12, "F2", BLUE)
y -= 22
for i, (label, value) in enumerate(profile):
    x = x1 if i < 3 else x2
    yy = y - (i % 3) * 22
    text(x, yy, f"{label} :", 9.5, "F2", GREY)
    text(x + 100, yy, value, 9.5, "F1", DARK)

# Summary
summary_y = y - 82
text(MARGIN, summary_y, "PROFIL PROFESSIONNEL", 12, "F2", BLUE)
line(MARGIN, summary_y - 8, PAGE_W - MARGIN, summary_y - 8)
summary = "Professionnelle sérieuse, rigoureuse et polyvalente, disposant d’une expérience confirmée dans le nettoyage, l’hygiène, le traitement des produits de la mer et les tâches opérationnelles en entreprise."
ty = summary_y - 28
for ln in wrapped(summary, 92):
    text(MARGIN, ty, ln, 10.5)
    ty -= 15

# Sections
y = ty - 18
for title, bullets in sections:
    text(MARGIN, y, title, 12, "F2", BLUE)
    line(MARGIN, y - 8, PAGE_W - MARGIN, y - 8)
    y -= 28
    for bullet in bullets:
        lines = wrapped(bullet, 87)
        text(MARGIN + 4, y, "•", 10.5, "F2", BLUE)
        for j, ln in enumerate(lines):
            text(MARGIN + 20, y - j * 15, ln, 10.2)
        y -= max(1, len(lines)) * 15 + 9
    y -= 8

# Footer
line(MARGIN, 42, PAGE_W - MARGIN, 42, "0.82 0.82 0.82 RG", 0.6)
text(MARGIN, 26, "Curriculum Vitae — FATIMA EZ-ZINE", 8.5, "F1", GREY)

content = "\n".join(ops).encode("cp1252", "replace")
objects = []
objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>")
objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
objects.append(b"<< /Length " + str(len(content)).encode() + b" >>\nstream\n" + content + b"\nendstream")

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
