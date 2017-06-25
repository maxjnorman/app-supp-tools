from django import forms
from django.contrib.auth.models import User

from .models import Shift, ShiftTemplate

class ShiftForm(forms.ModelForm):

    class Meta:
        model = Shift
        fields = [
            'users',
        ]

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        self.fields['users'].widget = forms.CheckboxSelectMultiple()
        self.fields['users'].queryset = User.objects.all()


class TemplateForm(forms.ModelForm):

    class Meta:
        model = ShiftTemplate
        fields = (
            'shift_name',
            'shift_description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'mon',
            'tue',
            'wed',
            'thu',
            'fri',
            'sat',
            'sun',
        )
