from django.contrib import admin

from feedback_suggestions_app.models import TblSuggestion , TblIndicatorAssesment,TblSuggestionTeam,TblRejectSuggestionByIt,TblSendSuggestionItToCommittee ,TblExpertReviewIndicatorAssessment , TblExpertReview_suggestion , Tblcommitte_comment_result , TblWorkingGroupReview_suggestion


admin.site.register(TblSuggestion)
admin.site.register(TblIndicatorAssesment)
admin.site.register(TblSuggestionTeam)
admin.site.register(TblRejectSuggestionByIt)
admin.site.register(TblSendSuggestionItToCommittee)
admin.site.register(TblExpertReviewIndicatorAssessment)
admin.site.register(TblExpertReview_suggestion)
admin.site.register(Tblcommitte_comment_result)
admin.site.register(TblWorkingGroupReview_suggestion)
# Register your models here.
