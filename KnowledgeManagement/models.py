from gettext import NullTranslations
from msilib.schema import Class
from operator import mod
import os
from pyexpat import model
import code
from secrets import choice
from unicodedata import name
import uuid
from venv import create
from django.utils.text import slugify
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.db.models.fields import BooleanField, CharField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey
from django.forms import DateTimeField, FloatField
from APAUtility import LibAPADateTime
from django.db import models
import datetime
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.db.models import Q
from APAvalidations import is_valid_iran_code, validate_image , validate_filesize

# from KnowledgeManagement.views import score_calculator



class Members(AbstractUser):
    
    member = models.AutoField(verbose_name='شماره ثبت', primary_key=True)
    nationalCode = models.IntegerField(verbose_name='کد ملی',validators=[is_valid_iran_code], null=True)
    mobileNumber = models.CharField(verbose_name='شماره همراه', max_length=11, null=True, unique=True)
    personal_number = models.CharField(verbose_name='شماره ی پرسنلی',max_length=160, blank=True, null=True)
    identity_number = models.IntegerField(verbose_name='شماره شناسنامه', blank=True, null=True)
    birthday_age = models.IntegerField(verbose_name='سال تولد', blank=True, null=True)
    address = models.TextField(verbose_name='ادرس', max_length=200, blank=True, default='ahvaz')
    degree = models.CharField(verbose_name='مدرک', max_length=50,null=True, blank=True,default='ندارد')
    organization_email = models.EmailField(verbose_name='ایمیل سازمانی',max_length=70,null=True, blank=True)
    profile_picture = models.ImageField(verbose_name='عکس پروفایل',validators=[validate_image],upload_to='Knowledge_document/',null=True, blank=True)
    latest_edu_degree = models.CharField(verbose_name='اخرین مدرک', max_length=70,null=True, blank=True,default='ندارد')        
    mobile_number2 = models.CharField(verbose_name='شماره تلفن دوم', max_length=16, null=True, blank=True)
    mobile_number3 = models.CharField(verbose_name='شماره تلفن سوم', max_length=16, null=True, blank=True)
    score = models.FloatField(blank=True, null=True)

    real_user = 1
    admin_user = 2
    KnowlesgeTypeChoices = (
        (real_user, "خود کاربر"),
        (admin_user , 'ادمین به جای کاربر'),
    )

    Status = IntegerField('وضعیت', default=1,
                          choices=KnowlesgeTypeChoices, null=True, blank=True)
    def __str__(self):
        return str(self.member)


Active = 1
Deactive = -1
StatusChoices = (
    (Active, "فعال"),
    (Deactive, "غیر فعال"),
)

class Documentation(models.Model):
    documentation_title = models.CharField(verbose_name='عنوان مستند',max_length=200)
    KnowledgeProcess = ForeignKey('TblChart', on_delete=PROTECT, blank=True, null=True)
    KnowledgeKeywords = CharField(max_length=4000, blank=True, null=True)
    describe_documentation = TextField(verbose_name='شرح مستند',max_length=4000,blank=True, null=True)
    documentation_file = models.FileField(upload_to='document_file/', blank=True, null=True)
    CreatorUserID = models.ForeignKey(Members, on_delete=models.PROTECT, null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)

    def __str__(self):
        return str(self.documentation_title)



class TblTeamDocumentation(models.Model):
    joinPercentage=IntegerField(null=True, blank=True)
    DocumentationCode = models.ForeignKey(Documentation, on_delete=models.PROTECT)
    TeamMember = models.ForeignKey(Members, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.DocumentationCode)

class FeedFileDocumentation(models.Model):
    feed = models.ForeignKey(Documentation, on_delete=models.CASCADE)
    file = models.FileField(upload_to='Documentation_document/', blank=True, null=True)
    title=models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return str(self.file)

