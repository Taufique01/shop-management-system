import calendar
import datetime

def monthFirstAndLastDate(any_date):
    print(any_date)
    print(any_date.year)
    month_first_day, month_last_day=calendar.monthrange(any_date.year,any_date.month)
    month_first_date=datetime.date(any_date.year, any_date.month, 1)
    month_last_date=datetime.date(any_date.year, any_date.month, month_last_day)
    return (month_first_date,month_last_date)