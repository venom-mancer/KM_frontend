from django.urls import path
from feedback_suggestions_app import views

urlpatterns = [
    path("", views.home, name="home_feedback"),
    #submit
    path("submit_suggestion/", views.submit_suggestion, name="submit_suggestion"),

    #list
    path("send_user_suggestion_it/<int:id>", views.send_user_suggestion_it, name="send_user_suggestion_it"),
    path("suggestion_list/", views.suggestion_list, name="suggestion_list"),
    path("suggestion_paperwork/", views.suggestion_paperwork, name="suggestion_paperwork"),
    path("edit_submit_suggestion/<int:id>", views.edit_submit_suggestion, name="edit_submit_suggestion"),
    path("delete_submit_suggestion/<int:id>", views.delete_submit_suggestion, name="delete_submit_suggestion"),
    path("suggestion_paperwork/<int:id>", views.suggestion_paperwork, name="suggestion_paperwork"),
    path("reject_suggestion_reason/<int:id>", views.reject_suggestion_reason, name="reject_suggestion_reason"),

    #mailroom
    path("public_section_list/", views.public_section_list, name="public_section_list"),
    path("accepted_public_section/<int:id>", views.accepted_public_section, name="accepted_public_section"),
    path("rejected_public_section/<int:id>", views.rejected_public_section, name="rejected_public_section"),
    path("accepted_proficiency_section/", views.accepted_proficiency_section, name="accepted_proficiency_section"),
    path("rejected_proficiency_section/", views.rejected_proficiency_section, name="rejected_proficiency_section"),
    path("committee_comment_for_mailroom/<int:id>", views.committee_comment_for_mailroom, name="committee_comment_for_mailroom"),
    path("working_group_comment_for_mailroom/<int:id>", views.working_group_comment_for_mailroom, name="working_group_comment_for_mailroom"),

    path("working_group_specialty/", views.working_group_specialty, name="working_group_specialty"),

    
    #کمیته
    path("suggestion_list_committee/", views.suggestion_list_committee, name="suggestion_list_committee"),
    path("indicator_assessment/", views.indicator_assessment, name="indicator_assessment"),
    path("indicator_assessment_list/", views.indicator_assessment_list, name="indicator_assessment_list"),
    path("delete_indicator_assessment/<int:id>", views.delete_indicator_assessment, name="delete_indicator_assessment"),
    path("committee_comment/<int:id>", views.committee_comment, name="committee_comment"),
    path("edit_indicator_assessment/<int:id>", views.edit_indicator_assessment, name="edit_indicator_assessment"),
    path("mailroom_accepted_suggestion_comment/<int:id>", views.mailroom_accepted_suggestion_comment, name="mailroom_accepted_suggestion_comment"),
    path("committe_specialty/", views.committe_specialty, name="committe_specialty"),
    path("committee_comment_resultpoint/<int:id>", views.committee_comment_resultpoint, name="committee_comment_resultpoint"),
    
    #work in group
    path("work_ingroup_suggesstion_list/", views.work_ingroup_suggesstion_list, name="work_ingroup_suggesstion_list"),
    path("work_ingroup_indicator_assessment/", views.work_ingroup_indicator_assessment, name="work_ingroup_indicator_assessment"),
    path("work_ingroup_indicator_assessment_list/", views.work_ingroup_indicator_assessment_list, name="work_ingroup_indicator_assessment_list"),
    path("edit_indicator_assessment_work_ingroup/<int:id>", views.edit_indicator_assessment_work_ingroup, name="edit_indicator_assessment_work_ingroup"),
    path("delete_indicator_assessment_work_ingroup/<int:id>", views.delete_indicator_assessment_work_ingroup, name="delete_indicator_assessment_work_ingroup"),
    path("work_ingroup_comment/<int:id>", views.work_ingroup_comment, name="work_ingroup_comment"),
    path("work_ingroup_comment_resultpoint/<int:id>", views.work_ingroup_comment_resultpoint, name="work_ingroup_comment_resultpoint"),

]