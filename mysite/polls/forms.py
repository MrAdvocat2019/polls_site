import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Question, Choice


class NewQuestionForm(forms.Form):
    question_text=forms.CharField(max_length=200)
    pub_date=forms.DateTimeField()

    def clean_pub_date(self):
        data=self.cleaned_data['pub_date']
        if data < timezone.now()-datetime.timedelta(hours=12):
            raise ValidationError("Date is in the past")
        return data
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'productiondate']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']