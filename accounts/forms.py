from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=125)
    password = forms.CharField(widget=forms.PasswordInput)


class PeriodForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
