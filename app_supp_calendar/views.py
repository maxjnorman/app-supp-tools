from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from datetime import date
from calendar import monthrange

from .functions import month_date_range
from app_supp_shifts import Shift, ShiftTemplate

# maybe make a dataframe of pks pointing at dicts of objects


@login_required
def month_calendar(request, pk, year, month, day):
    team = get_object_or_404(Team, pk=pk)
    start_date, end_date = month_date_range(year, month, day)
    dates = pd.date_range(start_date, end_date).date
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
    template_names = shift_templates.values_list(
        'shift_name',
        flat=True
    )
    templates_dict = dict(zip(template_names, templates))











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
