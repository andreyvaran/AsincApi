import datetime


def datetime_with_delta(timedelta: float):
    try:
        timedelta = float(timedelta)
    except TypeError as e :
        timedelta = 0

    now = datetime.datetime.now()
    min = abs(int(60 * float(timedelta)))
    hour = min // 60
    min = min % 60
    delt = datetime.timedelta(minutes=min, hours=hour)
    if float(timedelta) > 0:
        return now + delt
    else:
        return now - delt


def get_str_hellow(date: datetime.datetime) -> str:
    if date.time().hour >= 0 and date.time().hour <= 6:
        return str('Good night')
    elif date.time().hour >= 6 and date.time().hour <= 12:
        return str('Good morning')
    elif date.time().hour >= 12 and date.time().hour <= 18:
        return str('Good afternoon')
    else:
        return str('Good evening')


