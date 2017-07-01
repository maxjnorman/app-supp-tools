from django.db import models
from django.forms import ModelForm

class Upload(models.Model):
    docfile = models.FileField("Document", upload_to="uploads/")
    file_name = models.CharField(max_length=100)
    upload_datetime = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey('app_supp_teams.Team', related_name='uploads')
    active = models.BooleanField(default=True)
