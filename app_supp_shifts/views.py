from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import date

from .models import Shift, ShiftTemplate
from .forms import TemplateForm, ShiftForm
from app_supp_teams.models import Team
from app_supp_shifts.models import ShiftTemplate





@login_required
def shift_create(request, pk, year, month, day):
    template = get_object_or_404(ShiftTemplate, pk=pk)
    date_obj = date(int(year), int(month), int(day))
    shift = Shift(
        day=date_obj,
        shift_template=template
    )
    shift.save()
    return redirect(
        'shifts:shift_assign',
        pk=shift.pk,
        year=date_obj.year,
        month=date_obj.month,
        day=date_obj.day,
    )


@login_required
def shift_assign(request, pk, year, month, day):
    shift = get_object_or_404(Shift, pk=pk)
    date_obj = date(int(year), int(month), int(day))
    if request.method == "POST":
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.save()
            form.save_m2m()
            return redirect(
                'calendar:month_view',
                pk=shift.shift_template.team.pk,
                year=year,
                month=month,
                day=day,
            )
    else:
        form = ShiftForm(instance=shift)
    return render(
        request,
        'app_supp_shifts/shift_create.html',
        {'form': form,}
    )




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
        {'form': form,
        'team': team,}
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
        {'form': form,
        'team': template.team,}
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
