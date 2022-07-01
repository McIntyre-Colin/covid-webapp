from django import forms
from apps.core.models import Book, ReadingList, Chart


class AddChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ['chart_type', 'day', 'month', 'year', 'stateAbr','filter_field']

class EditChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ['chart_type', 'day', 'month', 'year', 'stateAbr','filter_field']

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']

class AddReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['title', 'category', 'description']

