from datetime import datetime

def get_infos(request):
    date_actuelle = datetime.now()

    if date_actuelle.month >= 10:
        date_actuelle = f"{date_actuelle.day} / {date_actuelle.month} / {date_actuelle.year} : {date_actuelle.hour}h {date_actuelle.minute}"

    date_actuelle = f"{date_actuelle.day} / 0{date_actuelle.month} / {date_actuelle.year} : {date_actuelle.hour}h {date_actuelle.minute}"
    return {'date_actuelle': date_actuelle}
