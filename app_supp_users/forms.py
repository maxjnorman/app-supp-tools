from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Profile

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'date_joined',
        ]




class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'job_title',
            'job_description',
            'start_date',
            'end_date',
        ]
