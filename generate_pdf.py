from PyPDF2 import PdfFileWriter, PdfFileReader
import qrcode
import datetime
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import sys
import argparse


# Motifs
# travail-courses-sante-famille-sport-judiciaire-missions

def parse_args():
    parser = argparse.ArgumentParser(prog='main.py')
    parser.add_argument("--first-name", required=True, type=str)
    parser.add_argument("--last-name", required=True, type=str)
    parser.add_argument("--birth-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--birth-city", required=True, type=str)
    parser.add_argument("--address", required=True, type=str, help="Address Postcode City")
    parser.add_argument("--current-city", required=True, type=str)
    parser.add_argument("--leave-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--leave-hour", required=True, type=str, help="HH:MM")
    parser.add_argument("--motifs", required=True, type=str, help="- delimited: travail-courses-sante-famille-sport-judiciaire-missions")
    
    return parser.parse_args()

# ---------------------------
#  First Page (All fields to fill)
# ---------------------------
def draw_first_page_layout():
    img = Image.open("input-page1.png")
    img_array = np.array(img)

    # Erase fields
    img_array[300:330, 250:] = 255
    img_array[355:390, 250:] = 255
    img_array[400:430, 185:] = 255
    img_array[450:490, 270:] = 255
    img_array[895:925, 155:180] = 255
    img_array[635:660, 155:180] = 255

    # Erase crosses
    img_array[630:660, 155:185] = 255
    img_array[735:765, 155:185] = 255
    img_array[820:850, 155:185] = 255
    img_array[895:925, 155:185] = 255
    img_array[1010:1040, 155:185] = 255
    img_array[1110:1140, 155:185] = 255
    img_array[1185:1215, 155:185] = 255

    # Erase Current city
    img_array[1260:1300, 220:527] = 255

    # Erase Current date
    img_array[1316:1339, 190:319] = 255

    # Erase Current time
    img_array[1315:1339, 409:500] = 255

    # Erase Current time under QR
    img_array[1442:1453, 948:1078] = 255

    # Erase QR
    img_array[1217:1430, 800:1100] = 255

    img = Image.fromarray(img_array)
    return img_array

# Create crosses:
def get_cross():
    image = Image.new('RGB', (30, 30), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    try:
        image_font = ImageFont.truetype("Arial.ttf", 35)
    except OSError:
        try:
            image_font = ImageFont.truetype("arial.ttf", 22)
        except OSError:
            sys.exit("arial.ttf n'est pas installé")
    image_draw.text((3, -4), f'X', (0, 0, 0), font=image_font)
    return np.array(image)


# travail-courses-sante-famille-sport-judiciaire-missions
def check_motif_boxes(img_array, motifs):
    #img_array = np.array(first_page_img)
    
    cross = get_cross()
    if "travail" in motifs:
        img_array[630:660, 155:185] = cross
    if "courses" in motifs:
        img_array[735:765, 155:185] = cross
    if "sante" in motifs:
        img_array[820:850, 155:185] = cross
    if "famille" in motifs:
        img_array[895:925, 155:185] = cross
    if "sport" in motifs:
        img_array[1010:1040, 155:185] = cross
    if "judiciaire" in motifs:
        img_array[1110:1140, 155:185] = cross
    if "missions" in motifs:
        img_array[1185:1215, 155:185] = cross
    return img_array

# QR CODE
def draw_QR_code(img_array,first_name, last_name, birth_date, birth_city, address, leave_date, leave_hour, motifs):
    # Pas de diacritiques, est-ce normal ? (alors qu'il peut y en avoir dans les cases à remplir)
    qr_text = f"Cree le: {datetime.datetime.now().strftime('%d/%m/%Y a %H:%M')};" \
              f" Nom: {last_name};" \
              f" Prenom: {first_name};" \
              f" Naissance: {birth_date} a {birth_city};" \
              f" Adresse: {address};" \
              f" Sortie: {leave_date} a {leave_hour};" \
              f" Motifs: {motifs}"

    # qr_text="hyduzqhdzoiqd zqoihdpodqz"
    qr = qrcode.make(qr_text, border=0)
    qr = qr.resize((200, 200))
    qr = np.array(qr).astype(np.uint8) * 255
    qr = qr.repeat(3).reshape(qr.shape[0], qr.shape[1], -1)
    
    return qr


# Fill args
def fill_save_first_page(img_array, qr, first_name, last_name, birth_date, birth_city, current_city, address):
    # Draw QR code
    img_array[1228:1428, 890:1090] = np.array(qr)
    
    img = Image.fromarray(img_array)

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("Arial.ttf", 22)
        font_small = ImageFont.truetype("Arial.ttf", 14)
    except OSError:
        try:
            font = ImageFont.truetype("arial.ttf", 22)
            font_small = ImageFont.truetype("arial.ttf", 14)
        except OSError:
            sys.exit("arial.ttf n'est pas installé")
    draw.text((260, 307), f'{first_name} {last_name}', (0, 0, 0), font=font)
    draw.text((255, 357), f'{birth_date}', (0, 0, 0), font=font)
    draw.text((190, 407), f"{birth_city}", (0, 0, 0), font=font)
    draw.text((280, 458), f"{address}", (0, 0, 0), font=font)

    draw.text((228, 1268), f"{current_city}", (0, 0, 0), font=font)
    draw.text((190, 1319), datetime.datetime.now().strftime("%d/%m/%Y"), (0, 0, 0), font=font)
    draw.text((411, 1318), datetime.datetime.now().strftime("%H:%M"), (0, 0, 0), font=font)

    draw.text((948, 1443), datetime.datetime.now().strftime("%d/%m/%Y à %H:%M"), (0, 0, 0), font=font_small)

    plt.imsave("output-1.pdf", np.array(img), format="pdf")

# ---------------------------
#  Second Page (Big QR code)
# ---------------------------
def draw_save_second_page(qr):
    img = np.array(Image.open('input-page2.png'))
    img[:] = 255
    qr = Image.fromarray(qr)
    qr = qr.resize((qr.size[0] * 3, qr.size[1] * 3))
    qr = np.array(qr)
    img[113:113 + qr.shape[0], 113:113 + qr.shape[1]] = qr
    plt.imsave("output-2.pdf", img, format="pdf")

# --------------------
# Merge PDFs
# --------------------
def merge_pdfs():
    pdf1 = PdfFileReader('output-1.pdf')
    pdf2 = PdfFileReader('output-2.pdf')
    writer = PdfFileWriter()
    writer.addPage(pdf1.getPage(0))
    writer.addPage(pdf2.getPage(0))
    writer.write(open("output.pdf", "wb"))

def generate_pdf(first_name, last_name, birth_date, birth_city, current_city, address, leave_date, leave_hour, motifs):
    first_page_array = draw_first_page_layout()
    first_page_array = check_motif_boxes(first_page_array,motifs)
    qr = draw_QR_code(first_page_array, first_name, last_name, birth_date, birth_city, address, leave_date, leave_hour, motifs)
    fill_save_first_page(first_page_array, qr, first_name, last_name, birth_date, birth_city,current_city, address)
    draw_save_second_page(qr)
    merge_pdfs()
    print("Le fichier output.pdf a été créé avec succès.")

if __name__ == '__main__':
    args = parse_args()
    generate_pdf(args.first_name, args.last_name, args.birth_date, args.birth_city, args.current_city, args.address, args.leave_date, args.leave_hour, args.motifs)

