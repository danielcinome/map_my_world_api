from datetime import datetime, timedelta


def format_datetime(date_obj):
    if date_obj is None:
        return None

    try:
        return date_obj.strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return None