from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

import os

from .models import Upload, UploadForm

@login_required()
def manage_documents(request, pk):
    team = get_object_or_404('app_supp_teams.Team', pk=pk)
    uploads = team.uploads.filter(
        active=True
    ).order_by(
        '-upload_datetime'
    )
    return render(
        request,
        'app_supp_uploads/manage_documents.html',
        {'team': team,
        'uploads': uploads,}
    )


@login_required()
def upload_file(request, pk):
    team = get_object_or_404('app_supp_teams.Team', pk=pk)
    if request.method=="POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            data_file = form.save(commit=False)
            data_file.team = team
            data_file.save()
            return redirect('team_detail', pk=team.pk)
    else:
        form=UploadForm()
    files=Upload.objects.all()
    return render(
        request,
        'app_supp_upload/upload_file.html',
        {'form':form,
        'files':files}
    )


@login_required
def delete_file(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    team = upload.team
    file_location = upload.docfile.path
    upload.delete()
    os.remove(file_location)
    return redirect('team_detail', pk=team.pk)
