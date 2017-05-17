import pandas as pd
from datetime import date

def get_month_name(integer):
    month_dict = {
        1 : 'January',
        2 : 'Febuary',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 : 'November',
        12 : 'December'
    }
    month_name = month_dict[integer]
    return month_name


def month_date_range(year, month, day):
    date_object = date(int(year), int(month), int(day))
    start_day = 1
    end_day = monthrange(date_object.year, date_object.month)[1]
    month_start_date = date_object.replace(day=start_day)
    month_end_date = date_object.replace(day=end_day)
    start_date = month_start_date - timedelta(month_start_date.weekday())
    end_date = month_end_date + timedelta(6 - month_end_date.weekday())
    return pd.date_range(start_date, end_date).date

def week_date_range(year, month, day):
    date_object = date(int(year), int(month), int(day))
    start_date = date_object - timedelta(date_object.weekday())
    end_date = start_date + timedelta(7)
    return pd.date_range(start_date, end_date).date
