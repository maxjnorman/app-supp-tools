from django.shortcuts import render, redirect

@login_required
def home_page(request):
    return redirect('landing_page')

@login_required
def landing_page(request):
    member_teams = request.user.profile.teams.all()
    non_member_teams = Team.objects.filter(
        active=True,
    ).exclude(pk__in=member_teams.values_list(pk, flat=True))
    return render(
        request,
        'app_supp_teams/team_list.html',
        {'member_teams': member_teams,
        'non_member_teams': non_member_teams,
        'user': request.user,
        'profile': request.user.profile}
    )
