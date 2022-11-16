from msilib.schema import Class
from pyexpat import model
from django import forms
from django.db.models import fields
from django.db.models.fields import CharField
from feedback_suggestions_app.models import TblSuggestion , TblIndicatorAssesment , TblExpertReview_suggestion , TblRejectSuggestionByIt , TblIndicatorAssesment_workingroup , TblWorkingGroupReview_suggestion


class TblSuggestionForm(forms.ModelForm):
    class Meta:
        model = TblSuggestion
        exclude = ('create_date','creator_user_id','suggestion_specialty','register_status')


class TblIndicatorAssesment_Form(forms.ModelForm):
    class Meta:
        model = TblIndicatorAssesment
        fields = "__all__"


class TblExpertReview_suggestionForm(forms.ModelForm):
    class Meta :
        model = TblExpertReview_suggestion
        fields = ['description',]


class TblRejectSuggestionByIt_Form(forms.ModelForm):
    class Meta :
        model = TblRejectSuggestionByIt
        fields = ['reason' , 'title']


class TblIndicatorAssesment_workingroupForm(forms.ModelForm):
    class Meta :
        model = TblIndicatorAssesment_workingroup
        fields = "__all__"


class TblWorkingGroupReview_suggestionForm(forms.ModelForm):
    class Meta :
        model = TblWorkingGroupReview_suggestion
        fields = ['description',]