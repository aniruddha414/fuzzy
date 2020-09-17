from django import forms

class FormName(forms.Form):
    temperature = forms.FloatField()
    humidity = forms.IntegerField()

class FormRules(forms.Form):
    temperature = forms.CharField()
    humidity = forms.CharField()
    power = forms.CharField()

class FormDel(forms.Form):
    temperature = forms.CharField()
    humidity = forms.CharField()