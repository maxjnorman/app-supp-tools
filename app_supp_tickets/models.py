from django.db import models
from django.contrib.auth.models import User

from app_supp_teams.models import Team

from datetime import datetime, timedelta

class UserMap(models.Model):
    name = models.CharField(unique=True, max_length=100)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='usermaps',
        on_delete=models.SET_NULL,
    )


#might need a team map but not sure
#class TeamMap(models.Model):
#    name = models.CharField(unique=True, max_length=100)
#    team = models.ForeignKey(Team, blank=True, null=True, related_name='maps')


class Ticket(models.Model):
    code = models.PositiveSmallIntegerField()
    #could use string instead of fk(?)
    #might be better to use a TeamMap object (if the usermaps turn out well)
    #might be good for deleting / altering teams
    team = models.ForeignKey('app_supp_teams.Team', related_name='tickets', blank=True, null=True)
    #need to choose whether to assign an actual fk or not
    #just using a string may work better with the usermaps and for unassigned tickets
    #could also assign to a UserMap but it's not clear what the benefit would be (if any)
    assigned_to_str = models.CharField(max_length=25)
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='tickets')
    created_date = models.DateTimeField()
    #last_modified = models.DateTimeField() #Not needed?
    priority = models.PositiveSmallIntegerField(default=3)
    sla_date = models.DateTimeField()
    #status = models.PositiveSmallIntegerField(max_length=1) #Might not be needed - implied from resolved date
    resolved_date = models.DateTimeField(blank=True, null=True)
    #sla_achieved = models.NullBooleanField(null=True)
    source = models.CharField(default='unknown', max_length=20)
    title = models.CharField(max_length=150) #For humans only? #Even needed at all?
    affected_party = models.CharField(max_length=50) #Probably not needed (but maybe)
    affected_department = models.CharField(default='unknown', max_length=50) #Could be a foreignkey but ++complexity overall

    def __str__(self):
        return self.ir_code


    def is_resolved(self):
        if not self.resolved_date:
            return False
        else:
            return True


    def get_sla_date(self):
        delta_dict = {
            '1': timedelta(days=1),
            '2': timedelta(days=2),
            '3': timedelta(days=7),
            '4': timedelta(days=14),
        }
        return self.created_date + delta_dict[self.priority]
