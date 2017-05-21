from django.db import models
from django.contrib.auth.models import User

from datetime import date, timedelta
import numpy as np
import pandas as pd

class ShiftTemplate(models.Model):
    team = models.ForeignKey(
        'app_supp_teams.Team',
        related_name='shift_templates',
    )
    shift_name = models.CharField(max_length=25)
    shift_description = models.CharField(max_length=50)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    active = models.BooleanField(default=True)
    mon = models.BooleanField(default=True)
    tue = models.BooleanField(default=True)
    wed = models.BooleanField(default=True)
    thu = models.BooleanField(default=True)
    fri = models.BooleanField(default=True)
    sat = models.BooleanField(default=True)
    sun = models.BooleanField(default=True)

    def __str__(self):
        return '%s_%s' % (self.team.team_name, self.shift_name)



class ShiftTemplateOld(models.Model):
    team = models.ForeignKey(
        'app_supp_teams.Team',
        related_name='shift_templates_old',
    )
    shift_name = models.CharField(max_length=25)
    shift_description = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s_%s' % (self.team.team_name, self.shift_name)

    def apply_shift_template(self, start_date, end_date, day_pattern):   #create Shift objs even if no Day exists (not hard linked)
        start_date_obj = date(start_date.year, start_date.month, start_date.day)
        end_date_obj = date(end_date.year, end_date.month, end_date.day)
        dates = pd.date_range(start_date_obj, end_date_obj).date
        weekdays = (pd.date_range(start_date_obj, end_date_obj).dayofweek)  #uses Mon=0 Sun=6
        dates_df = pd.DataFrame(np.vstack((dates, weekdays)).transpose())
        dates_df.columns = ['dates', 'weekday']
        date_list = []
        for weekday in day_pattern:     #day_pattern should be a list of ints representing weekdays that are selected
            weekday_df = dates_df[['dates']][dates_df['weekday']==weekday]
            date_list = date_list + weekday_df['dates'].tolist()
        database_shifts = Shift.objects.filter(
            shift_template__pk=self.pk,
            day__in=date_list,
        )
        if database_shifts.exists():
            database_dates = database_shifts.values_list('day', flat=True)
            inactive_shifts = database_shifts.filter(
                active=False
            )
            if inactive_shifts.exists():
                inactive_shifts.update(active=True)
            else:
                pass
        else:
            database_dates = []
        missing_dates = set(date_list).difference(set(database_dates))
        if len(missing_dates) > 0:
            new_shifts = []
            for missing_date in missing_dates:
                new_shift = Shift(
                    shift_template=self,
                    day=missing_date
                )
                new_shifts.append(new_shift)
            Shift.objects.bulk_create(new_shifts)
        else:
            pass

    def remove_shift_tempate(self, start_date, end_date, day_pattern):
        start_date_obj = date(start_date.year, start_date.month, start_date.day)
        end_date_obj = date(end_date.year, end_date.month, end_date.day)
        dates = (pd.date_range(start_date_obj, end_date_obj).date)
        weekdays = (pd.date_range(start_date_obj, end_date_obj).dayofweek)  #uses Mon=0 Sun=6
        dates_df = pd.DataFrame(np.vstack((dates, weekdays)).transpose())
        dates_df.columns = ['dates', 'weekday']
        date_list = []
        for weekday in day_pattern:     #day_pattern should be a list of ints representing weekdays that are selected
            weekday_df = dates_df[['dates']][dates_df['weekday']==weekday]
            date_list = date_list + weekday_df['dates'].tolist()
        database_shifts = Shift.objects.filter(
            shift_template__pk=self.pk,
            day__in=date_list,
        )
        if database_shifts.exists():
            database_shifts.update(active=False)
        else:
            pass

class Shift(models.Model):
    shift_template = models.ForeignKey(
        'app_supp_shifts.ShiftTemplate',
        related_name='shifts',
    )
    day = models.DateField()
    users = models.ManyToManyField(
        User,
        related_name='shifts',
        blank=True,
    )

    def __str__(self):
        return '%s_%s_%s' % (self.team.team_name, self.shift_name, str(self.day))

    def get_users(self):
        return self.users.filter(
            is_active=True
        ).values_list('username', flat=True) # Note: not the Profile model
