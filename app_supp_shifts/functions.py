




class ShiftTemplateOld():
    team = models.ForeignKey(
        'app_supp_teams.Team',
        related_name='shift_templates_old',
    )
    shift_name = models.CharField(max_length=25)
    shift_description = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return '%s_%s' % (self.team.team_name, self.shift_name)

    def apply_shift_template(self, start_date, end_date, day_pattern):   #create Shift objs even if no Day exists (not hard linked)
        start_date_obj = date(start_date.year, start_date.month, start_date.day)
        end_date_obj = date(end_date.year, end_date.month, end_date.day)
        dates = pd.date_range(start_date_obj, end_date_obj).date
        weekdays = (pd.date_range(start_date_obj, end_date_obj).dayofweek)  #uses Mon=0 Sun=6
        dates_df = pd.DataFrame(np.vstack((dates, weekdays)).transpose())
        dates_df.columns = ['dates', 'weekday']
        date_list = []
        for weekday in day_pattern:     #day_pattern should be a list of ints representing weekdays that are selected
            weekday_df = dates_df[['dates']][dates_df['weekday']==weekday]
            date_list = date_list + weekday_df['dates'].tolist()
        database_shifts = Shift.objects.filter(
            shift_template__pk=self.pk,
            day__in=date_list,
        )
        if database_shifts.exists():
            database_dates = database_shifts.values_list('day', flat=True)
            inactive_shifts = database_shifts.filter(
                active=False
            )
            if inactive_shifts.exists():
                inactive_shifts.update(active=True)
            else:
                pass
        else:
            database_dates = []
        missing_dates = set(date_list).difference(set(database_dates))
        if len(missing_dates) > 0:
            new_shifts = []
            for missing_date in missing_dates:
                new_shift = Shift(
                    shift_template=self,
                    day=missing_date
                )
                new_shifts.append(new_shift)
            Shift.objects.bulk_create(new_shifts)
        else:
            pass

    def remove_shift_tempate(self, start_date, end_date, day_pattern):
        start_date_obj = date(start_date.year, start_date.month, start_date.day)
        end_date_obj = date(end_date.year, end_date.month, end_date.day)
        dates = (pd.date_range(start_date_obj, end_date_obj).date)
        weekdays = (pd.date_range(start_date_obj, end_date_obj).dayofweek)  #uses Mon=0 Sun=6
        dates_df = pd.DataFrame(np.vstack((dates, weekdays)).transpose())
        dates_df.columns = ['dates', 'weekday']
        date_list = []
        for weekday in day_pattern:     #day_pattern should be a list of ints representing weekdays that are selected
            weekday_df = dates_df[['dates']][dates_df['weekday']==weekday]
            date_list = date_list + weekday_df['dates'].tolist()
        database_shifts = Shift.objects.filter(
            shift_template__pk=self.pk,
            day__in=date_list,
        )
        if database_shifts.exists():
            database_shifts.update(active=False)
        else:
            pass
