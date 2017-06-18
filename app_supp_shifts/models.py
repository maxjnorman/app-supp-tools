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
    deleted_date = models.DateTimeField(blank=True, null=True)
    mon = models.BooleanField(default=True)
    tue = models.BooleanField(default=True)
    wed = models.BooleanField(default=True)
    thu = models.BooleanField(default=True)
    fri = models.BooleanField(default=True)
    sat = models.BooleanField(default=False)
    sun = models.BooleanField(default=False)

    def __str__(self):
        return '%s_%s' % (self.team.team_name, self.shift_name)



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

    def get_users_or_(self, variable):
        users = self.users.filter(
            is_active=True
        ) # Note: not the Profile model
        if users.exists():
            return users
        else:
            return variable
