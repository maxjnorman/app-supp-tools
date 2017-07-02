from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction

from .models import Ticket, UserMap
from app_supp_upload.models import Upload
from app_supp_users.models import Profile
from .forms import UserMapForm, BaseMapFormSet

import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

def read_worksheet(xls_file, worksheet):
    dataframe = xls_file.parse(worksheet)
    dataframe.columns = [string.lower() for string in dataframe.columns]
    if dataframe.empty:
        return None
    else:
        return dataframe


def build_dataframe(file_location):
    xls_file = pd.ExcelFile(file_location)
    dataframe_list = [
            read_worksheet(xls_file, worksheet)
            for worksheet
            in xls_file.sheet_names
        ]
    return pd.concat(dataframe_list)


def find_code_column(dataframe):
    code_column = False
    n = 0
    while not code_column:
        n += 1
        for column in dataframe.columns:
            if type(dataframe[column][n]) == str:
                if dataframe[column][n][:2] == 'IR':
                    if len(dataframe[column][n]) == 8:
                        code_column = column
    return code_column


def process_dataframe(dataframe):
    code_column = find_code_column(dataframe)
    dataframe['code'] = pd.to_numeric(dataframe[code_column].str[2:])
    dataframe['title'] = dataframe['title'].str[:150]
    dataframe['display name'] = dataframe['display name'].str[:50]
    dataframe['source'] = dataframe['source'].str[:20]
    dataframe['first name'] = dataframe['first name'].str[:25]
    dataframe['office'] = dataframe['office'].str[:50]
    desired_columns = [
        'code',
        'first name',
        'created date',
        'priority',
        'resolved date',
        'source',
        'title',
        'display name',
        'office',
    ]
    processed_data = dataframe[desired_columns]
    processed_columns = [
        'code',
        'assigned_to_str',
        'created_date',
        'priority',
        'resolved_date',
        'source',
        'title',
        'affected_party',
        'affected_department',
    ]
    processed_data.columns = processed_columns
    return processed_data


def get_usermaps(names_list):
    database_names = UserMap.objects.filter(
        name__in=names_list
    ).values_list(
        'name', flat=True
    )
    if set(database_names) != set(names_list):
        unknown_names = list(set(names_list).difference(set(database_names)))
        new_usermaps = [UserMap(name=name, user=None) for name in unknown_names]
        UserMap.objects.bulk_create(new_usermaps)
    return UserMap.objects.filter(name__in=names_list).order_by('name')


# upload the document, get the usermaps from the database (or create new ones)
# send doc + usermaps to view to check mapping is correct and/or perform mapping
# after mapping
def map_docfile(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    file_location = upload.docfile.path
    dataframe = build_dataframe(file_location)
    names = np.unique(dataframe['first name'].dropna(axis=0, how=any).values)
    #loop through usermaps and display username + team (or something)
    #have button to assign user object to unmapped usermaps
    #probably need a 'create user' button as well in case the user doesn't exist
    usermaps = get_usermaps(names)
    UserMapFormSet = formset_factory(UserMapForm, formset=BaseFormSet)
    map_data = [
        {'name': usermap.name,
        'user': usermap.user,}
        for usermap
        in usermaps
        ]
    if request.method == 'POST':
        map_formset = UserMapFormSet(request.POST)
        if map_formset.is_valid():
            new_mappings = []
            #Note: this creates new objects after each submit
            #Note: need to check if new UserMaps different from old ones
            for map_form in map_formset:
                name = map_form.cleaned_data.get('name')
                user = map_form.cleaned_data.get('user')
                if name and user:
                    new_mappings.append(UserMap(name=name, user=user))
            valid_mappings = [
                usermap
                for usermap
                in new_mappings
                if usermap.user
                is not None
            ]
            valid_map_names = [usermap.name for usermap in valid_mappings]
            try:
                with transaction.atomic():
                    UserMap.objects.filter(name__in=valid_map_names).delete()
                    UserMap.objects.bulk_create(valid_mappings)
            except IntegrityError:
                return render(
                    request,
                    'app_supp_global/landing_page.html'
                )
            return populate_database(request, pk=upload.pk, dataframe=dataframe)

    else:
        map_formset = UserMapFormSet(initial=map_data)
    return render(
        request,
        'app_supp_tickets/map_docfile.html',
        {'usermaps': usermaps,
        'upload': upload,
        'map_formset': map_formset,}
    )

#start with the saved document (if possible, if not, build it again)
#use the user supplied data to match the fields with the database objects for users etc...
def populate_database(request, pk, dataframe):
    upload = get_object_or_404(Upload, pk=pk)
    dataframe = process_dataframe(dataframe)
    team_mapstrings = UserMap.objects.filter(
        user__in=User.objects.filter(
            profile__in=upload.team.members.all(),
        ),
    ).values_list('name', flat=True)
    database_codes = Ticket.objects.filter(
        team=upload.team,
        code__gte=min(dataframe['code']),
        code__lte=max(dataframe['code']),
    ).values_list('code', flat=True)
    conflict_rows = dataframe[
        (dataframe['code'].isin(database_codes))
        &
        (dataframe['assigned_to_str'].isin(team_mapstrings))
    ].values
    safe_rows = dataframe[
        (~dataframe['code'].isin(database_codes))
        &
        (dataframe['assigned_to_str'].isin(team_mapstrings))
    ].values
    safe_tickets = []
    for n in range(0, safe_rows.shape[0]):
        safe_tickets.append(
            Ticket(
                code=safe_rows[n,0],
                assigned_to_str=safe_rows[n,1],
                created_date=safe_rows[n,2],
                priority=safe_rows[n,3],
                resolved_date=safe_rows[n,4],
                source=safe_rows[n,5],
                title=safe_rows[n,6],
                affected_party=safe_rows[n,7],
                affected_department=safe_rows[n,8]
            )
        )
    test = safe_tickets[0]
    test.save()
    k=k
    return render(
        request,
        'app_supp_global/landing_page.html'
    )
