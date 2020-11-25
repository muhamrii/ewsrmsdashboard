from django import forms
##


class RequestHistoricalForm(forms.Form):
    startdate = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    enddate = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])