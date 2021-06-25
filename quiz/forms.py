from django import forms


class QForm(forms.Form):
    answer = forms.CharField(max_length=200)