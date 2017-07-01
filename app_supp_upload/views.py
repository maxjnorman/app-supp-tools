from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

import os

from .models import Upload
from .forms import UploadForm
from app_supp_teams.models import Team

@login_required()
def manage_documents(request, pk):
    team = get_object_or_404(Team, pk=pk)
    active_uploads = team.uploads.filter(
        active=True
    ).order_by(
        '-upload_datetime'
    )
    inactive_uploads = team.uploads.filter(
        active=False
    ).order_by(
        '-upload_datetime'
    )
    return render(
        request,
        'app_supp_upload/manage_documents.html',
        {'team': team,
        'active_uploads': active_uploads,
        'archived_uploads': inactive_uploads,}
    )


@login_required()
def upload_file(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method=="POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = form.save(commit=False)
            data_file.team = team
            data_file.save()
            return manage_documents(request, pk=team.pk)
    else:
        form=UploadForm()
    files=Upload.objects.filter(
        team=team,
    ).order_by(
        '-upload_datetime',
    )[:5]
    return render(
        request,
        'app_supp_upload/upload_file.html',
        {'form':form,
        'files':files,
        'team': team,}
    )


@login_required()
def delete_file(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    team = upload.team
    file_location = upload.docfile.path
    upload.delete()
    os.remove(file_location)
    return manage_documents(request, pk=team.pk)


@login_required()
def active_file(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    team = upload.team
    upload.active = True
    upload.save()
    return manage_documents(request, pk=team.pk)


@login_required()
def deactive_file(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    team = upload.team
    upload.active = False
    upload.save()
    return manage_documents(request, pk=team.pk)
