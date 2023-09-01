from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.ChoiceField(choices=CustomUser.objects.all().values_list('username', 'username'))
    password = forms.CharField(widget=forms.PasswordInput)


class PeriodForm(forms.Form):
    start_date = forms.DateField(input_formats='%d-%m-%Y', widget=forms.DateInput(attrs={'type':'date', 'placeholder':'dd-mm-yyyy'}))
    end_date = forms.DateField(input_formats='%d-%m-%Y', widget=forms.DateInput(attrs={'type':'date', 'placeholder':'dd-mm-yyyy'}))

    def clean_end_date(self):
        if self.cleaned_data.get('start_date', False) < self.cleaned_data.get('end_date', False):
            return forms.ValidationError("You can upload only one of image or video.")
        return self.cleaned_data['end_date']