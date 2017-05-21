from datetime import datetime, timedelta, date
from calendar import monthrange
from collections import defaultdict
import pandas as pd
import numpy as np

dates = pd.date_range(date(2017,4,4), date(2017,4,20))

class Day:
    
    def __init__(self, date):
        self.date = date
    
    def return_date(self):
        return date(self.date.year, self.date.month, self.date.day)

days = [Day(date=date) for date in dates]
day_dict = dict(zip(dates, days))
users_dict = {}
for key in day_dict.keys():
    users_dict[key] = day_dict[key].return_date()
#print(users_dict.values())


#maybe make a dataframe of pks pointing at dicts of objects
list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
list6 = [6, 7, 8, 9, 10]
listc = ['c', 'd', 'e', 'f', 'g']
list4 = [4, 6, 8, 10]
listf = ['f', 'h', 'j', 'l']
dicta1 = dict(zip(lista, list1))
dictc6 = dict(zip(listc, days))
dict4f = dict(zip(listf, list4))
dicts = [dicta1, dictc6, dict4f]
frame = pd.DataFrame(dicts)
frame['index'] = ['A', 'B', 'C']
frame1 = frame.set_index('index')
array1 = frame1.values.reshape(len(dicts), int(len(list1)/6), 6)
print()
#print(frame1.shape[1])

week_frame = pd.DataFrame(array1[:,0,:])
#print(week_frame)

for index, x in np.ndenumerate(array1):
    if type(x) is Day:
        array1[index] = x.return_date()
print(array1)
print()
print()
print()
for n in range(0, array1.shape[1]):
    print()
    print(n)
    print(pd.DataFrame(array1[:,n,:]))
print()
print()
print()
print(array1.shape)



#keys1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
#list1 = list(range(0, 7))
#dict1 = dict(zip(keys1, list1))
#keys2 = ['d', 'e', 'f', 'g', 'h']
#list2 = list(range(10, 20))
#dict2 = dict(zip(keys2, list2))
#keys3 = list(set(keys1).union(set(keys2)))
#list3 = []
#for key in keys3:
#    if key in keys1:
#        list3.append(dict1[key])
#    elif key in keys2:
#        list3.append(dict2[key])
#    else:
#        None
#print(list(dict(zip(keys3, list3)).values()))

#list1 = list(range(0, 10))
#list2 = list(range(100, 110))
#listd = zip(list1, list2)
#print(pd.DataFrame(listd))


#date1 = datetime(2017,5,10)
#date2 = datetime(2017,5,21)
#date3 = datetime(2017,5,12)
#
#date_range = pd.date_range(date1, date2).date
#active_dates = pd.date_range(date1, date3).date
#active_list = [True] * len(active_dates)                            
#active_dict = dict(zip(active_dates, active_list))
#null_dates = date_range
#null_list = [False] * len(null_dates)
#null_dict = dict(zip(null_dates, null_list))
#dicts = [active_dict, null_dict]
#print(pd.DataFrame(dicts))

#
#def get_week_pattern():
#    weekdays = list(range(0, 7))
#    week_pattern = [
#        True,
#        True,
#        True,
#        True,
#        True,
#        False,
#        False,
#    ]
#    return(dict(zip(weekdays, week_pattern)))
#
#pattern_dict = get_week_pattern()
#
#
#valid_dates = [
#        date 
#        for date in pd.date_range(date1, date2).date 
#        if pattern_dict[date.weekday()]
#    ]
#print(valid_dates)
#
#print(list(pattern_dict.values()))
#print()
#print()
#print()






#listk = list(range(3,7))
#list1 = [1] * len(listk)
#dict1 = dict(zip(listk, list1))
#list2 = list(range(0,5))
#for n in list2:
#    if n in dict1.keys():
#        print(dict1[n])

#x = range(16)
#x = np.reshape(x, (4,4))
#x = x[:,1:3]
#print(x)

#list1 = [1, 2, 3, 4, 5]
#lista = pd.date_range(datetime(2017,4,6), datetime(2017,4,11)).date
#list6 = [6, 7, 8, 9, 10]
#listc = pd.date_range(datetime(2017,4,7), datetime(2017,4,12)).date
#dicta1 = dict(zip(lista, list1))
#dictc6 = dict(zip(listc, list6))
#dicts = [dicta1, dictc6]
#frame = pd.DataFrame(dicts)
#frame['index'] = ['A', 'B']
#frame1 = frame.set_index('index')
#print(frame1.values)

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


#current_date = datetime(2017, 5, 14).date()
#start_day = 1
#end_day = monthrange(current_date.year, current_date.month)[1]
#month_start_date = current_date.replace(day=start_day)
#month_end_date = current_date.replace(day=end_day)
#start_date = month_start_date - timedelta(month_start_date.weekday())
#end_date = month_end_date + timedelta(6 - month_end_date.weekday())
#dates = pd.date_range(start_date, end_date).date
#weeks_array = np.reshape(dates, (int(len(dates)/7), 7))
#weeks_list = weeks_array.tolist()
#print(weeks_list[4])

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