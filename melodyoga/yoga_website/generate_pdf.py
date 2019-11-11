from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime as d
from random import randint


def form_adhesion(email, username):
    pdf = canvas.Canvas("Forumulaire_adhésion.pdf")
    pdf.drawString(200, 800, "Formulaire d'adhésion : ")
    pdf.drawString(150, 770, "Association Melodyoga 1496 quartier des longuettes")
    pdf.drawString(180, 790, "."*53)
    pdf.drawString(50, 680, "Username : {} ".format(username))

    pdf.drawString(50, 650, "Prénom : ")
    pdf.drawString(50, 620, "Nom : ")
    pdf.drawString(50, 590, "Email : {} ".format(email))
    pdf.drawString(50, 560, "Téléphone : ")

    pdf.drawString(50, 450, "Date de naissance : ")
    pdf.drawString(50, 100, "Date : ")
    pdf.drawString(420, 100, "Signature" + "."*30)
    pdf.showPage()
    pdf.save()
