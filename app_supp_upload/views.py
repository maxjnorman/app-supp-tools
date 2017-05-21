from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Upload, UploadForm

import os


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
        'uploader/upload_file.html',
        {'form':form,
        'files':files}
    )


def delete_file(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    team = upload.team
    file_location = upload.docfile.path
    upload.delete()
    os.remove(file_location)
    return redirect('team_detail', pk=team.pk)
