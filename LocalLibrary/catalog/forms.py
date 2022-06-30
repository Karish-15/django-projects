from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between no and 4 weeks (default is 3).", required=False)
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        if data<datetime.date.today():
            raise ValidationError(_('Invalid date - Renewal date cannot be past'))
        
        if data>datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data