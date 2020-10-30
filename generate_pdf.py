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
# travail-achats-sante-famille-handicap-sport_animaux-convocation-missions-enfants

FONT = "Arial.ttf"
SMALL_LETTER_FONT = "arial.ttf"

def load_font(font_size):
  try:
    image_font = ImageFont.truetype(FONT, font_size)
    return image_font
  except OSError:
    try:
      image_font = ImageFont.truetype(SMALL_LETTER_FONT, font_size)
      return image_font
    except OSError:
      sys.exit(f"{FONT} n'est pas installé")

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
    parser.add_argument("--motifs", required=True, type=str, help="- delimited: travail-achats-sante-famille-handicap-sport_animaux-convocation-missions-enfants")
    
    return parser.parse_args()

def draw_first_page_layout():
  img = Image.open("input-page1.png")
  return np.array(img)


# Create crosses:
def get_cross():
    image = Image.new('RGB', (30, 30), color=(255, 255, 255))
    image_draw = ImageDraw.Draw(image)
    image_font = load_font(35)
    image_draw.text((3, -4), f'x', (0, 0, 0), font=image_font)
    return np.array(image)
# travail-achats-sante-famille-handicap-sport_animaux-convocation-missions-enfants
def check_motif_boxes(img_array, motifs):
    cross = get_cross()
    if "travail" in motifs:
        img_array[523:553, 169:199] = cross
    if "achats" in motifs:
        img_array[617:647, 169:199] = cross
    if "sante" in motifs:
        img_array[732:762, 169:199] = cross
    if "famille" in motifs:
        img_array[817:847, 169:199] = cross
    if "handicap" in motifs:
        img_array[904:934, 169:199] = cross
    if "sport_animaux" in motifs:
        img_array[982:1012, 169:199] = cross
    if "convocation" in motifs:
        img_array[1114:1144, 169:199] = cross
    if "missions" in motifs:
        img_array[1195:1225, 169:199] = cross
    if "enfants" in motifs:
        img_array[1291:1321, 169:199] = cross
    return img_array


# QR CODE
def draw_QR_code(img_array,first_name, last_name, birth_date, birth_city, address, leave_date, leave_hour, motifs):
    # Dans le QR code del'attestation officielle, motifs sont séparés par des virgules (suvi d'un espace)
    motifs = motifs.replace('-', ', ')

    # Pas de diacritiques, est-ce normal ? (alors qu'il peut y en avoir dans les cases à remplir)
    # Oui, c'est comme c'est qu'est conçu le QR dans les fichiers sources du repo du gouv
    qr_text = f"Cree le: {datetime.datetime.now().strftime('%d/%m/%Y a %H:%M')};\n" \
              f" Nom: {last_name};\n" \
              f" Prenom: {first_name};\n" \
              f" Naissance: {birth_date} a {birth_city};\n" \
              f" Adresse: {address};\n" \
              f" Sortie: {leave_date} a {leave_hour};\n" \
              f" Motifs: {motifs}"

    qr = qrcode.make(qr_text, border=0)
    qr = qr.resize((200, 200))
    qr = np.array(qr).astype(np.uint8) * 255
    qr = qr.repeat(3).reshape(qr.shape[0], qr.shape[1], -1)
    
    return qr

# Fill args
def fill_save_first_page(img_array, qr, first_name, last_name, birth_date, birth_city, current_city, address):
    # Draw QR code
    img_array[1344:1544, 910:1110] = np.array(qr)
    
    img = Image.fromarray(img_array)

    draw = ImageDraw.Draw(img)
    font = load_font(22)
    font_small = load_font(14)

    draw.text((250, 282), f'{first_name} {last_name}', (0, 0, 0), font=font)
    draw.text((250, 328), f'{birth_date}', (0, 0, 0), font=font)
    draw.text((630, 328), f"{birth_city}", (0, 0, 0), font=font)
    draw.text((280, 374), f"{address}", (0, 0, 0), font=font)

    draw.text((228, 1368), f"{current_city}", (0, 0, 0), font=font)
    draw.text((205, 1416), datetime.datetime.now().strftime("%d/%m/%Y"), (0, 0, 0), font=font)
    draw.text((535, 1416), datetime.datetime.now().strftime("%H:%M"), (0, 0, 0), font=font)

    # No more in reconfinement
    # draw.text((948, 1443), datetime.datetime.now().strftime("%d/%m/%Y à %H:%M"), (0, 0, 0), font=font_small)

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

    writer.addMetadata({
        '/Title':'COVID-19 - Déclaration de déplacement',
        '/Subject':'Attestation de déplacement dérogatoire',
        #'/Keywords': 'covid19','covid-19','attestation','déclaration','déplacement','officielle','gouvernement',
        '/Keywords': 'covid19 covid-19 attestation déclaration déplacement officielle gouvernement',
        '/Producer':'DNUM/SDIT',
        '/Creator':'',
        '/Author':'Ministère de l\'intérieur'
    })

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


def fake_generation():
  motifs = ['travail', 'achats', 'sante', 'famille', 'handicap', 'sport_animaux', 'convocation', 'missions', 'enfants']
  first_name = "AAAAAAA"
  last_name = "BBBBBBBB"
  birth_date = "11/20/2000"
  birth_city = "BIRTHCITYYYYYYYYYYYYYYYY"
  current_city = "CURRENTCITYYYYYYYYYYY"
  address = "1112 PLACE DE LARUE QUI EST LONGUE 12312 LONGUEVIIIIIIIIILLE"

  leave_date = "11/11/1111"
  leave_hour = "12h12"

  generate_pdf(first_name, last_name, birth_date, birth_city, current_city, address, leave_date, leave_hour, motifs)

