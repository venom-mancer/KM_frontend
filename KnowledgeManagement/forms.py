from msilib.schema import Class
from pyexpat import model
from django import forms
from django.db.models import fields
from django.db.models.fields import CharField
from KnowledgeManagement.models import TblKnowledgeDocuments, TblKnowledgeTitle,TblKnowledgeRequest,send_to_evaluator
from KnowledgeManagement.models import TblKnowledge,Informs_meeting,FeedFile_Jalase,recive_invitation,rejected_knowledge, Members,Documentation, TblKnowledgeCategory,books,TblJalase,passed_trials ,inventions,articles,FeedFile,skills,pro_degree,edu_records,job_record
from KnowledgeManagement.models import TblKnowledge, Members,Documentation,TblQuestionRequest,TblInform,TblKeyIndicator,TblAnswerQuestionRequest,TblUserRewards, TblKnowledgeCategory,TblExpertReview,books,indicator_assessment_model,passed_trials ,inventions,articles,FeedFile,skills,pro_degree,edu_records,job_record,TblExam,TblQuestion,TblAnswerKnowledgeRequest
from APAvalidations import validate_name, validate_file, validate_image, validate_date
from django.contrib.auth.forms import PasswordChangeForm,UserCreationForm
from .models import Members, TblChartAdvanceInfo, TblKnowledgeValueIT, TblSuervey
from django.forms import ClearableFileInput


class TblInform_FORM(forms.ModelForm):
    class Meta:
        model = TblInform
        fields = "__all__"


class TblKnowledgeValueITForm(forms.ModelForm):
    class Meta:
        model = TblKnowledgeValueIT
        fields = "__all__"
        exclude = ("knowledge",)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Members
        fields = "__all__"  

class DocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = '__all__'

class TblSurveyForm(forms.ModelForm):
    class Meta:
        model = TblSuervey
        fields = '__all__'

class TblExamForm(forms.ModelForm):
    class Meta:
        model = TblExam
        fields = '__all__'


class TblQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
            
    class Meta:
        model = TblQuestion
        fields = '__all__'
        exclude = ("exam_id",)
        required = (
            "question",
            "correct_answer",
            "grade",
        )


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['email','first_name','last_name','username','nationalCode','latest_edu_degree','profile_picture','personal_number','mobileNumber','identity_number','birthday_age','degree','organization_email']

class TblKnowledgeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['KnowledgeTitle'].required = True
        self.fields['KnowledgeProcess'].required = True
        self.fields['KnowledgeFromDate'].required = True
        self.fields['KnowledgetoDate'].required = True
        self.fields['KnowledgeKeywords'].required = True
        self.fields['KnowledgeTextSummary'].required = True

    class Meta:
        model = TblKnowledge
        fields = "__all__"


class TblKnowledgeErteghaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['KnowledgeTitle'].required = True
        self.fields['KnowledgeProcess'].required = True


    class Meta:
        model = TblKnowledge
        fields = "__all__"

class indicator_assessmentForm(forms.ModelForm):
    class Meta:
        model = indicator_assessment_model
        fields = "__all__"

class indicator_KeyForm(forms.ModelForm):
    class Meta:
        model = TblKeyIndicator
        fields = "__all__"

class Informs_meetingForm(forms.ModelForm):
    class Meta:
        model = Informs_meeting
        fields = "__all__"

class TblExpertReviewForm(forms.ModelForm):
    class Meta :
        model = TblExpertReview
        fields = ['description','active_status']
        
class send_to_evaluatorForm(forms.ModelForm):
    class Meta:
        model = send_to_evaluator
        exclude = ('Creater_UserID','mozo1_id','mozo2_id','mozo3_id','knowledge','nazar')


class TblJalaseForm(forms.ModelForm):
    class Meta :
        model = TblJalase
        fields = "__all__"

class DocFileForm(forms.ModelForm):
    class Meta:
        model = FeedFile
        fields = ['file']


class skillsForm(forms.ModelForm):
    class Meta:
        model = skills
        fields = ['skills_file']
        widgets = {
            'skills_file': ClearableFileInput(attrs={'multiple': True}),
        }

class job_recordForm(forms.ModelForm):
    class Meta:
        model = job_record
        fields = ['job_record_file']
        widgets = {
            'job_record_file': ClearableFileInput(attrs={'multiple': True}),
        }

class inventionsForm(forms.ModelForm):
    class Meta:
        model = inventions
        fields = ['inventions_file']
        widgets = {
            'inventions_file': ClearableFileInput(attrs={'multiple': True}),
        }

