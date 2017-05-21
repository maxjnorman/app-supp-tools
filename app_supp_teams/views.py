from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Team

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    member_profiles = team.members.filter(
        user__is_active=True,
    ).order_by('user.first_name')
    manager_profiles = member_profiles.filter(
        user__pk__in=team.manager_group,
    )

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    active_members = team.members.filter(
        user__is_active=True
    )
    manager_profiles = active_members.filter(
        user__in=team.manager_group.users,
    ).order_by('user.first_name')
    member_profiles = active_members.exclude(
        pk__in=manager_profiles.values_list('id', flat=True)
    ).order_by('user.first_name')

    return render(
        'app_supp_teams/team_detail.html',
        {'team': team,
        }
    )
