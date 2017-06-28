from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch

import pandas as pd
from datetime import date, timedelta
from calendar import monthrange

from .functions import (
    month_date_range,
    shape_range,
    get_previous_month,
    get_next_month,
    get_month_name,
)
from app_supp_shifts.models import Shift, ShiftTemplate
from app_supp_teams.models import Team

#Note : move to app_supp_calendar/classes.py
class Week:

    def __init__(self, dates_list, data):
        self.dates = dates_list
        self.data = data
        self.week_start = min(dates_list)
        self.rows = []




class WeekRow:

    def __init__(self, template, shifts):
        self.template = template
        self.shifts = shifts



class Day:

    #Note: context dict and the 4 variables are not needed, doens;t work quite as desired
    inactive_context = '0'
    active_context = '1'
    unoccupied_context = '2'
    occupied_context = '3'

    context_dict = {
        'inactive': inactive_context,
        'active': active_context,
        'unoccupied': unoccupied_context,
        'occupied': occupied_context,
    }

    def __init__(self, date):
        self.date = date
        self.weekday = date.weekday()#RemoveThis
        self.users = []
        self.context = 'inactive'
        self.shift = None#RemoveThis


    def get_context(self):
        return self.context_dict[self.context]


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
                pk=0,
                team=self.team,
                shift_name='No Active Shifts',
                shift_description='Blank',
                start_date=self.start_date,
                end_date=self.end_date,
                start_time='',
                end_time='',
                active=True,
                mon=False,
                tue=False,
                wed=False,
                thu=False,
                fri=False,
                sat=False,
                sun=False,
            )
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
        if template.end_date:
            end_date = min(self.end_date, template.end_date)
        else:
            end_date = self.end_date
        pattern_dict = self.week_pattern(template)
        return [
            date
            for date
            in pd.date_range(start_date, end_date).date
            if pattern_dict[date.weekday()]
        ]


    def get_active_templates(self):
        templates = self.team.shift_templates.filter(
            active=True,
        ).exclude(
            start_date__gt=self.end_date,
            end_date__lt=self.start_date,
        ).order_by('start_time')
        if not templates.exists():
            templates = self.dummy_template()
        return templates


    def day_date_constructor(self, dates, context):
        day_list = []
        for date in dates:
            day = Day(date)
            day.context = context
            day_list.append(day)
        return day_list


    def day_shift_constructor(self, shifts, context):
        day_list = []
        for shift in shifts:
            day = Day(shift.day)
            day.context = context
            day.users = shift.get_users_or_(None)
            day_list.append(day)
        return day_list


    def build_calendar(self):
        templates = self.get_active_templates()
        output_list = []
        for template in templates:
            database_shifts = template.shifts.filter(
                day__in=self.active_template_dates(template),
            )
            unoccupied_shifts = database_shifts.filter(
                users=None,
            )
            occupied_shifts = database_shifts.exclude(
                users=None,
            )
            inactive_dates = list(set(
                pd.date_range(self.start_date, self.end_date).date
            ).difference(set(
                self.active_template_dates(template)
            )))
            active_dates = list(set(
                self.active_template_dates(template)
            ).difference(set(
                database_shifts.values_list('day', flat=True)
            )))
            unoccupied_dates = unoccupied_shifts.values_list('day', flat=True)
            occupied_dates = occupied_shifts.values_list('day', flat=True)
            inactive_days = self.day_date_constructor(
                inactive_dates,
                'inactive',
            )
            active_days = self.day_date_constructor(
                active_dates,
                'active',
            )
            unoccupied_days = self.day_shift_constructor(
                unoccupied_shifts,
                'unoccupied',
            )
            occupied_days = self.day_shift_constructor(
                occupied_shifts,
                'occupied',
            )
            output = {}
            output.update(dict(zip(inactive_dates, inactive_days)))
            output.update(dict(zip(active_dates, active_days)))
            output.update(dict(zip(unoccupied_dates, unoccupied_days)))
            output.update(dict(zip(occupied_dates, occupied_days)))
            output_list.append(output)  #Note: end up with a list of dictionaries. Each dict corresponding to a template
        #Turn dicts into dataframe
        output_frame = pd.DataFrame(output_list)
        #Turn dataframe into array
        #Chop array up into weeks
        output_array = output_frame.values.reshape(
            len(output_list),
            int((output_frame.shape[1])/7),
            7
        ).transpose(1,0,2)  #Note: first_week = output_array[0]
        #Zip each list of weeks with the list of templates
        #Will end up with 5 (or 4) lists of template:week pairs
        output = [zip(templates, week) for week in output_array]
        #Get date ranges for weeks
        dates_array = pd.date_range(self.start_date, self.end_date).date.reshape(
            int(len(pd.date_range(self.start_date, self.end_date))/7),
            7,
        )
        #Assign each list to a Week obj
        weeks = [
            Week(list(dates), list(shifts))
            for dates, shifts
            in zip(dates_array, output)
        ]
        #pretty it up by making it a class function? or just making it better earlier
        for week in weeks:
            for item in week.data:
                week.rows.append(WeekRow(item[0], item[1]))
#        testtemplate = weeks[0].rows[0].template
#        testshifts = weeks[0].rows[0].shifts
#        testday = testshifts[0].date
        return weeks




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
    prev_date = get_previous_month(date_obj)
    next_date = get_next_month(date_obj)
    month_name = '%s %s' % (get_month_name(int(month)), year)
    month_calendar = MonthCalendar(date=date_obj, team=team)
    calendar = month_calendar.build_calendar()
    return render(
        request,
        'app_supp_calendar/view_calendar.html',
        {'current_user': request.user,
        'current_profile': request.user.profile,
        'team': team,
        'current_date': timezone.now().date,
        'date': date_obj,
        'prev_date': prev_date,
        'next_date': next_date,
        'month_name': month_name,
        'calendar': calendar,}
    )


@login_required
def week_view(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    date_obj = date(int(year), int(month), int(day))
    week_calendar = WeekCalendar(date=date_obj, team=team)
    output_array, templates = week_calendar.build_calendar()
    return render(
        request,
        'app_supp_calendar/view_calendar.html',
        {'current_user': request.user,
        'current_profile': request.user.profile,
        'team': team,
        'date': date_obj,
        'calendar': output_array,
        'templates': templates,}
    )


@login_required
def day_view(request, pk, year, month, day):
    return None
