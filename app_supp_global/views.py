from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from app_supp_teams.models import Team

@login_required
def home_page(request): # Note: return back here afterwards
    return redirect('global:landing_page')

@login_required
def landing_page(request):
    try:
        request.user.profile
    except ObjectDoesNotExist:
        return redirect('users:create_profile')
    member_teams = request.user.profile.teams.all()
    non_member_teams = Team.objects.filter(
        active=True,
    ).exclude(pk__in=member_teams.values_list('id', flat=True))
    return render(
        request,
        'app_supp_global/landing_page.html',
        {'user': request.user,
        'profile': request.user.profile,
        'member_teams': member_teams,
        'non_member_teams': non_member_teams,}
    )