class edu_recordsForm(forms.ModelForm):
    class Meta:
        model = edu_records
        fields = ['file_edu_records']
        widgets = {
            'file_edu_records': ClearableFileInput(attrs={'multiple': True}),
        }
class articlesForm(forms.ModelForm):
    class Meta:
        model = articles
        fields = ['articles_file']
        widgets = {
            'articles_file': ClearableFileInput(attrs={'multiple': True}),
        }
class pro_degreeForm(forms.ModelForm):
    class Meta:
        model = pro_degree
        fields = ['degree_file']
        widgets = {
            'degree_file': ClearableFileInput(attrs={'multiple': True}),
        }

class FileModelForm(forms.ModelForm):
    class Meta:
        model = FeedFile
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class FeedFile_JalaseForm(forms.ModelForm):
    class Meta:
        model = FeedFile_Jalase
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }

class passed_trialsForm(forms.ModelForm):
    class Meta:
        model = passed_trials
        fields = ['passed_trials_file']
        widgets = {
            'passed_trials_file': ClearableFileInput(attrs={'multiple': True}),
        }

class booksForm(forms.ModelForm):
    class Meta:
        model = books
        fields = ['books_file']
        widgets = {
            'books_file': ClearableFileInput(attrs={'multiple': True}),
        }

class TblKnowledgeDocumentsForm(forms.ModelForm):
    class Meta:
        model = TblKnowledgeDocuments
        fields = "__all__"


class TblUserRewardsForm(forms.ModelForm):
    class Meta:
        model = TblUserRewards
        fields = "__all__"
        exclude = ('reward',)


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=60,
                                   widget=forms.PasswordInput(attrs={'class': "form-control", 'type': 'password'}))
    new_password1 = forms.CharField(max_length=60,
                                    widget=forms.PasswordInput(attrs={'class': "form-control", 'type': 'password'}))
    new_password2 = forms.CharField(max_length=60,
                                    widget=forms.PasswordInput(attrs={'class': "form-control", 'type': 'password'}))

    class Meta:
        model = Members
        fields = ('old_password', 'new_password1', 'new_password2')

class send_invite(forms.ModelForm):
    class Meta:
        model = recive_invitation
        fields = '__all__'
        

class TblKnowledgeRequestForm(forms.ModelForm):
    class Meta:
        model = TblKnowledgeRequest
        fields = ['KnowledgeTitle','KnowledgeProcess','Requestcontents','KnowledgeExpireDate','show_name','send_to_all','knowledge_keywords']


class TblQuestionRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['KnowledgeTitle'].required = True

    class Meta:
        model = TblQuestionRequest
        fields = ['KnowledgeTitle','KnowledgeProcess','Requestcontents','KnowledgeExpireDate','show_name','send_to_all','knowledge_keywords']


class TblAnswerKnowledgeRequestForm(forms.ModelForm):
    class Meta:
        model = TblAnswerKnowledgeRequest
        fields = ['text',]


class TblAnswerQuestionRequestForm(forms.ModelForm):
    class Meta:
        model = TblAnswerQuestionRequest
        fields = ['text',]

class SearchForm(forms.Form):
    # user_name_registered = forms.CharField(label='نام کاربری', max_length=100, required=False,
    #                                        validators=[validate_name])
    user_name_registered = forms.ModelChoiceField(queryset=Members.objects.all(), required=False)
    KnowledgeCategory = forms.ModelChoiceField(queryset=TblKnowledgeCategory.objects.filter(), required=False)
    # from_int_field3 = forms.IntegerField(max_value=200, min_value=0, required=False)
    # to_int_field3 = forms.IntegerField(max_value=200, min_value=0, required=False)
    # from_float_field3 = forms.FloatField(max_value=700.0, min_value=0.0, required=False)
    # to_float_field3 = forms.FloatField(max_value=700.0, min_value=0.0, required=False)
    # char_field3_1 = forms.CharField(max_length=20, required=False)
    # char_field3_2 = forms.CharField(max_length=20, required=False)
    from_date3 = forms.CharField(max_length=10, required=False, validators=[validate_date])
    to_date3 = forms.CharField(max_length=10, required=False, validators=[validate_date])

class rejectForm(forms.ModelForm):
    class Meta:
        model = rejected_knowledge
        fields = '__all__'

    
class TblChartAdvanceInfoForm(forms.ModelForm):
    class Meta:
        model = TblChartAdvanceInfo
        fields = '__all__'
        exclude = ("chart",)