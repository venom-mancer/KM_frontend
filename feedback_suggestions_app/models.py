import datetime
from django.db import models
from APAUtility import LibAPADateTime
from KnowledgeManagement.models import Members, TblChart 
from django.db.models.deletion import PROTECT
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import BooleanField, CharField, IntegerField, TextField

Active = 1
Deactive = -1
StatusChoices = (
    (Active, "فعال"),
    (Deactive, "غیر فعال"),
)

TRUE_SHAPE = 1 
FALSE_SHAPE = 0
SHAPE_CHOICES = (
    (TRUE_SHAPE , 'True'),
    (FALSE_SHAPE , 'False')
)

class TblSuggestion(models.Model):

    suggestion_background = models.CharField(max_length=200, blank=True, null=True)
    suggestion_title = models.CharField(max_length=200,blank=True, null=True)
    description_of_proposed_suggestion = models.TextField(max_length=4000, blank=True, null=True)
    required_facilities = models.TextField(max_length=4000, blank=True, null=True)
    describe_method = models.TextField(max_length=4000, blank=True, null=True)
    is_way_fix_bugs_disadvantages = models.IntegerField('وضعیت', default=0,choices=SHAPE_CHOICES, null=True, blank=True)
    is_suggestion_group = models.IntegerField('وضعیت', default=0,choices=SHAPE_CHOICES, null=True, blank=True)
    create_date = models.IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    creator_user_id = models.ForeignKey(Members, on_delete=models.PROTECT, null=True, blank=True)
    status = models.IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)

    PERM_REGISTER = 1
    SENT_TO_IT_FROM_SUGGESTOR = 2
    REJECTED_BY_IT = 3
    SENT_IT_TO_COMMITEE = 4
    COMMITEE_SENT_IT = 5
    IT_TO_WORKING_GROUP = 6
    WORKING_GROUP_TO_IT = 7
    FINAL_ACCEPT_IT = 8
    status_choices = (
        (PERM_REGISTER, "ثبت "),
        (SENT_TO_IT_FROM_SUGGESTOR, "ارسال شده به آی تی از طرف پیشنهاد دهنده "),
        (REJECTED_BY_IT , 'توسط دبیرخانه رد شد'),
        (SENT_IT_TO_COMMITEE, "ارسال از دبیرخانه به کمیته"),
        (COMMITEE_SENT_IT, "ارسال ازکمیته به دبیرخانه  "),
        (IT_TO_WORKING_GROUP, "ارسال از دبیرخانه به کارگروه "),
        (WORKING_GROUP_TO_IT , 'ارسال از کارگروه به دبیرخانه'),
        (FINAL_ACCEPT_IT , ' تایید نهایی توسط دبیرخانه'),

    )

    register_status = models.IntegerField('وضعیت ثبت', default=1, choices=status_choices)
    suggestion_specialty = models.ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)


    def __str__(self):
        return str(self.id)


class TblSuggestionTeam(models.Model):
    join_percentage=IntegerField(null=True, blank=True)
    suggestion_id = models.ForeignKey(TblSuggestion, on_delete=models.PROTECT)
    user = models.ForeignKey(Members, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.id)

class TblIndicatorAssesment(models.Model):
    indicator_point = models.FloatField(default=1.0,
    validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],)
    indicator = CharField(max_length=600)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.id)


class TblExpertReview_suggestion(models.Model):
    description = TextField(max_length=4000,blank=True,null=True)      
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    suggestion = ForeignKey(TblSuggestion,on_delete=PROTECT, null=True, blank=True)
    committe_given_score = IntegerField(default=0)
    time = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    def __str__(self):
        return str(self.id)


class TblExpertReviewIndicatorAssessment(models.Model):
    committee_review = ForeignKey(TblExpertReview_suggestion,on_delete=PROTECT)
    indicator_assessment = ForeignKey(TblIndicatorAssesment,on_delete=PROTECT)
    score = IntegerField(default=0)
    def __str__(self):
        return str(self.id)



class TblRejectSuggestionByIt(models.Model):
    suggestion_id = ForeignKey(TblSuggestion,on_delete=PROTECT, blank=True, null=True)
    reason = TextField(max_length=4000,default='',null=False, blank=False)
    commenter = ForeignKey(Members,on_delete=PROTECT, blank=True, null=True)
    title = CharField(max_length=500, blank=True, null=True)
    status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    time = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)

    def __str__(self):
        return str(self.id)

class TblSendSuggestionItToCommittee(models.Model):
    suggestion_id = ForeignKey(TblSuggestion,on_delete=PROTECT, blank=True, null=True)
    explenation = TextField(max_length=4000,default='',null=False, blank=False)
    user_id = ForeignKey(Members,on_delete=PROTECT, blank=True, null=True)
    status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    time = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)

    def __str__(self):
        return str(self.id)



class TblCommitteeSpecialty(models.Model):
    user = models.ForeignKey(Members, on_delete=models.PROTECT)
    specialty = models.ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class TblWorkingGroupSpecialty(models.Model):
    user = models.ForeignKey(Members, on_delete=models.PROTECT)
    specialty = models.ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Tblcommitte_comment_result(models.Model):
    committee_review = ForeignKey(TblExpertReview_suggestion,on_delete=PROTECT, blank=True, null=True)
    committe_given_score = IntegerField(default=0)
    def __str__(self):
        return str(self.id)


class TblIndicatorAssesment_workingroup(models.Model):
    indicator_point = models.FloatField(default=1.0,
    validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],)
    indicator = CharField(max_length=600)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.id)


class TblWorkingGroupReview_suggestion(models.Model):
    description = TextField(max_length=4000,blank=True,null=True)      
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    suggestion = ForeignKey(TblSuggestion,on_delete=PROTECT, null=True, blank=True)
    workingroup_given_score = IntegerField(default=0)
    time = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    def __str__(self):
        return str(self.id)


class TblWorkingroupReviewIndicatorAssessment(models.Model):
    workingroup_review = ForeignKey(TblWorkingGroupReview_suggestion,on_delete=PROTECT)
    indicator_assessment = ForeignKey(TblIndicatorAssesment_workingroup,on_delete=PROTECT)
    score = IntegerField(default=0)
    def __str__(self):
        return str(self.id)
