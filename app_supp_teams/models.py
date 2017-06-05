from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from app_supp_calendar.models import Year


class Team(models.Model):
    manager_group = models.OneToOneField(Group, related_name='team', null=True)        #use to check if User is in Group. Allow editing etc...
    team_name = models.CharField(max_length=50)
    manager_group_name = models.CharField(max_length=60, default='No Name Set')
    start_date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    default_shift_templates = models.ManyToManyField(
        'app_supp_shifts.ShiftTemplate',
        related_name='default_shifts',
        blank=True,
    )

    def __str__(self):
        return self.team_name

    def create_year_set(self):
        database_year_list = list(Year.objects.filter(
            team__pk=self.pk,
            year__gte=self.start_date.year,
            year__lte=timezone.now().year
        ).values_list('year', flat=True))
        if timezone.now().month <= 10:
            year_delta = 1
        else:
            year_delta = 2
        year_list = list(range(
            self.start_date.year,
            timezone.now().year + year_delta
            ))
        if set(database_year_list) == set(year_list):
            pass
        else:
            missing_years = set(year_list).difference(set(database_year_list))
            new_years = []
            for n in missing_years:
                new_year = Year(
                    account=self,
                    year=n,
                )
                new_years.append(new_year)
            Year.objects.bulk_create(new_years)

    def create_manager_group(self):
        if hasattr(self, manager_group):
            if self.manager_group.name == self.manager_group_name:
                pass
            else:
                self.manager_group.name = self.manager_group_name
                self.manager_group.save()
        else:
            manager_group = Group(name = self.manager_group_name)
            manager_group.save()
            self.manager_group = manager_group
            self.save()
