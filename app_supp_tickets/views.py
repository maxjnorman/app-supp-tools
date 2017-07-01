from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Ticket, UserMap

import pandas as pd
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
    raw_data['code'] = pd.to_numeric(df[code_column].str[2:])
    raw_data['title'] = dataframe['title'].str[:150]
    raw_data['display name'] = dataframe['display name'].str[:50]
    raw_data['source'] = dataframe['source'].str[:20]
    raw_data['first name'] = dataframe['first name'].str[:25]
    raw_data['office'] = dataframe['office'].str[:50]
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
    processed_data = raw_data[desired_columns]
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
def process_docfile(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    file_location = upload.docfile.path
    dataframe = build_dataframe(file_location)
    names = np.unique(df['first name'].dropna(axis=0, how=any).values)
    #loop through usermaps and display username + team (or something)
    #have button to assign user object to unmapped usermaps
    #probably need a 'create user' button as well in case the user doesn't exist
    usermaps = get_usermaps(names)
    #profiles needed?
    team_profiles = upload.team.members.all()
    team_users = User.objects.filter(
        profile__in=upload.team.members.all()
    ).order_by('last_name')
    return render(
        request,
        'app_supp_tickets/process_docfile.html',
        {'usermaps': usermaps,
        'upload': upload,}
    )

#start with the saved document (if possible, if not, build it again)
#use the user supplied data to match the fields with the database objects for users etc...
def populate_database(request, pk):
    upload = get_object_or_404(Upload, pk=pk)
    file_location = upload.docfile.path
    dataframe = process_dataframe(build_dataframe(file_location))
    database_codes = Ticket.objects.filter(
        team=upload.team,
        code__gte=min(dataframe['code']),
        code__lte=max(dataframe['code']),
    ).values_list('code', flat=True)
    conflict_rows = dataframe[(dataframe['code'].isin(database_codes))]
    safe_rows = dataframe[(~dataframe['code'].isin(database_codes))]    #Note: '~' is 'not'
