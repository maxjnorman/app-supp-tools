from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProfileForm, UserForm
from app_supp_teams.models import Team

#Maybe set it to go from team page
#Stop reg users from creating profiles
@login_required()
def admin_user_create(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
        return redirect('users:admin_profile_create', user_pk=user.pk, team_pk=team_pk)
    else:
        form = UserForm()
    return render(
        request,
        'app_supp_users/admin_user_create.html',
        {'form': form,
        'team': team,}
    )


@login_required()
def admin_profile_create(request, team_pk, user_pk):
    team = get_object_or_404(Team, pk=team_pk)
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            if not profile.teams.filter(members=profile).exists():
                profile.teams.add(team)
        return redirect('users:user_detail', pk=user.pk)
    else:
        form = ProfileForm()
    return render(
        request,
        'app_supp_users/admin_profile_create.html',
        {'form': form,
        'user': user,
        'team': team,}
    )


@login_required
def user_detail(request, user_pk):
    redirect('global:home_page')


@login_required()
def create_profile(request):    #Note: Only for creating 'own' profile
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


@login_required()
def user_admin(request):
    try:
        request.user.profile
    except ObjectDoesNotExist:
        return redirect('users:create_profile')
    return render(
        request,
        'app_supp_users/user_admin.html',
        {'user': request.user,
        'profile': request.user.profile,}
    )


#Note: maybe make into a user_edit_self function
@login_required
def user_edit(request, pk):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            pass
    return None
