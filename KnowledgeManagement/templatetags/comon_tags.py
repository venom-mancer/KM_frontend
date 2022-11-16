from django import template
from KnowledgeManagement.models import TblAnswerOptionSurvey,TblUsedQuestionRequest,Members,TblFollowerFollowedIndicator,TblFollowed, TblExam,TblUsedQuestionKnowledge,TblUsedKnowledge, TblKnowledge, TblSuervey, TblSuerveyOptions, TblVoteQuestion,TblVoteSendQuestion,TblVoteQuestionAnswer,TblUsedKnowledge,TblVotesForQuestionAnswer
from APAUtility.LibAPADateTime import get_persian_date_normalized
from django.db.models import Q
from KnowledgeManagement.views import score_calculator

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 


@register.filter
def in_question_options(option, question):
    return option.filter(question_id=question)


today_date=get_persian_date_normalized()

@register.filter
def taken_exams_by_user(user_id,tblsend_exam2_member):
    this_user_send_exams = tblsend_exam2_member.values_list('exam_id', flat=True).filter(member_id=user_id)
    this_user_exams = TblExam.objects.filter(id__in=this_user_send_exams,to_date__lt=today_date)

    return len(this_user_exams)

@register.filter
def topic_children(topic_id, topic_child_objects):
    return topic_child_objects.filter(mozo1=topic_id)

@register.filter
def topic_children_counter(topic_id, topic_child_objects):
    return len(topic_child_objects.filter(mozo1=topic_id))

@register.filter
def topic_children2(topic_id, topic_child_objects):
    return topic_child_objects.filter(mozo2=topic_id)

@register.filter
def topic_children_counter2(topic_id, topic_child_objects):
    return len(topic_child_objects.filter(mozo2=topic_id))

@register.filter
def knowledge_counter(user_id):
    return len(TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID=user_id).filter(Status = 1))


@register.filter
def vote_knowledge_request_counter(post_id):
    Tbl_vote = TblVoteQuestion.objects.all()

    up_vote = len(Tbl_vote.filter(knowledge_request=post_id,vote_status=1))
    down_vote= len(Tbl_vote.filter(knowledge_request=post_id,vote_status=2))
    result = up_vote-down_vote
    return result

@register.filter
def up_vote_knowledge_request_color(post_id,user_id):
    Tbl_vote = TblVoteQuestion.objects.all()

    if Tbl_vote.filter(knowledge_request=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 1:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''

    return result

@register.filter
def down_vote_knowledge_request_color(post_id,user_id):
    Tbl_vote = TblVoteQuestion.objects.all()

    if Tbl_vote.filter(knowledge_request=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 2:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''

    return result

@register.filter
def vote_question_request_counter(post_id):
    Tbl_vote = TblVoteSendQuestion.objects.all()

    up_vote = len(Tbl_vote.filter(knowledge_request=post_id,vote_status=1))
    down_vote= len(Tbl_vote.filter(knowledge_request=post_id,vote_status=2))
    result = up_vote-down_vote
    return result

@register.filter
def up_vote_question_request_color(post_id,user_id):
    Tbl_vote = TblVoteSendQuestion.objects.all()

    if Tbl_vote.filter(knowledge_request=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 1:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''
  
    return result

@register.filter
def down_vote_question_request_color(post_id,user_id):
    Tbl_vote = TblVoteSendQuestion.objects.all()

    if Tbl_vote.filter(knowledge_request=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 2:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''

    return result

@register.filter
def vote_answer_knowledge_request_counter(post_id):
    Tbl_vote = TblVoteQuestionAnswer.objects.all()

    up_vote = len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=1))
    down_vote= len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=2))
    result = up_vote-down_vote
    return result


@register.filter
def up_vote_answer_knowledge_request_color(post_id,user_id):
    Tbl_vote = TblVoteQuestionAnswer.objects.all()

    if Tbl_vote.filter(knowledge_request_answer=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request_answer=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 1:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''

    return result

@register.filter
def down_vote_answer_knowledge_request_color(post_id,user_id):
    Tbl_vote = TblVoteQuestionAnswer.objects.all()

    if Tbl_vote.filter(knowledge_request_answer=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request_answer=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 2:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''
        
    return result

@register.filter
def vote_answer_question_request_counter(post_id):
    Tbl_vote = TblVotesForQuestionAnswer.objects.all()

    up_vote = len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=1))
    down_vote= len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=2))
    result = up_vote-down_vote
    return result