class pro_degree(models.Model):
    pro_degree_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    degree_file = models.FileField(verbose_name='مدرک حرفه ای',upload_to='Knowledge_document/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class MemberChart(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    chart = models.ForeignKey('TblChart', on_delete=models.PROTECT)
    def __str__(self):
        return str(self.id)
        
class edu_records(models.Model):
    edu_records_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    file_edu_records = models.FileField(verbose_name='سوابق تحصیلی',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class job_record(models.Model):
    job_record_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    job_record_file =  models.FileField(verbose_name='سوابق شغلی',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class skills(models.Model):
    skills_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    skills_file = models.FileField(verbose_name='مهارت ها',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class articles(models.Model):
    article_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    articles_file= models.FileField(verbose_name='مقالات ',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class books(models.Model):
    books_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    books_file = models.FileField(verbose_name='کتاب ها',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class inventions(models.Model):
    inventions_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    inventions_file = models.FileField(verbose_name='اختراعات ',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class passed_trials(models.Model):
    passed_trials_key = models.ForeignKey(Members, on_delete=models.CASCADE)
    passed_trials_file = models.FileField(verbose_name='دوره های گذرانده شده',upload_to='Knowledge_Files/',null=True, blank=True)
    title=models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return str(self.id)




class TblKnowledgeCategory(models.Model):
    """دسته بندی دانش"""


    KnowledgeCategory = models.AutoField(primary_key=True)
    KnowledgeCategoryText = CharField('دسته دانش', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeCategoryText)


class TblKnowledgePermission(models.Model):
    """سطح محرمانگی دانش"""


    KnowledgePermission = models.AutoField(primary_key=True)
    KnowledgePermissionText = CharField('سطح دسترسی', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgePermissionText)


class TblKnowledgeTitle(models.Model):
    """عنوان دانش"""


    KnowledgeTitle = models.AutoField(primary_key=True)
    KnowledgeTitleText = CharField('عنوان تجربه', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeTitleText)



class TblKnowledgeCause(models.Model):
    """علت"""

    KnowledgeCause = models.AutoField(primary_key=True)
    KnowledgeCauseText = CharField('علت', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeCauseText)


# class TblChartManager(models.Manager):
#     def __init__(self)
#         if Parent is None:
#             self.Parent__status = 1


class TblChart(models.Model):

    Chart = models.AutoField(primary_key=True)
    ChartText = CharField('سمت', max_length=200)
    Parent = ForeignKey('TblChart', on_delete=PROTECT, blank=True, null=True)
    location=CharField(max_length=2000,null=True, blank=True)
    
    OrganizationalChart = 1
    KnowledgeField = 2
    Process = 3
    ChartTypesChoices = (
        (OrganizationalChart, "ساختار سازمانی"),
        (KnowledgeField, "حوزه دانش"),
        (Process, "فرآیند دانش")
    )
    ChartType = IntegerField('نوع', default=1, choices=ChartTypesChoices)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.ChartText)


class TblChartDocument(models.Model):
    feed = models.ForeignKey(TblChart, on_delete=models.CASCADE)
    file = models.FileField(upload_to='Knowledge_document/', blank=True, null=True)
    title=models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return str(self.id)

class TblDependentChart(models.Model):
    owner =ForeignKey('TblChartAdvanceInfo', on_delete=PROTECT, blank=True, null=True)
    chart = ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.id)

class TblChartAdvanceInfo(models.Model):
    chart = ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)

    management = 1
    support = 2
    serve = 3
    exclusive = 4
    common = 5
    process_type_choices = (
        (management, "مدیریتی"),
        (support, "پشتیبانی"),
        (serve, "خدمت"),
        (exclusive, "اختصاصی"),
        (common, "مشترک"),
    )
    process_type = IntegerField(default=1, choices=process_type_choices)

    level_0 = 1
    level_1 = 2
    level_2 = 3
    process_level_choices = (
        (level_0, "سطح صفر"),
        (level_1, "سطح یک "),
        (level_2, "سطح دو"),
    )
    process_level = IntegerField( default=1, choices=process_level_choices)

    no_interaction = 1
    has_Sequential = 2
    has_interaction = 3
    connection_with_other_processes_choices = (
        (no_interaction, "بدون تعامل"),
        (has_Sequential, "دارای توالی"),
        (has_interaction, "دارای تعامل"),
    )
    connection_with_other_processes = IntegerField(default=1, choices=connection_with_other_processes_choices)

    request_of_service_recipient = BooleanField(null=True,blank=True)
    arrival_of_specific_time = BooleanField(null=True,blank=True)
    specific_event_occurrence = BooleanField(null=True,blank=True)
    device_detection = BooleanField(null=True,blank=True)

    def __str__(self):
        return str(self.id)


class TblKnowledgeWhichAction(models.Model):
    """چه کاری"""


    KnowledgeDo = models.AutoField(primary_key=True)
    KnowledgeDoText = CharField('چه کاری', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeDoText)


class TblKnowledgeHow(models.Model):
    """چگونه"""

    KnowledgeHow = models.AutoField(primary_key=True)
    KnowledgeHowText = CharField('چگونه', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeHowText)


class TblKnowledgeResource(models.Model):
    """با چه منابعی"""

    KnowledgeResource = models.AutoField(primary_key=True)
    KnowledgeResourceText = CharField('منبع', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeResourceText)


class TblKnowledgeEvaluation(models.Model):
    """ارزیابی"""

    KnowledgeEvaluation = models.AutoField(primary_key=True)
    KnowledgeEvaluationText = CharField('ارزیابی دانش', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeEvaluationText)


class TblKnowledgeConditions(models.Model):
    """تحت چه شرایطی"""


    KnowledgeConditions = models.AutoField(primary_key=True)
    KnowledgeConditionsText = CharField('تحت چه شرایطی', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeConditionsText)


class TblKnowledgeRisks(models.Model):
    """ریسک ها"""



    KnowledgeRisks = models.AutoField(primary_key=True)
    KnowledgeRisksText = CharField('ریسک ها', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeRisksText)


class TblKnowledgeResults(models.Model):
    """نتایج"""



    KnowledgeResults = models.AutoField(primary_key=True)
    KnowledgeResultsText = CharField('نتایج', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeResultsText)


class TblKnowledgeUsedCases(models.Model):
    """موارد استفاده"""



    KnowledgeUsedCases = models.AutoField(primary_key=True)
    KnowledgeUsedCasesText = CharField('موارد استفاده', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeUsedCasesText)


class TblKnowledgeOpportunities(models.Model):
    """موارد استفاده"""


    KnowledgeOpportunities = models.AutoField(primary_key=True)
    KnowledgeOpportunitiesText = CharField('فرصت ها', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeOpportunitiesText)


class TblUsedDomain(models.Model):
    """دامنه کاربرد"""


    UsedDomain = models.AutoField(primary_key=True)
    UsedDomainText = CharField(max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.UsedDomainText)


class TblKnowledgeProblemPreventation(models.Model):
    """چگونه می توان از بروز تجربه مشکل جلوگیری کرد"""


    KnowledgeProblemPreventation = models.AutoField(primary_key=True)
    KnowledgeProblemPreventationText = CharField(
        'چگونه می توان از بروز تجربه مشکل جلوگیری کرد', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeProblemPreventationText)


class TblManagmentSystemTrend(models.Model):
    """اولویت گردش اطلاعات"""
    SystemId = models.AutoField(primary_key=True)
    SystemText = CharField(max_length=200)
    Priority = IntegerField()

    CreatorUserID = models.ForeignKey(
        Members, on_delete=models.PROTECT, null=True)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)
    field1 = IntegerField(blank=True, null=True)
    field2 = IntegerField(blank=True, null=True)
    field3 = CharField(max_length=200, blank=True, null=True)
    field4 = CharField(max_length=200, blank=True, null=True)


class TblKnowledgeSpecial(models.Model):
    """سطح ویژگی دانش"""



    KnowledgeSpecial = models.AutoField(primary_key=True)
    KnowledgeSpecialText = CharField('ویژه', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KnowledgeSpecialText)


class TblIsGroup(models.Model):
    """گروه دانش """

    IsGroup = models.AutoField(primary_key=True)
    IsGroupText = CharField('گروه', max_length=200)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.IsGroupText)



class TblKnowledge(models.Model):
    """دانش"""
    KnowledgeCode = models.AutoField(primary_key=True)
    KnowledgeIsSpecial=ForeignKey(
        TblKnowledgeSpecial, on_delete=PROTECT, blank=True, null=True)
    KnowledgePermission = ForeignKey(
        TblKnowledgePermission, on_delete=PROTECT, blank=True, null=True)
    KnowledgeIsGroup=ForeignKey(
        TblIsGroup, on_delete=PROTECT, blank=True, null=True)
    KnowledgeTitle = CharField(max_length=200, blank=True, null=True)
    KnowledgePlace = CharField(verbose_name='مکان',max_length=200,blank=True, null=True)
    KnowledgeFromDate = IntegerField(blank=True, null=True,verbose_name='از تاریخ')
    KnowledgetoDate = IntegerField(blank=True, null=True,verbose_name='تا تاریخ')
    KnowledgeCause = TextField(verbose_name='رویداد یا مشکلی که منجر به کسب تجربه شده',max_length=4000, blank=True, null=True)
    KnowledgeProcess = ForeignKey(
        TblChart, on_delete=PROTECT, blank=True, null=True)
    KnowledgeWhichAction = TextField(verbose_name='شرح تجربه(روش حل مشکل)',max_length=4000, blank=True, null=True)
    Knowledgedate = CharField(max_length=800, blank=True, null=True)
    KnowledgeResults = TextField(verbose_name='نتایج اجرای تجربه',max_length=4000, blank=True, null=True)
    KnowledgeUsedCases = TextField(verbose_name='پیشنهادات حاصل از تجربه',max_length=4000, blank=True, null=True)
    KnowledgeUsers = TextField(verbose_name='مخاطبان و کاربران (موارد کاربرد)',max_length=4000, blank=True, null=True)
    KnowledgeTextSummary = TextField('خلاصه ی دانش',max_length=4000, blank=True, null=True) 
    KnowledgeKeywords = CharField(max_length=4000, blank=True, null=True,verbose_name='واژگان کلیدی ')
    KnowledgeProblems=TextField(verbose_name='بیان مشکلات',max_length=4000, blank=True, null=True) 
    KnowledgeSolution=TextField(verbose_name='ارایه راهکار های اجرای حل مشکلات',max_length=4000, blank=True, null=True)
    KnowledgeTellJobSpecial=TextField(verbose_name='بیان خصوصیات و ویژگی های شغل خود',max_length=4000, blank=True, null=True)
    KnowledgeJobSuccess=TextField(verbose_name='موفقیت های شغلی کسب شده',max_length=4000, blank=True, null=True)
    KnowledgeSpecialReason = TextField('دلیل ویژه بودن', max_length=4000,default='ندارد',blank=True, null=True)
    CreatorUserID = models.ForeignKey(
        Members, on_delete=models.PROTECT, null=True, blank=True)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    voice_url = models.CharField(max_length=350, blank=True, null=True)
    KnowledgeVideo = models.FileField(upload_to='Knowledge_video/', blank=True, null=True)
    KnowledgeVoice = models.FileField(upload_to='Knowledge_voice/', blank=True, null=True)
    KnowledgeDocument = models.FileField(upload_to='Knowledge_document/', blank=True, null=True)
    field1 = IntegerField(blank=True, null=True)
    field2 = IntegerField(blank=True, null=True)
    field3 = CharField(max_length=200, blank=True, null=True)
    field4 = CharField(max_length=200, blank=True, null=True)
    Experience = 1
    Documentation = 6
    Comparative = 3
    Skills = 4
    JobImprovement = 5
    KnowlesgeTypeChoices = (
        (Experience, "تجربه"),
        (Documentation , 'مستندات'),
        (Comparative, "تجربه تطبیقی"),
        (Skills, "تجربه مهارت"),
        (JobImprovement, "ارتقای شغلی"),
    )
    Type = IntegerField('نوع دانش', default=1, choices=KnowlesgeTypeChoices)

    perm_register = 1
    temp_register = 2
    temp_register2 = 3
    it_canceled = 4
    it_sent_to_evaluator = 5
    rejected_by_eval = 6
    its_knowledge = 7
    rejected_by_security = 8
    accepted_by_security = 9

    status_choices = (
        (perm_register, "(ارسال شده)"),
        (temp_register, "(ثبت معمولی) "),
        (temp_register2, "(ثبت موقت)"),
        (it_canceled, "کنسل کردن تجربه توسط آی تی"),
        (it_sent_to_evaluator, "فرستادن تجربه توسط آی تی به ارزیاب"),
        (rejected_by_eval, "این تجربه توسط ارزیاب رد شد"),
        (its_knowledge, "این تجربه توسط ارزیاب تایید شده"),
        (rejected_by_security, " دانش توسط حراست رد شد"),
        (accepted_by_security, "دانش توسط حراست قبول شد"),
    )
    register_status = IntegerField('وضعیت ثبت', default=2, choices=status_choices)
    liked_count = IntegerField('تعداد لایک ها', default=0, blank=True)
    view_count = IntegerField('تعداد بازدید', default=0, blank=True)

    real_user = 1
    admin_user = 2
    who_registered = (
        (real_user, "خود کاربر"),
        (admin_user , 'ادمین به جای کاربر'),
    )

    Status_who_registered = IntegerField('وضعیت', default=1,
                          choices=who_registered, null=True, blank=True)

    set_number = IntegerField(default=1, null=True, blank=True)

    R = models.FloatField( blank=True, null=True)
    kpi = models.IntegerField( blank=True, null=True)


    def __str__(self):
        return str(self.KnowledgeTitle)



class TblKnowledgeStatusNotification(models.Model):
    """
    tells knowledge status to knowledge worker
    """

    notif = ForeignKey(TblKnowledge,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)

    IT_ACCEPT = 6
    IT_REJECT = 7
    EXPERT_ACCEPT = 8
    EXPERT_REJECT = 9
    SECURITY_ACCEPT = 14
    SECURITY_REJECT = 15

    NOTIF_TYPE_CHOICES = (
        (IT_ACCEPT, "نوتیف دبیرخانه قبول کردن"),
        (IT_REJECT, "نوتیف دبیرخانه رد کردن"),
        (EXPERT_ACCEPT , "نوتیف خبره قبول"),
        (SECURITY_ACCEPT , " قبول کردن نوتیف حراست"),
        (SECURITY_REJECT , " رد کردن نوتیف حراست"),

    )
    notif_type = IntegerField(default =  6 , choices = NOTIF_TYPE_CHOICES)


    def __str__(self):
        return str(self.id)

class FeedFile(models.Model):
    feed = models.ForeignKey(TblKnowledge, on_delete=models.CASCADE)
    file = models.FileField(upload_to='Knowledge_document/', blank=True, null=True)
    title=models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return str(self.file)

class FeedFile_Jalase(models.Model):
    feed = models.ForeignKey('TblJalase', on_delete=models.CASCADE)
    file = models.FileField(upload_to='jalase_document/', blank=True, null=True)
    title=models.CharField(max_length=500, blank=True, null=True)
    def __str__(self):
        return str(self.title)

class view(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    post = models.ForeignKey(TblKnowledge, on_delete=models.CASCADE)
    CreateDate = IntegerField(
        'تاریخ بازدید', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class like(models.Model):
    user = models.ForeignKey(Members, on_delete=models.CASCADE)
    post = models.ForeignKey(TblKnowledge, on_delete=models.CASCADE)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)

    def __str__(self):
        return str(self.id)

class TblTeam_Jalase(models.Model):
    TeamId = models.AutoField(primary_key=True)
    joinPercentage=IntegerField(null=True, blank=True)
    JalaseCode = models.ForeignKey('TblJalase', on_delete=models.PROTECT)
    TeamMember = models.ForeignKey(Members, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.TeamId)
        
class TblTeam(models.Model):
    TeamId = models.AutoField(primary_key=True)
    joinPercentage=IntegerField(null=True, blank=True)
    KnowledgeCode = models.ForeignKey(TblKnowledge, on_delete=models.PROTECT)
    TeamMember = models.ForeignKey(Members, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.KnowledgeCode)


class TblKnowledgeDocuments(models.Model):
    KnowledgeDocumentsCode = models.AutoField(primary_key=True)
    KnowledgeCode = models.OneToOneField(
        TblKnowledge, on_delete=models.PROTECT, null=True, blank=True)
    KnowledgeMap = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    Knowledgeslides = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    Knowledgefilm = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    Knowledgedocument = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeJournal = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgePicture = models.ImageField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeProceedings = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgePaper = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeHandout = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeProcessingMethod = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeBook = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeInstructions = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeLetter = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    KnowledgeReport = models.FileField(
        upload_to='KnowledgeDocuments/', blank=True, null=True)
    CreatorUserID = models.ForeignKey(
        Members, on_delete=models.PROTECT, null=True, blank=True)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    field1 = IntegerField(blank=True, null=True)
    field2 = IntegerField(blank=True, null=True)
    field3 = CharField(max_length=200, blank=True, null=True)
    field4 = CharField(max_length=200, blank=True, null=True)


class TblKeywords(models.Model):
    """کلید واژه ها"""


    Keywords = models.AutoField(primary_key=True)
    KeywordsText = CharField(max_length=200, verbose_name='کلمات کلیدی')
    Knowledge = ForeignKey(TblKnowledge, on_delete=PROTECT)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    Status = IntegerField('وضعیت', default=1, choices=StatusChoices)

    def __str__(self):
        return str(self.KeywordsText)

class TblKnowledgeRequest(models.Model):
    """ درخواست دانش"""


    KnowledgeTitle = CharField(max_length=200, blank=True, null=True)
    KnowledgeProcess = ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)
    Requestcontents = TextField(verbose_name='محتویات درخواست',max_length=4000, blank=True, null=True)
    CreatorUserID = models.ForeignKey(Members, on_delete=models.PROTECT, null=True, blank=True)
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    KnowledgeExpireDate = IntegerField(blank=True, null=True)
    show_name = BooleanField(default=True)
    knowledge_keywords = CharField(max_length=500,blank=True, null=True)
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    send_to_all=BooleanField(default=False)
    mozo3_id = ForeignKey('topic3',on_delete=models.PROTECT,blank=True, null=True)

    def __str__(self):
        return str(self.KnowledgeTitle)



class TblKnowledgeRequestNotification(models.Model):

    notif = ForeignKey(TblKnowledgeRequest,on_delete=models.CASCADE,blank=True, null=True)
    user = ForeignKey(Members,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    notif_type = IntegerField(default =  3 )


    def __str__(self):
        return str(self.id)

class TblQuestionRequest(models.Model):
    """ درخواست سوال"""
#I used the same model as TblKnowledgeRequest so then we dont have to make another template

    KnowledgeTitle = CharField(max_length=200, blank=True, null=True)
    KnowledgeProcess = ForeignKey(TblChart, on_delete=PROTECT, blank=True, null=True)
    Requestcontents = TextField(verbose_name='محتویات درخواست سوال',max_length=4000, blank=True, null=True)
    CreatorUserID = models.ForeignKey(Members, on_delete=models.PROTECT, null=True, blank=True)
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    KnowledgeExpireDate = IntegerField(blank=True, null=True)
    show_name = BooleanField(default=True)
    knowledge_keywords = CharField(max_length=500,blank=True, null=True)
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    send_to_all=BooleanField(default=False)
    mozo3_id = ForeignKey('topic3',on_delete=models.PROTECT,blank=True, null=True)

    def __str__(self):
        return str(self.KnowledgeTitle)



class TblQuestionRequestNotification(models.Model):

    notif = ForeignKey(TblQuestionRequest,on_delete=models.CASCADE,blank=True, null=True)
    user = ForeignKey(Members,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    notif_type = IntegerField(default = 4)

    def __str__(self):
        return str(self.id)


class TblAnswerKnowledgeRequest(models.Model):

    text = TextField(verbose_name='محتویات درخواست',max_length=4000, blank=True, null=True)
    CreatorUserID = models.ForeignKey(Members, on_delete=models.PROTECT, null=True, blank=True)
    knowledge_request = models.ForeignKey(TblKnowledgeRequest, on_delete=models.PROTECT, null=True, blank=True)
    CreateDate = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)


class TblAnswerQuestionRequest(models.Model):

    text = TextField(verbose_name='محتویات درخواست',max_length=4000, blank=True, null=True)
    CreatorUserID = models.ForeignKey(Members, on_delete=models.PROTECT, null=True, blank=True)
    knowledge_request = models.ForeignKey(TblQuestionRequest, on_delete=models.PROTECT, null=True, blank=True)
    CreateDate = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)


class TblTeam2(models.Model):
    TeamId = models.AutoField(primary_key=True)
    KnowledgeCode = models.ForeignKey(TblKnowledgeRequest, on_delete=models.PROTECT)
    TeamMember = models.ForeignKey(Members, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.TeamId)

class TblJalase(models.Model):
    """جلسات"""
    JalaseCode = models.AutoField(primary_key=True)
    KnowledgeIsSpecial=ForeignKey(
        'TblKnowledgeSpecial', on_delete=PROTECT, blank=True, null=True)
    KnowledgePermission = ForeignKey(
        'TblKnowledgePermission', on_delete=PROTECT, blank=True, null=True)
    KnowledgeIsGroup=ForeignKey(
        'TblIsGroup', on_delete=PROTECT, blank=True, null=True)
    JalaseTitle = CharField(max_length=200, blank=True, null=True)
    JalasePlace = CharField(verbose_name='مکان',max_length=200,blank=True, null=True)
    JalaseFromDate = IntegerField(blank=True, null=True)
    JalasetoDate = IntegerField(blank=True, null=True)
    JalaseCause = TextField(max_length=4000, blank=True, null=True)
    KnowledgeProcess = ForeignKey(
        'TblChart', on_delete=PROTECT, blank=True, null=True)
    JalaseWhichAction = TextField(max_length=4000, blank=True, null=True)
    Jalasedate = CharField(max_length=800, blank=True, null=True)
    JalaseResults = TextField(max_length=4000, blank=True, null=True)
    JalaseUsedCases = TextField(max_length=4000, blank=True, null=True)
    JalaseUsers = TextField(max_length=4000, blank=True, null=True)
    JalaseSummary = TextField(max_length=4000, blank=True, null=True) 
    JalaseKeywords = CharField(max_length=4000, blank=True, null=True)
    JalaseSpecialReason = TextField(max_length=4000,default='ندارد',blank=True, null=True)
    CreatorUserID = models.ForeignKey(
        Members, on_delete=models.PROTECT, null=True, blank=True)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    voice_url = models.CharField(max_length=350, blank=True, null=True)
    it_canceled = 1
    submited = 2
    status_choices = (
        (it_canceled, "کنسل شد "),
        (submited, "ثبت شد"),
    )
    jalase_status = IntegerField('وضعیت', default=2,
                          choices=status_choices, null=True, blank=True)

    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.JalaseTitle)

class recive_invitation(models.Model):

    JalaseCode = models.ForeignKey('TblJalase', on_delete=models.PROTECT,blank=True, null=True)
    send_to_users = ForeignKey(Members,on_delete=PROTECT, blank=True, null=True)
    def __str__(self):
        return str(self.send_to_users)

class rejected_knowledge(models.Model):
    knowledge_id = ForeignKey(TblKnowledge,on_delete=PROTECT, blank=True, null=True)
    reject_reason = TextField(max_length=4000,default='',null=False, blank=False)
    rejecter_user_id = ForeignKey(Members,on_delete=PROTECT, blank=True, null=True)
    rejected_title = CharField(max_length=500, blank=True, null=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    rejected_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    CreateDate = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
        
class TblExam(models.Model):
    code=CharField(max_length=200, blank=True, null=True)
    name=CharField(max_length=200, blank=True, null=True)
    create_date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), blank=True, null=True)
    from_date=IntegerField(blank=True, null=True)
    to_date=IntegerField(blank=True, null=True)
    from_hour=models.TimeField(blank=True, null=True)
    question_file = models.FileField(upload_to='Question_file/', blank=True, null=True)
    to_hour=models.TimeField(blank=True, null=True)
    creator=models.ForeignKey(Members, on_delete=models.PROTECT , blank=True, null=True)
    description=TextField(max_length=4000, blank=True, null=True) 
    Status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    sent=1
    not_sent=-1
    examSendChoices = (
        (sent, "ارسال شده"),
        (not_sent , 'ارسال نشده'),
    )
    send_status = IntegerField(default=-1, choices=examSendChoices, null=True, blank=True)

    sent_to_all = BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return str(self.name)

