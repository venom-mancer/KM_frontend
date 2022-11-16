from django.contrib import admin
from django.db.models import fields
from KnowledgeManagement.models import Members
from .models import Members, SendSurvey2Member, TblAnswerOptionSurvey, TblChartAdvanceInfo, TblChartDocument, TblDependentChart, TblKnowledgeValueIT, TblKpiExpertReview, TblScoreFormula, TblSuervey, TblSuerveyOptions, books 
from .forms import UserCreationForm,CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from KnowledgeManagement.models import TblKnowledge, TblKnowledgeCategory, TblKnowledgePermission, \
    TblKnowledgeTitle, TblKnowledgeCause, TblKnowledgeWhichAction, TblKnowledgeHow, \
    TblKnowledgeResource, TblKnowledgeEvaluation, TblKnowledgeConditions, TblKnowledgeRisks,books,Documentation, TblKnowledgeResults, TblUserRewards,\
    TblKnowledgeUsedCases,send_to_evaluator,TblVoiceRecord,TblInform,TblTeamDocumentation,TblKnowledgeNotificationForEliteUsers,TblKeyIndicator,TblExamNotification,TblSurveyotification,TblTeam_Jalase,TblUsedKnowledge,TblExpertReview,TblQuestionRequest,TblVoteSendQuestion,TblAnswerQuestionRequest,TblExpertReviewIndicatorAssessment,recive_invitation,Informs_meeting,indicator_assessment_model, TblUsedDomain,rejected_knowledge,skills,inventions,passed_trials,FeedFile_Jalase, TblKnowledgeProblemPreventation,articles, TblChart,pro_degree,job_record, TblKeywords,edu_records, TblTeam, like, view,TblKnowledgeDocuments,FeedFile,TblKnowledgeSpecial,TblIsGroup,TblKnowledgeRequest,TblTeam2,FeedFileDocumentation,TblJalase,TblKnowledgeUsedCases, TblUsedDomain,skills,inventions,passed_trials, TblKnowledgeProblemPreventation,articles, TblChart,pro_degree,job_record, TblKeywords,edu_records, TblTeam, like, view,TblKnowledgeDocuments,FeedFile,TblKnowledgeSpecial,TblIsGroup,TblKnowledgeRequest,TblTeam2,FeedFileDocumentation,TblExam,TblQuestion,TblQuestionOptions,SendExam2member,MemberChart,topic1,topic2,topic3,ExpertChart,TblAnswerOption,TblAnswerKnowledgeRequest,TblVoteQuestion,TblVoteQuestionAnswer,TblFollowerFollowedIndicator,TblFollowed,TblMessageUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = Members
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'اطلاعات کاربری',
            {
                'fields':(
                    'nationalCode','mobileNumber','personal_number','identity_number','birthday_age','degree','organization_email','profile_picture','Status',
                )
            }
        )
      
    )

class TblKnowledgePermissionConfig(admin.ModelAdmin):
    """دسترسی"""
    ordering = ('KnowledgePermissionText',)
    list_display = ('KnowledgePermissionText', 'Status')
    list_filter = ('KnowledgePermissionText', 'Status')
    search_fields = ('KnowledgePermissionText',)


class TblKnowledgeEvaluationConfig(admin.ModelAdmin):
    """ارزیابی"""
    ordering = ('KnowledgeEvaluationText',)
    list_display = ('KnowledgeEvaluationText', 'Status')
    list_filter = ('KnowledgeEvaluationText', 'Status')
    search_fields = ('KnowledgeEvaluationText',)


class TblKnowledgeResourceConfig(admin.ModelAdmin):
    """با چه منابعی"""
    ordering = ('KnowledgeResourceText',)
    list_display = ('KnowledgeResourceText', 'Status')
    list_filter = ('KnowledgeResourceText', 'Status')
    search_fields = ('KnowledgeResourceText',)


