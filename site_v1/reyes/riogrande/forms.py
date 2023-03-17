from django import forms 

class ContactForm(forms.Form):
    sender_choices = [('me', 'Me'),
                       ('you', 'You'),
                       ('NULL', 'Somebody Else')]

    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.CharField(label='Who From?' , widget=forms.Select(choices=sender_choices))
    cc_myself = forms.BooleanField(required=False)

class DryLenFlowForm(forms.Form):
    month_choices =     [(6, "Jun"),
                         (7, "Jul"),
                         (8, "Aug"),
                         (9, "Sep"),
                         (10, "Oct"),
                         (None, "All" )]
    


    month_select = forms.CharField(label='Months of Interest: ', widget=forms.Select(choices=month_choices))
    subplot_bool = forms.BooleanField(label='Hide Subplots?')

class DrySelectForm(forms.Form):
    group_by_choices = [('YEAR', 'Year'),
                        ('MONTH', 'Month'),
                        ('DATE', 'Date')]

    reach_choices = [   ('All', 'All'),
                        ('Angostura', 'Angostura'),
                        ('San Acacia', 'San Acacia'),
                        ('Isleta', 'Isleta')]

    group_by = forms.CharField(label='Group by time period', widget=forms.Select(choices=group_by_choices))
    reach_select = forms.CharField(label='Filter by reach', widget=forms.Select(choices=reach_choices))