from django import forms

from .models import ShiftTemplate

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
