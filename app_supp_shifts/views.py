from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import ShiftTemplate
from .forms import TemplateForm
from app_supp_teams.models import Team

@login_required
def template_activate(request, pk):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    template.active = True
    template.save()
    return redirect('teams:team_detail', pk=template.team.pk)


@login_required
def template_create(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.team = team
            template.save()
            return redirect('teams:team_detail', pk=team.pk)
    else:
        form = TemplateForm()
    return render(
        request,
        'app_supp_shifts/template_create.html',
        {'form': form}
    )


@login_required
def template_deactivate(request, pk):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    template.active = False
    template.save()
    return redirect('teams:team_detail', pk=template.team.pk)


@login_required
def template_deactivate_calendar(request, pk, year, month, day):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    template.active = False
    template.save()
    return redirect(
        'calendar:month_view',
        pk=template.team.pk,
        year=year,
        month=month,
        day=day
    )


@login_required
def template_delete(request, pk):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    template.active = False
    template.deleted_date = timezone.now()
    template.save()
    return redirect('teams:team_detail', pk=template.team.pk)


@login_required
def template_edit(request, pk):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    if request.method == "POST":
        form = TemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            template.save()
            return redirect('teams:team_detail', pk=template.team.pk)
    else:
        form = TemplateForm(instance=template)
    return render(
        request,
        'app_supp_shifts/template_create.html',
        {'form': form}
    )


@login_required
def template_edit_calendar(request, pk, year, month, day):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    if request.method == "POST":
        form = TemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            template.save()
            return redirect(
                'calendar:month_view',
                pk=template.team.pk,
                year=year,
                month=month,
                day=day
            )
    else:
        form = TemplateForm(instance=template)
    return render(
        request,
        'app_supp_shifts/template_create.html',
        {'form': form}
    )
