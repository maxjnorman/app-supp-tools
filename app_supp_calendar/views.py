from django.shortcuts import render, get_object_or_404
from django.utils import timezone

import pandas as pd
from datetime import date
from calendar import monthrange

from .functions import month_date_range
from app_supp_shifts import Shift, ShiftTemplate

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

    def __init__(self, date, shifts, templates, template_names):
        self.date_range = month_date_range(date.year, date.month, date.day)
        self.shifts = shifts
        self.templates = templates
        self.template_names = template_names
        self.templates_dict = dict(zip(template_names, templates))
        self.create_shifts_dict()


    def create_shift_dicts(self):
        shift_dicts = []
        for template in self.templates:
            shifts = self.shifts.filter(
                shift_template=template
            )
            dates = shifts.values_list('day', flat=True)
            shift_dict = dict(zip(dates, shifts))
            shift_dict_list.append(shift_dict)
        return shift_dicts


    def get_week_starts(self):
        return [date for date in self.date_range if date.weekday() == 0]


    def create_week_frame(self, date):
        week_dates = week_date_range(date.year, date.month, date.day)
        for name in self.template_names:
            for date in week_dates:
                if date in self.shifts_dict[name].keys():







@login_required
def month_calendar(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    dates = month_date_range(year, month, day)
    week_starts = [date for date in dates if date.weekday() == 0]
    database_shifts = Shift.objects.filter(
        shift_template__team=team,
        active=True
        day__gte=start_date,
        day__lte=end_date,
    )
    template_pks = database_shifts.distinct(
        'shift_template__pk'
    ).values_list(
        'shift_template__pk',
        flat=True
    )
    templates = ShiftTemplate.objects.filter(
        pk__in=template_pks,
    ).order_by('start_time')
    template_names = templates.values_list(
        'shift_name',
        flat=True
    )

    shift_dicts_list = []
    user_dicts_list = []
    for template in templates:
        shifts = database_shifts.filter(
            shift_template=template
        )
        shift_dates = shifts.values_list('day', flat=True)
        empty_dates = list(set(dates).difference(set(shift_dates)))
        none_list = [None] * len(empty_dates)
        none_dict = dict(zip(empty_dates, none_list))
        database_dict = dict(zip(shift_dates, shifts))
        shift_dict = {}
        shift_dict.update(none_dict)
        shift_dict.update(database_dates)
        shift_dicts_list.append(shift_dict)
        shift_users = shifts.values_list('users__username')
