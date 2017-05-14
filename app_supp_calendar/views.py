from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from datetime import date
from calendar import monthrange

@login_required
def month_calendar(request, pk):
    team = get_object_or_404(Team, pk=pk)
    start_day = 1
    month_start_date = timezone.now().date().replace(day=start_day)
    start_date = month_start_date - timedelta(month_start_date.weekday())
    end_day = monthrange(timezone.now().year, timezone.now().month)[1]
    month_end_date = timezone.now().date().replace(day=end_day)
    end_date = month_end_date + timedelta(6-month_end_date.weekday())
    # need code to get the final days of the last month to create a 'full' first week.
    # same for the end week.
    start_date = timezone.now().date().replace(day=start_day)
    end_date = timezone.now().date().replace(day=end_day)
    dates = pd.date_range(start_date, end_date).date
    database_shifts = Shift.objects.filter(
        shift_template__team=team,
        day__in=dates,
    ).order_by('day')
    distinct_shift_ids = shifts.distinct('pk').values_list('pk', flat=True)
    # will need to loop over the distinct shift id's (needs a function)
    database_dates = database_shifts.values_list('day', flat=True)
    empty_dates = list(set(dates).difference(set(database_dates)))
    none_list = [None] * len(empty_dates)
    none_dict = dict(zip(empty_dates, none_list))
    database_dict = dict(zip(database_dates, database_shifts))
    shift_dict = {}
    shift_dict.update(none_dict)
    shift_dict.update(database_dates)
    # should be able to loop over dates to get items from the dictionary (or none)
