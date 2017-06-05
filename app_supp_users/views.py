from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProfileForm

@login_required()
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            try:
                request.user.profile
            except ObjectDoesNotExist:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
            return redirect('global:home_page')
    else:
        form = ProfileForm()
    return render(
        request,
        'app_supp_users/create_profile.html',
        {'user': request.user,
        'form': form}
    )