@register.filter
def up_vote_answer_question_request_color(post_id,user_id):
    Tbl_vote = TblVotesForQuestionAnswer.objects.all()

    if Tbl_vote.filter(knowledge_request_answer=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request_answer=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 1:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''

    return result

@register.filter
def down_vote_answer_question_request_color(post_id,user_id):
    Tbl_vote = TblVotesForQuestionAnswer.objects.all()

    if Tbl_vote.filter(knowledge_request_answer=post_id,creater_user_id=user_id).exists():
        this_user_vote = Tbl_vote.get(knowledge_request_answer=post_id,creater_user_id=user_id)

        if this_user_vote.vote_status == 2:
            result ='color: orange;'
        else:
            result=''
    else:
        result=''
        
    return result

@register.filter
def used_knowledge_counter(post_id):

    return len(TblUsedKnowledge.objects.filter(knowledge=post_id))

@register.filter
def used_knowledge_color(post_id,user_id):
    Tbl_vote = TblUsedKnowledge.objects.all()

    if Tbl_vote.filter(knowledge=post_id,creater_user_id=user_id).exists():
        this_user_used = Tbl_vote.get(knowledge=post_id,creater_user_id=user_id)
        result ='color: green;'
    else:
        result=''
        
    return result



@register.filter
def percentage_servey_answer(id,type):
    this_option=TblSuerveyOptions.objects.get(id=id)

    this_user_survey = TblSuervey.objects.get(id=this_option.survey_id.id)

    this_survey_options = TblSuerveyOptions.objects.filter(survey_id=this_user_survey)

    answers = TblAnswerOptionSurvey.objects.filter(suervey = this_user_survey)

    count_members=[]

    for this_survey_option in this_survey_options:
        count_members.append(len(answers.filter(option_id=this_survey_option)))

    percentage = []

    # if anyone participate in the survey it calculates the percenteges
    # otherwise it returns zeros for all options
    if answers.count() > 0 :
        for count_member in count_members:
            percentage.append(float("{:.2f}".format((count_member/sum(count_members))*100)))
    else:
        for this_survey_option in this_survey_options:
            percentage.append(0)

    if type == 1 :
        return percentage[this_option.option_number-1]
    else:
        return count_members[this_option.option_number-1]

#this is for Question Knowledge Used times
@register.filter
def used_Question_knowledge_counter(post_id):

    return len(TblUsedQuestionKnowledge.objects.filter(Questionknowledge=post_id))

@register.filter
def used_Question_knowledge_color(post_id,user_id):
    Tbl_vote = TblUsedQuestionKnowledge.objects.all()

    if Tbl_vote.filter(Questionknowledge=post_id,creater_user_id=user_id).exists():
        this_user_used = Tbl_vote.get(Questionknowledge=post_id,creater_user_id=user_id)
        result ='color: green;'
    else:
        result=''
        
    return result

#this is for Question request Used times
@register.filter
def used_Question_request_counter(post_id):

    return len(TblUsedQuestionRequest.objects.filter(QuestionkRequest=post_id))

@register.filter
def used_Question_request_color(post_id,user_id):
    Tbl_vote = TblUsedQuestionRequest.objects.all()

    if Tbl_vote.filter(QuestionkRequest=post_id,creater_user_id=user_id).exists():
        this_user_used = Tbl_vote.get(QuestionkRequest=post_id,creater_user_id=user_id)
        result ='color: green;'
    else:
        result=''
        
    return result

@register.filter
def calculator(user):
    return score_calculator(user)


@register.filter
def user_activity_tag_used_knowledge(user):
    used_knowledge = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID=user)
    used = TblUsedKnowledge.objects.filter(knowledge__in=used_knowledge)
    return len(used)


@register.filter
def user_activity_tag_knowledge(user):
    used_knowledge = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID=user)
    return len(used_knowledge)


@register.filter
def user_activity_tag_followers(user):

    followings = TblFollowerFollowedIndicator.objects.filter(follower=user).values_list('followed', flat=True)
        
    all_users = Members.objects.filter(member__in=TblFollowed.objects.filter(id__in=followings).values_list('who_is_followed', flat=True))

    return len(all_users)