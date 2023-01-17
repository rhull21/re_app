from django import forms 

class ContactForm(forms.Form):
    sender_choices = [('me', 'Me'),
                       ('you', 'You'),
                       ('NULL', 'Somebody Else')]

    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.CharField(label='Who From?' , widget=forms.Select(choices=sender_choices))
    cc_myself = forms.BooleanField(required=False)

class DeltaDryForm(forms.Form):
    group_by_choices = [('YEAR', 'Year'),
                        ('MONTH', 'Month'),
                        ('DATE', 'Date')]

    group_by = forms.CharField(label='Group Selection By... ', widget=forms.Select(choices=group_by_choices))