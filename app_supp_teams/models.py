from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group


class Team(models.Model):
    manager_group = models.OneToOneField(Group, related_name='team', null=True)        #use to check if User is in Group. Allow editing etc...
    team_name = models.CharField(max_length=50)
    start_date = models.DateField(default=timezone.now)
    active = models.BooleanField(default=True)
    deleted_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.team_name


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


    def start_time(self):
        return min(
            team.shift_templates.filter(
                active=True,
            ).exclude(
                deleted_date__lte=timezone.now(),
                start_date__gte=timezone.now().date,
                end_date__lte=timezone.now().date,
            ).values_list(
                'start_time', flat=True
            ), default=None
        )


    def end_time(self):
        return max(
            team.shift_templates.filter(
                active=True,
            ).exclude(
                deleted_date__lte=timezone.now(),
                start_date__gte=timezone.now().date,
                end_date__lte=timezone.now().date,
            ).values_list(
                'end_time', flat=True
            ), default=None
        )
