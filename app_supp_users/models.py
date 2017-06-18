from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    job_title = models.CharField(max_length=25)
    job_description = models.CharField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    teams = models.ManyToManyField(
        'app_supp_teams.Team',
        related_name='members',
        blank=True
    )

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
