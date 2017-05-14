from django.db import models
from django.utils import timezone

from calendar import monthrange

class Year(models.Model):
    team = models.ForeignKey('app_supp_teams.Team', related_name='years')
    year = models.IntegerField()

    def __str__(self):
        return '%s %s' % (
            self.team.team_name,
            self.year.year,
        )

    def create_month_set(self):
        if self.year > self.team.start_date.year:
            start_month = 1
        else:
            start_month = self.account.start_date.month
        if self.year < timezone.now().year:
            end_month = 12
        elif self.year == timezone.now().year:
            end_month = min(timezone.now().month + 3, 12)
        else:
            end_month = 15 - timezone.now().month
        month_list = list(range(start_month, end_month + 1))
        query_months = Month.objects.filter(
            year__pk=self.pk,
        ).values_list('month_date', flat=True)
        database_months = []
        for month_date in query_months:
            database_months.append(month_date.month)
        if set(database_months) == set(month_list):
            pass
        else:
            missing_months = set(month_list).difference(set(database_months))
            new_months = []
            for n in missing_months:
                new_month = Month(
                    year=self,
                    month_date=date(self.year, n, 1),
                )
                new_months.append(new_month)
            Month.objects.bulk_create(new_months)




class Month(models.Model):
    year = models.ForeignKey('app_supp_calendar.Year', related_name='months')
    month_date = models.DateField()

    def __str__(self):
        return '%s %s %s' % (
            self.year.team.team_name,
            self.year.year,
            self.month_name,
        )

    def create_day_set(self):
        start_day = 1
        end_day = monthrange(self.month_date.year, self.month_date.month)[1]
        day_list = list(range(start_day, end_day + 1))
        query_days = Day.objects.filter(
            month__pk=self.pk,
        ).values_list('day_date', flat=True)
        database_days = []
        for day_date in query_days:
            database_days.append(day_date.day)
        if set(database_days) == set(day_list):
            pass
        else:
            missing_days = set(day_list).difference(set(database_days))
            new_days = []
            for n in missing_days:
                new_day = Day(
                    month=self,
                    day_date = date(self.year.year, self.month_date.month, n),
                    weekday_int = weekday(date(
                        self.year.year,
                        self.month_date.month,
                        n
                    )),
                )
                new_days.append(new_day)
            Day.objects.bulk_create(new_days)




# Not needed(?) - could generate all this in the view
class Day(models.Model):
    month = models.ForeignKey('app_supp_calendar.Month', related_name='days')
    day_date = models.DateField()
    weekday_int = models.IntegerField()
    workday = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s %s' % (
            self.month.year.team.team_name,
            self.month.year.year,
            self.month.month_name,
            weekday(self.weekday_int),
        )
