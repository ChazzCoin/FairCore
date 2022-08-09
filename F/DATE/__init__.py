import datetime
import time
from dateutil import parser
import dateutil.relativedelta

n = "\n"
s = " "
co = ", "
p = "."
c = ":"

DATETIME_MONTH = "%B"
DATETIME_DAY = "%d"
DATETIME_YEAR = "%Y"
DATETIME_FULL_MONGO = "%B %d %Y"
DATETIME_REDDIT = "'%Y-%m-%d %H:%M:%S'"

""" toString Extractors """
def get_datetime_month(datetimeObject: datetime) -> str:
    return datetimeObject.strftime(DATETIME_MONTH)

def get_datetime_day(datetimeObject: datetime) -> str:
    return datetimeObject.strftime(DATETIME_DAY)

def get_datetime_year(datetimeObject: datetime) -> str:
    return datetimeObject.strftime(DATETIME_YEAR)

def get_month_day_year_str(dtObject: datetime) -> str:
    return str(get_datetime_month(dtObject)) + s + str(get_datetime_day(dtObject)) + s + str(get_datetime_year(dtObject))

def get_now_month_day_year_str() -> str:
    obj = get_now_date_dt()
    return get_month_day_year_str(obj)

""" Logging / Mongo """
def get_timestamp_str() -> str:
    return str(time.time())

def get_log_date_time_dt() -> datetime:
    return datetime.datetime.now()

def to_hours_minutes_seconds(seconds) -> str:
    return str(datetime.timedelta(seconds=seconds))

def mongo_date_today_str() -> str:
    obj = get_now_date_dt()
    return get_month_day_year_str(obj)

""" Now Time / Build Date """
# Get Now
def get_now_date_dt() -> datetime:
    return datetime.datetime.now().date()

def build_date_dt(day, month, year) -> datetime:
    return datetime.datetime(year, month, day).date()

def build_date_str(day, month, year) -> str:
    return to_month_day_year_str(datetime.datetime(year, month, day))

""" Parsers """
# -> Master Parser

TO_DATETIME = lambda strObj: parse_str_to_datetime(strObj)

def parse_str_to_datetime(obj: str) -> datetime.datetime:
    return parser.parse(obj)

def parse_obj_to_month_day_year_str(obj=None):
    try:
        if type(obj) is str:
            obj = parse_str_to_datetime(obj)
        elif type(obj) is list:
            return False
        return get_month_day_year_str(obj)
    except Exception as e:
        print(e)
        return False

def parse_from_db_date(str_date: str) -> datetime.datetime:
    date_obj = parser.parse(str_date)
    return date_obj

def parse_reddit_timestamp_to_datetime(timestamp) -> str:
    return datetime.datetime.utcfromtimestamp(timestamp).strftime(DATETIME_REDDIT)

""" Converters """
def to_month_day_year_str(t=None) -> str:
    if t is None:
        t = datetime.datetime.now()
    return get_month_day_year_str(t)

""" Manipulation """
# -> Months
def add_months(startDate, monthsForward=1, toString=False):
    date = parser.parse(startDate)
    newDate = date + dateutil.relativedelta.relativedelta(months=monthsForward)
    if toString:
        return to_month_day_year_str(newDate)
    return newDate

def subtract_months(startDate, monthsBack=1, toString=False):
    date = parser.parse(startDate)
    newDate = date - dateutil.relativedelta.relativedelta(months=monthsBack)
    if toString:
        return to_month_day_year_str(newDate)
    return newDate

# -> Years
def subtract_years(startDate, yearsBack=1, toString=False):
    date = parser.parse(startDate)
    newDate = date - dateutil.relativedelta.relativedelta(years=yearsBack)
    if toString:
        return to_month_day_year_str(newDate)
    return newDate

# -> Hours
def subtract_hours(startDate, hoursBack=1, toString=False):
    date = parser.parse(startDate)
    newDate = date - dateutil.relativedelta.relativedelta(hours=hoursBack)
    if toString:
        return to_month_day_year_str(newDate)
    return newDate

# -> Days
def subtract_days(startDate, daysBack=1, toString=True):
    date = parser.parse(startDate)
    newDate = date - dateutil.relativedelta.relativedelta(days=daysBack)
    if toString:
        return to_month_day_year_str(newDate)
    return newDate

def get_range_of_dates_by_day(startDate, daysBack=1):
    current_date = startDate
    list_of_dates = [startDate]
    for i in range(daysBack):
        current_date = subtract_days(current_date, 1, toString=True)
        list_of_dates.append(current_date)
    return list_of_dates

def get_current_year():
    obj = get_now_date_dt()
    return str(obj.strftime("%Y"))

def get_current_month():
    obj = get_now_date_dt()
    return str(obj.strftime("%B"))

def get_current_day():
    obj = get_now_date_dt()
    return str(obj.strftime("%d"))


months = {
    "January": ["January", "Jan"],
    "February": ["February", "Feb"],
    "March": ["March", "Mar"],
    "April": ["April", "Apr"],
    "May": ["May"],
    "June": ["June", "Jun"],
    "July": ["July", "Jul"],
    "August": ["August", "Aug"],
    "September": ["September", "Sept", "Sep"],
    "October": ["October", "Oct"],
    "November": ["November", "Nov"],
    "December": ["December", "Dec"]
}

days = {
    "Monday": ["Monday", "Mon"],
    "Tuesday": ["Tuesday", "Tues"],
    "Wednesday": ["Wednesday", "Wed"],
    "Thursday": ["Thursday", "Thur", "Thurs"],
    "Friday": ["Friday", "Fri"],
    "Saturday": ["Saturday", "Sat"],
    "Sunday": ["Sunday", "Sun"]
}