class TblKnowledgeConditionsConfig(admin.ModelAdmin):
    """تحت چه شرایطی"""
    ordering = ('KnowledgeConditionsText',)
    list_display = ('KnowledgeConditionsText', 'Status')
    list_filter = ('KnowledgeConditionsText', 'Status')
    search_fields = ('KnowledgeConditionsText',)


class TblUsedDomainConfig(admin.ModelAdmin):
    """دامنه کاربرد"""
    ordering = ('UsedDomainText',)
    list_display = ('UsedDomainText', 'Status')
    list_filter = ('UsedDomainText', 'Status')
    search_fields = ('UsedDomainText',)


class TblKnowledgeCategoryConfig(admin.ModelAdmin):
    """دسته بندی دانش"""
    ordering = ('KnowledgeCategoryText',)
    list_display = ('KnowledgeCategoryText', 'Status')
    list_filter = ('KnowledgeCategoryText', 'Status')
    search_fields = ('KnowledgeCategoryText',)


class TblKnowledgeRisksConfig(admin.ModelAdmin):
    """ریسک ها"""
    ordering = ('KnowledgeRisksText',)
    list_display = ('KnowledgeRisksText', 'Status')
    list_filter = ('KnowledgeRisksText', 'Status')
    search_fields = ('KnowledgeRisksText',)


class TblKnowledgeCauseConfig(admin.ModelAdmin):
    """علت"""
    ordering = ('KnowledgeCauseText',)
    list_display = ('KnowledgeCauseText', 'Status')
    list_filter = ('KnowledgeCauseText', 'Status')
    search_fields = ('KnowledgeCauseText',)


class TblKnowledgeTitleConfig(admin.ModelAdmin):
    """عنوان دانش"""
    ordering = ('KnowledgeTitleText',)
    list_display = ('KnowledgeTitleText', 'Status')
    list_filter = ('KnowledgeTitleText', 'Status')
    search_fields = ('KnowledgeTitleText',)


class TblKnowledgeUsedCasesConfig(admin.ModelAdmin):
    """موارد استفاده"""
    ordering = ('KnowledgeUsedCasesText',)
    list_display = ('KnowledgeUsedCasesText', 'Status')
    list_filter = ('KnowledgeUsedCasesText', 'Status')
    search_fields = ('KnowledgeUsedCasesText',)



class TblKnowledgeResultsConfig(admin.ModelAdmin):
    """نتایج"""
    ordering = ('KnowledgeResultsText',)
    list_display = ('KnowledgeResultsText', 'Status')
    list_filter = ('KnowledgeResultsText', 'Status')
    search_fields = ('KnowledgeResultsText',)


class TblKnowledgeWhichActionConfig(admin.ModelAdmin):
    """چه کاری"""
    ordering = ('KnowledgeDoText',)
    list_display = ('KnowledgeDoText', 'Status')
    list_filter = ('KnowledgeDoText', 'Status')
    search_fields = ('KnowledgeDoText',)


class TblKnowledgeHowConfig(admin.ModelAdmin):
    """چگونه"""
    ordering = ('KnowledgeHowText',)
    list_display = ('KnowledgeHowText', 'Status')
    list_filter = ('KnowledgeHowText', 'Status')
    search_fields = ('KnowledgeHowText',)


class TblKnowledgeProblemPreventationConfig(admin.ModelAdmin):
    """چگونه می توان از بروز تجربه مشکل جلوگیری کرد"""
    ordering = ('KnowledgeProblemPreventationText',)
    list_display = ('KnowledgeProblemPreventationText', 'Status')
    list_filter = ('KnowledgeProblemPreventationText', 'Status')
    search_fields = ('KnowledgeProblemPreventationText',)