class TblExamNotification(models.Model):

    notif = ForeignKey(TblExam,on_delete=models.CASCADE,blank=True, null=True)
    user = ForeignKey(Members,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    notif_type = IntegerField(default = 1)

    def save(self, *args, **kwargs):
        self.url = 'inform_exam/'+ str(self.notif.id)
        super(TblExamNotification, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class SendExam2member(models.Model):
    exam_id = models.ForeignKey(TblExam, on_delete=models.PROTECT)
    member_id = models.ForeignKey(Members, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

class TblQuestion(models.Model):
    exam_id = models.ForeignKey(TblExam, on_delete=models.PROTECT , null=True, blank=True)
    question=TextField(max_length=4000, blank=True, null=True)
    correct_answer=IntegerField(blank=True, null=True)
    grade=IntegerField(blank=True, null=True)
    quesion_file = models.FileField(upload_to='Question_file/', blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class TblQuestionOptions(models.Model):
    question_id = models.ForeignKey(TblQuestion, on_delete=models.PROTECT)
    option_text=CharField(max_length=200, blank=True, null=True)
    option_number=IntegerField(blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    is_answer=BooleanField(null=True,blank=True)
    def __str__(self):
        return str(self.id)

class TblAnswerOption(models.Model):
    option_id=models.ForeignKey(TblQuestionOptions, on_delete=models.PROTECT, null=True, blank=True)
    member_id = models.ForeignKey(Members, on_delete=models.PROTECT)
    exam_id= models.ForeignKey(TblExam, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class topic1(models.Model):
    mozo1= models.CharField(max_length=200)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class topic2(models.Model):
    state=models.CharField(max_length=200)
    mozo1 = models.ForeignKey(topic1,on_delete=models.PROTECT)    
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)   
    def __str__(self):
        return str(self.id)
        
class topic3(models.Model):
    city=models.CharField(max_length=200)
    mozo2=models.ForeignKey(topic2 ,on_delete=models.PROTECT)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class ExpertChart(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    chart = models.ForeignKey('TblChart', on_delete=models.PROTECT)
    def __str__(self):
        return str(self.id)

class send_to_evaluator(models.Model):

    mozo1_id = ForeignKey(topic1,on_delete=models.PROTECT,blank=True, null=True)
    mozo2_id = ForeignKey(topic2,on_delete=models.PROTECT,blank=True, null=True)
    mozo3_id = ForeignKey(topic3,on_delete=models.PROTECT,blank=True, null=True)
    nazar = TextField(verbose_name='اظهار نظر',max_length=4000)
    create_date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), blank=True, null=True)
    Creater_UserID = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    knowledge = ForeignKey(TblKnowledge,on_delete=models.PROTECT,blank=True, null=True)
    def __str__(self):
        return str(self.id)

class Informs_meeting(models.Model):

    meeting_reciver = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    meeting_title = CharField(verbose_name='عنوان جلسه',max_length=600)
    create_date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), blank=True, null=True)
    it_canceled = 1
    sent = 2
    status_choices = (
        (it_canceled, "کنسل شد "),
        (sent, "ارسال شده"),
    )
    meeting_status = IntegerField('وضعیت جلسه', default=2,
                          choices=status_choices, null=True, blank=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)

    has_notif = 1
    remove_notif = 2
    notif_choices = (
        (has_notif, " notification دارد "),
        (remove_notif, "notification حذف "),
    )               
    notif_status = IntegerField('notif_status', default=1,
                          choices=notif_choices, null=True, blank=True)
    
    meeting_location_place = CharField(verbose_name='مکان جلسه',max_length=600,default='')
    meeting_start_time=models.TimeField(blank=True, null=True)
    meeting_start_date=IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class indicator_assessment_model(models.Model):
    indicator_point = models.FloatField(default=1.0,
    validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
)
    indicator = CharField(max_length=600)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class TblExpertReview(models.Model):
    description = TextField(max_length=4000,blank=True,null=True)
    expert = ForeignKey(Members,on_delete=PROTECT, null=True, blank=True)
    active = 1
    inactive = 2
    active_status_choices = (
        (active, " فعال  "),
        (inactive, "  راکد"),
    )               
    active_status = IntegerField('وضعیت فعال بودن', default=1,
                          choices=active_status_choices)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)
    knowledge = ForeignKey(TblKnowledge,on_delete=PROTECT, null=True, blank=True)
    score = IntegerField(default=0, null=True, blank=True)
    set_number = IntegerField(default=1, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class TblExpertReviewIndicatorAssessment(models.Model):
    expert_review = ForeignKey(TblExpertReview,on_delete=PROTECT)
    indicator_assessment = ForeignKey(indicator_assessment_model,on_delete=PROTECT)
    score = IntegerField(default=0)
    def __str__(self):
        return str(self.id)


class TblVoteQuestion(models.Model):
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    knowledge_request = models.ForeignKey(TblKnowledgeRequest, on_delete=models.PROTECT, null=True, blank=True)

    like = 1
    dislike = 2
    vote_status_choices = (
        (like, " لایک  "),
        (dislike, " دیس لایک"),
    )

    vote_status= IntegerField('وضعیت', default=1,choices=vote_status_choices, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class TblVoteSendQuestion(models.Model):
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    knowledge_request = models.ForeignKey(TblQuestionRequest, on_delete=models.PROTECT, null=True, blank=True)

    like = 1
    dislike = 2
    vote_status_choices = (
        (like, " لایک  "),
        (dislike, " دیس لایک"),
    )

    vote_status= IntegerField('وضعیت', default=1,choices=vote_status_choices, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class TblUsedKnowledge(models.Model):
    
    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    knowledge = models.ForeignKey(TblKnowledge, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return str(self.id)


class TblVotesForQuestionAnswer(models.Model):
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    knowledge_request_answer = models.ForeignKey(TblAnswerQuestionRequest, on_delete=models.PROTECT, null=True, blank=True)

    like = 1
    dislike = 2
    vote_status_choices = (
        (like, " لایک  "),
        (dislike, " دیس لایک"),
    )

    vote_status= IntegerField('وضعیت', default=1,choices=vote_status_choices, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class TblVoteQuestionAnswer(models.Model):
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized())
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    knowledge_request_answer = models.ForeignKey(TblAnswerKnowledgeRequest, on_delete=models.PROTECT, null=True, blank=True)

    like = 1
    dislike = 2
    vote_status_choices = (
        (like, " لایک  "),
        (dislike, " دیس لایک"),
    )

    vote_status= IntegerField('وضعیت', default=1,choices=vote_status_choices, null=True, blank=True)

    def __str__(self):
        return str(self.id)



class TblSuervey(models.Model):
    code=CharField(max_length=200, blank=True, null=True)
    name=CharField(max_length=200, blank=True, null=True)
    create_date = IntegerField(
        'تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), blank=True, null=True)
    from_date=IntegerField(blank=True, null=True)
    to_date=IntegerField(blank=True, null=True)
    from_hour=models.TimeField(blank=True, null=True)
    to_hour=models.TimeField(blank=True, null=True)
    creator=models.ForeignKey(Members, on_delete=models.PROTECT , blank=True, null=True)
    description=TextField(max_length=4000, blank=True, null=True) 
    Status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    sent=1
    not_sent=-1
    suerveySendChoices = (
        (sent, "ارسال شده"),
        (not_sent , 'ارسال نشده'),
    )
    send_status = IntegerField(default=-1, choices=suerveySendChoices, null=True, blank=True)

    question=TextField(max_length=4000, blank=True, null=True)
    
    one_choice = 1
    multiple_choice = 2
    answer_choices = (
        (one_choice, "جواب تک گزینه ای"),
        (multiple_choice , 'جواب چند گزینه ای'),
    )

    answer_status = IntegerField(default=1, choices=answer_choices, null=True, blank=True)

    sent_to_all = BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return str(self.name)


class TblSurveyotification(models.Model):

    notif = ForeignKey(TblSuervey,on_delete=models.CASCADE,blank=True, null=True)
    user = ForeignKey(Members,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    notif_type = IntegerField(default = 2)

    def __str__(self):
        return str(self.id)


class TblSuerveyOptions(models.Model):
    survey_id = models.ForeignKey(TblSuervey, on_delete=models.PROTECT)
    option_text=CharField(max_length=200, blank=True, null=True)
    option_number=IntegerField(blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)
    def __str__(self):
        return str(self.id)


class TblAnswerOptionSurvey(models.Model):
    option_id=models.ForeignKey(TblSuerveyOptions, on_delete=models.PROTECT, null=True, blank=True)
    member_id = models.ForeignKey(Members, on_delete=models.PROTECT)
    suervey= models.ForeignKey(TblSuervey, on_delete=models.PROTECT, null=True, blank=True)
    comment=TextField(max_length=4000, blank=True, null=True) 
    def __str__(self):
        return str(self.id)


class SendSurvey2Member(models.Model):
    survey = models.ForeignKey(TblSuervey, on_delete=models.PROTECT)
    member = models.ForeignKey(Members, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)


class TblFollowed(models.Model):
    """
    this table indicates the person who is followed
    """

    who_is_followed = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class TblFollowerFollowedIndicator(models.Model):
    """
    this table indicates the person who is followed plus the person who is the follower
    """

    followed = ForeignKey(TblFollowed,on_delete=models.PROTECT,blank=True, null=True)
    follower = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)

    def __str__(self):
        return str(self.id)



class TblMessageUser(models.Model):
    """
    this table indicates the person who gets the message and sends the message
    """

    reciver = IntegerField(null=True, blank=True)
    sender = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    text = TextField(max_length=4000,blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)

    def __str__(self):
        return str(self.text)


class TblMessageUserNotification(models.Model):

    notif = ForeignKey(TblMessageUser,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    notif_type = IntegerField(default = 5)

    def __str__(self):
        return str(self.id)

class TblInform(models.Model):

    Creater_UserID = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    from_date=IntegerField(blank=True, null=True)
    to_date=IntegerField(blank=True, null=True)
    title = CharField(max_length=300,blank=True, null=True)
    text = TextField(max_length=4000,blank=True, null=True)
    Status = IntegerField('وضعیت', default=1,
                          choices=StatusChoices, null=True, blank=True)

    def __str__(self):
        return str(self.id)



class TblScoreFormula(models.Model):

    like=IntegerField(blank=True, null=True)
    followers=IntegerField(blank=True, null=True)
    use_knowledge=IntegerField(blank=True, null=True)
    knowledge_seen=IntegerField(blank=True, null=True)
    registered_knowledge_count=IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)





class TblUsedQuestionKnowledge(models.Model):
    
    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    Questionknowledge = models.ForeignKey(TblKnowledgeRequest, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class TblUsedQuestionRequest(models.Model):

    creater_user_id = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    QuestionkRequest = models.ForeignKey(TblQuestionRequest, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return str(self.id)





def score_calculator(user):
    my_questions = TblKnowledgeRequest.objects.filter(CreatorUserID=user)
    total_user_likes = TblVoteQuestion.objects.filter(knowledge_request__in=my_questions)
    up_votes = len(total_user_likes.filter(vote_status = 1))
    if TblFollowed.objects.filter(who_is_followed = user).exists():
        followers = len(TblFollowerFollowedIndicator.objects.filter(followed=TblFollowed.objects.get(who_is_followed = user)))
    else:
        followers = 0
    view_count = len(view.objects.filter(post__in = TblKnowledge.objects.values_list('KnowledgeCode', flat=True).filter(CreatorUserID=user)))
    my_knowledge = len(TblKnowledge.objects.filter(CreatorUserID=user).filter(Q(register_status=7) | Q(register_status=9)).filter(Status=1))
    my_knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID=user)
    my_used_knowledge = len(TblUsedKnowledge.objects.filter(knowledge__in=my_knowledges))
    score_formula = TblScoreFormula.objects.all()

    score  = score_formula[0]

    score = ( (up_votes * score.like) + (followers * score.followers) + (view_count * score.knowledge_seen) + (my_knowledge * score.registered_knowledge_count) + (my_used_knowledge * score.use_knowledge) ) / (score.like + score.followers + score.knowledge_seen + score.registered_knowledge_count + score.use_knowledge )

    return score

def score_trigger(sender , **kwargs):
    if kwargs['created']:
        users = Members.objects.all()
        for user in users:
            user.score = score_calculator(user)
            user.save()


post_save.connect(score_trigger,sender=TblScoreFormula)


class TblChatMessage(models.Model):

    reciver = IntegerField(null=True, blank=True)
    sender = ForeignKey(Members,on_delete=models.PROTECT,blank=True, null=True)
    create_hour = models.TimeField(default=datetime.datetime.now(), null=True, blank=True)
    create_date = IntegerField('تاریخ ثبت', default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)
    text = TextField(max_length=4000,blank=True, null=True)
    status = IntegerField('وضعیت', default=1,choices=StatusChoices, null=True, blank=True)

    def __str__(self):
        return str(self.id)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename_without_ext = '.'.join(filename.split('.')[:-1])
    filename = "{}{}.{}".format(filename_without_ext , uuid.uuid4() ,ext )
    return os.path.join(f'records', filename)        


class TblVoiceRecord(models.Model):

    voice_url = models.CharField(max_length=3500,unique=True, blank=True, null=True)
    voice_record = models.FileField(upload_to='records')

    def __str__(self):
        return str(self.id)


class TblKnowledgeNotificationForEliteUsers(models.Model):

    notif = ForeignKey(TblKnowledge,on_delete=models.CASCADE,blank=True, null=True)
    user = ForeignKey(Members,on_delete=models.CASCADE,blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)

    IT_has_Notif = 10
    Expert_has_Notif = 11
    Security_has_Notif = 12
    notif_choices = (
        (IT_has_Notif, "  تجربه جدید برای دبیرخانه "),
        (Expert_has_Notif, " تجربه جدید برای خبره  "),
        (Security_has_Notif, " تجربه جدید برای حراست  "),
    )

    notif_type = IntegerField(choices=notif_choices, null=True, blank=True)

    def __str__(self):
        return str(self.notif)

class TblKeyIndicator(models.Model):

    key_indicator = CharField(max_length=300)
    from_range = models.PositiveIntegerField('از بازه', default=1, )
    to_range = models.PositiveIntegerField('تا بازه', default=10,)
    expire_date = IntegerField(blank=True, null=True,verbose_name=' تاریخ انقضا')

    active = 1
    inactive = 0
    status_choice = (
        (active, "  فعال"),
        (inactive, " غیر فعال "),
    )
    status = IntegerField(choices=status_choice, default=1, null=True, blank=True)

    def __str__(self):
        return str(self.key_indicator)



class TblKpiExpertReview(models.Model):
    kpi = ForeignKey(TblKeyIndicator ,on_delete=models.CASCADE,blank=True, null=True)
    expert_review = ForeignKey(TblExpertReview,on_delete=models.CASCADE,blank=True, null=True)
    percent = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)], blank=True, null=True)
    knowledge = ForeignKey(TblKnowledge,on_delete=PROTECT, null=True, blank=True)
    set_number = IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class TblKnowledgeValueIT(models.Model):
    knowledge = ForeignKey(TblKnowledge,on_delete=PROTECT, null=True, blank=True)
    profit_before = models.IntegerField( blank=True, null=True)
    profit_after = models.IntegerField( blank=True, null=True)
    knowledge_cost = models.IntegerField( blank=True, null=True)
    date = IntegerField(default=LibAPADateTime.get_persian_date_normalized(), null=True, blank=True)

    def __str__(self):
        return str(self.id)


class TblUserRewards(models.Model):

    user = ForeignKey(Members,on_delete=PROTECT, null=True, blank=True)
    admin_point = models.IntegerField( blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    date = IntegerField(default=LibAPADateTime.get_persian_year_normalized(), null=True, blank=True)
    base_salary_cofficent = models.FloatField(blank=True, null=True)
    reward = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
        