from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

import pandas as pd
from datetime import date
from calendar import monthrange

from .functions import month_date_range
from app_supp_shifts.models import Shift, ShiftTemplate

#Note : move to app_supp_calendar/classes.py
#Note : better to get users first then get occupied shifts from there?
class ShiftCalendar:

    def __init__(self, date, team):
        self.date = date
        self.team = team
        self.start_date = date      #variables to use this class as is
        self.end_date = date


    def week_pattern_dict(self, template):
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
        pattern_dict = self.week_pattern_dict(template)
        return [
            date
            for date in pd.date_range(start_date, end_date).date
            if pattern_dict[date.weekday()]
        ]


    def build_calendar_arrays(self):
        valid_dates = pd.date_range(self.start_date, self.end_date).date
        null_list = [None] * len(valid_dates)
        null_dict = dict(zip(valid_dates, null_list))
        templates = self.team.shift_templates.filter(
            active=True,
        ).exclude(
            start_date__lt=self.start_date,
            end_date__gt=self.end_date,
        ).order_by('start_time')
        active_dates_dict_list = []
        users_dict_list = []
        for template in templates:
            active_dates = self.template_dates(template)
            true_list = [True] * len(active_dates)
            active_dates_dict = dict(zip(active_dates, true_list))
            active_dates_output = {}
            active_dates_output.update(null_dict)
            active_dates_output.update(active_dates_dict)
            active_dates_dict_list.append(active_dates_output)
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
                users_dict[date] = shifts_dict[date].get_users_or_none()
            users_output = {}
            users_output.update(null_dict)
            users_output.update(users_dict)
            users_dict_list.append(users_output)
        shifts_frame = pd.DataFrame(shift_dicts_list)
        shifts_array = shift_frame.values.reshape(
            len(shift_dicts_list),
            int((shift_frame.shape[1])/7),
            7
        )
        users_frame = pd.DataFrame(users_dicts_list)
        users_array = users_frame.values.reshape(
            len(users_dicts_list),
            int((users_frame.shape[1])/7),
            7
        )
        return shifts_array, users_array
        #for n in range(0, shift_frame.shape[1]):
            #week_array = shift_array[:,n,:]
            #week_frame = pd.DataFrame(week_array)  # Note: arrays are faster?
            #etc...




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
        self.start_date = month_start_date - timedelta(
            month_start_date.weekday()
        )
        self.end_date = month_end_date + timedelta(
            6 - month_end_date.weekday()
        )




@login_required
def month_view(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    date_obj = date(year, month, day)
    shifts_array, users_array = MonthCalendar(
        date=date_obj, team=team
    ).build_calendar_arrays()
    return render(
        request,
        'app_supp_calendar/view_calendar.html',
        {'current_user': request.user,
        'current_profile': request.user.profile,
        'team': team,
        'current_date': current_date,
        'shifts_array': shifts_array,
        'users_array': users_array,}
    )


@login_required
def week_view(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    date_obj = date(year, month, day)
    shifts_array, users_array = WeekCalendar(
        date=date_obj, team=team
    ).build_calendar_arrays()
    return render(
        request,
        'app_supp_calendar/view_calendar.html',
        {'current_user': request.user,
        'current_profile': request.user.profile,
        'team': team,
        'current_date': current_date,
        'shifts_array': shifts_array,
        'users_array': users_array,}
    )


@login_required
def day_view(request, pk, year, month, day):
    return None
