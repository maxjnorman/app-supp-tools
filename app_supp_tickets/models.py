from django.db import models

class Ticket(models.Model):
    ir_code = models.PositiveSmallIntegerField(max_length=6)
    team = models.ForeignKey(blank=True, null=True, related_name='tickets')
    assigned_to = models.ForeignKey(blank=True, null=True, related_name='tickets')
    created_date = models.DateTimeField()
    last_modified = models.DateTimeField() #Not needed?
    priority = models.PositiveSmallIntegerField(max_length=1, default=3)
    status = models.PositiveSmallIntegerField(max_length=1) #Might not be needed - implied from resolved date
    resolved_date = models.DateTimeField(blank=True, null=True)
    sla_achieved = models.NullBooleanField(null=True)
    source = models.CharField(default='unknown')
    title = models.CharField() #For humans only? #Even needed at all?
    affected_party = models.CharField() #Probably not needed (but maybe)
    affected_department = models.CharField(default='unknown') #Could be a foreignkey but ++complexity overall

    def __str__(self):
        return self.ir_code


    def get_status(self):
        #return string rep of active/resolved/pending
        pass


    def get_source(self):
        #return string rep of ticket source (email, console, or phone)
