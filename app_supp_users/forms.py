from django.forms import ModelForm

from .models import Profile

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'job_title',
            'job_description',
            'start_date',
            'end_date',
        ]
