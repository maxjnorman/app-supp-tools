from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

import pandas as pd
from datetime import date, timedelta
from calendar import monthrange

from .functions import month_date_range, shape_range
from app_supp_shifts.models import Shift, ShiftTemplate
from app_supp_teams.models import Team

#Note : move to app_supp_calendar/classes.py
#Note : better to get users first then get occupied shifts from there?
class ShiftCalendar:

    def __init__(self, date, team):
        self.date = date
        self.team = team
        self.start_date = date      #variables to use this class as is
        self.end_date = date


    def dates_array(self): #Note: Could merge with 'build_data_arrays'
        dates = pd.date_range(
            start=self.start_date,
            end=self.end_date,
        ).date
        if len(dates) == 1:
            return dates
        else:
            return dates.reshape(
                int(len(dates)/7),
                7,
            )


    def dummy_template(self):
        return [
            ShiftTemplate(
                team=self.team,
                shift_name='Blank',
                shift_description='Blank',
                start_date=self.start_date,
                end_date=self.end_date,
                start_time=timezone.now().time(),
                end_time=timezone.now().time(),
                active=True,
                mon=False,
                tue=False,
                wed=False,
                thu=False,
                fri=False,
                sat=False,
                sun=False,
            ),
            ShiftTemplate(
                team=self.team,
                shift_name='Dummy',
                shift_description='Blank',
                start_date=self.start_date,
                end_date=self.end_date,
                start_time=timezone.now().time(),
                end_time=timezone.now().time(),
                active=True,
                mon=True,
                tue=True,
                wed=True,
                thu=True,
                fri=True,
                sat=True,
                sun=True,
            ),
        ]


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


    def active_template_dates(self, template):
        start_date = max(self.start_date, template.start_date)
        end_date = min(self.end_date, template.end_date)
        pattern_dict = self.week_pattern(template)
        return [
            date
            for date in pd.date_range(start_date, end_date).date
            if pattern_dict[date.weekday()]
        ]


    def dates_dict(self, dates, variable):
        variable_list = [variable] * len(dates)
        output_list = zip(dates, variable_list)
        return dict(zip(dates, output_list))


    def build_data_array(self):
        templates = self.team.shift_templates.filter(
            active=True,
        ).exclude(
            start_date__lt=self.start_date,
            end_date__gt=self.end_date,
        ).order_by('start_time')
        if not templates.exists():
            templates = self.dummy_template()
        output_list = []
        for template in templates:
            null_output = self.dates_dict(
                pd.date_range(self.start_date, self.end_date).date,
                'inactive'
            )
            active_output = self.dates_dict(
                self.active_template_dates(template),
                'active'
            )
            database_shifts = template.shifts.filter(
                day__in=self.active_template_dates(template),
            )
            database_dates = database_shifts.values_list('day', flat=True)
            database_context = []
            for shift in database_shifts:
                database_context.append(shift.get_users_or_unoccupied())
            database_output = dict(zip(
                database_dates,
                zip(database_shifts, database_context)
            ))
            output = {}
            output.update(null_output)
            output.update(active_output)
            output.update(database_output)
            output_list.append(output)
        output_frame = pd.DataFrame(output_list)
        output_array = output_frame.values.reshape(
            len(output_list),
            int((output_frame.shape[1])/7),
            7
        ).transpose(1,0,2)
        zipped_output = []
        for week in list(output_array):
            zipped_output.append(zip(templates, week))
        return zipped_output





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
    date_obj = date(int(year), int(month), int(day))
    month_calendar = MonthCalendar(date=date_obj, team=team)
    output_array = month_calendar.build_data_array()
    return render(
        request,
        'app_supp_calendar/view_calendar.html',
        {'current_user': request.user,
        'current_profile': request.user.profile,
        'team': team,
        'date': date_obj,
        'calendar': output_array,}
    )


@login_required
def week_view(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    date_obj = date(int(year), int(month), int(day))
    week_calendar = WeekCalendar(date=date_obj, team=team)
    output_array = week_calendar.build_data_array()
    return render(
        request,
        'app_supp_calendar/view_calendar.html',
        {'current_user': request.user,
        'current_profile': request.user.profile,
        'team': team,
        'date': date_obj,
        'calendar': output_array,}
    )


@login_required
def day_view(request, pk, year, month, day):
    return None