admin.site.register(TblKnowledgePermission, TblKnowledgePermissionConfig)
admin.site.register(TblKnowledgeEvaluation, TblKnowledgeEvaluationConfig)
admin.site.register(TblKnowledgeResource, TblKnowledgeResourceConfig)
admin.site.register(TblKnowledgeConditions, TblKnowledgeConditionsConfig)
admin.site.register(TblUsedDomain, TblUsedDomainConfig)
admin.site.register(TblKnowledgeCategory, TblKnowledgeCategoryConfig)
admin.site.register(TblKnowledgeRisks, TblKnowledgeRisksConfig)
admin.site.register(TblKnowledgeCause, TblKnowledgeCauseConfig)
admin.site.register(TblKnowledgeTitle, TblKnowledgeTitleConfig)
admin.site.register(TblKnowledgeUsedCases, TblKnowledgeUsedCasesConfig)
admin.site.register(TblKnowledgeResults, TblKnowledgeResultsConfig)
admin.site.register(TblKnowledgeWhichAction, TblKnowledgeWhichActionConfig)
admin.site.register(TblKnowledgeHow, TblKnowledgeHowConfig)
admin.site.register(TblKnowledge)
admin.site.register(TblKnowledgeProblemPreventation,
                    TblKnowledgeProblemPreventationConfig)
admin.site.register(TblChart)
admin.site.register(TblTeam)
admin.site.register(TblKeywords)
admin.site.register(like)
admin.site.register(view)
admin.site.register(Members,CustomUserAdmin)
admin.site.register(TblKnowledgeDocuments)
admin.site.register(FeedFile)
admin.site.register(TblKnowledgeSpecial)
admin.site.register(TblIsGroup)
admin.site.register(TblKnowledgeRequest)
admin.site.register(TblTeam2)
admin.site.register(pro_degree)
admin.site.register(edu_records)
admin.site.register(job_record)
admin.site.register(skills)
admin.site.register(articles)
admin.site.register(books)
admin.site.register(inventions)
admin.site.register(passed_trials)
admin.site.register(Documentation)
admin.site.register(FeedFileDocumentation)
admin.site.register(TblJalase)
admin.site.register(FeedFile_Jalase)
admin.site.register(TblTeam_Jalase)
admin.site.register(recive_invitation)
admin.site.register(rejected_knowledge)
admin.site.register(TblExam)
admin.site.register(TblQuestion)
admin.site.register(TblQuestionOptions)
admin.site.register(SendExam2member)
admin.site.register(MemberChart)
admin.site.register(topic1)
admin.site.register(topic2)
admin.site.register(topic3)
admin.site.register(ExpertChart)
admin.site.register(send_to_evaluator)
admin.site.register(Informs_meeting)
admin.site.register(TblAnswerOption)
admin.site.register(indicator_assessment_model)
admin.site.register(TblExpertReviewIndicatorAssessment)
admin.site.register(TblExpertReview)
admin.site.register(TblAnswerKnowledgeRequest)
admin.site.register(TblQuestionRequest)
admin.site.register(TblVoteQuestion)
admin.site.register(TblAnswerQuestionRequest)
admin.site.register(TblVoteSendQuestion)
admin.site.register(TblVoteQuestionAnswer)
admin.site.register(TblChartAdvanceInfo)
admin.site.register(TblChartDocument)
admin.site.register(TblSuervey)
admin.site.register(TblSuerveyOptions)
admin.site.register(TblAnswerOptionSurvey)
admin.site.register(SendSurvey2Member)
admin.site.register(TblDependentChart)
admin.site.register(TblFollowed)
admin.site.register(TblFollowerFollowedIndicator)
admin.site.register(TblMessageUser)
admin.site.register(TblInform)
admin.site.register(TblUsedKnowledge)
admin.site.register(TblScoreFormula)
admin.site.register(TblVoiceRecord)
admin.site.register(TblExamNotification)
admin.site.register(TblSurveyotification)
admin.site.register(TblKnowledgeNotificationForEliteUsers)
admin.site.register(TblTeamDocumentation)
admin.site.register(TblKeyIndicator)
admin.site.register(TblKpiExpertReview)
admin.site.register(TblKnowledgeValueIT)
admin.site.register(TblUserRewards)