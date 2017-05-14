from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from datetime import date
from calendar import monthrange

@login_required
def month_calendar(request, pk):
    team = get_object_or_404(Team, pk=pk)
    start_day = 1
    end_day = monthrange(timezone.now().year, timezone.now().month)[1]
    start_date = timezone.now().date().replace(day=start_day)
    end_date = timezone.now().date().replace(day=end_day)
    dates = pd.date_range(start_date_obj, end_date_obj).date
    shifts = Shift.objects.filter(
        shift_template__team=team,
        day__in=dates,
    ).order_by('day')
    distinct_shift_ids = #distinct pks of shifts. order by start time
    vacent_shifts = shifts.filter(

    )
