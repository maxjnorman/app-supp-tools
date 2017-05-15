from datetime import datetime, timedelta
from calendar import monthrange
from collections import defaultdict
import pandas as pd
import numpy as np

#start_day = 1
#month_start_date = datetime.now().date().replace(day=start_day, month=4)
#start_date = month_start_date - timedelta(month_start_date.weekday())
#end_day = monthrange(datetime.now().year, datetime.now().replace(month=4).month)[1]
#month_end_date = datetime.now().date().replace(day=end_day, month=4)
#end_date = month_end_date + timedelta(6-month_end_date.weekday())
## need code to get the final days of the last month to create a 'full' first week.
## same for the end week.
#start_date = datetime.now().replace(month=4).date().replace(day=start_day)
#end_date = datetime.now().replace(month=4).date().replace(day=end_day)
#dates = pd.date_range(start_date, end_date).date
#print(dates)



current_date = datetime(2017, 5, 14).date()
start_day = 1
end_day = monthrange(current_date.year, current_date.month)[1]
month_start_date = current_date.replace(day=start_day)
month_end_date = current_date.replace(day=end_day)
start_date = month_start_date - timedelta(month_start_date.weekday())
end_date = month_end_date + timedelta(6 - month_end_date.weekday())
dates = pd.date_range(start_date, end_date).date
weeks_array = np.reshape(dates, (int(len(dates)/7), 7))
weeks_list = weeks_array.tolist()
print(weeks_list[4])
#week_starts = [date for date in dates if date.weekday() == 0]
#ints = range(0, len(dates))
#ints_dict = dict(zip(dates, ints))
#ones = [1] * len(dates)
#ones_dict = dict(zip(dates, ones))
#weekdays = pd.date_range(start_date, end_date).dayofweek
#weekdays_dict = dict(zip(dates, weekdays))
#dicts_list = []
#dicts_list.append(ones_dict)
#dicts_list.append(ints_dict)
#dicts_list.append(weekdays_dict)
#frame = pd.DataFrame(dicts_list)
#frame = frame.values.transpose()
#frame = frame.tolist()
#frame_dict = dict(zip(dates, frame))
#print(frame_dict)
#current_date = datetime(2017, 5, 14).date()
#start_day = 1
#end_day = monthrange(current_date.year, current_date.month)[1]
#month_start_date = current_date.replace(day=start_day)
#month_end_date = current_date.replace(day=end_day)
#start_date = month_start_date - timedelta(month_start_date.weekday())
#end_date = month_end_date + timedelta(6 - month_end_date.weekday())
#dates = pd.date_range(start_date, end_date).date
#dates = np.reshape(dates, (7, int(len(dates)/7)))
#print(dates)