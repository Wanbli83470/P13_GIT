from reportlab.pdfgen import canvas
import os


class ExportPdf:
    def generate_pdf(email, username):
        rep_actuel = os.getcwd()
        print(rep_actuel)  # renvoie le répertoire actuel
        if rep_actuel == "/home/thomas/Bureau/P13_ESTIVAL_THOMAS/user_experience":
            pdf = canvas.Canvas(f"static/user_experience/formulaire_adhésion_{username}.pdf")
        else:
            pdf = canvas.Canvas(f"user_experience/static/user_experience/formulaire_adhésion_{username}.pdf")
        pdf.drawString(200, 800, "Formulaire d'adhésion : ")
        pdf.drawString(130, 770, "Association Melodyoga 1496 quartier des longuettes")
        pdf.drawString(170, 790, "."*53)
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

