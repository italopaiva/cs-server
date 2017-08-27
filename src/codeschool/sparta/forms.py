from django import forms
from .models import UserGrade

class CsvUploadForm(forms.Form):
    csv_file = forms.FileField()


class NewUserGradeForm(forms.ModelForm):
    class Meta:
        model = UserGrade
        fields = ('user', 'grade')
