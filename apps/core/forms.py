from django import forms
from apps.core.models import Chart, StatesList, ChartProperties


class AddChartForm(forms.ModelForm):
    class Meta:
        model = ChartProperties
        fields = ['title','chart_type', 'day', 'month', 'year', 'stateAbr','filter_field']

class EditChartForm(forms.ModelForm):
    class Meta:
        model = ChartProperties
        fields = ['title','chart_type', 'day', 'month', 'year','filter_field']

class AddStateForm(forms.ModelForm):
    class Meta:
        model = StatesList
        fields = ['state']
      

