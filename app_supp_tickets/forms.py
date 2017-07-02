from django import forms
from django.forms import Form, ModelForm
from django.forms.formsets import BaseFormSet
from django.contrib.auth.models import User

from .models import UserMap

#Probs. edit to make user readonly
class UserMapForm(Form):
    name = forms.CharField(max_length=100, required=False)
    user = forms.ModelChoiceField(
        User.objects.all(),
        required=False,
        empty_label='',
    )


class BaseMapFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same name or user
        and that all links have both an name and user.
        """
        if any(self.errors):
            return

        names = []
        users = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                name = form.cleaned_data['name']
                user = form.cleaned_data['user']

                # Check that no two links have the same name or user
                if name and user:
                    if name in names:
                        duplicates = True
                    names.append(name)

#                    if user in users:
#                        duplicates = True
#                    users.append(user)

                if duplicates:
                    raise forms.ValidationError(
                        'Links must have unique names and users.',
                        code='duplicate_links'
                    )
#
#                # Check that all links have both an name and user
#                if user and not name:
#                    raise forms.ValidationError(
#                        'All links must have an name.',
#                        code='missing_name'
#                    )
#                elif name and not user:
#                    raise forms.ValidationError(
#                        'All links must have a user.',
#                        code='missing_user'
#                    )
