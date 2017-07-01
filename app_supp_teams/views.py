from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Team
from app_supp_users.models import Profile

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    active_profiles = team.members.filter(
        user__is_active=True
    )
    manager_profiles = active_profiles.filter(
        user__in=team.manager_group.user_set.all(),
    ).order_by('user__last_name')
    member_profiles = active_profiles.exclude(
        user__in=team.manager_group.user_set.all(),
    ).order_by('user__last_name')
    active_templates = team.shift_templates.filter(
        active=True,
    ).exclude(
        deleted_date__lte=timezone.now()
    )
    inactive_templates = team.shift_templates.filter(
        active=False,
    ).exclude(
        deleted_date__lte=timezone.now()
    )
    return render(
        request,
        'app_supp_teams/team_detail.html',
        {'team': team,
        'user': request.user,
        'profile': request.user.profile,
        'date': timezone.now().date,
        'managers': manager_profiles,
        'members': member_profiles,
        'active_templates': active_templates,
        'inactive_templates': inactive_templates,}
    )


@login_required
def edit_membership(request, pk):
    team = get_object_or_404(Team, pk=pk)
    active_profiles = team.members.filter(
        user__is_active=True
    )
    manager_profiles = active_profiles.filter(
        user__in=team.manager_group.user_set.all(),
    ).order_by('user__last_name')
    member_profiles = active_profiles.exclude(
        user__in=team.manager_group.user_set.all(),
    ).order_by('user__last_name')
    non_member_profiles = Profile.objects.filter(
        user__is_active=True,
    ).exclude(
        pk__in=active_profiles.values_list('pk', flat=True),
    ).order_by('user__last_name')
    return render(
        request,
        'app_supp_teams/edit_membership.html',
        {'team': team,
        'user': request.user,
        'profile': request.user.profile,
        'date': timezone.now().date,
        'managers': manager_profiles,
        'members': member_profiles,
        'non_members': non_member_profiles,}
    )


@login_required
def add_manager(request, team_pk, profile_pk):
    team = get_object_or_404(Team, pk=team_pk)
    profile = get_object_or_404(Profile, pk=profile_pk)
    profile.user.groups.add(team.manager_group)
    return edit_membership(request, pk=team.pk)


@login_required
def remove_manager(request, team_pk, profile_pk):
    team = get_object_or_404(Team, pk=team_pk)
    profile = get_object_or_404(Profile, pk=profile_pk)
    if team.manager_group.user_set.count() > 1:
        profile.user.groups.remove(team.manager_group)
    else:
        pass
    return edit_membership(request, pk=team.pk)


@login_required
def add_member(request, team_pk, profile_pk):
    team = get_object_or_404(Team, pk=team_pk)
    profile = get_object_or_404(Profile, pk=profile_pk)
    profile.teams.add(team)
    return edit_membership(request, pk=team.pk)


@login_required
def remove_member(request, team_pk, profile_pk):
    team = get_object_or_404(Team, pk=team_pk)
    profile = get_object_or_404(Profile, pk=profile_pk)
    profile.teams.remove(team)
    return edit_membership(request, pk=team.pk)
