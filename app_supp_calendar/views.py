from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

import pandas as pd
from datetime import date
from calendar import monthrange

from .functions import month_date_range
from app_supp_shifts.models import Shift, ShiftTemplate

# maybe make a dataframe of pks pointing at dicts of objects
#list1 = [1, 2, 3, 4, 5]
#lista = ['a', 'b', 'c', 'd', 'e']
#list6 = [6, 7, 8, 9, 10]
#listc = ['c', 'd', 'e', 'f', 'g']
#dicta1 = dict(zip(lista, list1))
#dictc6 = dict(zip(listc, list6))
#dicts = [dicta1, dictc6]
#frame = pd.DataFrame(dicts)
#frame['index'] = ['A', 'B']
#frame1 = frame.set_index('index')
#print(frame1)


class ShiftCalendar:

    def __init__(self, date, team):
        self.date = date
        self.team = team
        self.start_date = date      #variables to use this class as is
        self.end_date = date


    def week_pattern(self, template):
        weekdays = list(range(0, 7))
        week_pattern = [
            template.mon,
            template.tue,
            template.wed,
            template.thu,
            template.fri,
            template.sat,
            template.sun
        ]
        return dict(zip(weekdays, week_pattern))


    def template_dates(self, template):
        start_date = max(self.start_date, template.start_date)
        end_date = min(self.end_date, template.end_date)
        pattern_dict = self.week_pattern(template)
        return [
            date
            for date in pd.date_range(start_date, end_date).date
            if pattern_dict[date.weekday()]
        ]


    def build_shift_array(self):
        valid_dates = pd.date_range(self.start_date, self.end_date).date
        null_list = [None] * len(valid_dates)
        null_dict = dict(zip(valid_dates, null_list))
        templates = self.team.shift_templates.filter(
            active=True,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date,
        )
        shift_dicts_list = []
        for template in templates:
            active_dates = self.template_dates(template)
            active_dates_dict = dict(zip(active_dates, active_dates))
            database_shifts = template.shifts.filter(
                day__in=active_dates
            ).prefetch_related(
                Prefetch(
                    'users',
                    queryset=template.shifts.users.filter(
                        is_active=True
                    )
                )
            )
            database_dates = database_shifts.values_list('day', flat=True)
            shifts_dict = dict(zip(database_dates, database_shifts))
            users_dict = {}
            for date in shifts_dict.keys():
                users_dict[date] = shifts_dict[date].get_users()
            output_dict = {}
            output_dict.update(null_dict)
            output_dict.update(active_dates_dict)
            output_dict.update(users_dict)
            shift_dicts_list.append(output_dict)
        shift_frame = pd.DataFrame(shift_dicts_list)
        shift_array = shift_frame.values.reshape(
            len(shift_dicts_list),
            int((shift_frame.shape[1])/7),
            7
        )
        return shift_array
        #for n in range(0, shift_frame.shape[1]):
            #week_array = shift_array[:,n,:]




class WeekCalendar(ShiftCalendar):

    def __init__(self, date, team):
        ShiftCalendar.__init__(self, date, team)
        self.get_date_range()


    def get_date_range(self):
        self.start_date = self.date - timedelta(self.date.weekday())
        self.end_date = start_date + timedelta(7)




class MonthCalendar(ShiftCalendar):

    def __init__(self, date, team):
        ShiftCalendar.__init__(self, date, team)
        self.get_date_range()


    def get_date_range(self):
        start_day = 1
        end_day = monthrange(self.date.year, self.date.month)[1]
        month_start_date = self.date.replace(day=start_day)
        month_end_date = self.date.replace(day=end_day)
        self.start_date = month_start_date - timedelta(month_start_date.weekday())
        self.end_date = month_end_date + timedelta(6 - month_end_date.weekday())




@login_required
def month_calendar(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    dates = month_date_range(year, month, day)
