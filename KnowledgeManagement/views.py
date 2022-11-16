from ast import Not
from asyncio.windows_events import NULL
from atexit import register
from calendar import month
from dataclasses import replace
from genericpath import exists
from itertools import count
import json
from posixpath import split
from APAUtility.text_mining import spaces_between_words_dict
import re
from multiprocessing import context
from re import S
from itertools import chain
from tkinter.messagebox import NO
from turtle import down
from typing import Generic
from unittest import result
from django.db.models import Avg , Max
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from APAUtility.LibAPADateTime import get_persian_date_normalized , get_persian_year_normalized
from KnowledgeManagement.forms import TblKnowledgeDocumentsForm,TblInform_FORM,TblAnswerQuestionRequestForm,TblExpertReviewForm,DocumentationForm,indicator_assessmentForm,passed_trialsForm,inventionsForm,booksForm,articlesForm,skillsForm,pro_degreeForm,edu_recordsForm,job_recordForm, TblKnowledgeForm, SearchForm,CustomUserCreationForm,UpdateProfileForm,TblKnowledgeRequestForm,TblExamForm,TblQuestionForm,TblAnswerKnowledgeRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.urls import resolve, reverse
import jdatetime
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Count , Q , F
from KnowledgeManagement.notifications import km_notifications
from .forms import PasswordChangingForm,FileModelForm,Informs_meetingForm, TblKnowledgeValueITForm,TblUserRewardsForm, indicator_KeyForm,TblChartAdvanceInfoForm, TblKnowledgeErteghaForm,TblQuestionRequestForm, TblJalaseForm, TblSurveyForm,send_to_evaluatorForm,FeedFile_JalaseForm,send_invite,rejectForm
from django.http.response import JsonResponse
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from django.contrib.auth.models import Group
import os
from django.contrib import messages
import datetime
from .search_functions import knowledge_advance_search
from KnowledgeManagement.models import Members, SendSurvey2Member, TblAnswerKnowledgeRequest, TblAnswerOptionSurvey,TblAnswerQuestionRequest, TblChartAdvanceInfo, TblChartDocument, TblExpertReview, TblFollowed, TblFollowerFollowedIndicator, TblJalase, TblKnowledgeRequestNotification, TblKnowledgeStatusNotification, TblKnowledgeValueIT, TblKpiExpertReview,TblMessageUser, TblMessageUserNotification, TblQuestionRequestNotification, TblScoreFormula, TblSuervey, TblSuerveyOptions, TblTeamDocumentation, TblUserRewards, TblVoteQuestionAnswer,books,passed_trials,Documentation, TblChart, TblKeywords, TblKnowledgeCategory, TblKnowledgeConditions, \
    TblKnowledgeDocuments, \
    TblKnowledgeHow, \
    TblKnowledgeOpportunities,TblVoteQuestion,TblUsedQuestionKnowledge,TblUsedQuestionRequest, TblKnowledgeProblemPreventation,TblChartAdvanceInfo,TblQuestionRequest,Informs_meeting,indicator_assessment_model, TblKnowledgeResource, TblKnowledgeResults, \
    TblKnowledgeRisks, TblKnowledgeTitle,FeedFile_Jalase,TblTeam_Jalase, TblKnowledge, TblKnowledgeCause, TblKnowledgeUsedCases, \
    TblKnowledgeWhichAction, TblKnowledgeEvaluation, rejected_knowledge,skills,inventions,TblKnowledgeSpecial, TblTeam, \
    articles, TblTeam2,edu_records,job_record, TblUsedDomain,pro_degree, like, view,FeedFile,TblKnowledgeRequest,TblUserRewards,\
    FeedFileDocumentation,TblExamNotification,TblExam,TblKnowledgeNotificationForEliteUsers,TblKeyIndicator,TblKpiExpertReview,TblQuestion,TblSurveyotification,TblChartDocument,TblQuestionOptions,TblVotesForQuestionAnswer,TblVoiceRecord,TblInform,send_to_evaluator,SendExam2member,TblDependentChart,TblUsedKnowledge,MemberChart,topic1,topic2,topic3,ExpertChart,TblAnswerOption,TblExpertReviewIndicatorAssessment,TblVoteSendQuestion


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



def is_knowlege_worker(user):
    return user.groups.filter(name='KnowlegeWorker').exists()


def is_expert(user):
    return user.groups.filter(name='Expert').exists()


def is_IT(user):
    return user.groups.filter(name='IT').exists()

def is_Security(user):
    return user.groups.filter(name='Security').exists()

def set_contex(user):
    if user.first_name =="" or user.last_name =="":
        user_name = user.username
    else:
        user_name = user.first_name + ' ' + user.last_name

    contex = {
        'UserName': user_name,
        'NotificationsCount': 0,
        'UsersImg': 'assets/images/user.png',
    }
    return contex


def create_chart_tree(parent_num):
    if parent_num is None:
        chart = TblChart.objects.filter(Parent__isnull=True).filter(Status=1)
    else:
        chart = TblChart.objects.filter(Parent=parent_num).filter(Status=1)
    tree = ""
    for item in chart:
        sub_chart = TblChart.objects.filter(
            Parent=item.Chart).filter(Status=1).count()
        style = "color: #337ab7;"
        if item.ChartType == 2:
            style = "color: #ffc107"
        if item.ChartType == 3:
            style = "color: #3c763d;"

        if sub_chart == 0:
            tree += '<li><a href="#" style="' + style + '" onclick="setChartId(' + str(
                item.Chart) + ',\'' + item.ChartText + '\',\'' + str(item.ChartType) + '\');">' + \
                    item.ChartText + '</a></li>'
        else:
            tree += '<li><a href="#" style="' + style + '" onclick="setChartId(' + str(
                item.Chart) + ',\'' + item.ChartText + '\',\'' + str(
                item.ChartType) + '\');">' + item.ChartText + '</a>'
            tree += '<ul>' + \
                    create_chart_tree(item.Chart) + '</ul></li>'
    return tree


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


def login_view(request):
    next_url = request.GET.get('next')
    if request.user.is_authenticated and is_knowlege_worker(request.user):
        return HttpResponseRedirect(reverse('loginRoute'))
    today_date = get_persian_date_normalized()
    get_information = TblInform.objects.filter(Status = 1 ,to_date__gte = today_date)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Successful login
            login(request, user)
            user.Status=1
            user.save()
            redirect_url = next_url if next_url else reverse('loginRoute')
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request,'نام کاربری یا گزرواژه اشتباه است ')
            return redirect('login')
            
    else:
        context = {
            'get_information' : get_information,
        }
    return render(request, 'login_form.html', context)


def enter_as_others(request):
    if is_IT(request.user):
        if request.method == 'POST':
            username_id = request.POST.get('members')
            user = Members.objects.get(member=username_id)
            if user is not None:
                # Successful login
                login(request, user)
                user.Status=2
                user.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                context = {
                    'username': username_id,
                    'error': 'کاربری با این مشخصات یافت نشد'
                }
        else:
            All_users = Members.objects.all().exclude(member=request.user.member)
            context = {
                'members':All_users,
                }
        return render(request, 'joinAsothers.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginRoute'))

def knowledge_process_counter(process_list):
    count=0
    for i in process_list:
        count=count+len(TblKnowledge.objects.filter(KnowledgeProcess=i))

    return count


def linegraph_month_counter(type):
    
    this_year = int(jdatetime.datetime.now().strftime("%Y"))
    data_month = []

    if type == 1:
        knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(Status=1)
    else:
        knowledges = TblKnowledge.objects.exclude(Q(register_status=7) | Q(register_status=9)).filter(Status=1)

    list_start_month=['0101','0201','0301','0401','0501','0601','0701','0801','0901','1001','1101','1201']
    list_end_month=  ['0132','0232','0332','0432','0532','0632','0732','0832','0932','1032','1132','1232']

    for i in range(12):
        current_month=len(knowledges.filter(CreateDate__gte = '{}{}'.format(this_year,list_start_month[i]),CreateDate__lte='{}{}'.format(this_year,list_end_month[i])))
        data_month.append(current_month)

    return data_month

def login_route(request):
    today_date = get_persian_date_normalized()
    get_information = TblInform.objects.filter(Status = 1 ,to_date__gte = today_date)
    context = {
        'get_information' : get_information,
    }

    return render(request, "login_routes.html",context)


@login_required
def home(request):
    if not is_knowlege_worker(request.user) and not is_expert(request.user) and not is_IT(request.user):
        return HttpResponseRedirect('/login')

    # if there is no instance of TblFollowed we first make it
    if not TblFollowed.objects.filter(who_is_followed=request.user).exists():
        obj_followed = TblFollowed()
        obj_followed.who_is_followed = request.user
        obj_followed.save()

    followings = len(TblFollowerFollowedIndicator.objects.filter(follower=request.user))
    followers = len(TblFollowerFollowedIndicator.objects.filter(followed=TblFollowed.objects.get(who_is_followed = request.user)))

    #UNchecking knowledge
    unchecked_knowledges = len(TblKnowledge.objects.exclude(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID = request.user).filter(Status=1))

    #used knowledge
    my_knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID=request.user.member)
    used = len(TblUsedKnowledge.objects.filter(knowledge__in=my_knowledges))

    view_count = len(view.objects.filter(post__in = TblKnowledge.objects.values_list('KnowledgeCode', flat=True).filter(CreatorUserID=request.user)))
    total_knowledge = len(TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(Status=1))
    my_knowledge = len(TblKnowledge.objects.filter(CreatorUserID=request.user).filter(Q(register_status=7) | Q(register_status=9)).filter(Status=1))
    knowldge_in_check_process = len(TblKnowledge.objects.exclude(Q(register_status=7) | Q(register_status=9)).filter(Status=1))
    notif_len = 0
    notif_status = 2

    #likes count
    my_questions = TblKnowledgeRequest.objects.filter(CreatorUserID=request.user)
    total_user_likes = TblVoteQuestion.objects.filter(knowledge_request__in=my_questions)
    up_votes = len(total_user_likes.filter(vote_status = 1))


    knowledges = TblKnowledge.objects.filter(Status__gte=0).filter(Q(register_status=7) | Q(register_status=9))
    knowledges_len=len(knowledges)
    if knowledges_len >= 5:
        knowledges=knowledges[knowledges_len-5:]
    
    notif_button = 2

    #counts the meeting notifications and notification messages
    today_date = get_persian_date_normalized()
    notification = Informs_meeting.objects.all()
    notifs = Informs_meeting.objects.filter(meeting_reciver=request.user,notif_status = 1)
    if notifs:
        notif_len = len(notifs)
        notif_status = 1
    elif Informs_meeting.objects.filter(meeting_reciver=request.user,notif_status = 2):
        notif_len = 0
        notif_status = 2

    if Informs_meeting.objects.filter(meeting_start_date__lte=today_date):
        Informs_meeting.objects.filter(meeting_start_date__lte=today_date).delete()

    show_button = 1
#pie chart
    labels=[]
    data=[]

    for i in TblChart.objects.filter(Parent_id=1,ChartType=1,Status=1):
        children=TblChart.objects.filter(location__startswith=i.location,ChartType=3,Status=1)
        count_children=knowledge_process_counter(children)
        data.append(count_children)
        labels.append(i.ChartText)
#pie chart


#submitted_line graph
    data_month = linegraph_month_counter(1)
#submitted_line graph

#UN-SUBMITTED_line graph
    unsubmitted_data_month = linegraph_month_counter(2)
#UN-SUBMITTED_line graph

    #score calculator
    score = score_calculator(request.user)
    # topics
    get_topic1 = topic1.objects.filter(status=1)

    conetxt = dict(set_contex(request.user))
    conetxt.update({
    'data':data,
    'unchecked_knowledges' : unchecked_knowledges,
    'notif_button' : notif_button,
    'notification' : notification,
    'notif_len' : notif_len,
    'notifs' : notifs,
    'used' : used,
    'up_votes' : up_votes,
    'show_button' : 1,
    'notif_status' : notif_status,
    'labels':labels,
    'unsubmitted_data_month' : unsubmitted_data_month,
    'items':total_knowledge,
    'get_topic1' : get_topic1,
    'data_month' : data_month,
    'my_knowledge' : my_knowledge,
    'knowldge_in_check_process' : knowldge_in_check_process,
    'Knowledges': knowledges,
    'view_count': view_count,
    'followers':followers,
    'followings':followings,
    'score':score,   
    'Title': 'داشبورد', })
    return render(
        request,
        'Home.html',
        conetxt
    )



@login_required
def RegintserExperience(request, type):
    
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    conetxt = dict(set_contex(request.user))
    html_chart = create_chart_tree(None)

    status_determiner=request.POST.get('registerDeterminer')

    memebers = Members.objects.all()
    if type == 3:
        skill_experience = 'دانش تطبیقی : دانش کسب شده از بازدید ها و نمایشگاه ها و دوره های اموزشی'
        Title = 'ثبت تجربه ی تطبیقی'
    elif type == 4:
        Title = 'ثبت تجربه ی مهارت'
        skill_experience = 'دانش ناشی از داشتن فن و مهارت و حرفه ی خاص نسبت به سایر همکاران'
    elif type == 5:
        skill_experience = 'دانش که منجر به ترفیع شغلی شده است'
        Title = '(خبره و عالی) ثبت تجربه ی ارتقای شغلی  '
    elif type == 1:
        skill_experience = 'تجربه ی شامل دانش کسب شده از حوادث و رویداد ها و بهبود فرایند و تصمیمات است'
        Title = 'ثبت تجربه'


    file_form = FileModelForm()
    conetxt.update({
        'teamCount': 1,
        'Title': '{}'.format(Title),
        'skill_experience': '{}'.format(skill_experience),
        'html_chart': html_chart,
        'knowledgeType': type,
        'members': memebers,
        'FileModelForm':file_form,
        'voice' : 0 ,   
    
    })

    if request.method == "POST":
        doc_files_title = request.POST.getlist('docTitle')
        audio_name = request.POST.get('hidden_audio')
        audio = audio_name + ".mp3"
        doc_files=request.FILES.getlist('Allfiles')
        user_key_words = []

        if type == 5:
            form = TblKnowledgeErteghaForm(request.POST, request.FILES)
        else:
            form = TblKnowledgeForm(request.POST, request.FILES)

        
        if form.is_valid():
            obj = form.save()
            obj.voice_url = audio
            try:                       
                memebers_to_save = request.POST.getlist('member')
                join_percentage=request.POST.getlist('percentageJoin')
                if len(join_percentage) > 1:
                    if all(flag.isdigit() for  flag in join_percentage):
                        join_percentage=list(map(int, join_percentage))
                    else:
                        join_percentage=[0]
                if form.cleaned_data['KnowledgeProcess'] is None:
                    emptyChart_Error = 'حوزه ی دانشی نمیتواند خالی باشد'
                if form.cleaned_data['KnowledgeKeywords'] is not None:
                    keywords = form.data['KnowledgeKeywords']
                    keywords = keywords.strip()
                else:
                    keywords=''
                obj = form.save()
                if request.user.Status == 2:
                    obj.Status_who_registered=2
                    obj.save()

                if int(status_determiner) == 2:
                    obj.register_status=3
                    obj.save()
                if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                    for itemFile,itemTitle in zip(doc_files,doc_files_title):
                        obj_file_doc=FeedFile()
                        obj_file_doc.file=itemFile
                        obj_file_doc.title=itemTitle
                        obj_file_doc.feed=TblKnowledge.objects.get(KnowledgeCode=obj.KnowledgeCode)
                        obj_file_doc.save()

                if len(join_percentage) > 1:
                    if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                        for item,percentage in zip(memebers_to_save,join_percentage):
                            obj_Team = TblTeam()
                            obj_Team.joinPercentage=percentage
                            obj_Team.KnowledgeCode = obj
                            obj_Team.TeamMember = Members.objects.get(member=item)
                            obj_Team.save()
                    else:
                        conetxt.update({
                        'KnowledgeForm': form,
                        'errors': 'درصد چه کسی درست نیست',
                        'emptyChart_Error' : emptyChart_Error,
                        
                        })
                        return render(request, 'RegintserExperience.html', conetxt)

                if keywords !='':
                    splited_keywords = keywords.split(",")
                    for keyword in splited_keywords:
                        obj_keyword = TblKeywords()
                        obj_keyword.KeywordsText = keyword
                        obj_keyword.Knowledge = obj
                        obj_keyword.save()
                        user_key_words.append(obj_keyword)

                return HttpResponseRedirect('/KnowledgeList/1')
            except:
                conetxt.update({
                    'KnowledgeForm': form,
                    'errors': str(form.errors),
                })
                return render(request, 'RegintserExperience.html', conetxt)
        else:
            conetxt.update({
                'KnowledgeForm': form,
                'errors': str(form.errors),
            })
            return render(request, 'RegintserExperience.html', conetxt)
    else:
        if type == 5:
            knowledge_form = TblKnowledgeErteghaForm()
        else:
            knowledge_form = TblKnowledgeForm()

        conetxt.update({
            'KnowledgeForm': knowledge_form,
        })
        return render(request, 'RegintserExperience.html', conetxt)



@login_required
def  save_voice_knowledge(request):
    if request.method == 'POST':
        audio_file=request.FILES.get('audio_data')
        audio_file.name = audio_file.name + '.mp3'
        obj = TblVoiceRecord.objects.create(voice_url=audio_file.name, voice_record=audio_file)
        obj.save()


@login_required
def remove_voice(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        obj = TblKnowledge.objects.get(KnowledgeCode=id)
        voice_name = obj.voice_url 
        obj_voice = TblVoiceRecord.objects.get(voice_url=voice_name)
        obj.voice_url = ''
        obj.save()
        obj_voice.delete()



@login_required
def EditExperience(request, id):
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect(reverse('login'))

    #delete notif experience rejected by experts
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 9).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 9).delete()

    obj_knowledge = get_object_or_404(TblKnowledge, KnowledgeCode=id)
    
    knowledgeType = obj_knowledge.Type

    if TblKnowledge.objects.filter(KnowledgeCode=id).exists():
        obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
        obj_knowledge_status=obj_knowledge.register_status

        voice_name = obj_knowledge.voice_url
        if TblVoiceRecord.objects.filter(voice_url = voice_name).exists():
            voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        else:
            voice = 0
        if (obj_knowledge_status >=1 and obj_knowledge_status <=4) or obj_knowledge_status == 6 and obj_knowledge.CreatorUserID == request.user :
            status_determiner=request.POST.get('registerDeterminer')

            if obj_knowledge.KnowledgePermission.KnowledgePermission == 1:
                permission_knowledge=1
            else:
                permission_knowledge=2

            if obj_knowledge.KnowledgeIsSpecial.KnowledgeSpecial == 1:
                special_knowledge=1
            else:
                special_knowledge=2

            conetxt = dict(set_contex(request.user))

            len_team=len(TblTeam.objects.filter(KnowledgeCode=id))
            obj_files=FeedFile.objects.filter(feed=id)    

            if knowledgeType == 5:
                knowledge_form = TblKnowledgeErteghaForm(
                request.POST or None, instance=obj_knowledge)
            else:
                knowledge_form = TblKnowledgeForm(
                request.POST or None, instance=obj_knowledge)

            html_chart = create_chart_tree(None)
            if knowledge_form.is_valid() and request.method == "POST":


                audio_name = request.POST.get('hidden_audio')
                if audio_name != '':
                    if TblVoiceRecord.objects.filter(voice_url = voice_name).exists():
                        TblVoiceRecord.objects.filter(voice_url = voice_name).delete()
                    obj_knowledge.voice_url = audio_name + '.mp3'
                    obj_knowledge.save()
                
                if knowledge_form.cleaned_data['KnowledgeKeywords'] is not None:
                    keywords = knowledge_form.data['KnowledgeKeywords']
                    keywords = keywords.strip()
                else:
                    keywords=''

                obj = knowledge_form.save()
                obj.Status_who_registered = request.user.Status
                obj.save()
                if int(status_determiner) == 2:
                    obj.register_status=3
                    obj.save()

                
                doc_files_title = request.POST.getlist('docTitle')
                doc_files=request.FILES.getlist('Allfiles')
                if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                    for itemFile,itemTitle in zip(doc_files,doc_files_title):
                        obj_file_doc=FeedFile()
                        obj_file_doc.file=itemFile
                        obj_file_doc.title=itemTitle
                        obj_file_doc.feed=TblKnowledge.objects.get(KnowledgeCode=obj.KnowledgeCode)
                        obj_file_doc.save()


                memebers_to_save = request.POST.getlist('member')
                join_percentage=request.POST.getlist('percentageJoin')

                if len(join_percentage) > 1:
                    if all(flag.isdigit() for  flag in join_percentage):
                        join_percentage=list(map(int, join_percentage))
                    else:
                        join_percentage=[0]

                TblTeam.objects.filter(KnowledgeCode=obj_knowledge.KnowledgeCode).delete()

                if len(join_percentage) > 1:
                    if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                        for item,percentage in zip(memebers_to_save,join_percentage):
                            obj_Team = TblTeam()
                            obj_Team.joinPercentage=percentage
                            obj_Team.KnowledgeCode = obj
                            obj_Team.TeamMember = Members.objects.get(member=item)
                            obj_Team.save()
                    else:
                        memebers = Members.objects.all()
                        team = TblTeam.objects.filter(KnowledgeCode=obj_knowledge.KnowledgeCode).exclude(TeamMember=request.user.member)
                        if TblTeam.objects.filter(KnowledgeCode=obj_knowledge.KnowledgeCode,TeamMember=request.user.member).exists():
                            userPercentage = TblTeam.objects.get(KnowledgeCode=obj_knowledge.KnowledgeCode,TeamMember=request.user.member)
                            userPercentage=userPercentage.joinPercentage
                        else:
                            userPercentage=-1
                        conetxt.update({
                            'errors': 'درصد چه کسی درست نیست',
                            'team': team,
                            'voice' : voice ,
                            'userPercentage':userPercentage,
                            'members': memebers,
                            'teamCount': team.count(),
                            'KnowledgeForm': knowledge_form,
                            'KnowledgeProcess': obj_knowledge.KnowledgeProcess,
                            'UserId': request.user.member,
                            'html_chart': html_chart,
                            'knowledgeType': knowledgeType,
                            'obj_files':obj_files,
                            'len_team':len_team,
                            'permission_knowledge':permission_knowledge,
                            'special_knowledge':special_knowledge,
                            'id':id,
                            'edit':'edit',
                            'obj_knowledge':obj_knowledge,
                        }
                        )
                        return render(
                            request,
                            'RegintserExperience.html',
                            conetxt
                        )

                if keywords !='':
                    splited_keywords = keywords.split(",")
                    keywords_to_delete = TblKeywords.objects.filter(
                        Knowledge=obj_knowledge)
                    keywords_to_delete.delete()
                    for keyword in splited_keywords:
                        obj_keyword = TblKeywords()
                        obj_keyword.KeywordsText = keyword
                        obj_keyword.Knowledge = obj
                        obj_keyword.save()
                return HttpResponseRedirect('/KnowledgeList/1')
            
            memebers = Members.objects.all()
            team = TblTeam.objects.filter(KnowledgeCode=obj_knowledge.KnowledgeCode).exclude(TeamMember=request.user.member)
            if TblTeam.objects.filter(KnowledgeCode=obj_knowledge.KnowledgeCode,TeamMember=request.user.member).exists():
                userPercentage = TblTeam.objects.get(KnowledgeCode=obj_knowledge.KnowledgeCode,TeamMember=request.user.member)
                userPercentage=userPercentage.joinPercentage
            else:
                userPercentage=-1

            conetxt.update({
                'team': team,
                'userPercentage':userPercentage,
                'members': memebers,
                'teamCount': team.count(),
                'KnowledgeForm': knowledge_form,
                'KnowledgeProcess': obj_knowledge.KnowledgeProcess,
                'errors': str(knowledge_form.errors),
                'UserId': request.user.member,
                'html_chart': html_chart,
                'knowledgeType': knowledgeType,
                'obj_files':obj_files,
                'len_team':len_team,
                'permission_knowledge':permission_knowledge,
                'special_knowledge':special_knowledge,
                'edit':'edit',
                'id':id,
                'obj_knowledge':obj_knowledge,
                'voice' : voice ,

            }
            )
            return render(
                request,
                'RegintserExperience.html',
                conetxt
            )
    return HttpResponseRedirect('/KnowledgeList/1')
    

def Recycle_Knowledge(request,id):

    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect(reverse('login'))

    today_date = get_persian_date_normalized()

    
    if TblKnowledge.objects.filter(KnowledgeCode=id).exists():
        
        Clone_Knowledge_Obj = TblKnowledge.objects.get(KnowledgeCode=id)

        Clone_Knowledge_Obj.pk = None
        Clone_Knowledge_Obj.register_status = 2
        Clone_Knowledge_Obj.set_number = 1
        Clone_Knowledge_Obj.view_count = 0
        Clone_Knowledge_Obj.Status = 1
        Clone_Knowledge_Obj.CreateDate = today_date
        Clone_Knowledge_Obj.save()

        #creates the same files for the new recycled knowledge
        filefeed = FeedFile.objects.filter(feed__KnowledgeCode = id)
        for file in filefeed:
            file.pk = None
            file.feed = Clone_Knowledge_Obj
            file.save()
        
        #creates the same team members for the new recycled knowledge
        knowledge_team = TblTeam.objects.filter(KnowledgeCode__KnowledgeCode = id)
        for member in knowledge_team:
            member.pk = None
            member.KnowledgeCode = Clone_Knowledge_Obj
            member.save()

    return HttpResponseRedirect('/EditExperience/{}'.format(Clone_Knowledge_Obj.KnowledgeCode))


@login_required
def document_list(request):

    show_button = 1
    document = Documentation.objects.filter(Status__gte=0,CreatorUserID = request.user.member)
    context = {
        'show_button' : show_button,
        'document': document,
        'Title': 'گزارش مستندات',
    }
    return render(request, "document_list.html", context)
    

@login_required
def document_delete(request,id):

    document = Documentation.objects.get(id=id)
    document.Status=-1
    document.save()
    return HttpResponseRedirect('/document_list/')


def documentation_view(request):
    members = Members.objects.all()
    file = DocumentationForm(request.POST or None)
    html_chart = create_chart_tree(None)

    context = {
        'file' : file,
        'Title' : 'ثبت مستندات',
        'html_chart': html_chart,
        'mostanad' : 'مستندات مرتبط با تجربه',
        'members':members,
        'teamCount': 1,
        }

    if request.method == 'POST':
        doc_files_title = request.POST.getlist('docTitle')
        doc_files=request.FILES.getlist('Allfiles') 
        memebers_to_save = request.POST.getlist('member')
        join_percentage=request.POST.getlist('percentageJoin')
        if len(join_percentage) > 1:
            if all(flag.isdigit() for  flag in join_percentage):
                join_percentage=list(map(int, join_percentage))
            else:
                join_percentage=[0]
        if file.is_valid():
            obj=file.save()
            if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                for itemFile,itemTitle in zip(doc_files,doc_files_title):
                    obj_file_doc=FeedFileDocumentation()
                    obj_file_doc.file=itemFile
                    obj_file_doc.title=itemTitle
                    obj_file_doc.feed=Documentation.objects.get(id=obj.id)
                    obj_file_doc.save()

            if len(join_percentage) > 1:
                if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                    for item,percentage in zip(memebers_to_save,join_percentage):
                        obj_Team = TblTeamDocumentation()
                        obj_Team.joinPercentage=percentage
                        obj_Team.DocumentationCode = obj
                        obj_Team.TeamMember = Members.objects.get(member=item)
                        obj_Team.save()
                else:
                    context.update({
                    'file' : file,
                    'errors': 'درصد چه کسی درست نیست',
                    })
                    return render(request, 'send_document.html', context)
            return HttpResponseRedirect('/document_list/')
        else:
            return render(request, 'send_document.html',)

    return render(request,'send_document.html',context)


def documentation_edit_view(request,id):
    len_team=len(TblTeamDocumentation.objects.filter(DocumentationCode=id))
    members = Members.objects.all()
    obj_Documentation = get_object_or_404(Documentation, id=id)
    file = DocumentationForm(request.POST or None ,instance=obj_Documentation)
    obj_files=FeedFileDocumentation.objects.filter(feed=id) 
    html_chart = create_chart_tree(None)
    team = TblTeamDocumentation.objects.filter(DocumentationCode=obj_Documentation.id).exclude(TeamMember=request.user.member)

    if TblTeamDocumentation.objects.filter(DocumentationCode=obj_Documentation.id,TeamMember=request.user.member).exists():
        userPercentage = TblTeamDocumentation.objects.get(DocumentationCode=obj_Documentation.id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    context = {
        'file' : file,
        'Title' : 'ثبت مستندات',
        'html_chart': html_chart,
        'obj_files':obj_files,
        'members':members,
        'teamCount': 1,
        'len_team':len_team,
        'team':team,
        'userPercentage':userPercentage,
        }

    if request.method == "POST":
        memebers_to_save = request.POST.getlist('member')
        join_percentage=request.POST.getlist('percentageJoin')
        describe_documentation = request.POST.get('describe_documentation')

        if file.is_valid():
            obj=file.save()
            obj.describe_documentation = describe_documentation
            obj.save()
            doc_files_title = request.POST.getlist('docTitle')
            doc_files=request.FILES.getlist('Allfiles') 
            if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                for itemFile,itemTitle in zip(doc_files,doc_files_title):
                    obj_file_doc=FeedFileDocumentation()
                    obj_file_doc.file=itemFile
                    obj_file_doc.title=itemTitle
                    obj_file_doc.feed=Documentation.objects.get(id=obj.id)
                    obj_file_doc.save()

            if len(join_percentage) > 1:
                if all(flag.isdigit() for  flag in join_percentage):
                    join_percentage=list(map(int, join_percentage))
                else:
                    join_percentage=[0]

            TblTeamDocumentation.objects.filter(DocumentationCode=obj_Documentation.id).delete()

            if len(join_percentage) > 1:
                if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                    for item,percentage in zip(memebers_to_save,join_percentage):
                        obj_Team = TblTeamDocumentation()
                        obj_Team.joinPercentage=percentage
                        obj_Team.DocumentationCode = obj
                        obj_Team.TeamMember = Members.objects.get(member=item)
                        obj_Team.save()
                else:
                    context.update({
                    'file' : file,
                    'errors': 'درصد چه کسی درست نیست',
                    })
                    return render(request, 'send_document.html', context)


            return HttpResponseRedirect('/document_list/')
        else:
            return render(request, 'send_document.html',context)


    return render(request,'send_document.html',context)

@login_required
def Profile(request):
    obj_profile = get_object_or_404(Members, member=request.user.member)
    members_form = UpdateProfileForm(
        request.POST or None, request.FILES or None, instance=obj_profile)

    html_chart = create_chart_tree(None)

    degree_objects=pro_degree.objects.filter(pro_degree_key=request.user)
    edu_record_objects=edu_records.objects.filter(edu_records_key=request.user)
    job_record_objects=job_record.objects.filter(job_record_key=request.user)
    skills_objects=skills.objects.filter(skills_key=request.user)
    articles_objects=articles.objects.filter(article_key=request.user)
    books_objects=books.objects.filter(books_key=request.user)
    inventions_objects=inventions.objects.filter(inventions_key=request.user)
    passed_trials_objects=passed_trials.objects.filter(passed_trials_key=request.user)
    member_charts=MemberChart.objects.filter(member=request.user)


    conetxt = dict(set_contex(request.user))
    conetxt.update({
        'members_form': members_form,
        'Title': 'پروفایل کاربری',
        'html_chart' : html_chart,
        'degree_objects':degree_objects,
        'edu_record_objects' : edu_record_objects,
        'job_record_objects' : job_record_objects,
        'skills_objects' : skills_objects,
        'articles_objects' : articles_objects,
        'books_objects':books_objects,
        'inventions_objects':inventions_objects,
        'passed_trials_objects':passed_trials_objects,
        'member_charts':member_charts,
         })

    if request.method == "POST":
        degree_title = request.POST.getlist('degree_title')
        degree_files=request.FILES.getlist('degree_files')

        edu_records_title = request.POST.getlist('edu_records_title')
        edu_records_files=request.FILES.getlist('edu_records_files')

        job_record_title = request.POST.getlist('job_record_title')
        job_record_files=request.FILES.getlist('job_record_files')

        skills_title = request.POST.getlist('skills_title')
        skills_files=request.FILES.getlist('skills_files')

        articles_title = request.POST.getlist('articles_title')
        articles_files=request.FILES.getlist('articles_files')

        books_title = request.POST.getlist('books_title')
        books_files=request.FILES.getlist('books_files')

        inventions_title = request.POST.getlist('inventions_title')
        inventions_files=request.FILES.getlist('inventions_files')

        passed_trials_title = request.POST.getlist('passed_trials_title')
        passed_trials_files=request.FILES.getlist('passed_trials_files')

        chart_members_list=set(request.POST.getlist('chartMember'))


        
        if len(chart_members_list) !=0:
            this_user_objects=MemberChart.objects.filter(member=request.user)
            for object in this_user_objects:
                object.delete()
            for chart_member_list in chart_members_list:
                obj_member_chart=MemberChart()
                obj_member_chart.member=Members.objects.get(member=request.user.member)
                obj_member_chart.chart=TblChart.objects.get(Chart=chart_member_list)
                obj_member_chart.save()

        if len(degree_files) !=0 and len(degree_title) !=0 and len(degree_files) == len(degree_title) :
            for itemFile,itemTitle in zip(degree_files,degree_title):
                obj_file_doc=pro_degree()
                obj_file_doc.degree_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.pro_degree_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()

        if len(edu_records_files) !=0 and len(edu_records_title) !=0 and len(edu_records_files) == len(edu_records_title) :
            for itemFile,itemTitle in zip(edu_records_files,edu_records_title):
                obj_file_doc=edu_records()
                obj_file_doc.file_edu_records=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.edu_records_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()
                
        if len(job_record_files) !=0 and len(job_record_title) !=0 and len(job_record_files) == len(job_record_title) :
            for itemFile,itemTitle in zip(job_record_files,job_record_title):
                obj_file_doc=job_record()
                obj_file_doc.job_record_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.job_record_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()
        
        if len(skills_files) !=0 and len(skills_title) !=0 and len(skills_files) == len(skills_title) :
            for itemFile,itemTitle in zip(skills_files,skills_title):
                obj_file_doc=skills()
                obj_file_doc.skills_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.skills_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()

        if len(articles_files) !=0 and len(articles_title) !=0 and len(articles_files) == len(articles_title) :
            for itemFile,itemTitle in zip(articles_files,articles_title):
                obj_file_doc=articles()
                obj_file_doc.articles_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.article_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()

        if len(books_files) !=0 and len(books_title) !=0 and len(books_files) == len(books_title) :
            for itemFile,itemTitle in zip(books_files,books_title):
                obj_file_doc=books()
                obj_file_doc.books_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.books_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()

        if len(inventions_files) !=0 and len(inventions_title) !=0 and len(inventions_files) == len(inventions_title) :
            for itemFile,itemTitle in zip(inventions_files,inventions_title):
                obj_file_doc=inventions()
                obj_file_doc.inventions_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.inventions_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()

        if len(passed_trials_files) !=0 and len(passed_trials_title) !=0 and len(passed_trials_files) == len(passed_trials_title) :
            for itemFile,itemTitle in zip(passed_trials_files,passed_trials_title):
                obj_file_doc=passed_trials()
                obj_file_doc.passed_trials_file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.passed_trials_key=Members.objects.get(member=request.user.member)
                obj_file_doc.save()


        if members_form.is_valid():    
            members_form.save()
            return HttpResponseRedirect(reverse('successfullsave'))


    return render(request, 'Profile_page.html', conetxt)

@login_required
def successfullsave(request):

    return render(request,'successfullsave.html',{})

@login_required
def successfullsubmit(request):

    return render(request,'successfullsubmit.html',{})
    
@login_required
def permanent_submit(request, id):
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    submited_Knowledge = TblKnowledge.objects.all()
    if submited_Knowledge.filter(KnowledgeCode=id):
        submited_Knowledge1 = submited_Knowledge.get(KnowledgeCode=id)
        submited_Knowledge1.register_status = 1
        submited_Knowledge1.set_number = submited_Knowledge1.set_number + 1
        submited_Knowledge1.save()

        members = Members.objects.filter(groups__name='IT').exclude( member = request.user.member )

        items = [
        TblKnowledgeNotificationForEliteUsers(user= member , notif = submited_Knowledge1 , url='KnowledgeView/{}'.format(id),notif_type=10)
        for member in members
        ]

        TblKnowledgeNotificationForEliteUsers.objects.bulk_create(items)
    return HttpResponseRedirect('/KnowledgeList/1')


@login_required
def It_send_to_evaluator(request, id):
    """
    it sends the knowledge to evaluator
    """
    if not is_IT(request.user):
        return HttpResponseRedirect('/')

    submited_Knowledge = TblKnowledge.objects.all()
    if submited_Knowledge.filter(KnowledgeCode=id):
        submited_Knowledge1 = submited_Knowledge.get(KnowledgeCode=id)
        if submited_Knowledge1.register_status == 1:
            submited_Knowledge1.register_status = 5
            submited_Knowledge1.save()
    return HttpResponseRedirect('/ITworker')

@login_required
def It_send_back_to_evaluator(request,id):
    """
    it sends the knowledge to evaluator
    """
    if not is_IT(request.user):
        return HttpResponseRedirect('/')
    get_topic1 = topic1.objects.filter(status=1)
    submited_Knowledge = TblKnowledge.objects.all()
    if request.method == "POST":
        form = send_to_evaluatorForm(request.POST or None)
        mozo3=request.POST.get('mozo3')
        mozo1=request.POST.get('mozo1')
        mozo2=request.POST.get('mozo2')
        nazar=request.POST.get('nazar')
        if form.is_valid:
            obj = form.save()
            obj.nazar = nazar
            obj.Creater_UserID = request.user
            obj.knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
            if obj.mozo3_id == None and mozo2 != None:
                obj.mozo2_id = topic2.objects.get(id=mozo2)
                obj.mozo1_id = topic1.objects.get(id=mozo1)
                obj.mozo3_id = topic3.objects.get(id=mozo3)
                obj.save()
            elif obj.mozo3_id == None and mozo2 == None:
                obj.mozo1_id = topic1.objects.get(id=mozo1)
                obj.save()
            else:
                obj.mozo3_id = topic3.objects.get(id=mozo3)
                obj.save()
            
            if submited_Knowledge.filter(KnowledgeCode=id):
                submited_Knowledge1 = submited_Knowledge.get(KnowledgeCode=id)
                if submited_Knowledge1.register_status == 1:
                    submited_Knowledge1.register_status = 5
                    submited_Knowledge1.save()
                    #creates notif for owner and notifies him that the knowledge is accepted
                    TblKnowledgeStatusNotification.objects.create( notif = submited_Knowledge1 , url = 'KnowledgeList/1' )
                    
                    knowledge_chart = TblKnowledge.objects.get(KnowledgeCode=id).KnowledgeProcess
                    this_knowledge_expert_members_list = ExpertChart.objects.filter(chart=knowledge_chart).values_list('member',flat=True)
                    expert_members = Members.objects.filter(member__in = this_knowledge_expert_members_list)
                    
                    items = [
                    TblKnowledgeNotificationForEliteUsers(user= member , notif = submited_Knowledge1 , url='KnowledgeView/{}'.format(id),notif_type=11)
                    for member in expert_members
                    ]

                    TblKnowledgeNotificationForEliteUsers.objects.bulk_create(items)

                    if TblKnowledgeNotificationForEliteUsers.objects.filter(notif__KnowledgeCode = id).filter(notif_type = 10).exists():
                        TblKnowledgeNotificationForEliteUsers.objects.filter(notif__KnowledgeCode = id).filter(notif_type = 10).delete()

        return HttpResponseRedirect('/ITworker')
    context = {
        'get_topic1' : get_topic1 ,
        'send_to_evaluatorForm' : send_to_evaluatorForm(),
    }
    return render(request, 'itSendsBackToEvaluator.html',context)


@login_required
def It_send_back_to_knowledgeWorker_review(request,id):
    """
    it sends the knowledge to knowledgeWorker
    """
    if not is_IT(request.user):
        return HttpResponseRedirect('/')
    members = Members.objects.all()
    if request.method == "POST":
        
        form = rejectForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.rejecter_user_id=request.user
            obj.knowledge_id = TblKnowledge.objects.get(KnowledgeCode=id)
            obj.save()
            submited_Knowledge = TblKnowledge.objects.all()
            if submited_Knowledge.filter(KnowledgeCode=id):
                submited_Knowledge1 = submited_Knowledge.get(KnowledgeCode=id)
                if submited_Knowledge1.register_status == 1:
                    submited_Knowledge1.register_status = 4
                    submited_Knowledge1.save()

                    #creates notif for owner and notifies him that the knowledge is rejected by it
                    TblKnowledgeStatusNotification.objects.create( notif = submited_Knowledge1 , url = 'rejected_knowledgeView/'+str(submited_Knowledge1.KnowledgeCode), notif_type = 7 )

                    if TblKnowledgeNotificationForEliteUsers.objects.filter(notif__KnowledgeCode = id).filter(notif_type = 10).exists():
                        TblKnowledgeNotificationForEliteUsers.objects.filter(notif__KnowledgeCode = id).filter(notif_type = 10).delete()

                return HttpResponseRedirect('/ITworker')
    context = {
        'rejectForm' : rejectForm(),
    }
    return render(request, 'rejected_knowledge_by_it.html',context)


@login_required
def It_send_to_experts(request, id):
    """
    it sends the knowledge to expert
    """
    if not is_IT(request.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        submited_Knowledge = TblKnowledge.objects.all()
        if submited_Knowledge.filter(KnowledgeCode=id):
            submited_Knowledge1 = submited_Knowledge.get(KnowledgeCode=id)

    users=Members.objects.all()
    expert_users=[]

    for user in users:
        if is_expert(user):
            expert_users.append(user)

    context={
        'members':expert_users,
        'teamCount': 0,
    }

    return render(request, 'it_sends_to_expert.html', context)

@login_required
def It_send_back_to_knowledgeWorker(request, id):
    """
    it sends the knowledge to back to knowledge worker
    """
    if not is_IT(request.user):
        return HttpResponseRedirect('/')

    submited_Knowledge = TblKnowledge.objects.all()
    if submited_Knowledge.filter(KnowledgeCode=id):
        submited_Knowledge1 = submited_Knowledge.get(KnowledgeCode=id)
        if submited_Knowledge1.register_status == 1:
            submited_Knowledge1.register_status = 4
            submited_Knowledge1.save()
    return HttpResponseRedirect('/ITworker')


@login_required
def DeleteExperience(request, id):
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if TblKnowledge.objects.filter(KnowledgeCode=id).exists():
        obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
        obj_knowledge_status=obj_knowledge.register_status
        if (obj_knowledge_status >=1 and obj_knowledge_status <=4) or obj_knowledge_status == 6 and obj_knowledge.CreatorUserID == request.user :
            try:
                obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
            except:
                return HttpResponseRedirect('/KnowledgeList/1')
            sucsse_delete = False
            video = None
            document = None
            voice = None
            if obj_knowledge.CreatorUserID.member == request.user.member:
                try:
                    obj_keywords = TblKeywords.objects.filter(Knowledge=id)
                    obj_keywords.delete()
                    video = obj_knowledge.KnowledgeVideo
                    document = obj_knowledge.KnowledgeDocument
                    voice = obj_knowledge.KnowledgeVoice
                    obj_knowledge.delete()
                    sucsse_delete = True
                except:
                    splited_keywords = obj_knowledge.KnowledgeKeywords
                    if splited_keywords is not None:
                        splited_keywords = obj_knowledge.KnowledgeKeywords.split(",")
                        for keyword in splited_keywords:
                            obj_keyword = TblKeywords()
                            obj_keyword.KeywordsText = keyword
                            obj_keyword.Knowledge = obj_knowledge
                            obj_keyword.save()
                    obj_knowledge.Status = -1
                    obj_knowledge.save()
                if sucsse_delete:
                    try:
                        _delete_file(video.path)
                    except:
                        pass
                    try:
                        _delete_file(document.path)
                    except:
                        pass
                    try:
                        _delete_file(voice.path)
                    except:
                        pass
    return HttpResponseRedirect('/KnowledgeList/1')


@login_required
def IT(request, id):
    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')
    knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    conetxt = dict(set_contex(request.user))
    conetxt.update({'Knowledge': knowledge, 'Title': 'فناوری اطلاعات'})
    return render(request, 'iT.html', conetxt)


@login_required
def ITworker(request):
    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')
    knowledges = TblKnowledge.objects.filter(Status__gte=0, register_status=1).exclude(CreatorUserID = request.user)

    context = dict(set_contex(request.user))
    context.update({
        'Knowledges': knowledges,
        'Title': 'دبیر خانه ی مدیریت دانش',
    })

    return render(request, "iT.html", context)


@login_required
def KnowledgeList(request,id):

    #delete notif knowledge accepted by IT
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif_type = 6).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif_type = 6).delete()


    members = Members.objects.all()
    user_name_registered = request.POST.get('members')
    from_date = request.POST.get('from_date3')
    to_date = request.POST.get('to_date3')
    SearchTitle = request.POST.get('SearchTitle')
    SearchKeyword = request.POST.getlist('SearchKeyword')


    if request.user.is_superuser:
        knowledges = TblKnowledge.objects.filter(Status__gte=0)
    else:
        knowledges = TblKnowledge.objects.filter(
            CreatorUserID=request.user.member).filter(Status__gte=0)
    
    context = dict(set_contex(request.user))


    knowledges = knowledge_advance_search( knowledges=knowledges.filter(Type = 1 ) , from_date= from_date , to_date= to_date , search_title= SearchTitle , search_keyword= SearchKeyword , creator_user = user_name_registered)

    if id == 1:
        pageType = 1
    if id == 2:
        pageType = 2


    context.update({
        'Knowledges': knowledges,
        'Title': 'لیست تجربیات',
        'members' : members ,
        'pageType':pageType,

    })
    return render(request, "KnowledgeList.html", context)



@login_required
def comparativeـknowledge_list(request):


    members = Members.objects.all()
    user_name_registered = request.POST.get('members')
    from_date = request.POST.get('from_date3')
    to_date = request.POST.get('to_date3')
    SearchTitle = request.POST.get('SearchTitle')
    SearchKeyword = request.POST.getlist('SearchKeyword')


    if request.user.is_superuser:
        knowledges = TblKnowledge.objects.filter(Status__gte=0)
    else:
        knowledges = TblKnowledge.objects.filter(
            CreatorUserID=request.user.member).filter(Status__gte=0)
    
    context = dict(set_contex(request.user))


    knowledges = knowledge_advance_search( knowledges=knowledges.filter(Type = 3 ) , from_date= from_date , to_date= to_date , search_title= SearchTitle , search_keyword= SearchKeyword , creator_user = user_name_registered)


    context.update({
        'Knowledges': knowledges,
        'Title': 'لیست دانش تطبیقی',
        'members' : members ,
    })
    return render(request, "comparativeـknowledge_list.html", context)


@login_required
def comparative_knowledge_view(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    #delete notif experience became knowledge rejected by IT(status 8) status 14 and 15 are for deleting security notifs
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).delete()
    
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).delete()

    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).delete()
        
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).delete()

    knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_type = TblKnowledge.objects.get(KnowledgeCode=id).Type
    tbl_view = view.objects.all()
    if not tbl_view.filter(user=request.user, post=id).exists():
        obj_view = view()
        obj_view.user = request.user
        obj_view.post = knowledge
        knowledge.view_count += 1
        knowledge.save()
        obj_view.save()

        # calculating the score of the owner of the knowledge and saving it
        obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
        knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
        knowledge_owner.score = score_calculator(knowledge_owner)
        knowledge_owner.save()


    knowledge_owner = Members.objects.get(member=knowledge.CreatorUserID.member)
    team = TblTeam.objects.filter(KnowledgeCode=id).exclude(TeamMember=knowledge_owner)
    if TblTeam.objects.filter(KnowledgeCode=id,TeamMember=request.user.member).exists():
        userPercentage = TblTeam.objects.get(KnowledgeCode=id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    obj_files=FeedFile.objects.filter(feed=id) 
    if len(obj_files) ==0:
        len_files=0
    else:
        len_files=1

    voice = 0 
    
    voice_name = knowledge.voice_url
    if voice_name != None and voice_name != '.mp3':

        voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        
    
    context = dict(set_contex(request.user))
    context.update({
        'post_views': TblKnowledge.objects.get(KnowledgeCode=id).view_count,
        'Knowledge': knowledge,
        'knowledge_type' : knowledge_type,
        'Title': 'کاربرگ',
        'userPercentage':userPercentage,
        'team':team,
        'voice' : voice ,
        'knowledge_owner' : knowledge_owner,
        'obj_files':obj_files,
        'len_files':len_files
    })
    return render(request, "comparative_knowledge_view.html", context)




@login_required
def skillـexperience_list(request):


    members = Members.objects.all()
    user_name_registered = request.POST.get('members')
    from_date = request.POST.get('from_date3')
    to_date = request.POST.get('to_date3')
    SearchTitle = request.POST.get('SearchTitle')
    SearchKeyword = request.POST.getlist('SearchKeyword')


    if request.user.is_superuser:
        knowledges = TblKnowledge.objects.filter(Status__gte=0)
    else:
        knowledges = TblKnowledge.objects.filter(
            CreatorUserID=request.user.member).filter(Status__gte=0)
    
    context = dict(set_contex(request.user))


    knowledges = knowledge_advance_search( knowledges=knowledges.filter(Type = 4 ) , from_date= from_date , to_date= to_date , search_title= SearchTitle , search_keyword= SearchKeyword , creator_user = user_name_registered)


    context.update({
        'Knowledges': knowledges,
        'Title': 'لیست تجربه مهارت',
        'members' : members ,
    })
    return render(request, "skill_experience_list.html", context)



@login_required
def skill_experience_view(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    #delete notif experience became knowledge rejected by IT(status 8) status 14 and 15 are for deleting security notifs
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).delete()
    
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).delete()

    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).delete()
        
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).delete()

    knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_type = TblKnowledge.objects.get(KnowledgeCode=id).Type
    tbl_view = view.objects.all()
    if not tbl_view.filter(user=request.user, post=id).exists():
        obj_view = view()
        obj_view.user = request.user
        obj_view.post = knowledge
        knowledge.view_count += 1
        knowledge.save()
        obj_view.save()

        # calculating the score of the owner of the knowledge and saving it
        obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
        knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
        knowledge_owner.score = score_calculator(knowledge_owner)
        knowledge_owner.save()


    knowledge_owner = Members.objects.get(member=knowledge.CreatorUserID.member)
    team = TblTeam.objects.filter(KnowledgeCode=id).exclude(TeamMember=knowledge_owner)
    if TblTeam.objects.filter(KnowledgeCode=id,TeamMember=request.user.member).exists():
        userPercentage = TblTeam.objects.get(KnowledgeCode=id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    obj_files=FeedFile.objects.filter(feed=id) 
    if len(obj_files) ==0:
        len_files=0
    else:
        len_files=1

    voice = 0 
    
    voice_name = knowledge.voice_url
    if voice_name != None and voice_name != '.mp3':

        voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        
    
    context = dict(set_contex(request.user))
    context.update({
        'post_views': TblKnowledge.objects.get(KnowledgeCode=id).view_count,
        'Knowledge': knowledge,
        'knowledge_type' : knowledge_type,
        'Title': 'کاربرگ',
        'userPercentage':userPercentage,
        'team':team,
        'voice' : voice ,
        'knowledge_owner' : knowledge_owner,
        'obj_files':obj_files,
        'len_files':len_files
    })
    return render(request, "skill_experience_view.html", context)



@login_required
def jobـpromotion(request):


    members = Members.objects.all()
    user_name_registered = request.POST.get('members')
    from_date = request.POST.get('from_date3')
    to_date = request.POST.get('to_date3')
    SearchTitle = request.POST.get('SearchTitle')
    SearchKeyword = request.POST.getlist('SearchKeyword')


    if request.user.is_superuser:
        knowledges = TblKnowledge.objects.filter(Status__gte=0)
    else:
        knowledges = TblKnowledge.objects.filter(
            CreatorUserID=request.user.member).filter(Status__gte=0)
    
    context = dict(set_contex(request.user))


    knowledges = knowledge_advance_search( knowledges=knowledges.filter(Type = 5 ) , from_date= from_date , to_date= to_date , search_title= SearchTitle , search_keyword= SearchKeyword , creator_user = user_name_registered)


    context.update({
        'Knowledges': knowledges,
        'Title': 'لیست  ارتقای شغلی',
        'members' : members ,
    })
    return render(request, "skill_experience_list.html", context)

@login_required
def KnowledgeReport(request):

    get_topic1 = topic1.objects.filter(status=1)
    # knowledges = TblKnowledge.objects.filter(Status__gte=0).filter(Q(register_status=7) | Q(register_status=9))

    # knowledges = TblKnowledge.objects.raw('''
    #     SELECT KnowledgeManagement_tblknowledge.KnowledgeCode,KnowledgeManagement_tblknowledge.KnowledgeTitle,KnowledgeManagement_tblknowledge.CreateDate,KnowledgeManagement_tblknowledge.CreatorUserID_id
    #     FROM KnowledgeManagement_tblknowledge 
    #     LEFT JOIN KnowledgeManagement_tblusedknowledge ON KnowledgeManagement_tblknowledge.KnowledgeCode = KnowledgeManagement_tblusedknowledge.knowledge_id
    #     where register_status = 7 or register_status = 9 and Status = 1
    #     Group by KnowledgeManagement_tblknowledge.KnowledgeCode
    #     order by count( KnowledgeManagement_tblusedknowledge.id) desc;
    #  ''')

    knowledges = TblKnowledge.objects.filter(Status__gte=0).filter(Q(register_status=7) | Q(register_status=9))

    if request.method == "POST":
        user_name_registered = request.POST.get('user_name_registered')
        KnowledgeCategory = request.POST.get('KnowledgeCategory')
        from_date = request.POST.get('from_date3')
        to_date = request.POST.get('to_date3')
        SearchUsedDomain = request.POST.get('SearchUsedDomain')
        SearchTitle = request.POST.get('SearchTitle')
        SearchKeyword = request.POST.getlist('SearchKeyword')
        topic3_pk = request.POST.get('mozo3')
        topic2_pk = request.POST.get('topic2-subject')
        topic1_pk = request.POST.get('topic1-subject')

        if KnowledgeCategory is not None and int(KnowledgeCategory) != -1:
            knowledges = knowledges.filter(KnowledgeCategory=KnowledgeCategory)

        if SearchUsedDomain is not None and int(SearchUsedDomain) != -1:
            knowledges = knowledges.filter(KnowledgeUsers=SearchUsedDomain)

        knowledges = knowledge_advance_search(knowledges , from_date , to_date , search_keyword= SearchKeyword , search_title=SearchTitle,creator_user= user_name_registered)
        
        if topic3_pk is not None:
            topic3_knowledges_list = send_to_evaluator.objects.values_list('knowledge', flat=True).filter(mozo3_id=topic3.objects.get(id=topic3_pk))
            knowledges = knowledges.filter(KnowledgeCode__in=topic3_knowledges_list)

        elif topic2_pk is not None:
            topic2_knowledges_list = send_to_evaluator.objects.values_list('knowledge', flat=True).filter(mozo2_id=topic2.objects.get(id=topic2_pk))
            knowledges = knowledges.filter(KnowledgeCode__in=topic2_knowledges_list)

        elif topic1_pk is not None and topic1_pk != '-1':
            topic1_knowledges_list = send_to_evaluator.objects.values_list('knowledge', flat=True).filter(mozo1_id=topic1.objects.get(id=topic1_pk))
            knowledges = knowledges.filter(KnowledgeCode__in=topic1_knowledges_list)

    context = dict(set_contex(request.user))
    context.update({
        'Knowledges': knowledges,
        'Title': 'گزارش دانش ها',
        'show_button':1,
        'get_topic1':get_topic1,
        'knowledge_report_indicator':1,
    })
    return render(request, "Knowledge_Report_List.html", context)


@login_required
def matchingknowledge(request, id):

    max_value = 0
    max_key = 1
    comparing_dict = {}
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_words_loop = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9))
    for item in knowledge_words_loop:
        if item.KnowledgeCode != knowledge:
            temp_text_summary = item.KnowledgeTextSummary
            current_splited_title = knowledge.KnowledgeTitle.split(' ')
            temp_splited_title = item.KnowledgeTitle.split(' ')
            
            len_current_splited_title = len(current_splited_title)
            len_temp_splited_title = len(temp_splited_title)
            title_result = len(set(temp_splited_title) & set(current_splited_title))
            sum_split_titles = len_current_splited_title + len_temp_splited_title - title_result
            title_point = (title_result / sum_split_titles) * 100
            
            temp_keywords = item.KnowledgeKeywords
            if temp_keywords != None:
                splited_temp_keywords = re.split('; |, |،',temp_keywords)
                current_keywords = knowledge.KnowledgeKeywords
                if current_keywords == None:
                    current_keywords = 'سلام'
                splited_current_keywords = re.split('; |, |،',current_keywords)

                len_splited_temp_keywords = len(splited_temp_keywords)
                len_splited_current_keywords = len(splited_current_keywords)
                words_result = len(set(splited_temp_keywords) & set(splited_current_keywords))
                sum_words = len_splited_temp_keywords + len_splited_current_keywords - words_result
                words_point = (words_result / sum_words ) * 100
                total_point = words_point + title_point
                total_point = total_point / 2
                if words_result >= 2:
                    replaced_pattern = re.compile('|'.join(splited_current_keywords))
                    pattern = re.compile(r'{}'.format(replaced_pattern.pattern))
                    value = spaces_between_words_dict(pattern,temp_text_summary)
                    final_result_point = value + total_point

                    if final_result_point >= 50:
                        comparing_dict[item.KnowledgeCode]=final_result_point
        else:
            continue
    if len(comparing_dict) != 0:
        all_values = comparing_dict.values()
        max_value = str(max(all_values))
        max_key = max(comparing_dict, key=comparing_dict.get)

    
    context = {
        'Knowledge': knowledge,
        'Title': 'نمایش دانش منطبق',
        'max_value' : max_value,
        'max_key' : max_key,

    }

    return render(request, "matchingknowledge.html", context)

@login_required
def Request_view(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')
    report = TblKnowledgeRequest.objects.get(id=id)
    context = dict(set_contex(request.user))
    context.update({
        'Title': ' کاربرگ در خواست دانش','report' : report,
    })
    return render(request, "Request_view.html", context)


@login_required
def send_view(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')
    report = TblKnowledgeRequest.objects.get(id=id)

    team_this_knowledge = TblTeam2.objects.filter(KnowledgeCode=id)

    send_karbarg_code = 1
    context = dict(set_contex(request.user))
    context.update({
        'Title': ' کاربرگ در خواست دانش',
        'report' : report,
        'team_this_knowledge':team_this_knowledge,
        'send_karbarg_code':send_karbarg_code,
    })
    return render(request, "Request_view.html", context)



@login_required
def KnowledgeView(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    #delete notif experience became knowledge rejected by IT(status 8) status 14 and 15 are for deleting security notifs
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).delete()
    
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).delete()

    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).delete()
        
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).delete()

    knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_type = TblKnowledge.objects.get(KnowledgeCode=id).Type
    tbl_view = view.objects.all()
    if not tbl_view.filter(user=request.user, post=id).exists():
        obj_view = view()
        obj_view.user = request.user
        obj_view.post = knowledge
        knowledge.view_count += 1
        knowledge.save()
        obj_view.save()

        # calculating the score of the owner of the knowledge and saving it
        obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
        knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
        knowledge_owner.score = score_calculator(knowledge_owner)
        knowledge_owner.save()


    knowledge_owner = Members.objects.get(member=knowledge.CreatorUserID.member)
    team = TblTeam.objects.filter(KnowledgeCode=id).exclude(TeamMember=knowledge_owner)
    if TblTeam.objects.filter(KnowledgeCode=id,TeamMember=request.user.member).exists():
        userPercentage = TblTeam.objects.get(KnowledgeCode=id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    obj_files=FeedFile.objects.filter(feed=id) 
    if len(obj_files) ==0:
        len_files=0
    else:
        len_files=1

    voice = 0 
    
    voice_name = knowledge.voice_url
    if voice_name != None and voice_name != '.mp3':

        voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        
    
    context = dict(set_contex(request.user))
    context.update({
        'post_views': TblKnowledge.objects.get(KnowledgeCode=id).view_count,
        'Knowledge': knowledge,
        'knowledge_type' : knowledge_type,
        'Title': 'کاربرگ',
        'userPercentage':userPercentage,
        'team':team,
        'voice' : voice ,
        'knowledge_owner' : knowledge_owner,
        'obj_files':obj_files,
        'len_files':len_files
    })
    return render(request, "KnowledgeView.html", context)



@login_required
def job_promotion_view(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    #delete notif experience became knowledge rejected by IT(status 8) status 14 and 15 are for deleting security notifs
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(Q(notif_type = 8) | Q(notif_type = 14)| Q(notif_type = 15)).delete()
    
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 10).delete()

    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 11).delete()
        
    if TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).exists():
        TblKnowledgeNotificationForEliteUsers.objects.filter(user = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 12).delete()

    knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_type = TblKnowledge.objects.get(KnowledgeCode=id).Type
    tbl_view = view.objects.all()
    if not tbl_view.filter(user=request.user, post=id).exists():
        obj_view = view()
        obj_view.user = request.user
        obj_view.post = knowledge
        knowledge.view_count += 1
        knowledge.save()
        obj_view.save()

        # calculating the score of the owner of the knowledge and saving it
        obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
        knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
        knowledge_owner.score = score_calculator(knowledge_owner)
        knowledge_owner.save()


    knowledge_owner = Members.objects.get(member=knowledge.CreatorUserID.member)
    team = TblTeam.objects.filter(KnowledgeCode=id).exclude(TeamMember=knowledge_owner)
    if TblTeam.objects.filter(KnowledgeCode=id,TeamMember=request.user.member).exists():
        userPercentage = TblTeam.objects.get(KnowledgeCode=id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    obj_files=FeedFile.objects.filter(feed=id) 
    if len(obj_files) ==0:
        len_files=0
    else:
        len_files=1

    voice = 0 
    
    voice_name = knowledge.voice_url
    if voice_name != None and voice_name != '.mp3':

        voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        
    
    context = dict(set_contex(request.user))
    context.update({
        'post_views': TblKnowledge.objects.get(KnowledgeCode=id).view_count,
        'Knowledge': knowledge,
        'knowledge_type' : knowledge_type,
        'Title': 'کاربرگ',
        'userPercentage':userPercentage,
        'team':team,
        'voice' : voice ,
        'knowledge_owner' : knowledge_owner,
        'obj_files':obj_files,
        'len_files':len_files
    })
    return render(request, "job_promotion_view.html", context)


@login_required
def DocumentView(request, id):
    if not is_knowlege_worker(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    document = Documentation.objects.get(id=id)

    knowledge_owner = Members.objects.get(member=document.CreatorUserID.member)
    team = TblTeamDocumentation.objects.filter(DocumentationCode=id).exclude(TeamMember=knowledge_owner)
    if TblTeamDocumentation.objects.filter(DocumentationCode=id,TeamMember=request.user.member).exists():
        userPercentage = TblTeamDocumentation.objects.get(DocumentationCode=id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    obj_files=FeedFileDocumentation.objects.filter(feed=id) 
    if len(obj_files) ==0:
        len_files=0
    else:
        len_files=1

    context = dict(set_contex(request.user))
    context.update({
        'document': document,
        'Title': 'کاربرگ',
        'obj_files':obj_files,
        'team' : team ,
        'knowledge_owner' : knowledge_owner,
        'userPercentage' : userPercentage ,
        'len_files':len_files
    })
    return render(request, "DocumentView.html", context)


@login_required
def change_success(request):
     return HttpResponseRedirect('success_pass_changed')


@login_required
def PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('change_success')


@login_required
def ReportKnowledgeTree(request):
    if not is_expert(request.user):
        return HttpResponseRedirect('/login')
    context = dict(set_contex(request.user))
    context.update({
        'Title': 'درخت تصمیم گیری دانش',
    })
    return render(request, "ReportKnowledgeTree.html", context)


@login_required
def RegisterTitle(request):
    """Ajaxly register KnowledgeTitle"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeTitle()
        obj.KnowledgeTitleText = text
        obj.CreateDate = 14000622
        obj.save()
        knowledge_title_list = TblKnowledgeTitle.objects.filter(Status=1)
        # post_list = serializers.serialize('json', list(KnowledgeTitleList), fields=('KnowledgeTitle', 'KnowledgeTitleText'))
        json = "["
        for item in knowledge_title_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeTitle) + \
                    "\", \"text\":\"" + item.KnowledgeTitleText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def get_knowledge_category(request):
    knowledge_category_list = TblKnowledgeCategory.objects.filter(Status=1)
    json = "["
    for item in knowledge_category_list:
        if len(json) > 1:
            json += ","
        json += "{\"id\":\"" + str(item.KnowledgeCategory) + \
                "\", \"text\":\"" + item.KnowledgeCategoryText + "\"}"
    json += "]"
    return HttpResponse(json)


@login_required
def get_members(request):
    members_list = Members.objects.all()
    json = "["
    for item in members_list:
        if item.first_name and item.last_name:
            mamber_name = item.first_name + ' ' + item.last_name
        else:
            mamber_name = item.username
        if len(json) > 1:
            json += ","
        json += "{\"id\":\"" + str(item.member) + \
                "\", \"text\":\"" + mamber_name + "\"}"
    json += "]"
    return HttpResponse(json)


@login_required
def get_title(request):
    title_list = TblKnowledgeTitle.objects.filter()
    json = "["
    for item in title_list:
        if len(json) > 1:
            json += ","
        json += "{\"id\":\"" + str(item.KnowledgeTitle) + \
                "\", \"text\":\"" + item.KnowledgeTitleText + "\"}"
    json += "]"
    return HttpResponse(json)


@login_required
def RegisterCause(request):
    """Ajaxly register KnowledgeCause"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeCause()
        obj.KnowledgeCauseText = text
        obj.save()
        knowledge_cause_list = TblKnowledgeCause.objects.filter(Status=1)
        json = "["
        for item in knowledge_cause_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeCause) + \
                    "\", \"text\":\"" + item.KnowledgeCauseText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterWhichAction(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeWhichAction()
        obj.KnowledgeDoText = text
        obj.save()
        knowledge_which_action_list = TblKnowledgeWhichAction.objects.filter(
            Status=1)
        json = "["
        for item in knowledge_which_action_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeDo) + \
                    "\", \"text\":\"" + item.KnowledgeDoText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterHow(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeHow()
        obj.KnowledgeHowText = text
        obj.save()
        knowledge_how_list = TblKnowledgeHow.objects.filter(Status=1)
        json = "["
        for item in knowledge_how_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeHow) + \
                    "\", \"text\":\"" + item.KnowledgeHowText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterResource(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeResource()
        obj.KnowledgeResourceText = text
        obj.save()
        knowledge_resource_list = TblKnowledgeResource.objects.filter(
            Status=1)
        json = "["
        for item in knowledge_resource_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeResource) + \
                    "\", \"text\":\"" + item.KnowledgeResourceText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterEvaluation(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeEvaluation()
        obj.KnowledgeEvaluationText = text
        obj.save()
        knowledge_evaluation_list = TblKnowledgeEvaluation.objects.filter(
            Status=1)
        json = "["
        for item in knowledge_evaluation_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeEvaluation) + \
                    "\", \"text\":\"" + item.KnowledgeEvaluationText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterConditions(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeConditions()
        obj.KnowledgeConditionsText = text
        obj.save()
        knowledge_conditions_list = TblKnowledgeConditions.objects.filter(
            Status=1)
        json = "["
        for item in knowledge_conditions_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeConditions) + \
                    "\", \"text\":\"" + item.KnowledgeConditionsText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterRisks(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeRisks()
        obj.KnowledgeRisksText = text
        obj.save()
        knowledge_risks_list = TblKnowledgeRisks.objects.filter(Status=1)
        json = "["
        for item in knowledge_risks_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeRisks) + \
                    "\", \"text\":\"" + item.KnowledgeRisksText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterResults(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeResults()
        obj.KnowledgeResultsText = text
        obj.save()
        knowledge_results_list = TblKnowledgeResults.objects.filter(Status=1)
        json = "["
        for item in knowledge_results_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeResults) + \
                    "\", \"text\":\"" + item.KnowledgeResultsText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterUsedCases(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeUsedCases()
        obj.KnowledgeUsedCasesText = text
        obj.save()
        knowledge_used_cases_list = TblKnowledgeUsedCases.objects.filter(
            Status=1)
        json = "["
        for item in knowledge_used_cases_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeUsedCases) + \
                    "\", \"text\":\"" + item.KnowledgeUsedCasesText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterUsers(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        if text is not None and text != '':
            obj = TblUsedDomain()
            obj.UsedDomainText = text
            obj.save()
        used_domain_list = TblUsedDomain.objects.filter(Status=1)
        json = "["
        for item in used_domain_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.UsedDomain) + \
                    "\", \"text\":\"" + item.UsedDomainText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterKnowledgeOpportunities(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeOpportunities()
        obj.KnowledgeOpportunitiesText = text
        obj.save()
        opportunities_list = TblKnowledgeOpportunities.objects.filter(Status=1)
        json = "["
        for item in opportunities_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeOpportunities) + \
                    "\", \"text\":\"" + item.KnowledgeOpportunitiesText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def RegisterProblemPreventation(request):
    """Ajaxly register KnowledgeWhichAction"""
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        text = request.POST.get('text', None)
        obj = TblKnowledgeProblemPreventation()
        obj.KnowledgeProblemPreventationText = text
        obj.save()
        knowledge_problem_preventation_list = TblKnowledgeProblemPreventation.objects.filter(
            Status=1)
        json = "["
        for item in knowledge_problem_preventation_list:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.KnowledgeProblemPreventation) + \
                    "\", \"text\":\"" + item.KnowledgeProblemPreventationText + "\"}"
        json += "]"
        return HttpResponse(json)
    else:
        return HttpResponse("Request method is not a POST!")


@login_required
def define_3topics(request):
    topic1_objects = topic1.objects.filter(status=1)
    topic2_objects = topic2.objects.filter(status=1)
    topic3_objects = topic3.objects.filter(status=1)

    if request.method == 'POST':
        chart_text = request.POST.get('ChartText')
        parent_id = request.POST.get('Parent_Id')
        chart_type = request.POST.get('ChartType')

        if parent_id !='' and chart_type is not None:
            parent_id=int(parent_id)
            chart_type=int(chart_type)

            if chart_type == 1:
                topic1_obj=topic1()
                topic1_obj.mozo1=chart_text
                topic1_obj.save()

            elif chart_type == 2:
                topic2_obj=topic2()
                topic2_obj.state=chart_text
                topic2_obj.mozo1=topic1.objects.get(id=parent_id)
                topic2_obj.save()

            elif chart_type == 3:
                topic3_obj=topic3()
                topic3_obj.city=chart_text
                topic3_obj.mozo2=topic2.objects.get(id=parent_id)
                topic3_obj.save()

    context={
        'topic1_objects' :topic1_objects,
        'topic2_objects' :topic2_objects,
        'topic3_objects' :topic3_objects,
    }

    return render(request, 'define_3topics.html', context)

@login_required
def delete_topic_node(request,id,type):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))
    
    if type == 1:
        obj_topic1 = topic1.objects.get(id=id)
        obj_topic1.status=-1
        obj_topic1.save()

    elif type == 2:
        obj_topic2 = topic2.objects.get(id=id)
        obj_topic2.status=-1
        obj_topic2.save()

    elif type == 3:
        obj_topic3 = topic3.objects.get(id=id)
        obj_topic3.status=-1
        obj_topic3.save()

    return HttpResponseRedirect("/define_3topics")

@login_required
def edit_topic_node(request,id,type,text):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))
    
    if type == 1:
        obj_topic1 = topic1.objects.get(id=id)
        obj_topic1.mozo1=text
        obj_topic1.save()

    elif type == 2:
        obj_topic2 = topic2.objects.get(id=id)
        obj_topic2.state=text
        obj_topic2.save()

    elif type == 3:
        obj_topic3 = topic3.objects.get(id=id)
        obj_topic3.city=text
        obj_topic3.save()

    return HttpResponseRedirect("/define_3topics")

@login_required
def ChartManagment(request):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        chart_text = request.POST.get('ChartText')
        parent_id = request.POST.get('Parent_Id')
        chart_type = request.POST.get('ChartType')
        len_children=len(TblChart.objects.filter(Parent=parent_id))

        # if parent_id != '' and request.POST.get('CharText') is not None:
        if parent_id != '' and chart_text != '':
            obj_chart = TblChart()
            obj_chart.Parent = TblChart.objects.get(Chart=parent_id)
            obj_chart.ChartText = chart_text
            obj_chart.ChartType = chart_type
            obj_chart.save()
            Alphabet=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Aa', 'Ab', 'Ac', 'Ad', 'Ae', 'Af', 'Ag', 'Ah', 'Ai', 'Aj', 'Ak', 'Al', 'Am', 'An', 'Ao', 'Ap', 'Aq', 'Ar', 'As', 'At', 'Au', 'Av', 'Aw', 'Ax', 'Ay', 'Az', 'Ba', 'Bb', 'Bc', 'Bd', 'Be', 'Bf', 'Bg', 'Bh', 'Bi', 'Bj', 'Bk', 'Bl', 'Bm', 'Bn', 'Bo', 'Bp', 'Bq', 'Br', 'Bs', 'Bt', 'Bu', 'Bv', 'Bw', 'Bx', 'By', 'Bz', 'Ca', 'Cb', 'Cc', 'Cd', 'Ce', 'Cf', 'Cg', 'Ch', 'Ci', 'Cj', 'Ck', 'Cl', 'Cm', 'Cn', 'Co', 'Cp', 'Cq', 'Cr', 'Cs', 'Ct', 'Cu', 'Cv', 'Cw', 'Cx', 'Cy', 'Cz', 'Da', 'Db', 'Dc', 'Dd', 'De', 'Df', 'Dg', 'Dh', 'Di', 'Dj', 'Dk', 'Dl', 'Dm', 'Dn', 'Do', 'Dp', 'Dq', 'Dr', 'Ds', 'Dt', 'Du', 'Dv', 'Dw', 'Dx', 'Dy', 'Dz', 'Ea', 'Eb', 'Ec', 'Ed', 'Ee', 'Ef', 'Eg', 'Eh', 'Ei', 'Ej', 'Ek', 'El', 'Em', 'En', 'Eo', 'Ep', 'Eq', 'Er', 'Es', 'Et', 'Eu', 'Ev', 'Ew', 'Ex', 'Ey', 'Ez', 'Fa', 'Fb', 'Fc', 'Fd', 'Fe', 'Ff', 'Fg', 'Fh', 'Fi', 'Fj', 'Fk', 'Fl', 'Fm', 'Fn', 'Fo', 'Fp', 'Fq', 'Fr', 'Fs', 'Ft', 'Fu', 'Fv', 'Fw', 'Fx', 'Fy', 'Fz', 'Ga', 'Gb', 'Gc', 'Gd', 'Ge', 'Gf', 'Gg', 'Gh', 'Gi', 'Gj', 'Gk', 'Gl', 'Gm', 'Gn', 'Go', 'Gp', 'Gq', 'Gr', 'Gs', 'Gt', 'Gu', 'Gv', 'Gw', 'Gx', 'Gy', 'Gz', 'Ha', 'Hb', 'Hc', 'Hd', 'He', 'Hf', 'Hg', 'Hh', 'Hi', 'Hj', 'Hk', 'Hl', 'Hm', 'Hn', 'Ho', 'Hp', 'Hq', 'Hr', 'Hs', 'Ht', 'Hu', 'Hv', 'Hw', 'Hx', 'Hy', 'Hz', 'Ia', 'Ib', 'Ic', 'Id', 'Ie', 'If', 'Ig', 'Ih', 'Ii', 'Ij', 'Ik', 'Il', 'Im', 'In', 'Io', 'Ip', 'Iq', 'Ir', 'Is', 'It', 'Iu', 'Iv', 'Iw', 'Ix', 'Iy', 'Iz', 'Ja', 'Jb', 'Jc', 'Jd', 'Je', 'Jf', 'Jg', 'Jh', 'Ji', 'Jj', 'Jk', 'Jl', 'Jm', 'Jn', 'Jo', 'Jp', 'Jq', 'Jr', 'Js', 'Jt', 'Ju', 'Jv', 'Jw', 'Jx', 'Jy', 'Jz', 'Ka', 'Kb', 'Kc', 'Kd', 'Ke', 'Kf', 'Kg', 'Kh', 'Ki', 'Kj', 'Kk', 'Kl', 'Km', 'Kn', 'Ko', 'Kp', 'Kq', 'Kr', 'Ks', 'Kt', 'Ku', 'Kv', 'Kw', 'Kx', 'Ky', 'Kz', 'La', 'Lb', 'Lc', 'Ld', 'Le', 'Lf', 'Lg', 'Lh', 'Li', 'Lj', 'Lk', 'Ll', 'Lm', 'Ln', 'Lo', 'Lp', 'Lq', 'Lr', 'Ls', 'Lt', 'Lu', 'Lv', 'Lw', 'Lx', 'Ly', 'Lz', 'Ma', 'Mb', 'Mc', 'Md', 'Me', 'Mf', 'Mg', 'Mh', 'Mi', 'Mj', 'Mk', 'Ml', 'Mm', 'Mn', 'Mo', 'Mp', 'Mq', 'Mr', 'Ms', 'Mt', 'Mu', 'Mv', 'Mw', 'Mx', 'My', 'Mz', 'Na', 'Nb', 'Nc', 'Nd', 'Ne', 'Nf', 'Ng', 'Nh', 'Ni', 'Nj', 'Nk', 'Nl', 'Nm', 'Nn', 'No', 'Np', 'Nq', 'Nr', 'Ns', 'Nt', 'Nu', 'Nv', 'Nw', 'Nx', 'Ny', 'Nz', 'Oa', 'Ob', 'Oc', 'Od', 'Oe', 'Of', 'Og', 'Oh', 'Oi', 'Oj', 'Ok', 'Ol', 'Om', 'On', 'Oo', 'Op', 'Oq', 'Or', 'Os', 'Ot', 'Ou', 'Ov', 'Ow', 'Ox', 'Oy', 'Oz', 'Pa', 'Pb', 'Pc', 'Pd', 'Pe', 'Pf', 'Pg', 'Ph', 'Pi', 'Pj', 'Pk', 'Pl', 'Pm', 'Pn', 'Po', 'Pp', 'Pq', 'Pr', 'Ps', 'Pt', 'Pu', 'Pv', 'Pw', 'Px', 'Py', 'Pz', 'Qa', 'Qb', 'Qc', 'Qd', 'Qe', 'Qf', 'Qg', 'Qh', 'Qi', 'Qj', 'Qk', 'Ql', 'Qm', 'Qn', 'Qo', 'Qp', 'Qq', 'Qr', 'Qs', 'Qt', 'Qu', 'Qv', 'Qw', 'Qx', 'Qy', 'Qz', 'Ra', 'Rb', 'Rc', 'Rd', 'Re', 'Rf', 'Rg', 'Rh', 'Ri', 'Rj', 'Rk', 'Rl', 'Rm', 'Rn', 'Ro', 'Rp', 'Rq', 'Rr', 'Rs', 'Rt', 'Ru', 'Rv', 'Rw', 'Rx', 'Ry', 'Rz', 'Sa', 'Sb', 'Sc', 'Sd', 'Se', 'Sf', 'Sg', 'Sh', 'Si', 'Sj', 'Sk', 'Sl', 'Sm', 'Sn', 'So', 'Sp', 'Sq', 'Sr', 'Ss', 'St', 'Su', 'Sv', 'Sw', 'Sx', 'Sy', 'Sz', 'Ta', 'Tb', 'Tc', 'Td', 'Te', 'Tf', 'Tg', 'Th', 'Ti', 'Tj', 'Tk', 'Tl', 'Tm', 'Tn', 'To', 'Tp', 'Tq', 'Tr', 'Ts', 'Tt', 'Tu', 'Tv', 'Tw', 'Tx', 'Ty', 'Tz', 'Ua', 'Ub', 'Uc', 'Ud', 'Ue', 'Uf', 'Ug', 'Uh', 'Ui', 'Uj', 'Uk', 'Ul', 'Um', 'Un', 'Uo', 'Up', 'Uq', 'Ur', 'Us', 'Ut', 'Uu', 'Uv', 'Uw', 'Ux', 'Uy', 'Uz', 'Va', 'Vb', 'Vc', 'Vd', 'Ve', 'Vf', 'Vg', 'Vh', 'Vi', 'Vj', 'Vk', 'Vl', 'Vm', 'Vn', 'Vo', 'Vp', 'Vq', 'Vr', 'Vs', 'Vt', 'Vu', 'Vv', 'Vw', 'Vx', 'Vy', 'Vz', 'Wa', 'Wb', 'Wc', 'Wd', 'We', 'Wf', 'Wg', 'Wh', 'Wi', 'Wj', 'Wk', 'Wl', 'Wm', 'Wn', 'Wo', 'Wp', 'Wq', 'Wr', 'Ws', 'Wt', 'Wu', 'Wv', 'Ww', 'Wx', 'Wy', 'Wz', 'Xa', 'Xb', 'Xc', 'Xd', 'Xe', 'Xf', 'Xg', 'Xh', 'Xi', 'Xj', 'Xk', 'Xl', 'Xm', 'Xn', 'Xo', 'Xp', 'Xq', 'Xr', 'Xs', 'Xt', 'Xu', 'Xv', 'Xw', 'Xx', 'Xy', 'Xz', 'Ya', 'Yb', 'Yc', 'Yd', 'Ye', 'Yf', 'Yg', 'Yh', 'Yi', 'Yj', 'Yk', 'Yl', 'Ym', 'Yn', 'Yo', 'Yp', 'Yq', 'Yr', 'Ys', 'Yt', 'Yu', 'Yv', 'Yw', 'Yx', 'Yy', 'Yz', 'Za', 'Zb', 'Zc', 'Zd', 'Ze', 'Zf', 'Zg', 'Zh', 'Zi', 'Zj', 'Zk', 'Zl', 'Zm', 'Zn', 'Zo', 'Zp', 'Zq', 'Zr', 'Zs', 'Zt', 'Zu', 'Zv', 'Zw', 'Zx', 'Zy', 'Zz']
            if parent_id == "1":
                obj_chart.location=Alphabet[len_children]+str(len_children+1)
                obj_chart.save()
            else:
                obj_chart.location=TblChart.objects.get(Chart=parent_id).location+str(len_children+1)
                obj_chart.save()
            
    html_chart = create_chart_tree(None)
    chart_text = ""
    parent_id = ""
    context = dict(set_contex(request.user))
    context.update({
        'Title': 'مدیریت چارت',
        'html_chart': html_chart,
    })
    return render(request, 'ChartManagment.html', context)


@login_required
def EditChartNode(request, id):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))


    chart = ""
    chart_text = ""
    if id is not None:
        obj_chart = TblChart.objects.get(Chart=id)
        if obj_chart is not None:
            chart = obj_chart.Chart
            chart_text = obj_chart.ChartText
            chart_type = obj_chart.ChartType
            perent_type = None
            if obj_chart.Parent is not None:
                perent_type = obj_chart.Parent.ChartType
        else:
            return HttpResponseRedirect("/ChartManagment")
    else:
        return HttpResponseRedirect("/ChartManagment")
    context = dict(set_contex(request.user))
    context.update({
        'Title': 'مدیریت چارت',
        'chart': chart,
        'chartText': chart_text,
        'chartType': chart_type,
        'perentType': perent_type,
    })
    return render(request, 'EditChartNode.html', context)


@login_required
def UpdateChartNode(request):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        chart_id = request.POST.get('chart')
        chart_text = request.POST.get('ChartText')
        chart_type = request.POST.get('ChartType')

        obj_chart = TblChart.objects.get(Chart=chart_id)
        if obj_chart is not None:
            obj_chart.ChartText = chart_text
            obj_chart.ChartType = chart_type
            obj_chart.save()
        else:
            context = dict(set_contex(request.user))
            context.update({
                'Title': 'مدیریت چارت',
                'chart': chart_id,
                'chartText': chart_text,
            })
            return render(request, 'EditChartNode.html', )
    return HttpResponseRedirect('/ChartManagment')


@login_required
def DeleteChartNode(request, id):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))
    obj_chart = TblChart.objects.get(Chart=id)
    try:
        obj_chart.delete()
    except:
        if obj_chart.Parent is not None:
            obj_chart.Status = -1
        else:
            pass
        obj_chart.save()
    return HttpResponseRedirect('/ChartManagment')


# @login_required
# def KnowledgeDocuments(request, id):
#     if not is_knowlege_worker(request.user):
#         return HttpResponseRedirect('/login')
#     conetxt = dict(set_contex(request.user))
#     knowlege_document=TblKnowledgeDocuments.objects.all()

#     # if not knowlege_document.filter(KnowledgeCode=id).exists():
#     #     obj_doc=TblKnowledgeDocuments()
#     #     obj_doc.KnowledgeCode=TblKnowledge.objects.get(KnowledgeCode=id)
#     #     obj_doc.save()

#     # knowledge_document_form = TblKnowledgeDocumentsForm(request.POST or None, request.FILES or None,
#     #     instance=knowlege_document.get(KnowledgeCode=id))

#     if request.method == "POST":
#         if not knowlege_document.filter(KnowledgeCode=id).exists():
#             obj_doc=TblKnowledgeDocuments()
#             obj_doc.KnowledgeCode=TblKnowledge.objects.get(KnowledgeCode=id)
#             obj_doc.save()
#         knowledge_document_form = TblKnowledgeDocumentsForm(request.POST or None, request.FILES or None,
#         instance=knowlege_document.get(KnowledgeCode=id))

#         if knowledge_document_form.is_valid():
#             knowledge_document_form.save()
#             return HttpResponseRedirect('/KnowledgeList/2')
#         else:
#             conetxt.update({'errors': str(knowledge_document_form.errors)})

#     else:
#         if not knowlege_document.filter(KnowledgeCode=id).exists():
#             knowledge_document_form = TblKnowledgeDocumentsForm()
#         else:
#             knowledge_document_form = TblKnowledgeDocumentsForm(request.POST or None, request.FILES or None,
#             instance=knowlege_document.get(KnowledgeCode=id))


#     conetxt.update(
#         {'KnowledgeCode': id, 'KnowledgeDocumentForm': knowledge_document_form})
#     return render(
#         request,
#         'KnowledgeDocuments.html',
#         conetxt
#     )


@login_required
def like_view(request):
    Tbl_like = like.objects.all()
    knowledge = TblKnowledge.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        if Tbl_like.filter(post=post_id, user=request.user.member).exists():
            Tbl_like.filter(post=post_id, user=request.user.member).delete()
            knowledge = knowledge.get(KnowledgeCode=post_id)
            knowledge.liked_count -= 1
            result = knowledge.liked_count
            color = 'blue'
            knowledge.save()
        else:
            obj = like()
            obj.user = request.user
            knowledge1 = knowledge.get(KnowledgeCode=post_id)
            obj.post = knowledge1
            obj.save()
            knowledge = knowledge.get(KnowledgeCode=post_id)
            knowledge.liked_count += 1
            result = knowledge.liked_count
            color = 'red'
            knowledge.save()

        return JsonResponse({'result': result, 'color': color})

@login_required
def knowledgeRequest_view(request):
    members = Members.objects.all().exclude(member = request.user.member)
    get_topic1 = topic1.objects.filter(status=1)
    html_chart = create_chart_tree(None)
    if request.method == "POST":
        mozo3=request.POST.get('mozo3')
        form=TblKnowledgeRequestForm(request.POST)
        if form.is_valid():
            obj_knowledge_request = form.save()
            obj_knowledge_request.CreatorUserID = request.user
            
            if mozo3 is not None:
                obj_knowledge_request.mozo3_id=topic3.objects.get(id=mozo3)
                
            
            # checks if the user send the knowledge request for all users
            # then create notif for all users
            if obj_knowledge_request.send_to_all:
                    items = [
                    TblKnowledgeRequestNotification(user= member , notif = obj_knowledge_request , url='knowledgeSentForum/{}'.format(obj_knowledge_request.id))
                    for member in members
                    ]

                    TblKnowledgeRequestNotification.objects.bulk_create(items)


            # creates notif for specific members of this knowledge request chart
            else:
                # creates a list of users in this knowledge request chart
                userslist_knowledge_request_chart = MemberChart.objects.filter(chart = obj_knowledge_request.KnowledgeProcess ).exclude( member = request.user ).values_list('member', flat=True)

                members = Members.objects.filter( member__in = userslist_knowledge_request_chart )

                items = [
                TblKnowledgeRequestNotification(user= member , notif = obj_knowledge_request , url='knowledgeSentForum/{}'.format(obj_knowledge_request.id))
                for member in members
                ]

                TblKnowledgeRequestNotification.objects.bulk_create(items)

                

            obj_knowledge_request.save()

            return HttpResponseRedirect('/knowledgeSentForum/'+str(obj_knowledge_request.id))
        else:
            pass
 
    KnowledgeRequest_form = TblKnowledgeRequestForm()
    conetxt ={
    'Title' : 'درخواست دانش',
    'html_chart': html_chart,
    'KnowledgeRequest_form': KnowledgeRequest_form,
    'get_topic1':get_topic1,
    }
    return render(request, 'RegisterKnowledgeRequest.html', conetxt)

@login_required
def knowledgeRecive_view(request):
    today_date = get_persian_date_normalized()
    get_memberchart = MemberChart.objects.values_list('chart', flat=True).filter(member=request.user)
    knowledge_requests_recieves = TblKnowledgeRequest.objects.filter(Status=1).filter( Q(send_to_all=True) | Q(KnowledgeProcess__in=get_memberchart) ).filter(KnowledgeExpireDate__gte=today_date)
    context = {
        'knowledge_requests_recieves':knowledge_requests_recieves,
        'Title':'لیست دریافتی دانش های من ',
    }

    return render(request,'KnowledgeReciveMessage.html',context)

@login_required
def knowledgeSent_view(request):

    my_questions = TblKnowledgeRequest.objects.filter(CreatorUserID=request.user)

    context = {
        'my_questions' : my_questions,
        'Title':'لیست درخواست دانش های من'
    }

    return render(request,'My_sentKnowledge_list.html',context)


@login_required
def knowledge_sent_forum(request,id):

    # deletes the notif knowledge request for this user
    if TblKnowledgeRequestNotification.objects.filter( user = request.user ).filter( notif__id = id ).exists():
        TblKnowledgeRequestNotification.objects.get( notif__id = id , user = request.user ).delete()

    Tbl_vote = TblVoteQuestionAnswer.objects.all()
    knowledge_request_obj = TblKnowledgeRequest.objects.get(id=id)
    answer_objects = TblAnswerKnowledgeRequest.objects.filter(knowledge_request=knowledge_request_obj)

    if request.method == "POST":
        form=TblAnswerKnowledgeRequestForm(request.POST)
        if form.is_valid():
            obj_answer = form.save()
            obj_answer.CreatorUserID = request.user
            obj_answer.knowledge_request = TblKnowledgeRequest.objects.get(id=id)
            obj_answer.save()

    answer_objects_dict = dict()
    # count the votes of an answer and put them into a dictionary
    for answer_object in answer_objects:
        up_vote = len(Tbl_vote.filter(knowledge_request_answer=answer_object,vote_status=1))
        down_vote= len(Tbl_vote.filter(knowledge_request_answer=answer_object,vote_status=2))
        result = up_vote-down_vote
        answer_objects_dict[answer_object] = result

    # this sorts the dict based on vale(from low to high)    
    sorted_answer_objects_dict={k: v for k, v in sorted(answer_objects_dict.items(), key=lambda item: item[1])}
    # takes the sorted values reverse them and put them in a list 
    answer_objects = list(sorted_answer_objects_dict.keys())[::-1]



    form = TblAnswerKnowledgeRequestForm()
    context={
        'question':knowledge_request_obj,
        'form':form,
        'answer_objects':answer_objects,
    }

    return render(request,'knowledgeSentForum.html',context)


@login_required
def QuestionSentForum(request,id):

    # deletes  notif question request for this user
    if TblQuestionRequestNotification.objects.filter( user = request.user ).filter( notif__id = id ).exists():
        TblQuestionRequestNotification.objects.get( notif__id = id , user = request.user ).delete()

    Tbl_vote = TblVotesForQuestionAnswer.objects.all()
    knowledge_request_obj = TblQuestionRequest.objects.get(id=id)
    answer_objects = TblAnswerQuestionRequest.objects.filter(knowledge_request=knowledge_request_obj)

    if request.method == "POST":
        form=TblAnswerQuestionRequestForm(request.POST)
        if form.is_valid():
            obj_answer = form.save()
            obj_answer.CreatorUserID = request.user
            obj_answer.knowledge_request = TblQuestionRequest.objects.get(id=id)
            obj_answer.save()

    answer_objects_dict = dict()
    # count the votes of an answer and put them into a dictionary
    for answer_object in answer_objects:
        up_vote = len(Tbl_vote.filter(knowledge_request_answer=answer_object,vote_status=1))
        down_vote= len(Tbl_vote.filter(knowledge_request_answer=answer_object,vote_status=2))
        result = up_vote-down_vote
        answer_objects_dict[answer_object] = result

    # this sorts the dict based on vale(from low to high)    
    sorted_answer_objects_dict={k: v for k, v in sorted(answer_objects_dict.items(), key=lambda item: item[1])}
    # takes the sorted values reverse them and put them in a list 
    answer_objects = list(sorted_answer_objects_dict.keys())[::-1]


    form = TblAnswerQuestionRequestForm()
    context={
        'question':knowledge_request_obj,
        'form':form,
        'answer_objects':answer_objects,
    }

    return render(request,'QuestionSentForum.html',context)

@login_required
def remove_file_view(request):
    """Ajax func for removing zamaem from register experience"""
    Tbl_feed_file = FeedFile.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if Tbl_feed_file.filter(id=file_id).exists():
            obj_path=Tbl_feed_file.get(id=file_id).file.path
            Tbl_feed_file.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})



@login_required
def remove_docFile_view(request):
    """Ajax func for removing zamaem from documentation"""
    Tbl_feed_file = FeedFileDocumentation.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if Tbl_feed_file.filter(id=file_id).exists():
            obj_path=Tbl_feed_file.get(id=file_id).file.path
            Tbl_feed_file.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def edu_records_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    edu_records_files = edu_records.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if edu_records_files.filter(id=file_id).exists():
            obj_path=edu_records_files.get(id=file_id).file_edu_records.path
            edu_records_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def job_record_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    job_record_files = job_record.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if job_record_files.filter(id=file_id).exists():
            obj_path=job_record_files.get(id=file_id).job_record_file.path
            job_record_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})

@login_required
def skills_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    skills_files = skills.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if skills_files.filter(id=file_id).exists():
            obj_path=skills_files.get(id=file_id).skills_file.path
            skills_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})

@login_required
def articles_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    articles_files = articles.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if articles_files.filter(id=file_id).exists():
            obj_path=articles_files.get(id=file_id).articles_file.path
            articles_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def books_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    books_files = books.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if books_files.filter(id=file_id).exists():
            obj_path=books_files.get(id=file_id).books_file.path
            books_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def inventions_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    inventions_files = inventions.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if inventions_files.filter(id=file_id).exists():
            obj_path=inventions_files.get(id=file_id).inventions_file.path
            inventions_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def passed_trials_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    passed_trials_files = passed_trials.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if passed_trials_files.filter(id=file_id).exists():
            obj_path=passed_trials_files.get(id=file_id).passed_trials_file.path
            passed_trials_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def pro_degree_docs(request):
    """Ajax func for removing and editing docs from Profile"""
    pro_degree_files = pro_degree.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if pro_degree_files.filter(id=file_id).exists():
            obj_path=pro_degree_files.get(id=file_id).degree_file.path
            pro_degree_files.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})

@login_required
def security(request):

    members = Members.objects.all()
    knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9) | Q(register_status=8)).filter(Status = 1)
    context = dict(set_contex(request.user))
    if request.method == "POST":
        user_name_registered = request.POST.get('members')
        from_date = request.POST.get('from_date3')
        to_date = request.POST.get('to_date3')
        SearchTitle = request.POST.get('SearchTitle')
        SearchKeyword = request.POST.getlist('SearchKeyword')
        security_type = request.POST.get('security_type')
        

        if security_type != "" and security_type is not None:

            knowledges = knowledges.filter(register_status=security_type)
    
        knowledges = knowledge_advance_search(knowledges , from_date , to_date , search_keyword=SearchKeyword,search_title= SearchTitle , creator_user=user_name_registered)

    context.update({
        'Knowledges' : knowledges,
        'security_type':1,
        'members' : members,
        'Title': 'حراست',
    })
    return render(request,'security.html',context)


@login_required
def rejected_security(request,id):

    rejected = TblKnowledge.objects.get(KnowledgeCode=id)
    rejected.register_status=8
    rejected.save()

    obj_knowledge = TblKnowledge.objects.get( KnowledgeCode = id)
    
    #creates notif for owner and notifies him that the knowledge is rejected by security
    TblKnowledgeStatusNotification.objects.create( notif = obj_knowledge , url = 'KnowledgeView/'+str(obj_knowledge.KnowledgeCode), notif_type = 15 )

    #calculate the score of the knowledge owner
    obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
    knowledge_owner.score = score_calculator(knowledge_owner)
    knowledge_owner.save()


    return HttpResponseRedirect('/security/')

@login_required
def accepted_by_security(request,id):

    rejected = TblKnowledge.objects.get(KnowledgeCode=id)
    rejected.register_status=9
    rejected.save()

    obj_knowledge = TblKnowledge.objects.get( KnowledgeCode = id)

    #creates notif for owner and notifies him that the knowledge is now accepted by security
    TblKnowledgeStatusNotification.objects.create( notif = obj_knowledge , url = 'KnowledgeView/'+str(obj_knowledge.KnowledgeCode), notif_type = 14 )

    #calculate the score of the knowledge owner
    obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=id)
    knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
    knowledge_owner.score = score_calculator(knowledge_owner)
    knowledge_owner.save()

    return HttpResponseRedirect('/security/')


@login_required
def thinking_room(request):

    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')
    html_chart = create_chart_tree(None)
    context = dict(set_contex(request.user))
    memebers = Members.objects.all()
    memebers_to_save = request.POST.getlist('member')
    join_percentage=request.POST.getlist('percentageJoin')

    if request.method == "POST":
       audio_name = request.POST.get('hidden_audio')
       audio = audio_name + ".mp3"
       doc_files_title = request.POST.getlist('docTitle')
       doc_files=request.FILES.getlist('Allfiles')
       form=TblJalaseForm(request.POST, request.FILES)
       if form.is_valid():
           if len(join_percentage) > 1:
                if all(flag.isdigit() for  flag in join_percentage):
                    join_percentage=list(map(int, join_percentage))
                else:
                    join_percentage=[0]
           obj = form.save()
           obj.voice_url = audio
           obj.save()
           if len(doc_files) !=0 and len(doc_files_title) !=0 and len (doc_files) == len(doc_files_title) :
               for itemFile,itemTitle in zip(doc_files,doc_files_title):
                   obj_file_doc=FeedFile_Jalase()
                   obj_file_doc.file=itemFile
                   obj_file_doc.title=itemTitle
                   obj_file_doc.feed=TblJalase.objects.get(JalaseCode=obj.JalaseCode)
                   obj_file_doc.save()
           if len(join_percentage) > 1 and sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
               for item,percentage in zip(memebers_to_save,join_percentage):
                   obj_Team = TblTeam_Jalase()
                   obj_Team.joinPercentage=percentage
                   obj_Team.JalaseCode = obj
                   obj_Team.TeamMember = Members.objects.get(member=item)
                   obj_Team.save()


       return HttpResponseRedirect('/thinking_room')
    context = {
        'members': memebers,
        'html_chart' : html_chart,
        'TblJalaseForm' : TblJalaseForm,
        'teamCount': 1,

    }

    return render(request,'thinking_room.html',context)



@login_required
def thinking_room_paperwork(request,id):

    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')

    Jalase = TblJalase.objects.get(JalaseCode=id)

    Jalase_owner = Members.objects.get(member=Jalase.CreatorUserID.member)
    team = TblTeam_Jalase.objects.filter(JalaseCode=id).exclude(TeamMember=Jalase_owner)
    if TblTeam_Jalase.objects.filter(JalaseCode=id,TeamMember=request.user.member).exists():
        userPercentage = TblTeam_Jalase.objects.get(JalaseCode=id,TeamMember=request.user.member)
        userPercentage=userPercentage.joinPercentage
    else:
        userPercentage=-1

    obj_files=FeedFile_Jalase.objects.filter(feed=id) 
    if len(obj_files) ==0:
        len_files=0
    else:
        len_files=1

    voice = 0 
    
    voice_name = Jalase.voice_url
    if voice_name != None and voice_name != '.mp3':

        voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        
    context = {
        'Jalase': Jalase,
        'Title': 'کاربرگ',
        'userPercentage':userPercentage,
        'team':team,
        'voice' : voice ,
        'Jalase_owner' : Jalase_owner,
        'obj_files':obj_files,
        'len_files':len_files
    }
    return render(request, "thinking_room_paperwork.html", context)



@login_required
def thinking_room_list(request):

    jalase_items_list = TblJalase.objects.filter(Status__gte = 0,jalase_status__gte = 0)

    context = {
        'jalase_items_list' : jalase_items_list,
        'Title' : 'لیست جلسه های من  '
    }
    return render(request,'thinking_room_list.html',context)


@login_required
def delete_thinking_room_record(request,id):

    if not is_expert(request.user):
        return HttpResponseRedirect('/login')

    jalase = TblJalase.objects.get(JalaseCode=id)
    jalase.Status=-1
    jalase.save()
    return HttpResponseRedirect('/thinking_room_list/')


@login_required
def survey_generator(request):
    if request.method == "POST":
        form = TblSurveyForm(request.POST)
        options = request.POST.getlist('option')

        if form.is_valid():
            obj=form.save()
            obj.creator=request.user
            obj.save()

            for option in options:
                tbl_suervey_option = TblSuerveyOptions()
                tbl_suervey_option.survey_id = obj
                tbl_suervey_option.option_text = option
                tbl_suervey_option.option_number=options.index(option)+1
                tbl_suervey_option.save()


            return HttpResponseRedirect("/survey_list")

    tbl_survey_form=TblSurveyForm()
    context={
        'TblSurveyForm':tbl_survey_form,
    }
    return render(request, 'survey_generator.html', context)


@login_required
def edit_survey(request,id):
    survey_obj = TblSuervey.objects.get(id=id)
    form = TblSurveyForm(request.POST or None , instance = survey_obj)
    servey_options = TblSuerveyOptions.objects.filter(survey_id = survey_obj)
    if request.method == "POST":
        options = request.POST.getlist('option')

        if form.is_valid():
            obj=form.save()
            obj.creator=request.user
            obj.save()

            #deletes the user answers to enable editing 
            if TblAnswerOptionSurvey.objects.filter(suervey = survey_obj ).exists():
                TblAnswerOptionSurvey.objects.filter(suervey = survey_obj).delete()

            servey_options.delete()
            for option in options:
                tbl_suervey_option = TblSuerveyOptions()
                tbl_suervey_option.survey_id = obj
                tbl_suervey_option.option_text = option
                tbl_suervey_option.option_number=options.index(option)+1
                tbl_suervey_option.save()


            return HttpResponseRedirect("/survey_list")

    context={
        'TblSurveyForm':form,
        'servey_options':servey_options,
    }
    return render(request, 'survey_generator.html', context)



@login_required
def survey_list(request):
    this_user_surveys = TblSuervey.objects.filter(creator = request.user).filter(Status = 1)


    context={
        'surveys':this_user_surveys,

    }
    return render(request, 'survey_list.html', context)


@login_required
def delete_survey(request,id):
    this_user_survey = TblSuervey.objects.get(id=id)
    if request.user == this_user_survey.creator:
        try:
            this_user_survey.delete()
        except:
            this_user_survey.Status = -1
            this_user_survey.save()

        # deletes the exams that are sent to users
        if SendSurvey2Member.objects.filter(survey = this_user_survey).exists():
            SendSurvey2Member.objects.filter(survey = this_user_survey).delete()

        # deletes the user answers
        if TblAnswerOptionSurvey.objects.filter(suervey = this_user_survey).exists():
            TblAnswerOptionSurvey.objects.filter(suervey = this_user_survey).delete()





    return HttpResponseRedirect('/survey_list')


@login_required
def send_survey(request,id):
    this_user_survey = TblSuervey.objects.get(id=id)
    memebers = Members.objects.all()
    if request.method == "POST":
        # send to all = 1 means True #send to all = 2 means false
        send_to_all = request.POST.get('send_to_all')
        memebers_to_save = request.POST.getlist('member')
        if send_to_all == '2':
            if len(memebers_to_save) >1:
                for item in memebers_to_save:
                    if int(item) != request.user.member:
                        obj_SendSurvey2Member = SendSurvey2Member()
                        obj_SendSurvey2Member.survey = this_user_survey
                        obj_SendSurvey2Member.member = Members.objects.get(member=item)
                        obj_SendSurvey2Member.save() 
                notif_to_users = Members.objects.filter(member__in=memebers_to_save).exclude(member=request.user.member)
                this_user_survey.send_status=1
                this_user_survey.save()
                items = [
                TblSurveyotification(user=member , notif=this_user_survey , url='take_survey/{}'.format(id))
                for member in notif_to_users
                ]

                TblSurveyotification.objects.bulk_create(items)
                return HttpResponseRedirect("/survey_list")

            else:
                conetxt = {
                    'members': memebers,
                    'Title': ' ارسال نظر سنجی ',
                    'error':'حداقل یک کاربر را انتخاب نمایید!',
                    }
                return render(request, 'send_test.html', conetxt)

        else:
            this_user_survey.sent_to_all =True
            this_user_survey.send_status=1
            this_user_survey.save()
            items = [
            TblSurveyotification(user=member , notif=this_user_survey , url='take_survey/{}'.format(id))
            for member in memebers.exclude(member=request.user.member)
            ]

            TblSurveyotification.objects.bulk_create(items)
            return HttpResponseRedirect("/survey_list")

    
    conetxt = {
        'members': memebers,
        'Title': ' ارسال نظر سنجی ',
        }
    return render(request, 'send_test.html', conetxt)


@login_required
def survey_result(request,id):
    this_user_survey = TblSuervey.objects.get(id=id)
    this_survey_options = TblSuerveyOptions.objects.filter(survey_id=this_user_survey)
    answers_number = len(TblAnswerOptionSurvey.objects.filter(suervey = this_user_survey))
    conetxt = {
        'options': this_survey_options,
        'survey': this_user_survey,
        'answers_number':answers_number,
        }

    return render(request, 'survey_result.html', conetxt)



@login_required
def test_generator(request):
    if request.method == "POST":
        form = TblExamForm(request.POST, request.FILES or None)
        if form.is_valid():
            obj=form.save()
            obj.creator=request.user
            obj.save()
            return HttpResponseRedirect("/test_list")

    tbl_exam_form=TblExamForm()
    context={
        'TblExamForm':tbl_exam_form,
    }
    return render(request, 'test_generator.html', context)


@login_required
def my_surveys(request):

    today_date = get_persian_date_normalized()

    time_now=datetime.datetime.now().time()


    this_user_answers_for_Surveys = set(TblAnswerOptionSurvey.objects.filter(member_id = request.user).values_list('suervey', flat=True))

    this_user_surveys_recieved = SendSurvey2Member.objects.filter(member = request.user).values_list('survey', flat=True)
    this_user_surveys = TblSuervey.objects.filter(id__in= this_user_surveys_recieved).filter(Status =1).filter(Q(to_date__gt = today_date) | Q(to_date = today_date , to_hour__gt =time_now ,from_hour__lt=time_now )).exclude(id__in =list(this_user_answers_for_Surveys))

    all_user_surveys = TblSuervey.objects.filter(sent_to_all = True).filter(Status =1).filter(Q(to_date__gt = today_date) | Q(to_date = today_date , to_hour__gt =time_now ,from_hour__lt=time_now )).exclude(id__in =list(this_user_answers_for_Surveys))

    surveys = this_user_surveys | all_user_surveys

    context={
        'surveys':surveys,
        'mySurvey':'1',

    }

    return render(request, 'survey_list.html',context)

@login_required
def pros_and_cons(request):

    conetxt = dict(set_contex(request.user))

    status_determiner=request.POST.get('registerDeterminer')

    memebers = Members.objects.all()

    file_form = FileModelForm()
    conetxt.update({
        'teamCount': 1,
        'Title': '  انتقادات و پیشنهادات',
        'knowledgeType': 1,
        'members': memebers,
        'FileModelForm':file_form
    })

    if request.method == "POST":
        doc_files_title = request.POST.getlist('docTitle')
        doc_files=request.FILES.getlist('Allfiles')
        user_key_words = []
        form = TblKnowledgeForm(request.POST, request.FILES)

        if form.is_valid():
            try:                       
                memebers_to_save = request.POST.getlist('member')
                join_percentage=request.POST.getlist('percentageJoin')
                if len(join_percentage) > 1:
                    if all(flag.isdigit() for  flag in join_percentage):
                        join_percentage=list(map(int, join_percentage))
                    else:
                        join_percentage=[0]
                if form.cleaned_data['KnowledgeKeywords'] is not None:
                    keywords = form.data['KnowledgeKeywords']
                    keywords = keywords.strip()
                else:
                    keywords=''
                obj = form.save()
                if request.user.Status == 2:
                    obj.Status_who_registered=2
                    obj.save()

                if int(status_determiner) == 2:
                    obj.register_status=3
                    obj.save()
                if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                    for itemFile,itemTitle in zip(doc_files,doc_files_title):
                        obj_file_doc=FeedFile()
                        obj_file_doc.file=itemFile
                        obj_file_doc.title=itemTitle
                        obj_file_doc.feed=TblKnowledge.objects.get(KnowledgeCode=obj.KnowledgeCode)
                        obj_file_doc.save()

                if len(join_percentage) > 1:
                    if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                        for item,percentage in zip(memebers_to_save,join_percentage):
                            obj_Team = TblTeam()
                            obj_Team.joinPercentage=percentage
                            obj_Team.KnowledgeCode = obj
                            obj_Team.TeamMember = Members.objects.get(member=item)
                            obj_Team.save()
                    else:
                        conetxt.update({
                        'KnowledgeForm': form,
                        'errors': 'درصد چه کسی درست نیست',
                        })
                        return render(request, 'pros_and_cons.html', conetxt)

                if keywords !='':
                    splited_keywords = keywords.split(",")
                    for keyword in splited_keywords:
                        obj_keyword = TblKeywords()
                        obj_keyword.KeywordsText = keyword
                        obj_keyword.Knowledge = obj
                        obj_keyword.save()
                        user_key_words.append(obj_keyword)

                return HttpResponseRedirect('/KnowledgeList/1')
            except:
                conetxt.update({
                    'KnowledgeForm': form,
                    'errors': str(form.errors),
                })
                return render(request, 'pros_and_cons.html', conetxt)
        else:
            pass
    else:
        knowledge_form = TblKnowledgeForm()
        conetxt.update({
            'KnowledgeForm': knowledge_form,
        })
        return render(request, 'pros_and_cons.html', conetxt)

@login_required
def polls(request):
    conetxt = dict(set_contex(request.user))

    status_determiner=request.POST.get('registerDeterminer')

    memebers = Members.objects.all()

    file_form = FileModelForm()
    conetxt.update({
        'teamCount': 1,
        'Title': '  نظرنجی و پرسشنامه',
        'knowledgeType': 1,
        'members': memebers,
        'FileModelForm':file_form
    })

    if request.method == "POST":
        doc_files_title = request.POST.getlist('docTitle')
        doc_files=request.FILES.getlist('Allfiles')
        user_key_words = []
        form = TblKnowledgeForm(request.POST, request.FILES)

        if form.is_valid():
            try:                       
                memebers_to_save = request.POST.getlist('member')
                join_percentage=request.POST.getlist('percentageJoin')
                if len(join_percentage) > 1:
                    if all(flag.isdigit() for  flag in join_percentage):
                        join_percentage=list(map(int, join_percentage))
                    else:
                        join_percentage=[0]
                if form.cleaned_data['KnowledgeKeywords'] is not None:
                    keywords = form.data['KnowledgeKeywords']
                    keywords = keywords.strip()
                else:
                    keywords=''
                obj = form.save()
                if request.user.Status == 2:
                    obj.Status_who_registered=2
                    obj.save()

                if int(status_determiner) == 2:
                    obj.register_status=3
                    obj.save()
                if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                    for itemFile,itemTitle in zip(doc_files,doc_files_title):
                        obj_file_doc=FeedFile()
                        obj_file_doc.file=itemFile
                        obj_file_doc.title=itemTitle
                        obj_file_doc.feed=TblKnowledge.objects.get(KnowledgeCode=obj.KnowledgeCode)
                        obj_file_doc.save()

                if len(join_percentage) > 1:
                    if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                        for item,percentage in zip(memebers_to_save,join_percentage):
                            obj_Team = TblTeam()
                            obj_Team.joinPercentage=percentage
                            obj_Team.KnowledgeCode = obj
                            obj_Team.TeamMember = Members.objects.get(member=item)
                            obj_Team.save()
                    else:
                        conetxt.update({
                        'KnowledgeForm': form,
                        'errors': 'درصد چه کسی درست نیست',
                        })
                        return render(request, 'polls.html', conetxt)

                if keywords !='':
                    splited_keywords = keywords.split(",")
                    for keyword in splited_keywords:
                        obj_keyword = TblKeywords()
                        obj_keyword.KeywordsText = keyword
                        obj_keyword.Knowledge = obj
                        obj_keyword.save()
                        user_key_words.append(obj_keyword)

                return HttpResponseRedirect('/KnowledgeList/1')
            except:
                conetxt.update({
                    'KnowledgeForm': form,
                    'errors': str(form.errors),
                })
                return render(request, 'polls.html', conetxt)
        else:
            pass
    else:
        knowledge_form = TblKnowledgeForm()
        conetxt.update({
            'KnowledgeForm': knowledge_form,
        })
        return render(request, 'polls.html', conetxt)

@login_required
def Key_indicators(request):

    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    today_date = get_persian_date_normalized()

    if request.method == "POST":
        key_indicator_text = request.POST.get('key_indicator_text')
        from_range = request.POST.get('from_range')
        to_range = request.POST.get('to_range')
        expire_date = request.POST.get('expire_date')

        if int(expire_date) > today_date :
            TblKeyIndicator.objects.create(key_indicator=key_indicator_text , from_range = from_range , to_range = to_range , expire_date = expire_date)
            
            return HttpResponseRedirect('/Key_indicators_list')
        
        return render(request, 'Key_indicators.html')  
             
    else:
        context = {
        'Title' : 'تعریف شاخص های  کلیدی',
    }
        return render(request, 'Key_indicators.html', context)



@login_required
def edit_Key_indicators(request,id):

    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')
    today_date = get_persian_date_normalized()

    obj_indicator = get_object_or_404(TblKeyIndicator, id=id)
    key_indicator_text = obj_indicator.key_indicator
    from_range = obj_indicator.from_range
    to_range = obj_indicator.to_range
    expire_date = obj_indicator.expire_date
    if request.method == "POST":
        key_indicator_text = request.POST.get('key_indicator_text')
        from_range = request.POST.get('from_range')
        to_range = request.POST.get('to_range')
        expire_date = request.POST.get('expire_date')

        if int(expire_date) > today_date :

            TblKeyIndicator.objects.filter(id=id).update(key_indicator=key_indicator_text , from_range = from_range , to_range = to_range , expire_date = expire_date)
            return HttpResponseRedirect('/Key_indicators_list')
        
        return render(request, 'Key_indicators.html')

    else :

        context = {
            'key_indicator_text' : key_indicator_text ,
            'from_range' : from_range ,
            'to_range' : to_range ,
            'expire_date' : expire_date ,
        }
        return render(request, 'Key_indicators.html', context)


@login_required
def delete_Key_indicators(request,id):

    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    indicator_key = TblKeyIndicator.objects.get(id=id)
    indicator_key.status = 0
    indicator_key.save()
    return HttpResponseRedirect('/Key_indicators_list')


@login_required
def Key_indicators_list(request):

    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')

    all_active_key_indicators = TblKeyIndicator.objects.filter(status = 1)

    context = {
        'Title' : 'لیست شاخص های  کلیدی',
        'indicator' : all_active_key_indicators ,
    }

    return render(request,'Key_indicators_list.html',context)


@login_required
def indicator_assessment(request):
    
    form = indicator_assessmentForm()
    if request.method == "POST":
        form = indicator_assessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/indicator_assessment_list')
        else:
            context = {
                'error' : 'بارم شاخص نمیتواند بیش از 10 باشد'
            }
            return render(request, 'indicator_assessment.html', context)
    context = {
        'form' : form,
    }
    
    return render(request, 'indicator_assessment.html', context)

@login_required
def delete_indicator(request,id):

    indicator = indicator_assessment_model.objects.get(id=id)
    indicator.Status=-1
    indicator.save()
    return HttpResponseRedirect('/indicator_assessment_list/')


@login_required
def calculate_valuable_knowledge_list(request):
    today_date = str(get_persian_date_normalized())
    
    knowledges = TblKnowledge.objects.filter(Status__gte=0).filter(Q(register_status=7) | Q(register_status=9)).raw('''
    select * from KnowledgeManagement_tblknowledge
    where ( %s - CreateDate) >=10000
    ''',[today_date])

    context = {
        'knowledges':knowledges
    }

    return render(request, 'calculate_valuable_knowledge.html', context)

@login_required
def calculate_valuable_knowledge(request,id):
    knowledge = TblKnowledge.objects.get(KnowledgeCode = id )

    if TblKnowledgeValueIT.objects.filter(knowledge = knowledge ).exists():
        knowledge_value_it_obj = TblKnowledgeValueIT.objects.get(knowledge = knowledge)
        form = TblKnowledgeValueITForm(request.POST or None , instance = knowledge_value_it_obj)
    else:
        form = TblKnowledgeValueITForm(request.POST or None )
    

    if request.method == "POST":
        if form.is_valid():
            obj = form.save()
            obj.knowledge = knowledge
            Rvariable = (obj.profit_after - obj.profit_before) / obj.knowledge_cost
            Rvariable = round(Rvariable, 4)
            knowledge.R = Rvariable
            knowledge.save()
            obj.save()
            return HttpResponseRedirect('/calculate_valuable_knowledge/')



    context = {
        'knowledge':knowledge,
        'form':form,
    }

    return render(request, 'calculate_valuable_knowledge_list.html', context)

@login_required
def describe_experts(request):
    if not is_IT(request.user):
        return HttpResponseRedirect('/login')

    html_chart = create_chart_tree(None)
    users=Members.objects.all()

    if request.method == "POST":

        #gives the member the Expert Role.
        selected_user = request.POST.get('members')
        expert_group = Group.objects.get(name='Expert') 
        expert_group.user_set.add(selected_user)


        ExpertChart.objects.filter(member = Members.objects.get(member = selected_user)).delete()

        #gives the member the chosen charts.
        charts = request.POST.getlist('chart')

        # this means that all the specialty of the users are removed so he/she is not expert any more
        if len(charts) == 0:
            expert_group.user_set.remove(selected_user)

        for chart in charts:
            #checks if the member had the chart before or not
            if len(ExpertChart.objects.filter(member = Members.objects.get(member = selected_user)).filter(chart=TblChart.objects.get(Chart=chart))) == 0:
                obj_expert_chart = ExpertChart()
                obj_expert_chart.member=Members.objects.get(member=selected_user)
                obj_expert_chart.chart=TblChart.objects.get(Chart=chart)
                obj_expert_chart.save()

        return HttpResponseRedirect(reverse('home'))

    context={
        'members':users,
        'html_chart': html_chart,
    }

    return render(request, 'describe_experts.html', context)

@login_required
def get_expert_areas(request):
    if not is_IT(request.user):
        return HttpResponseRedirect('/login')

    user_id = request.POST['user_id']

    this_user_charts = ExpertChart.objects.filter(member = Members.objects.get(member = user_id))


    json = "["
    for chart in this_user_charts:
        if len(json) > 1:
            json += ","
        json += "{\"id\":\"" + str(chart.chart.Chart) + \
                "\", \"text\":\"" + chart.chart.ChartText + "\"}"
    json += "]"

    return JsonResponse(json,safe=False)

@login_required
def sorting_knowledge(request):

    get_topic1 = topic1.objects.filter(status=1)

    knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9) | Q(register_status=8))

    if request.method == 'POST':
        mozo3 = request.POST.get('mozo3')
        mozo3_chekbox = request.POST.get('mozo3_chekbox')
        mozo2 = request.POST.get('mozo2')
        mozo2_chekbox = request.POST.get('mozo2_chekbox')
        mozo1 = request.POST.get('mozo1')
        mozo1_chekbox = request.POST.get('mozo1_chekbox')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        if mozo3 is not None and mozo3_chekbox:
            topic3_knowledges_list = send_to_evaluator.objects.values_list('knowledge', flat=True).filter(mozo3_id=topic3.objects.get(id=mozo3))
            knowledges = knowledges.filter(KnowledgeCode__in=topic3_knowledges_list)

        elif mozo2 is not None and mozo2_chekbox:
            topic2_knowledges_list = send_to_evaluator.objects.values_list('knowledge', flat=True).filter(mozo2_id=topic2.objects.get(id=mozo2))
            knowledges = knowledges.filter(KnowledgeCode__in=topic2_knowledges_list)

        elif mozo1 != '' and mozo1 != '-1' and mozo1_chekbox :
            topic1_knowledges_list = send_to_evaluator.objects.values_list('knowledge', flat=True).filter(mozo1_id=topic1.objects.get(id=mozo1))
            knowledges = knowledges.filter(KnowledgeCode__in=topic1_knowledges_list)

        if from_date and to_date:
                from_date = int(''.join(from_date.split('/')))
                to_date = int(''.join(to_date.split('/')))
                knowledges = knowledges.filter(
                    CreateDate__gte=from_date,
                    CreateDate__lte=to_date)

        if to_date == "" and not from_date == "":
                from_date = int(''.join(from_date.split('/')))
                knowledges = knowledges.filter(CreateDate__gte=from_date)

        if from_date == "" and not to_date == "":
                to_date = int(''.join(to_date.split('/')))
                knowledges = knowledges.filter(CreateDate__lte=to_date)


    context = {
        'get_topic1' : get_topic1,
        'knowledges' : knowledges,

    }
    return render(request, 'sorting_knowledge.html',context) 


@login_required
def knowledge_review(request,id):

    get_knowledge_review = send_to_evaluator.objects.get(id=id)
    user_review = send_to_evaluator.objects.filter()
    if get_knowledge_review.mozo3_id != None :
        get_topic =  get_knowledge_review.mozo3_id.city
    elif get_knowledge_review.mozo2_id != None :
        get_topic =  get_knowledge_review.mozo2_id.state
    elif get_knowledge_review.mozo1_id != None :
        get_topic =  get_knowledge_review.mozo1_id.mozo1

    
    context = {
        'user_review' : user_review ,
        'get_knowledge_review' : get_knowledge_review,
        'get_topic' : get_topic,
    }
    return render(request,'Knowledge_Review.html',context)


@login_required
def question_request(request):
    members = Members.objects.all().exclude(member = request.user.member)
    get_topic1 = topic1.objects.filter(status=1)
    html_chart = create_chart_tree(None)
    if request.method == "POST":
        mozo3=request.POST.get('mozo3')
        form=TblQuestionRequestForm(request.POST)
        if form.is_valid():
            obj_knowledge_request = form.save()
            obj_knowledge_request.CreatorUserID = request.user

            if mozo3 is not None:
                obj_knowledge_request.mozo3_id=topic3.objects.get(id=mozo3)



            # checks if the user send the knowledge request for all users
            # then create notif for all users
            if obj_knowledge_request.send_to_all:
                    items = [
                    TblQuestionRequestNotification(user= member , notif = obj_knowledge_request , url='QuestionSentForum/{}'.format(obj_knowledge_request.id))
                    for member in members
                    ]

                    TblQuestionRequestNotification.objects.bulk_create(items)


            # creates notif for specific members of this knowledge request chart
            else:
                # creates a list of users in this knowledge request chart
                userslist_knowledge_request_chart = MemberChart.objects.filter(chart = obj_knowledge_request.KnowledgeProcess ).exclude( member = request.user ).values_list('member', flat=True)

                members = Members.objects.filter( member__in = userslist_knowledge_request_chart )

                items = [
                TblQuestionRequestNotification(user= member , notif = obj_knowledge_request , url='QuestionSentForum/{}'.format(obj_knowledge_request.id))
                for member in members
                ]

                TblQuestionRequestNotification.objects.bulk_create(items)

            obj_knowledge_request.save()


            return HttpResponseRedirect('/QuestionSentForum/'+str(obj_knowledge_request.id))
        else:
            pass
 
    KnowledgeRequest_form = TblQuestionRequestForm()
    context ={
    'Title' : 'درخواست سوال',
    'html_chart': html_chart,
    'KnowledgeRequest_form': KnowledgeRequest_form,
    'get_topic1':get_topic1,
    }
    return render(request, 'RegisterKnowledgeRequest.html', context)

@login_required
def question_recive(request):
    today_date = get_persian_date_normalized()
    get_memberchart = MemberChart.objects.values_list('chart', flat=True).filter(member=request.user)
    question_request_recieved = TblQuestionRequest.objects.filter(Status=1).filter( Q(send_to_all=True) | Q(KnowledgeProcess__in=get_memberchart) ).filter(KnowledgeExpireDate__gte=today_date)

    context = {
        'Title' : 'لیست دریافتی سوال',
        'question_request_recieved' : question_request_recieved,
    }
    return render(request,'question_recive.html',context)

@login_required
def question_sent(request):

    question_request_recieved = TblQuestionRequest.objects.filter(CreatorUserID=request.user)

    context = {
        'Title' : 'لیست ارسالی سوال',
        'question_request_recieved' : question_request_recieved,
    }
    return render(request,'question_sent.html',context)

@login_required
def test_list(request):

    exam_list = TblExam.objects.filter(Status__gte=0)

    conetxt = {
            'Title': ' لیست ازمون ها ',
            'ExamList':exam_list,
        }
    return render(request, 'test_list.html', conetxt)

@login_required
def polls_test(request):
    return render(request, 'polls_test.html')

@login_required
def pros_and_cons_test(request):

    return render(request, 'pros_and_cons_test.html')

@login_required
def unconfirmed_knowledge(request):
    if not is_IT(request.user) and not is_expert(request.user):
        return HttpResponseRedirect('/login')
    #this gives the exact id of the item you want(no need to use FOR)
    get_memberchart = ExpertChart.objects.values_list('chart', flat=True).filter(member=request.user)
    #this shows only the knowledges that have register_status = 5 
    #and their chart have the same chart in expertchart
    knowledges = TblKnowledge.objects.filter(register_status=5,KnowledgeProcess__in=get_memberchart).exclude(CreatorUserID = request.user)
    
    context = {
        'knowledges' : knowledges,
        'Title' : 'لیست ارسالی ها از سمت دبیرخانه ی مدیریت دانش'
    }
    return render(request,'unconfirmed_knowledge.html',context)

@login_required
def rate_knowledge(request,id):
    
    indicators = indicator_assessment_model.objects.filter(Status__gte=0)

    obj_knowledge = TblKnowledge.objects.get(KnowledgeCode = id)
    today_date = get_persian_date_normalized()

    KPI_indicators = TblKeyIndicator.objects.filter(expire_date__gte = today_date)

    #expert review for this knowldge 
    expert_review = TblExpertReview.objects.filter(expert = request.user).filter(knowledge=id).filter(Status__gte = 1).filter(set_number = obj_knowledge.set_number)

    saved_scores = 0

    form = TblExpertReviewForm()

    # it means that the user has not given their review yet
    if len(expert_review) == 0:
    
        if request.method == "POST":
            scores=request.POST.getlist('indicatorScore')
            Kpi_size = request.POST.getlist('kpi_percentage')
            kpi_pk = request.POST.getlist('kpi_pk')
            form = TblExpertReviewForm(request.POST)
            if form.is_valid():
                obj_review = form.save()
                obj_review.knowledge =TblKnowledge.objects.get(KnowledgeCode=id)
                obj_review.expert = request.user
                obj_review.set_number = obj_knowledge.set_number
                obj_review.save()
                
                for indicator,score in zip(indicators,scores):
                    expert_assessment = TblExpertReviewIndicatorAssessment()
                    expert_assessment.expert_review = obj_review
                    expert_assessment.indicator_assessment=indicator
                    expert_assessment.score=score
                    expert_assessment.save()

                for kpi_indicator , percent in zip(kpi_pk,Kpi_size):
                    TblKpiExpertReview.objects.create(kpi =TblKeyIndicator.objects.get(id=kpi_indicator) ,expert_review = TblExpertReview.objects.get(knowledge=id) , percent = percent , knowledge = TblKnowledge.objects.get(KnowledgeCode=id) , set_number = obj_knowledge.set_number )

                return HttpResponseRedirect("/knowledge_rate_result/"+str(obj_review.id))


    # it means that the user has given their review and now cand edit it
    else:
        form = TblExpertReviewForm(request.POST or None, instance=expert_review[0])
        saved_scores = TblExpertReviewIndicatorAssessment.objects.filter(expert_review  = expert_review[0]).values_list('score',flat=True)
        if request.method == "POST":
            Kpi_size = request.POST.getlist('kpi_percentage')
            scores=request.POST.getlist('indicatorScore')
            kpi_pk = request.POST.getlist('kpi_pk')
            if form.is_valid():
                obj_review = form.save()
                obj_review.knowledge =TblKnowledge.objects.get(KnowledgeCode=id)
                obj_review.expert = request.user
                obj_review.set_number = obj_knowledge.set_number
                obj_review.save()
                
                TblExpertReviewIndicatorAssessment.objects.filter(expert_review  = obj_review).delete()
                for indicator,score in zip(indicators,scores):
                    expert_assessment = TblExpertReviewIndicatorAssessment()
                    expert_assessment.expert_review = obj_review
                    expert_assessment.indicator_assessment=indicator
                    expert_assessment.score=score
                    expert_assessment.save()

                if TblKpiExpertReview.objects.filter(expert_review__knowledge = id).exists:
                    TblKpiExpertReview.objects.filter(expert_review__knowledge = id).delete()

                    for kpi_indicator , percent in zip(kpi_pk,Kpi_size):
                        TblKpiExpertReview.objects.create(kpi =TblKeyIndicator.objects.get(id=kpi_indicator) ,expert_review = TblExpertReview.objects.get(knowledge=id) , percent = percent )

                return HttpResponseRedirect("/knowledge_rate_result/"+str(obj_review.id))



    context={
        'indicators' : indicators,
        'Title': 'بررسی و نظر',
        'KPI_indicators' : KPI_indicators ,
        'saved_scores':saved_scores,
        'TblExpertReviewForm' : form,
    }
    return render(request,'rate_knowledge.html',context)

@login_required
def knowledge_rate_result(request,id):

    #this user review for this knowledge
    expert_review = TblExpertReview.objects.get(id=id)

    obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=expert_review.knowledge.KnowledgeCode)


    this_knowledge_chart = obj_knowledge.KnowledgeProcess


    # expert members list for this knowledge process
    expert_members = Members.objects.filter(groups__name='Expert').filter(member__in = ExpertChart.objects.filter(chart =this_knowledge_chart).exclude(member = obj_knowledge.CreatorUserID ).values_list('member',flat=True))

    #all reviews for this knowldge 
    expert_reviews = TblExpertReview.objects.filter(knowledge=obj_knowledge).filter(set_number = obj_knowledge.set_number).filter(Status__gte = 1)

    
    this_review_scores = TblExpertReviewIndicatorAssessment.objects.filter(expert_review=expert_review)

    ls_means=[]
    for this_review_score in this_review_scores:
        score = this_review_score.score
        weight = this_review_score.indicator_assessment.indicator_point
        mean = weight * score
        ls_means.append(mean)
    

    total_score = sum(ls_means)/len(ls_means)

    #stores the total score of the user for the experience
    expert_review.score = total_score
    expert_review.save()


    # checks if all experts gave their review
    if len(expert_reviews) == len(expert_members) :

        # gives us the latest scores of experts for this knowledge
        all_experts_scores_this_knowledge = expert_reviews.values_list('score', flat=True)
        all_experts_total_score = sum(all_experts_scores_this_knowledge)/len(all_experts_scores_this_knowledge)

        if all_experts_total_score >= 50:
            obj_knowledge.register_status=7
            obj_knowledge.save()

            register_staus='این تجربه با موفقیت تبدیل به دانش شد'

            kpi_avg = TblKpiExpertReview.objects.filter(knowledge = obj_knowledge).filter(set_number = obj_knowledge.set_number).aggregate(Avg('percent'))
            if kpi_avg['percent__avg'] is not None:
                kpi_avg =round(kpi_avg['percent__avg'], 4)
                obj_knowledge.kpi = kpi_avg
                obj_knowledge.save()

            #creates notif for owner and notifies him that the experience is now knowledge
            TblKnowledgeStatusNotification.objects.create( notif = obj_knowledge , url = 'KnowledgeView/'+str(obj_knowledge.KnowledgeCode), notif_type = 8 )
           
            
            members = Members.objects.filter(groups__name='Security')

            items = [
            TblKnowledgeNotificationForEliteUsers(user= member , notif = obj_knowledge , url='KnowledgeView/{}'.format(obj_knowledge.KnowledgeCode),notif_type=12)
            for member in members
            ]

            TblKnowledgeNotificationForEliteUsers.objects.bulk_create(items)

            #calculate the score of the owner of the knowledge
            knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
            knowledge_owner.score = score_calculator(knowledge_owner)
            knowledge_owner.save()

        else:
            obj_knowledge.register_status=6
            obj_knowledge.save()
            register_staus='این تجربه به دلیل نرسیدن امتیازش به حد نصاب رد شد'

            #creates notif for owner and notifies him that the experience is rejected by experts
            TblKnowledgeStatusNotification.objects.create( notif = obj_knowledge , url = 'EditExperience/'+str(obj_knowledge.KnowledgeCode), notif_type = 9 )

    else:
        register_staus='نظر شما با موفقیت ثبت شد این تجربه در صف بررسی بقیه خبرگان است'
        all_experts_total_score = 0

    context = {
        'total_score':int(total_score),
        'register_staus':register_staus,
        'Title' : 'نتیجه ی ارزیابی تجربه',
        'all_experts_total_score':int(all_experts_total_score),
    }
    return render(request,'knowledge_rate_result.html',context)

@login_required
def system_members(request):
    labels=["خبره","متخصص مدیریت دانش "," دانش کار"]
    data=[]

    data.append(Members.objects.filter(groups__name='Expert').count())

    data.append(Members.objects.filter(groups__name='IT').count())

    data.append(Members.objects.filter(groups__name='KnowlegeWorker').count())

    context={
        'Title': 'تعداد اعضای سیستم',
        'labels': labels,
        'data': data,
    }
    return render(request, 'systemMembers.html',context)

@login_required
def superior_knowledge_workers(request):
    all_members_count = len(Members.objects.all())

    ten_percent_users = int(( all_members_count * 10 ) / 100)
    
    all_users = Members.objects.all().order_by('-score')
    all_users = all_users[:ten_percent_users]

    p = Paginator(all_users, 12)
    page = request.GET.get('page')
    users = p.get_page(page)

    context={
        
        'Title': 'دانش کاران نمونه',
        'users':users,
    }

    return render(request,'superior_knowledge_workers.html',context)

@login_required
def special_knowledgeWorkers(request):

    all_users =  Members.objects.all()
    knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9),KnowledgeIsSpecial=1,CreatorUserID__in=all_users).values_list('CreatorUserID', flat=True)
    special_users = all_users.filter(member__in=knowledges)
    
    p = Paginator(special_users, 12)
    page = request.GET.get('page')
    users = p.get_page(page)
    context={

        'users' : users,
        'Title': 'دانش کاران ویژه',
    }
    return render(request,'special_knowledgeWorkers.html',context)


@login_required
def system_experts(request):

    expert_users = Members.objects.filter(groups__name='Expert').order_by('date_joined')

    context={

        'Title': '  خبره های سیستم',
        'expertUsers':expert_users,
    }

    return render(request, 'systemExperts.html',context)


@login_required
def system_expert_roles(request,id):

    expert_user = Members.objects.get(member = id)
    expert_user_roles = ExpertChart.objects.filter(member = expert_user)

    user_name = set_contex(expert_user)['UserName']

    context={
        'Title': 'نقش های ' + user_name ,
        'expert_user':expert_user,
        'expert_user_roles' : expert_user_roles,
    }

    return render(request, 'system_expert_roles.html',context)


@login_required
def process_experts(request):
    """
    takes experts in a specific process
    """

    id_chart = request.POST.get('id_KnowledgeProcess')

    html_chart = create_chart_tree(None)

    context={
        'Title':'خبره های حوزه ی دانشی',
        'html_chart':html_chart,
    }

    if request.method == 'POST':
        if id_chart is not None and id_chart != "":
            selected_chart = TblChart.objects.get(Chart=id_chart)
            if selected_chart.Parent is not None :
                chart_children = TblChart.objects.filter(location__startswith=selected_chart.location).filter(ChartType=3).filter(Status=1).values_list('Chart', flat=True)
                this_chart_expert_users = ExpertChart.objects.filter(chart__in = chart_children)
                context.update({
                    'this_chart_expert_users' : this_chart_expert_users ,
                    'selected_chart' : selected_chart,
                })



    return render(request, 'process_experts.html',context)

@login_required
def testet_users(request):

    user_name = request.GET.get('search')
    exam_code = request.GET.get('exam_code')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    all_users=Members.objects.all()
    send_exam2_member_objects=SendExam2member.objects.all()   

    if user_name != None and user_name !='':
        all_users = all_users.filter(Q(first_name__contains=user_name) | Q(last_name__contains=user_name))


    if exam_code != None and exam_code !='':
        users_participated_in_this_exam = SendExam2member.objects.filter(exam_id__code=exam_code).values_list('member_id', flat=True)   
        all_users = all_users.filter(member__in = users_participated_in_this_exam )



    if from_date and to_date:
        from_date = int(''.join(from_date.split('/')))
        to_date = int(''.join(to_date.split('/')))
        exam_list = SendExam2member.objects.filter(exam_id__from_date__gte=from_date,exam_id__to_date__lte=to_date).values_list('member_id', flat=True)  
        all_users = all_users.filter(member__in = exam_list )

    if to_date == "" and not from_date == "":
        from_date = int(''.join(from_date.split('/')))
        exam_list = SendExam2member.objects.filter(exam_id__from_date__gte=from_date).values_list('member_id', flat=True)  
        all_users = all_users.filter(member__in = exam_list )

    if from_date == "" and not to_date == "":
        to_date = int(''.join(to_date.split('/')))
        exam_list = SendExam2member.objects.filter(exam_id__to_date__lte=to_date).values_list('member_id', flat=True)  
        all_users = all_users.filter(member__in = exam_list )

    p = Paginator(all_users, 12)
    page = request.GET.get('page')
    users = p.get_page(page)

    context={
        
        'Title': ' گزارش ازمون ها',
        'users':users,
        'send_exam2_member_objects':send_exam2_member_objects,
    }
    return render(request,'tested_users.html',context)

@login_required
def list_of_tests(request,id):
    if not is_expert(request.user):
        return HttpResponseRedirect('/')

    today_date=get_persian_date_normalized()
    this_user_exams=SendExam2member.objects.filter(member_id=id,exam_id__to_date__lt=today_date)
    context={
        
        'Title': '  لیست ازمون ها',
        'exams':this_user_exams,
    }
    return render(request,'list_of_tests.html',context)

@login_required
def polled_users(request):
    name = request.GET.get('name')
    code = request.GET.get('code')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')


    today_date = get_persian_date_normalized()
    time_now=datetime.datetime.now().time()

    this_user_surveys = TblSuervey.objects.filter(Status =1).filter(Q(to_date__lt = today_date) | Q(to_date = today_date , to_hour__lt =time_now ))


    if name is not None and name != "":
        this_user_surveys = this_user_surveys.filter(name__contains =name)

    if code != "" and code is not None:
        this_user_surveys = this_user_surveys.filter(code=code)


    if from_date and to_date:
        from_date = int(''.join(from_date.split('/')))
        to_date = int(''.join(to_date.split('/')))
        this_user_surveys = this_user_surveys.filter(
            from_date__gte=from_date,
           to_date__lte=to_date)

    if to_date == "" and not from_date == "":
        from_date = int(''.join(from_date.split('/')))
        this_user_surveys = this_user_surveys.filter(from_date__gte=from_date)

    if from_date == "" and not to_date == "":
        to_date = int(''.join(to_date.split('/')))
        this_user_surveys = this_user_surveys.filter(to_date__lte=to_date)



    context={
        'Title': 'نظرسنجی ',
        'this_user_surveys':this_user_surveys,
    }
    return render(request,'polled_users.html',context)

@login_required
def ideasAndCriticism(request):
    context={
        
        'Title': 'انتقادات و پیشنهادات ',
    }
    return render(request,'ideasAndCriticism.html',context)

@login_required
def list_of_polls(request):
    context={
        
        'Title': ' لیست نظرسنجی ',
    }
    return render(request,'list_of_polls.html',context)

@login_required
def list_of_ideasAndCriticism(request):
    context={
        
        'Title': ' لیست انتقادات و پیشنهادات ',
    }
    return render(request,'list_of_ideasAndCriticism.html',context)

@login_required
def conversation_hall(request):
    """SEARCH FOR CONVERSATION HALL"""
    #all the queries we need
    all_knwoledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9))
    all_members = Members.objects.all()

    #users in conversation all
    KnowldgeRQ_users = TblKnowledgeRequest.objects.all()
    AnswerKnowledgeQ_users = TblAnswerKnowledgeRequest.objects.all()
    AnswerQuestion_users = TblAnswerQuestionRequest.objects.all()
    QuestionRequest_users = TblQuestionRequest.objects.all()
    AnswerKnowledgeQ_users_hall = all_members.filter(member__in=AnswerKnowledgeQ_users)
    QuestionRequest_users_hall = all_members.filter(member__in=QuestionRequest_users)
    users_in_KnowledgeRQhall = all_members.filter(member__in=KnowldgeRQ_users)
    users_in_Qhall = all_members.filter(member__in=AnswerQuestion_users)

    all_users =(AnswerKnowledgeQ_users_hall | QuestionRequest_users_hall | users_in_KnowledgeRQhall | users_in_Qhall ).distinct()


    #Search for the conversation hall 
    search_user = request.GET.get('search')
    search_point = request.GET.get('point')
    submitted_knowledges = request.GET.get('knowleges')
    if search_user != None and search_user != '':
        find_user = all_users.filter(Q(first_name__contains=search_user) | Q(last_name__contains=search_user))
        all_users = find_user


    if submitted_knowledges != None and submitted_knowledges != '':
        users_len = all_knwoledges.values_list('CreatorUserID', flat=True)
        users_len = list(users_len)
        result = set([x for x in users_len if users_len.count(x) >= int(submitted_knowledges) ])
        all_users = all_users.filter(member__in=result)

    if search_point != None and search_point != '':
        all_users = all_users.filter(score__gte = search_point)

    p = Paginator(all_users, 12)
    page = request.GET.get('page')
    users = p.get_page(page)

    context={
        'users':users,
        'all_members' : all_members,
        'Title': ' فعالان در تالار گفتمان ',
    }
    return render(request,'conversation_hall.html',context)

@login_required
def list_conversation_hall(request):
    context={
        
        'Title': 'لیست فعالان تالار گفتمان ',
    }
    return render(request,'list_conversation_hall.html',context)

@login_required
def indicator_key_report(request):
    today_date = get_persian_date_normalized()
    kpi_indicators = TblKeyIndicator.objects.filter(expire_date__gte = today_date)

    context={
        'kpi_indicators':kpi_indicators,
        'Title': ' گزارش شاخص کلیدی عملکرد',
    }
    return render(request,'indicator_key_report.html',context)

@login_required
def list_indicator_keys(request):
    context={
        
        'Title': '  لیست شاخص های کلیدی عملکرد',
    }
    return render(request,'list_indicator_keys.html',context)

@login_required
def question_list(request,id):
    questions=TblQuestion.objects.filter(exam_id=id,status__gte=0)
    grade=0
    for question in questions:
        grade += question.grade

    conetxt = {
            'Title': ' لیست سوالات ',
            'questions':questions,
            'grade':grade,
        }
    return render(request, 'question_list.html', conetxt)

@login_required
def delete_question(request,id):

    question=TblQuestion.objects.get(id=id)
    tbl_options=TblQuestionOptions.objects.filter(question_id=question)

    if TblAnswerOption.objects.filter(exam_id = question.exam_id).exists():
        TblAnswerOption.objects.filter(exam_id = question.exam_id).delete()
    for option in tbl_options:
        option.delete()

    question.delete()


    return HttpResponseRedirect("/question_list/"+str(question.exam_id.id))

@login_required
def delete_exam(request,id):
    exam=TblExam.objects.get(id=id)
    try:
        exam.delete()
    except:
        exam.Status=-1
        exam.save()

        # deletes the exams that are sent to users
        if SendExam2member.objects.filter(exam_id = exam).exists():
            SendExam2member.objects.filter(exam_id = exam).delete()

        # deletes the user answers
        if TblAnswerOption.objects.filter(exam_id = exam).exists():
            TblAnswerOption.objects.filter(exam_id = exam).delete()

    return HttpResponseRedirect("/test_list")

@login_required
def edit_exam(request,id):
    exam=TblExam.objects.get(id=id)
    exam_form = TblExamForm(request.POST or None, request.FILES or None, instance=exam)
    if request.method == "POST":
        if exam_form.is_valid():
            obj=exam_form.save()
            obj.creator=request.user
            obj.save()
            if TblAnswerOption.objects.filter(exam_id = exam).exists():
                TblAnswerOption.objects.filter(exam_id = exam).delete()
            return HttpResponseRedirect("/test_list")

    context={
        'TblExamForm':exam_form,
    }
    return render(request, 'test_generator.html', context)



@login_required
def edit_question(request,id):
    question=TblQuestion.objects.get(id=id)
    question_form = TblQuestionForm(request.POST or None , request.FILES or None , instance=question)
    if request.method == "POST":
        options = request.POST.getlist('option')
        check_box_answer = request.POST.getlist('correct_answer')
        if question_form.is_valid():
            obj=question_form.save()
            tbl_options=TblQuestionOptions.objects.filter(question_id=id)

            if TblAnswerOption.objects.filter(exam_id = question.exam_id).exists():
                TblAnswerOption.objects.filter(exam_id = question.exam_id).delete()
            for option in tbl_options:
                option.delete()
            for option in options:
                tbl_question_option=TblQuestionOptions()
                tbl_question_option.question_id=TblQuestion.objects.get(id=obj.id)
                tbl_question_option.option_text=option
                tbl_question_option.option_number=options.index(option)+1
                tbl_question_option.save()
                if tbl_question_option.option_number in list(map(int, check_box_answer)):
                    tbl_question_option.is_answer=True
                else:
                    tbl_question_option.is_answer=False
                tbl_question_option.save()
            return HttpResponseRedirect("/question_list/"+str(obj.exam_id.id))


    tbl_options=TblQuestionOptions.objects.filter(question_id=id)

    context={
        'TblQuestionForm':question_form,
        "editSign":"edit",
        'options':tbl_options,
        'question':question,
    }
    return render(request, 'add_question.html', context)

@login_required
def add_question(request,id):
    if request.method == "POST":
        form = TblQuestionForm(request.POST , request.FILES or None)
        options = request.POST.getlist('option')
        check_box_answer = request.POST.getlist('correct_answer')
        if form.is_valid():
            obj=form.save()
            obj.exam_id=TblExam.objects.get(id=id)
            obj.save()

            if TblAnswerOption.objects.filter(exam_id = TblExam.objects.get(id=id)).exists():
                TblAnswerOption.objects.filter(exam_id = TblExam.objects.get(id=id)).delete()

            for option in options:
                tbl_question_option=TblQuestionOptions()
                tbl_question_option.question_id=TblQuestion.objects.get(id=obj.id)
                tbl_question_option.option_text=option
                tbl_question_option.option_number=options.index(option)+1
                tbl_question_option.save()
                if tbl_question_option.option_number in list(map(int, check_box_answer)):
                    tbl_question_option.is_answer=True
                else:
                    tbl_question_option.is_answer=False
                tbl_question_option.save()
            return HttpResponseRedirect("/question_list/"+str(obj.exam_id.id))
        else:
            conetxt = {
            'Title': ' لیست سوالات ',
            'TblQuestionForm':form,
            }
            return render(request, 'add_question.html', conetxt)

            
    form=TblQuestionForm()
    conetxt = {
            'Title': ' لیست سوالات ',
            'TblQuestionForm':form,
        }
    return render(request, 'add_question.html', conetxt)

@login_required
def send_test(request,id):
    memebers = Members.objects.all()
    exam_obj = TblExam.objects.get(id=id)
    if TblQuestion.objects.filter(exam_id=TblExam.objects.get(id=id)).exists():
        if request.method == "POST":
            # send to all = 1 means True #send to all = 2 means false
            send_to_all = request.POST.get('send_to_all')
            memebers_to_save = request.POST.getlist('member')

            if send_to_all == '2':
                if len(memebers_to_save) >1:
                    for item in memebers_to_save:
                        if int(item) != request.user.member:
                            obj_SendExam2member = SendExam2member()
                            obj_SendExam2member.exam_id = TblExam.objects.get(id=id)
                            obj_SendExam2member.member_id = Members.objects.get(member=item)
                            obj_SendExam2member.save()
                    notif_to_users = Members.objects.filter(member__in=memebers_to_save).exclude(member=request.user.member)
                    exam_obj=TblExam.objects.get(id=id)
                    exam_obj.send_status=1
                    exam_obj.save()
                    items = [
                    TblExamNotification(user=member , notif=exam_obj , url='inform_exam/{}'.format(id))
                    for member in notif_to_users
                    ]

                    TblExamNotification.objects.bulk_create(items)
                    return HttpResponseRedirect("/test_list")
                else:
                    conetxt = {
                        'members': memebers,
                        'Title': ' ارسال ازمون ',
                        'error':'حداقل یک کاربر را انتخاب نمایید!',
                        }
                    return render(request, 'send_test.html', conetxt)

            else:

                exam_obj.sent_to_all =True
                exam_obj.send_status=1
                exam_obj.save()
                items = [
                TblExamNotification(user=member , notif=exam_obj , url='inform_exam/{}'.format(id))
                for member in memebers.exclude(member=request.user.member)
                ]

                TblExamNotification.objects.bulk_create(items)
                return HttpResponseRedirect("/test_list")


        conetxt = {
            'members': memebers,
            'Title': ' ارسال ازمون ',
            }
        return render(request, 'send_test.html', conetxt)
    conetxt = {
            'members': memebers,
            'Title': ' ارسال ازمون ',
            'error':'آزمون باید حداقل دارای یک سوال باشد',
            }
    return render(request, 'send_test.html', conetxt)


@login_required
def inform_meeting(request):
    members = Members.objects.all()
    form = Informs_meetingForm()

    if request.method == "POST":  
        form=Informs_meetingForm(request.POST)
        get_members = request.POST.getlist('member')
        get_title = request.POST.get('meeting_title')
        meeting_location_place = request.POST.get('meeting_location_place')
        meeting_start_time = request.POST.get('meeting_start_time')
        meeting_start_date = request.POST.get('meeting_start_date')

        send_to_all = request.POST.get('KnowledgeIsGroup')
        
        users_to_recive = Members.objects.filter(member__in=get_members).exclude(member=request.user.member)

        if int(send_to_all) == 1:     
            if form.is_valid():       
                items = [
                        Informs_meeting(meeting_reciver=member , meeting_title=get_title ,meeting_location_place=meeting_location_place ,meeting_start_time=meeting_start_time, meeting_start_date=int(meeting_start_date))
                        for member in members.exclude(member=request.user.member)
                        ]
                Informs_meeting.objects.bulk_create(items)       
                return HttpResponseRedirect('/home')
        else:
            send_to_all=2
            if form.is_valid():
                if len(get_members) >=2 :
                    items = [
                    Informs_meeting(meeting_reciver=member , meeting_title=get_title ,meeting_location_place=meeting_location_place ,meeting_start_time=meeting_start_time, meeting_start_date=int(meeting_start_date))
                    for member in users_to_recive
                    ]

                    Informs_meeting.objects.bulk_create(items)       
                    return HttpResponseRedirect('/home')
    context ={ 
    'members' : members,
    'Informs_meetingForm' : Informs_meetingForm()
    }

    return render(request, 'inform_meeting.html', context)

@login_required
def rejected_knowledgeView(request,id):


    #delete notif knowledge rejected by IT
    if TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 7).exists():
        TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = request.user).filter(notif__KnowledgeCode = id).filter(notif_type = 7).delete()

    rejected = rejected_knowledge.objects.filter(knowledge_id=id)
    context = {
        'rejected' : rejected[::-1],
        'Title': ' کاربرگ رد تجربه ',
    }
    return render(request, 'rejected_knowledgeView.html', context)


@login_required
def topic2_view(request):
    """Ajax func for topic2 dropw down list"""
    if request.method == "POST":
        subject_id = request.POST['subject_id']
        subject = topic2.objects.filter(mozo1=topic1.objects.get(id=subject_id)).filter(status=1)
        # data = serializers.serialize('json', list(subject), fields=('state','id'))
    json = "["
    for item in subject:
        if len(json) > 1:
            json += ","
        json += "{\"id\":\"" + str(item.id) + \
                "\", \"text\":\"" + item.state + "\"}"
    json += "]"

    return JsonResponse(json,safe=False)

@login_required
def topic3_view(request):
    """Ajax func for topic3 dropw down list"""

    if request.method == "POST":
        subject_id = request.POST['subject_id']
        subject = topic3.objects.filter(mozo2=topic2.objects.get(id=subject_id)).filter(status=1)
        # data = serializers.serialize('json', list(subject), fields=('state','id'))
    json = "["
    for item in subject:
        if len(json) > 1:
            json += ","
        json += "{\"id\":\"" + str(item.id) + \
                "\", \"text\":\"" + item.city + "\"}"
    json += "]"

    return JsonResponse(json,safe=False)


@login_required
def indicator_assessment_list(request):

    indicator = indicator_assessment_model.objects.filter(Status__gte=0)

    context = {
        'indicator' : indicator,
        'Title' : 'لیست شاخص های ارزیاب'
    }
    return render(request,'indicator_assessment_list.html',context)

@login_required
def edit_indicator_assessment(request,id):

    obj_indicator = get_object_or_404(indicator_assessment_model, id=id)
    indicator = indicator_assessmentForm(request.POST or None ,instance=obj_indicator)
    point_value = obj_indicator.indicator_point
    text_value = obj_indicator.indicator
    if request.method == "POST":
        points = request.POST.get('indicator_point')
        if indicator.is_valid():
            indicator.save()
            return HttpResponseRedirect('/indicator_assessment_list')
        else:
            text_value = obj_indicator.indicator
            context = {
                'error' : 'بارم شاخص نمیتواند بیش از 10 باشد',
                'text_value' : text_value,
            }
        return render(request,'indicator_assessment.html',context)
    context = {
        'indicator' : indicator,
        'Title' : 'ویرایش شاخص کلیدی ارزیاب',
        'point_value': point_value,
        'text_value' : text_value,
    }

    return render(request,'indicator_assessment.html',context)

@login_required
def take_exam_list(request):
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/')

    this_user_recieves = SendExam2member.objects.filter(member_id=request.user).values_list('exam_id', flat=True)

    this_user_exams = TblExam.objects.filter( id__in = this_user_recieves ).filter(Status = 1)

    all_user_exams = TblExam.objects.filter(sent_to_all = True).filter(Status = 1)

    exams = this_user_exams | all_user_exams

    today_date=get_persian_date_normalized()
    time_now=datetime.datetime.now().time()

    context={
        'exams':exams,
        'today_date':today_date,
        'time_now':time_now,
    }
    return render(request, 'take_exam_list.html', context)

@login_required
def inform_exam(request,id):
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')

    this_user_exam=TblExam.objects.get(id=id)
    #Deleteing the notification after user seen the notif

    if TblExamNotification.objects.filter( user = request.user ).filter( notif__id = id ).exists():
        TblExamNotification.objects.get( notif__id = id , user = request.user ).delete()

    if this_user_exam.sent_to_all == False:
        if not SendExam2member.objects.filter(member_id=request.user):
            return HttpResponseRedirect('/take_exam_list')

 
    today_date=get_persian_date_normalized()
    time_now=datetime.datetime.now().time()
    from_hour=this_user_exam.from_hour
    to_hour=this_user_exam.to_hour

    Permission=0

    if today_date >= this_user_exam.from_date and today_date <= this_user_exam.to_date and time_now >= from_hour and time_now <= to_hour:
        Permission=1

    if TblAnswerOption.objects.filter(member_id=request.user , exam_id=id):
        Permission=2
    context={
        'exam':this_user_exam,
        'permission':Permission,
    }
    return render(request, 'inform_exam.html', context)

@login_required
def take_exam(request,id):
    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect('/login')

    #checks if the member has taken the exam.if yes it does not allow the user to take exam
    if TblAnswerOption.objects.filter(member_id=request.user , exam_id=id):
        return HttpResponseRedirect('/take_exam_list')

    pdf_file = None
    image = None
    this_user_exam=TblExam.objects.get(id=id)
    #checks if the exam is defined for member
    if this_user_exam.sent_to_all == False:
        if not SendExam2member.objects.filter(member_id=request.user):
            return HttpResponseRedirect('/take_exam_list')

    today_date=get_persian_date_normalized()
    this_user_exam=TblExam.objects.get(id=id)

    time_now=datetime.datetime.now().time()

    # checks the time and the date of exam.
    if not (today_date >= this_user_exam.from_date and today_date <= this_user_exam.to_date and time_now >= this_user_exam.from_hour and time_now <= this_user_exam.to_hour):
        return HttpResponseRedirect('/take_exam_list')

    if this_user_exam.question_file != None:
        exam_file = this_user_exam.question_file
        file_format = exam_file.name.split(".")
        if file_format[1] == "pdf":
            pdf_file = exam_file
        else:
            image = exam_file

    this_exam_questions=TblQuestion.objects.filter(exam_id=TblExam.objects.get(id=id))
    options=TblQuestionOptions.objects.filter(question_id__in=this_exam_questions)

    #calculates the exam time: current time - exam to hour  
    to_hour=this_user_exam.to_hour
    to_hour_string=str(to_hour)
    time_now_exam = datetime.time(time_now.hour, time_now.minute, time_now.second)
    to_hour_exam = datetime.time(to_hour.hour, to_hour.minute, to_hour.second)
    date = datetime.date(1, 1, 1)
    datetime_now = datetime.datetime.combine(date, time_now_exam)
    datetime_exam = datetime.datetime.combine(date, to_hour_exam)
    exam_time = datetime_exam - datetime_now
    exam_time = exam_time.seconds * 1000
    print(exam_time)


    if request.method == "POST":
        none_counter=0
        for question in this_exam_questions:
            answer_options_user=request.POST.getlist('question'+str(question.id))
            if len(answer_options_user) > 0:
                for answer_option_user in answer_options_user:
                    user_answer=TblAnswerOption()
                    user_answer.option_id=TblQuestionOptions.objects.get(id=answer_option_user)
                    user_answer.member_id=request.user
                    user_answer.exam_id=TblExam.objects.get(id=id)
                    user_answer.save()
            else:
                none_counter += 1

        #if the user answers nothing creates a TblAnswerOption instance to which has no foreign key to any option
        # and indicate that the user attended the exam
        if none_counter == len(this_exam_questions):
            user_answer=TblAnswerOption()
            user_answer.member_id=request.user
            user_answer.exam_id=TblExam.objects.get(id=id)
            user_answer.save()

        return HttpResponseRedirect('/take_exam_list')



    context={
        'questions':this_exam_questions,
        'questionsـlen':len(this_exam_questions),
        'options':options,
        'exam_time':exam_time,
        'image' : image,
        'pdf_file' : pdf_file ,
        'to_hour_string':to_hour_string
    }
    return render(request, 'take_exam.html', context)

@login_required
def take_survey(request,id):
    this_survey = TblSuervey.objects.get(id=id)
    options = TblSuerveyOptions.objects.filter(survey_id = this_survey)
    #Deleteing the notification after user seen the notif

    if TblSurveyotification.objects.filter( user = request.user ).filter( notif__id = id ).exists():
        TblSurveyotification.objects.get( notif__id = id , user = request.user ).delete()

    today_date=get_persian_date_normalized()
    time_now=datetime.datetime.now().time()

    # checks the time and the date of exam.
    if not (today_date >= this_survey.from_date and today_date <= this_survey.to_date and time_now >= this_survey.from_hour and time_now <= this_survey.to_hour):
        return HttpResponseRedirect('/my_surveys')
        
    if request.method == "POST":
        answer_options_user = request.POST.getlist('checkboxOptions')
        comment = request.POST.get('nazar_comment')
        for answer_option_user in answer_options_user:
            TblAnswerOptionSurvey.objects.create(
                option_id = TblSuerveyOptions.objects.get(id = answer_option_user),
                member_id = request.user,
                suervey = this_survey,
                comment = comment
            )

        return HttpResponseRedirect('/my_surveys')



    context = {
        'survey':this_survey,
        'options':options,
    }

    return render(request, 'take_survey.html', context)


@login_required
def exam_score(request,id):
    this_exam=TblExam.objects.get(id=id)

    today_date=get_persian_date_normalized()
    time_now=datetime.datetime.now().time()

    #these 2 ifs, check if the exam time is finished inorder to show the user the result of their exam
    if today_date == this_exam.to_date and time_now < this_exam.to_hour :
        return HttpResponseRedirect('/take_exam_list')

    if today_date < this_exam.to_date:
        return HttpResponseRedirect('/take_exam_list')

    this_exam_questions=TblQuestion.objects.filter(exam_id=this_exam)
    this_user_answers=TblAnswerOption.objects.filter(member_id=request.user,exam_id=id)
    score_user=0
    total_score_exam=0


    for question in this_exam_questions:
        total_score_exam += question.grade
        
        exam_correct_options=set()

        #gives all the options for the current question
        question_options=TblQuestionOptions.objects.filter(question_id=question)

        #gets the answers of the user for the current question and add them to a set
        this_user_question_option_answers=this_user_answers.values_list('option_id', flat=True).filter(option_id__question_id=question)
        user_answers=set(TblQuestionOptions.objects.filter(id__in=this_user_question_option_answers))
        
        #finds the correct options (that are defined by the examiner) of a question and add them to a set
        for question_option in question_options:
            if question_option.is_answer:
                exam_correct_options.add(question_option)
        
        #checks if the user answers are equal to the question answers
        if exam_correct_options == user_answers:
            score_user += question.grade
    
    context={
        'score_user':score_user,
        'total_score_exam':total_score_exam,
    }

    return render(request, 'exam-result.html', context)


@login_required
def exam_review(request,id):
    this_exam=TblExam.objects.get(id=id)

    today_date=get_persian_date_normalized()
    time_now=datetime.datetime.now().time()

    #these 2 ifs, check if the exam time is finished inorder to show the user the result of their exam
    if today_date == this_exam.to_date and time_now < this_exam.to_hour :
        return HttpResponseRedirect('/take_exam_list')

    if today_date < this_exam.to_date:
        return HttpResponseRedirect('/take_exam_list')

    this_exam_questions=TblQuestion.objects.filter(exam_id=this_exam)
    options=TblQuestionOptions.objects.filter(question_id__in=this_exam_questions)
    this_user_answers=TblAnswerOption.objects.values_list('option_id', flat=True).filter(member_id=request.user,exam_id=id)
    this_user_answers_objects=TblQuestionOptions.objects.filter(id__in=this_user_answers)
    


    score_user=0
    total_score_exam=0


    for question in this_exam_questions:
        total_score_exam += question.grade
        
        exam_correct_options=set()

        #gives all the options for the current question
        question_options=TblQuestionOptions.objects.filter(question_id=question)

        #gets the answers of the user for the current question and add them to a set
        this_user_question_option_answers=this_user_answers.values_list('option_id', flat=True).filter(option_id__question_id=question)
        user_answers=set(TblQuestionOptions.objects.filter(id__in=this_user_question_option_answers))
        
        #finds the correct options (that are defined by the examiner) of a question and add them to a set
        for question_option in question_options:
            if question_option.is_answer:
                exam_correct_options.add(question_option)
        
        #checks if the user answers are equal to the question answers
        if exam_correct_options == user_answers:
            score_user += question.grade
    
    context={
        'score_user':score_user,
        'total_score_exam':total_score_exam,
        'questions':this_exam_questions,
        'options':options,
        'this_user_answers':this_user_answers_objects
    }

    return render(request, 'exam-review.html', context)

@login_required
def my_knowledge_list(request,id):

    Knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID = id)

    context = {
        'Knowledges' : Knowledges,
    }
    return render(request,'Knowledge_Report_List.html',context)


@login_required
def like_knowledge_request(request):
    Tbl_vote = TblVoteQuestion.objects.all()
    Tbl_knowledge_request = TblKnowledgeRequest.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        vote_type=request.POST.get('voteType')
        if Tbl_vote.filter(knowledge_request=post_id, creater_user_id=request.user.member).exists():
            Tbl_vote.filter(knowledge_request=post_id, creater_user_id=request.user.member).delete()
        
            up_vote = len(Tbl_vote.filter(knowledge_request=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request=post_id,vote_status=2))
            result = up_vote-down_vote
            color = ''
            ajax_vote_type=0

            #calculate the score of the knowledge owner
            obj_knowledge_request = TblKnowledgeRequest.objects.get(id=post_id)
            knowledge_owner = Members.objects.get(member=obj_knowledge_request.CreatorUserID.member)
            knowledge_owner.score = score_calculator(knowledge_owner)
            knowledge_owner.save()
        else:
            obj_vote = TblVoteQuestion()
            obj_vote.creater_user_id = request.user
            obj_vote.knowledge_request = Tbl_knowledge_request.get(id=post_id)
            
            #vote_type 1 means upVote  and vote_type 2 means downVote
            if vote_type == '1':
                obj_vote.vote_status = 1
                ajax_vote_type=1
            else:
                obj_vote.vote_status = 2
                ajax_vote_type=2

            obj_vote.save()

            up_vote = len(Tbl_vote.filter(knowledge_request=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request=post_id,vote_status=2))
            result = up_vote-down_vote
            color='orange'


            #calculate the score of the knowledge owner
            obj_knowledge_request = TblKnowledgeRequest.objects.get(id=post_id)
            knowledge_owner = Members.objects.get(member=obj_knowledge_request.CreatorUserID.member)
            knowledge_owner.score = score_calculator(knowledge_owner)
            knowledge_owner.save()

        return JsonResponse({'result': result, 'color': color,'ajax_vote_type':ajax_vote_type})

@login_required
def likeQuestionRequest(request):
    Tbl_vote = TblVoteSendQuestion.objects.all()
    Tbl_knowledge_request = TblQuestionRequest.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        vote_type=request.POST.get('voteType')
        if Tbl_vote.filter(knowledge_request=post_id, creater_user_id=request.user.member).exists():
            Tbl_vote.filter(knowledge_request=post_id, creater_user_id=request.user.member).delete()
        
            up_vote = len(Tbl_vote.filter(knowledge_request=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request=post_id,vote_status=2))

            result = up_vote-down_vote
            color = ''
            ajax_vote_type=0
        else:
            obj_vote = TblVoteSendQuestion()
            obj_vote.creater_user_id = request.user
            obj_vote.knowledge_request = Tbl_knowledge_request.get(id=post_id)

            #vote_type 1 means upVote  and vote_type 2 means downVote
            if vote_type == '1':
                obj_vote.vote_status = 1
                ajax_vote_type=1
            else:
                obj_vote.vote_status = 2
                ajax_vote_type=2

            obj_vote.save()
            
            up_vote = len(Tbl_vote.filter(knowledge_request=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request=post_id,vote_status=2))
            result = up_vote-down_vote
            color='orange'

        return JsonResponse({'result': result, 'color': color,'ajax_vote_type':ajax_vote_type})
        
@login_required
def like_answer_knowledge_request(request):
    Tbl_vote = TblVoteQuestionAnswer.objects.all()
    Tbl_knowledge_request_answer = TblAnswerKnowledgeRequest.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        vote_type=request.POST.get('voteType')
        if Tbl_vote.filter(knowledge_request_answer=post_id, creater_user_id=request.user.member).exists():
            Tbl_vote.filter(knowledge_request_answer=post_id, creater_user_id=request.user.member).delete()
        
            up_vote = len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=2))
            result = up_vote-down_vote
            color = ''
            ajax_vote_type=0
        else:
            obj_vote = TblVoteQuestionAnswer()
            obj_vote.creater_user_id = request.user
            obj_vote.knowledge_request_answer = Tbl_knowledge_request_answer.get(id=post_id)
            
            #vote_type 1 means upVote  and vote_type 2 means downVote
            if vote_type == '1':
                obj_vote.vote_status = 1
                ajax_vote_type=1
            else:
                obj_vote.vote_status = 2
                ajax_vote_type=2

            obj_vote.save()

            up_vote = len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=2))
            result = up_vote-down_vote
            color='orange'

        return JsonResponse({'result': result, 'color': color,'ajax_vote_type':ajax_vote_type})

@login_required
def likes_of_question_answers(request):
    Tbl_vote = TblVotesForQuestionAnswer.objects.all()
    Tbl_knowledge_request_answer = TblAnswerQuestionRequest.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        vote_type=request.POST.get('voteType')
        if Tbl_vote.filter(knowledge_request_answer=post_id, creater_user_id=request.user.member).exists():
            Tbl_vote.filter(knowledge_request_answer=post_id, creater_user_id=request.user.member).delete()
        
            up_vote = len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=2))
            result = up_vote-down_vote
            color = ''
            ajax_vote_type=0
        else:
            obj_vote = TblVotesForQuestionAnswer()
            obj_vote.creater_user_id = request.user
            obj_vote.knowledge_request_answer = Tbl_knowledge_request_answer.get(id=post_id)
            
            #vote_type 1 means upVote  and vote_type 2 means downVote
            if vote_type == '1':
                obj_vote.vote_status = 1
                ajax_vote_type=1
            else:
                obj_vote.vote_status = 2
                ajax_vote_type=2

            obj_vote.save()

            up_vote = len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=1))
            down_vote= len(Tbl_vote.filter(knowledge_request_answer=post_id,vote_status=2))
            result = up_vote-down_vote
            color='orange'

        return JsonResponse({'result': result, 'color': color,'ajax_vote_type':ajax_vote_type})

@login_required
def used_knowledge(request):
    Tbl_used_vote = TblUsedKnowledge.objects.all()
    Tbl_knowledge = TblKnowledge.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        if Tbl_used_vote.filter(knowledge=post_id, creater_user_id=request.user.member).exists():
            Tbl_used_vote.filter(knowledge=post_id, creater_user_id=request.user.member).delete()
            
            result = len(Tbl_used_vote.filter(knowledge=post_id))  
            color = ''

            #calculate the score of the knowledge owner
            obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=post_id)
            knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
            knowledge_owner.score = score_calculator(knowledge_owner)
            knowledge_owner.save()


        else:
            obj_vote = TblUsedKnowledge()
            obj_vote.creater_user_id = request.user
            obj_vote.knowledge = Tbl_knowledge.get(KnowledgeCode=post_id)
            obj_vote.save()

            result = len(Tbl_used_vote.filter(knowledge=post_id))  

            color='green'

            #calculate the score of the knowledge owner
            obj_knowledge = TblKnowledge.objects.get(KnowledgeCode=post_id)
            knowledge_owner = Members.objects.get(member=obj_knowledge.CreatorUserID.member)
            knowledge_owner.score = score_calculator(knowledge_owner)
            knowledge_owner.save()

        return JsonResponse({'result': result,'color' : color})

@login_required
def advanced_chart(request,id):
    if not is_IT(request.user):
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':

        # these 2 lines take the files and titles
        doc_files_title = request.POST.getlist('docTitle')
        doc_files=request.FILES.getlist('Allfiles')

        #checks if they are not empty and have the same len 
        # then it creates  instances of TblChartDocument and store the values in them
        if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
            for itemFile,itemTitle in zip(doc_files,doc_files_title):
                obj_file_doc=TblChartDocument()
                obj_file_doc.file=itemFile
                obj_file_doc.title=itemTitle
                obj_file_doc.feed=TblChart.objects.get(Chart=id)
                obj_file_doc.save()

        #if they are 1 it means that they are checked otherwise they are None
        request_of_service_recipient = request.POST.get('request_of_service_recipient')
        arrival_of_specific_time = request.POST.get('arrival_of_specific_time')
        specific_event_occurrence = request.POST.get('specific_event_occurrence')
        device_detection = request.POST.get('device_detection')

        #checks if there is any instance of TblChartAdvanceInfo for this chart
        # and if there is, it will pass it to the form as an instance
        if TblChartAdvanceInfo.objects.filter(chart=TblChart.objects.get(Chart=id)).exists():
            obj_advance_info=TblChartAdvanceInfo.objects.get(chart=TblChart.objects.get(Chart=id))
            form = TblChartAdvanceInfoForm(request.POST,instance=obj_advance_info)
        else:
            form = TblChartAdvanceInfoForm(request.POST)


        if form.is_valid():
            obj=form.save()

            obj.chart=TblChart.objects.get(Chart=id)

            # these ifs are for the checkboxes           
            if request_of_service_recipient == '1':
                obj.request_of_service_recipient = True
            else:
                obj.request_of_service_recipient = False

            if arrival_of_specific_time == '1':
                obj.arrival_of_specific_time = True
            else:
                obj.arrival_of_specific_time = False

            if specific_event_occurrence == '1':
                obj.specific_event_occurrence = True
            else:
                obj.specific_event_occurrence = False

            if device_detection == '1':
                obj.device_detection = True
            else:
                obj.device_detection = False
            
            # these ifs are for the checkboxes

            obj.save()

            chart_members_list=request.POST.getlist('chartMember')
            if len(chart_members_list) >=0:
                this_chart_objects=TblDependentChart.objects.filter(owner=obj.id)
                for object in this_chart_objects:
                    object.delete()

            if obj.connection_with_other_processes == 2 or obj.connection_with_other_processes == 3 :
                    for chart_member_list in chart_members_list:
                        obj_member_chart=TblDependentChart()
                        obj_member_chart.chart=TblChart.objects.get(Chart=chart_member_list)
                        obj_member_chart.owner=obj
                        obj_member_chart.save()

    html_chart = create_chart_tree(None)
    chart = ""
    chart_text = ""
    if id is not None:
        obj_chart = TblChart.objects.get(Chart=id)
        if obj_chart is not None:
            chart = obj_chart.Chart
            chart_text = obj_chart.ChartText
            chart_type = obj_chart.ChartType
        else:
            return HttpResponseRedirect("/ChartManagment")
    else:
        return HttpResponseRedirect("/ChartManagment")


    #checks if there is any instance of TblChartAdvanceInfo for this chart
    # and if there is, it will pass it to the form as an instance
    if TblChartAdvanceInfo.objects.filter(chart=obj_chart).exists():
        obj_advance_info=TblChartAdvanceInfo.objects.get(chart=obj_chart)
        form_advance_info = TblChartAdvanceInfoForm(instance=obj_advance_info)
    else:
        form_advance_info = TblChartAdvanceInfoForm()
        obj_advance_info=0

    # takes the documents of the current chart
    chart_document_objcts = TblChartDocument.objects.filter(feed=TblChart.objects.get(Chart=id))

    if obj_advance_info != 0 :
        this_chart_chart_objects=TblDependentChart.objects.filter(owner=obj_advance_info)
    else:
        this_chart_chart_objects=''

    context={
        'Title': ' چارت پیشرفته',
        'chart': chart,
        'html_chart' : html_chart,
        'chartText': chart_text,
        'chartType': chart_type,
        'form_advance_info':form_advance_info,
        'obj_advance_info':obj_advance_info,
        'chart_document_objcts':chart_document_objcts,
        'this_chart_chart_objects':this_chart_chart_objects,

    }
    return render(request, 'advanced_chart.html', context)

@login_required
def delete_advanced_chart(id):

    advanced_chart = TblChartAdvanceInfo.objects.filter(id=id)
    advanced_chart.delete()
        
    dependent_charts = TblDependentChart.objects.filter(id=id)
    if dependent_charts.exists():
        for dependency in dependent_charts:
            dependency.delete()

    chart_documents = TblChartDocument.objects.filter(id=id)
    if len(chart_documents) >= 1 and chart_documents.exists():
        for document in chart_documents:
            document.delete()

    return HttpResponseRedirect("/ChartManagment")

@login_required
def removeDocs(request):
    """Ajax func for removing docs from advance chart"""
    Tbl_feed_file = TblChartDocument.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        file_id = request.POST.get('fileid')
        if Tbl_feed_file.filter(id=file_id).exists():
            obj_path=Tbl_feed_file.get(id=file_id).file.path
            Tbl_feed_file.filter(id=file_id).delete()
            result="success"
            os.remove(obj_path)

        return JsonResponse({'result': result,})


@login_required
def user_list(request):

    all_charts = TblChart.objects.all()
  
    all_users=Members.objects.all()

    search_title = request.GET.get('search')
    search_chart = request.GET.get('chart')
    search_national_code = request.GET.get('nationalCode')
    search_personal_code = request.GET.get('personalCode')


    if search_title != None and search_title !='':
        find_user = Members.objects.filter(Q(first_name__contains=search_title) | Q(last_name__contains=search_title))
        all_users = find_user

    if search_national_code != None and search_national_code !='':
        find_user = Members.objects.filter(nationalCode=search_national_code)
        all_users = find_user

    if search_personal_code != None and search_personal_code !='':
        find_user = Members.objects.filter(personal_number=search_personal_code)
        all_users = find_user

    if search_chart != None and search_chart !='':
        get_memberchart = MemberChart.objects.filter(chart__in = all_charts).values_list('chart' , flat=True)
        charts_in_memberChart = all_charts.filter(Chart__in= get_memberchart)
        search_result = charts_in_memberChart.filter(ChartText__contains = search_chart)
        get_memberchart = MemberChart.objects.filter(chart__in = search_result).values_list('member',flat=True)
        get_member = Members.objects.filter(member__in = get_memberchart)
        all_users = get_member

    p = Paginator(all_users, 12)
    page = request.GET.get('page')
    users = p.get_page(page)
    nums = "a" * users.paginator.num_pages

    context = {
    'all_users' : all_users,
    'users':users,
    'Title' : 'لیست کاربران',
    'nums':nums,
    'search_show_button' : 1,
    }
    return render(request,'list_of_users.html',context)





@login_required
def followers(request):

    followers = TblFollowerFollowedIndicator.objects.filter(followed=TblFollowed.objects.get(who_is_followed = request.user)).values_list('follower', flat=True)

    
    all_users = Members.objects.filter(member__in=followers)

    if request.method == 'POST':
        search_title = request.POST.get('search')
        if search_title != None:
            find_user = all_users.filter(Q(first_name__contains=search_title) | Q(last_name__contains=search_title))

            all_users = find_user
    context = {
        'users' : all_users,
        'Title': '  دنبال کنندگان',
    }
    return render(request,'list_of_users.html',context)


@login_required
def followings(request):

    followings = TblFollowerFollowedIndicator.objects.filter(follower=request.user).values_list('followed', flat=True)
    
    
    all_users = Members.objects.filter(member__in=TblFollowed.objects.filter(id__in=followings).values_list('who_is_followed', flat=True))

    if request.method == 'POST':
        search_title = request.POST.get('search')
        if search_title != None:
            find_user = all_users.filter(Q(first_name__contains=search_title) | Q(last_name__contains=search_title))

            all_users = find_user
    context = {
        
        'users' : all_users,
        'Title': 'دنبال شوندگان  ',
    }
    return render(request,'list_of_users.html',context)

@login_required
def user_profile(request,id):

    # the person that is going to be either followed or unfollowed
    followed_person = Members.objects.get(member = id)

    # if there is no instance of TblFollowed we first make it
    if not TblFollowed.objects.filter(who_is_followed=followed_person).exists():
        obj_followed = TblFollowed()
        obj_followed.who_is_followed = followed_person
        obj_followed.save()

    #getting an instance of TblFollowed for the sake of TblFollowerFollowedIndicator
    obj_followed = TblFollowed.objects.get(who_is_followed=followed_person)

    #checking how many knowledge this person has
    total_knowledge = len(TblKnowledge.objects.filter(CreatorUserID = id , register_status = 9))

    #checking how many followers and following this person has
    followings = len(TblFollowerFollowedIndicator.objects.filter(follower=id).values_list('followed', flat=True))

    followers = len(TblFollowerFollowedIndicator.objects.filter(followed=TblFollowed.objects.get(who_is_followed = id)).values_list('follower', flat=True))


    user = Members.objects.get(member = id)
    skills_objects=skills.objects.filter(skills_key=user)
    member_charts=MemberChart.objects.filter(member=user)

    # tells if the this user has followed the chosen user or not
    # 1 means has followed
    # 0 means has not followed yet
    if TblFollowerFollowedIndicator.objects.filter(follower=request.user , followed=obj_followed).exists():
        follow_status = 1
    else:
        follow_status = 0

    context={
        'user':user,
        'followers' : followers,
        'followings' : followings,
        'total_knowledge' : total_knowledge,
        'skills_objects':skills_objects,
        'member_charts':member_charts,
        'follow_status':follow_status,

    }
    return render(request,'UserProfile.html',context)


@login_required
def follow_unfollow(request,id):
    # the person that is going to be either followed or unfollowed
    followed_person = Members.objects.get(member = id)

    # if there is no instance of TblFollowed we first make it
    if not TblFollowed.objects.filter(who_is_followed=followed_person).exists():
        obj_followed = TblFollowed()
        obj_followed.who_is_followed = followed_person
        obj_followed.save()

    #getting an instance of TblFollowed for the sake of TblFollowerFollowedIndicator
    obj_followed = TblFollowed.objects.get(who_is_followed=followed_person)

    # if there is no instance of TblFollowerFollowedIndicator we make one
    # it means that this user follows the chosen person
    if not TblFollowerFollowedIndicator.objects.filter(follower=request.user , followed=obj_followed).exists():
        obj_follower_followed_indicator = TblFollowerFollowedIndicator()
        obj_follower_followed_indicator.followed = obj_followed
        obj_follower_followed_indicator.follower = request.user
        obj_follower_followed_indicator.save()

        # calculating the score of the person who is followed and saving it to DB
        followed_person.score = score_calculator(followed_person)
        followed_person.save()
    
    # otherwise there is already an instance so we delete it
    # it means that this user unfollows the chosen person
    else:
        TblFollowerFollowedIndicator.objects.filter(follower=request.user , followed=obj_followed).delete()

        # calculating the score of the person who is unfollowed and saving it to DB
        followed_person.score = score_calculator(followed_person)
        followed_person.save()
    
    return HttpResponseRedirect('/userProfile/'+str(id))


@login_required
def message(request,id):
    # deletes the notifs for this chat page for this user
    if TblMessageUserNotification.objects.filter(notif__reciver = request.user.member , notif__sender__member = id ).exists():
        TblMessageUserNotification.objects.filter(notif__reciver = request.user.member, notif__sender__member = id).delete()

    chosen_user = Members.objects.get(member=id)

    messages = TblMessageUser.objects.filter(Q(sender=request.user,reciver=chosen_user.member) | Q(sender=chosen_user,reciver=request.user.member)).order_by('id')

    count_chosen_user_messages = len (TblMessageUser.objects.filter(sender=chosen_user,reciver=request.user.member))

    all_recieve_messages = TblMessageUser.objects.filter(sender=chosen_user,reciver=request.user.member).order_by('id')

    user = Members.objects.get(member = id)
    context = {
        'user' : user,
        'messages':messages,
        'count_recieve_messages':count_chosen_user_messages,
    }

    return render(request,'message.html',context)


@login_required
def send_message(request):

    if request.POST.get('action') == 'post':
        chosen_user_id = request.POST.get('chosenUserId')
        message_text = request.POST.get('text')

        obj_message = TblMessageUser()
        obj_message.sender = request.user
        obj_message.reciver = chosen_user_id
        obj_message.text = message_text
        obj_message.create_hour = datetime.datetime.now()
        obj_message.save()

        # creates notif for the message
        TblMessageUserNotification.objects.create(notif = obj_message , url = 'message/'+str(obj_message.sender.member) )

        json ='success'

        return JsonResponse({'result': json,})


@login_required
def message_recieve_updater(request):

    if request.POST.get('action') == 'post':
        chosen_user_id = request.POST.get('chosenUserId')
        chosen_user = Members.objects.get(member=chosen_user_id)
        previous_recieve_message_len = request.POST.get('count_recieve_messages')

        all_recieve_messages = TblMessageUser.objects.filter(sender=chosen_user,reciver=request.user.member).order_by('id')

        # deletes the notifs for this chat page for this user
        if TblMessageUserNotification.objects.filter(notif__reciver = request.user.member , notif__sender__member = chosen_user_id ).exists():
            TblMessageUserNotification.objects.filter(notif__reciver = request.user.member, notif__sender__member = chosen_user_id).delete()
        

        if len(all_recieve_messages) > int(previous_recieve_message_len):
            newMessage = all_recieve_messages.last()

            json='1'
            text = newMessage.text
            time = str(newMessage.create_hour.hour) +':'+str(newMessage.create_hour.minute)


        else:
            json = '0'
            text='0'
            time='0'

        return JsonResponse({'result': json,'text':text,'time':time,'len_recieve_message':str(len(all_recieve_messages)),})

@login_required
def inform(request):

    if request.method == "POST":
        form = TblInform_FORM(request.POST)
        if form.is_valid():  
            obj = form.save()
            obj.Creater_UserID = request.user
            obj.save()
            return HttpResponseRedirect('/inform_list')

    form = TblInform_FORM()
    context = {
        'Title' : 'اطلاع رسانی',
        'form' : form,
    }
    
    return render(request, 'inform.html', context)


@login_required
def inform_list(request):

    all_informs = TblInform.objects.filter(Status = 1)


    context = {
        'all_informs' : all_informs,
    }
    return render(request,'inform_list.html',context)

@login_required
def edit_inform(request,id):

    inform = TblInform.objects.get(id=id)
    form = TblInform_FORM(request.POST or None, instance=inform)
    if request.method == "POST":
        if form.is_valid():  
            obj = form.save()
            obj.Creater_UserID = request.user
            obj.save()
            return HttpResponseRedirect('/inform_list')

    context = {
        'Title' : 'اطلاع رسانی',
        'form' : form,
    }
    
    return render(request, 'inform.html', context)

@login_required
def score_formula(request):

    formula=TblScoreFormula.objects.all()

    if request.method == "POST":
        if len(formula) >= 1:
            formula.delete()

        percentages = request.POST.getlist('indicatorScore')

        obj = TblScoreFormula()
        obj.like =int(percentages[0])
        obj.followers =int(percentages[1])
        obj.use_knowledge =int(percentages[2])
        obj.knowledge_seen =int(percentages[3])
        obj.registered_knowledge_count =int(percentages[4])
        obj.save()

        return HttpResponseRedirect(reverse('home'))

    if len(formula) >= 1:
       obj_formula =formula[0]
       formula_exists=1

    else:
       obj_formula ="None"
       formula_exists=0


    context={
        'obj_formula':obj_formula,
        'formula_exists':formula_exists,
    }

    return render(request,'score_formula.html',context)



@login_required
def delete_inform(request,id):
    obj_inform = TblInform.objects.filter(id=id)
    obj_inform.delete()
    return HttpResponseRedirect('/inform_list')


@login_required
def used_knowlege(request):
    my_used_knowledges = []
    my_knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9)).filter(CreatorUserID=request.user.member)
    used = TblUsedKnowledge.objects.filter(knowledge__in=my_knowledges)
    for item in used :
        my_used_knowledges.append(item.knowledge)
    set_used = set(my_used_knowledges)

    context = {
        'used_knowledge' : set_used,
    }
    return render(request,'used_knowlege.html',context)

@login_required
def used_Question_knowledge(request):
    Tbl_used_vote = TblUsedQuestionKnowledge.objects.all()
    Tbl_knowledgeRequest = TblKnowledgeRequest.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        if Tbl_used_vote.filter(Questionknowledge=post_id, creater_user_id=request.user.member).exists():
            Tbl_used_vote.filter(Questionknowledge=post_id, creater_user_id=request.user.member).delete()
            
            result = len(Tbl_used_vote.filter(Questionknowledge=post_id))  
            color = ''

        else:
            obj_vote = TblUsedQuestionKnowledge()
            obj_vote.creater_user_id = request.user
            obj_vote.Questionknowledge = Tbl_knowledgeRequest.get(id=post_id)
            obj_vote.save()

            result = len(Tbl_used_vote.filter(Questionknowledge=post_id))  

            color='green'

        return JsonResponse({'result': result,'color' : color})

@login_required
def used_Question_Request(request):
    Tbl_used_vote = TblUsedQuestionRequest.objects.all()
    Tbl_QuestionRequest = TblQuestionRequest.objects.all()
    if request.POST.get('action') == 'post':
        result = ''
        post_id = request.POST.get('postid')
        if Tbl_used_vote.filter(QuestionkRequest=post_id, creater_user_id=request.user.member).exists():
            Tbl_used_vote.filter(QuestionkRequest=post_id, creater_user_id=request.user.member).delete()
            
            result = len(Tbl_used_vote.filter(QuestionkRequest=post_id))  
            color = ''

        else:
            obj_vote = TblUsedQuestionRequest()
            obj_vote.creater_user_id = request.user
            obj_vote.QuestionkRequest = Tbl_QuestionRequest.get(id=post_id)
            obj_vote.save()

            result = len(Tbl_used_vote.filter(QuestionkRequest=post_id))  

            color='green'

        return JsonResponse({'result': result,'color' : color})


@login_required
def score_of_users(request):
    all_users = Members.objects.all()

    search_user = request.GET.get('search')
    if search_user != None and search_user != '':
        all_users = all_users.filter(Q(first_name__contains=search_user) | Q(last_name__contains=search_user))



    p = Paginator(all_users, 12)
    page = request.GET.get('page')
    users = p.get_page(page)

    context = {
        'all_users' : all_users,
        'users':users,
        'Title' : 'لیست امتیاز کاربران'
    }
    

    return render(request, 'score_of_users.html',context )

@login_required
def report_reward_users(request):
    users = Members.objects.all()
    today_year = get_persian_year_normalized()
    context =dict()
    context.update({
        'users':users,
    })

         
    if request.method == 'POST':
        show_all_users_reward = int(request.POST.get('send_to_all'))
        selected_user = request.POST.get('members')
        # show all users reward
        if show_all_users_reward == 2 :
            rewards = TblUserRewards.objects.filter(date = today_year )

        else:
            rewards = TblUserRewards.objects.filter(date = today_year ).filter(user = request.user)

        context.update({
        'rewards':rewards,
        })





    return render(request, 'report_reward_users.html',context )


@login_required
def chatroom(request,id):


    context = {

    }
    return render(request, 'score_of_users.html',context )



@login_required
def edit_experts(request):

    expert_members = Members.objects.filter(groups__name='Expert')
    
    html_chart = create_chart_tree(None)

    context = {
        'expert_members' : expert_members,
        'html_chart' : html_chart,
    }

    return render(request, 'edit_experts.html',context )


@login_required
def view_experts_list(request):
    """Ajax func for displaying the experts"""

    if request.POST.get('action') == 'post':
        result = ''
        expert_id = request.POST.get('user')
        what_typeof_roles = ExpertChart.objects.filter(member__in=expert_id)
        json = "["
        for item in what_typeof_roles:
            if len(json) > 1:
                json += ","
            json += "{\"id\":\"" + str(item.id) + \
                    "\", \"text\":\"" + item.chart + "\"}"
            json += "]"
        return JsonResponse({'result': result},json)


def report_knowledge(request):

    knowledges = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9) | Q(register_status=8))
    members=Members.objects.all()
    html_chart = create_chart_tree(None)

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        from_date_chekbox = request.POST.get('from_date_check_box')
        to_date = request.POST.get('to_date')
        to_date_chekbox = request.POST.get('to_date_check_box')

        knowledge_keywords_chekbox = request.POST.get('key_words_check_box')

        key_words_text = request.POST.getlist('key_words_text')


        knowledge_title = request.POST.get('knowledge_title')
        knowledge_title_checkbox = request.POST.get('knowledge_title_check_box')

        KnowledgeIsGroup = request.POST.get('KnowledgeIsGroup')
        knowledge_is_group_checkbox = request.POST.get('group_check_box')


        KnowledgeIsSpecial = request.POST.get('KnowledgeIsSpecial')
        knowledge_is_special_checkbox = request.POST.get('special_knowledge_check_box')


        KnowledgePermission = request.POST.get('KnowledgePermission')
        Knowledge_permission_checkbox = request.POST.get('is_secret_check_box')

        user_registered_knowledge = request.POST.get('members')
        user_registered_knowledge_checkbox = request.POST.get('member_check_box')

        id_chart = request.POST.get('id_KnowledgeProcess')
        id_chart_checkbox = request.POST.get('chart_check_box')


        if from_date_chekbox is not None and to_date_chekbox:
            if from_date and to_date:
                    from_date = int(''.join(from_date.split('/')))
                    to_date = int(''.join(to_date.split('/')))
                    knowledges = knowledges.filter(
                        CreateDate__gte=from_date,
                        CreateDate__lte=to_date)


        elif from_date_chekbox is not None:
            if to_date == "" and not from_date == "":
                    from_date = int(''.join(from_date.split('/')))
                    knowledges = knowledges.filter(CreateDate__gte=from_date)

        elif to_date_chekbox is not None:
            if from_date == "" and not to_date == "":
                    to_date = int(''.join(to_date.split('/')))
                    knowledges = knowledges.filter(CreateDate__lte=to_date)

        if user_registered_knowledge_checkbox is not None:
            knowledges = knowledge_advance_search ( knowledges = knowledges , creator_user = user_registered_knowledge )

        if knowledge_keywords_chekbox is not None:
            knowledges = knowledge_advance_search ( knowledges = knowledges , search_keyword = key_words_text )

        if knowledge_title_checkbox is not None:
            knowledges = knowledge_advance_search ( knowledges = knowledges , search_title = knowledge_title )



        if id_chart_checkbox is not None :
            if id_chart is not None and id_chart != "":
                selected_chart = TblChart.objects.get(Chart=id_chart)
                if selected_chart.Parent is not None :
                    chart_children = TblChart.objects.filter(location__startswith=selected_chart.location).filter(ChartType=3).filter(Status=1).values_list('Chart', flat=True)
                    knowledges = knowledges.filter(KnowledgeProcess__in = chart_children)
            
        if knowledge_is_group_checkbox is not None:
            if KnowledgeIsGroup == '1':
                knowledges = knowledges.filter(KnowledgeIsGroup = '1')
            elif KnowledgeIsGroup == '2':
                knowledges = knowledges.filter(KnowledgeIsGroup = '2')

        if knowledge_is_special_checkbox is not None:
            if KnowledgeIsSpecial == '1':
                knowledges = knowledges.filter(KnowledgeIsSpecial = '1')
            elif KnowledgeIsSpecial == '2':
                knowledges = knowledges.filter(KnowledgeIsSpecial = '2')

        if Knowledge_permission_checkbox is not None:
            if KnowledgePermission == '1':
                knowledges = knowledges.filter(KnowledgePermission = '1')
            elif KnowledgePermission == '2':
                knowledges = knowledges.filter(KnowledgePermission = '2')

    context = {
        'members' : members,
        'knowledges' : knowledges,
        'html_chart': html_chart,
    }
    return render(request, 'report_knowledge.html',context)

def compare_knowledge_percent(request):

    max_key = 1
    comparing_dict = {}
    if request.POST.get('action') == 'post':
        input_value = request.POST.get('input_value')
        knowledge_id = request.POST.get('knowledge_id')
        knowledge = TblKnowledge.objects.get(KnowledgeCode=knowledge_id)
        knowledge_words_loop = TblKnowledge.objects.filter(Q(register_status=7) | Q(register_status=9))
        for item in knowledge_words_loop:
            if item.KnowledgeCode != int(knowledge_id):
                temp_text_summary = item.KnowledgeTextSummary
                current_splited_title = knowledge.KnowledgeTitle.split(' ')
                temp_splited_title = item.KnowledgeTitle.split(' ')
                
                len_current_splited_title = len(current_splited_title)
                len_temp_splited_title = len(temp_splited_title)
                title_result = len(set(temp_splited_title) & set(current_splited_title))
                sum_split_titles = len_current_splited_title + len_temp_splited_title - title_result
                title_point = (title_result / sum_split_titles) * 100

                temp_keywords = item.KnowledgeKeywords
                if temp_keywords != None:

                    splited_temp_keywords = re.split('; |, |،',temp_keywords)
                    current_keywords = knowledge.KnowledgeKeywords
                    if current_keywords == None:
                        current_keywords = 'سلام'
                    splited_current_keywords = re.split('; |, |،',current_keywords)

                    len_splited_temp_keywords = len(splited_temp_keywords)
                    len_splited_current_keywords = len(splited_current_keywords)
                    words_result = len(set(splited_temp_keywords) & set(splited_current_keywords))
                    sum_words = len_splited_temp_keywords + len_splited_current_keywords - words_result
                    words_point = (words_result / sum_words ) * 100
                    total_point = words_point + title_point
                    total_point = total_point / 2

                    if words_result >= 2:
                        replaced_pattern = re.compile('|'.join(splited_current_keywords))
                        pattern = re.compile(r'{}'.format(replaced_pattern.pattern))
                        value = spaces_between_words_dict(pattern,temp_text_summary)
                        final_result_point = value + total_point

                        if final_result_point >= int(input_value):
                            comparing_dict[item.KnowledgeCode]=final_result_point

                            if len(comparing_dict) != 0:
                                max_key = max(comparing_dict, key=comparing_dict.get)
                                knowledges = TblKnowledge.objects.filter(KnowledgeCode=max_key)
                            
                            if len(comparing_dict) == 0:
                                json = "["
                                json += "{\"knowledge_id\":\"" +'هیج داده ای با این درصد وجود ندارد' + \
                                        "\"}"
                                json += "]"
                                return JsonResponse(json,safe=False)
            else:
                continue
        else :

            json = "["
            for item in knowledges:
                if len(json) > 1:
                    json += ","
                json += "{\"knowledge_id\":\"" + str(item.KnowledgeCode) + \
                        "\", \"title\":\"" + item.KnowledgeTitle + \
                        "\", \"user_id\":\"" + str(item.CreatorUserID.first_name) + ' '+ str(item.CreatorUserID.last_name) + \
                        "\", \"knowledge_Type\":\"" + str(item.Type) + \
                        "\", \"knowledge_created_date\":\"" + str(item.CreateDate) + \
                        "\"}"
            json += "]"
            return JsonResponse(json,safe=False)




@login_required
def notifications_homepage(request):

    result = km_notifications(request.user)
    
    context = {
        'all_notifs' : result[0],
        'len_of_notifs' : result[1],
    }
    return render(request,'notifications_homepage.html',context)


@login_required
def get_notif_count_km(request):

    result = km_notifications(request.user)

    return JsonResponse({'response': result[1],})



@login_required
def valuable_knowledges(request):
    today_date = str(get_persian_date_normalized())
    
    knowledges = TblKnowledge.objects.filter(Status__gte=0).filter(Q(register_status=7) | Q(register_status=9)).raw('''
    select * from KnowledgeManagement_tblknowledge
    where ( %s - CreateDate) >=10000
    ''',[today_date])

    context = {
        'Knowledges':knowledges,
    }
    return render(request,'valuable_knowledges.html',context)


@login_required
def expert_review_report(request,id):
    knowledge = TblKnowledge.objects.get(KnowledgeCode = id)

    expert_reviews_this_knowledge = TblExpertReview.objects.filter( knowledge = knowledge ).filter(set_number = knowledge.set_number )

    context = {
        'expert_reviews':expert_reviews_this_knowledge,
    }
    return render(request,'expert_reviews_knowledge_report.html',context)



@login_required
def kpi_expert_review_report(request,id):
    expert_review = TblExpertReview.objects.get( id = id )
    expert_review_kpis = TblKpiExpertReview.objects.filter( expert_review = expert_review )

    context = {
        'kpis':expert_review_kpis,
    }
    return render(request,'expert_reviews_kpis.html',context)


@login_required
def kpi_knowledges(request,id):
    kpi = TblKeyIndicator.objects.get( id = id )
    expert_review_kpis = TblKpiExpertReview.objects.filter( kpi = kpi )


    context = {
        'kpis':expert_review_kpis,
    }
    return render(request,'kpis_knowledegs.html',context)

@login_required
def document_list_report(request):

    show_button = 1
    html_chart = create_chart_tree(None)
    document = Documentation.objects.filter(Status__gte=0)
    members = Members.objects.all()

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        from_date_chekbox = request.POST.get('from_date_check_box')

        to_date = request.POST.get('to_date')
        to_date_chekbox = request.POST.get('to_date_check_box')

        document_Title = request.POST.get('document_Title')
        Title_check_box = request.POST.get('Title_check_box')

        document_keywords = request.POST.get('document_keywords')
        key_words_check_box = request.POST.get('key_words_check_box')

        user_registered_document = request.POST.get('members')
        user_registered_document_checkbox = request.POST.get('member_check_box')

        id_chart = request.POST.get('id_KnowledgeProcess')
        id_chart_checkbox = request.POST.get('chart_check_box')

        if from_date_chekbox is not None and to_date_chekbox:
            if from_date and to_date:
                    from_date = int(''.join(from_date.split('/')))
                    to_date = int(''.join(to_date.split('/')))
                    document = document.filter(
                        CreateDate__gte=from_date,
                        CreateDate__lte=to_date)

        elif from_date_chekbox is not None:
            if to_date == "" and not from_date == "":
                    from_date = int(''.join(from_date.split('/')))
                    document = document.filter(CreateDate__gte=from_date)

        elif to_date_chekbox is not None:
            if from_date == "" and not to_date == "":
                    to_date = int(''.join(to_date.split('/')))
                    document = document.filter(CreateDate__lte=to_date)
        
        if id_chart_checkbox is not None :
            if id_chart is not None and id_chart != "":
                selected_chart = TblChart.objects.get(Chart=id_chart)
                if selected_chart.Parent is not None :
                    chart_children = TblChart.objects.filter(location__startswith=selected_chart.location).filter(ChartType=3).filter(Status=1).values_list('Chart', flat=True)
                    document = document.filter(KnowledgeProcess__in = chart_children)


        if user_registered_document_checkbox is not None:
            if int(user_registered_document) != -1:
                document = document.filter(CreatorUserID=user_registered_document)


        if key_words_check_box is not None:
            if document_keywords != "" and document_keywords is not None:
                document = document.filter(KnowledgeKeywords__contains=document_keywords)

        if document_Title is not None:
            if Title_check_box is not None and Title_check_box != "":
                knowledges = knowledges.filter(KnowledgeTitle__contains = document_Title)


    context = {
        'html_chart' : html_chart,
        'show_button' : show_button,
        'members' : members,
        'document': document,
        'Title': 'گزارش مستندات',
    }
    return render(request,'document_list_report.html',context)

@login_required
def edit_thinking_room(request,id):

    if not is_knowlege_worker(request.user):
        return HttpResponseRedirect(reverse('login'))

    obj_jalase = get_object_or_404(TblJalase, JalaseCode=id)
    
    if TblJalase.objects.filter(JalaseCode=id).exists():
        obj_jalase = TblJalase.objects.get(JalaseCode=id)

        voice_name = obj_jalase.voice_url

        if TblVoiceRecord.objects.filter(voice_url = voice_name).exists():
            voice = TblVoiceRecord.objects.get(voice_url = voice_name).voice_record.url
        else:
            voice = 0

        if obj_jalase.KnowledgePermission.KnowledgePermission == 1:
            permission_knowledge=1
        else:
            permission_knowledge=2

            
        len_team=len(TblTeam_Jalase.objects.filter(JalaseCode=id))
        obj_files=FeedFile_Jalase.objects.filter(feed=id)    
        jalase_form = TblJalaseForm(request.POST or None , instance = obj_jalase)
        html_chart = create_chart_tree(None)

        if request.method == "POST":
            
            audio_name = request.POST.get('hidden_audio')
            if audio_name != '':
                if TblVoiceRecord.objects.filter(voice_url = voice_name).exists():
                    TblVoiceRecord.objects.filter(voice_url = voice_name).delete()
                audio = audio_name + '.mp3'
                obj = jalase_form.save()
                obj.voice_url = audio
                obj.save()

            if jalase_form.is_valid():
                obj=jalase_form.save()
                obj.save()

            if jalase_form.cleaned_data['JalaseKeywords'] is not None:
                keywords = jalase_form.data['JalaseKeywords']
                keywords = keywords.strip()
            else:
                keywords=''
            
            doc_files_title = request.POST.getlist('docTitle')
            doc_files=request.FILES.getlist('Allfiles')
            if len(doc_files) !=0 and len(doc_files_title) !=0 and len(doc_files) == len(doc_files_title) :
                for itemFile,itemTitle in zip(doc_files,doc_files_title):
                    obj_file_doc=FeedFile_Jalase()
                    obj_file_doc.file=itemFile
                    obj_file_doc.title=itemTitle
                    obj_file_doc.feed=TblJalase.objects.get(JalaseCode=obj.JalaseCode)
                    obj_file_doc.save()


            memebers_to_save = request.POST.getlist('member')
            join_percentage=request.POST.getlist('percentageJoin')

            if len(join_percentage) > 1:
                if all(flag.isdigit() for  flag in join_percentage):
                    join_percentage=list(map(int, join_percentage))
                else:
                    join_percentage=[0]

            TblTeam_Jalase.objects.filter(JalaseCode=obj_jalase.JalaseCode).delete()

            if len(join_percentage) > 1:
                if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                    for item,percentage in zip(memebers_to_save,join_percentage):
                        obj_Team = TblTeam_Jalase()
                        obj_Team.joinPercentage=percentage
                        obj_Team.JalaseCode = obj
                        obj_Team.TeamMember = Members.objects.get(member=item)
                        obj_Team.save()
                else:
                    memebers = Members.objects.all()
                    team = TblTeam_Jalase.objects.filter(JalaseCode=obj_jalase.JalaseCode).exclude(TeamMember=request.user.member)
                    if TblTeam_Jalase.objects.filter(JalaseCode=obj_jalase.JalaseCode,TeamMember=request.user.member).exists():
                        userPercentage = TblTeam_Jalase.objects.get(JalaseCode=obj_jalase.JalaseCode,TeamMember=request.user.member)
                        userPercentage=userPercentage.joinPercentage
                    else:
                        userPercentage=-1
                    context = {
                        'errors': 'درصد چه کسی درست نیست',
                        'team': team,
                        'voice' : voice ,
                        'userPercentage':userPercentage,
                        'members': memebers,
                        'teamCount': team.count(),
                        'TblJalaseForm': jalase_form,
                        'KnowledgeProcess': obj_jalase.KnowledgeProcess,
                        'UserId': request.user.member,
                        'html_chart': html_chart,
                        'permission_knowledge' : permission_knowledge ,
                        'obj_files':obj_files,
                        'len_team':len_team,
                        'id':id,
                        'edit':'edit',
                    }
                    return render( request,'thinking_room.html',context)

            return HttpResponseRedirect('/thinking_room_list/')
        memebers = Members.objects.all()
        team = TblTeam_Jalase.objects.filter(JalaseCode=obj_jalase.JalaseCode).exclude(TeamMember=request.user.member)
        if TblTeam_Jalase.objects.filter(JalaseCode=obj_jalase.JalaseCode,TeamMember=request.user.member).exists():
            userPercentage = TblTeam_Jalase.objects.get(JalaseCode=obj_jalase.JalaseCode,TeamMember=request.user.member)
            userPercentage=userPercentage.joinPercentage
        else:
            userPercentage=-1
        context = {
                'team': team,
                'userPercentage':userPercentage,
                'members': memebers,
                'teamCount': team.count(),
                'TblJalaseForm': jalase_form,
                'KnowledgeProcess': obj_jalase.KnowledgeProcess,
                'errors': str(jalase_form.errors),
                'UserId': request.user.member,
                'html_chart': html_chart,
                'permission_knowledge' : permission_knowledge ,
                'obj_files':obj_files,
                'len_team':len_team,
                'edit':'edit',
                'id':id,
                'voice' : voice ,

            }
        return render(
                request,
                'thinking_room.html',
                context
            )
    return HttpResponseRedirect('/thinking_room_list/')


@login_required
def user_activity_report(request):

    members = Members.objects.all()


    p = Paginator(members, 12)
    page = request.GET.get('page')
    users = p.get_page(page)
    nums = "a" * users.paginator.num_pages

    context = {
    'members' : members,
    'users':users,
    'Title' : 'لیست کاربران',
    'nums':nums,
    }
    return render(request,'user_activity_report.html',context)


@login_required
def give_user_reward(request):

    members = Members.objects.all().exclude(member = request.user.member)
    all_knowledges = TblKnowledge.objects.all()
    this_year = get_persian_year_normalized()
    form = TblUserRewardsForm(request.POST or None)
    get_user = request.POST.get('members')
    get_user_knowledges = TblKnowledge.objects.filter(CreatorUserID = get_user)
    if request.method == "POST" : 
        if form.is_valid():
            obj = form.save()
            obj.user = Members.objects.get(member = get_user)
            max_user_kpi = TblKpiExpertReview.objects.filter(knowledge__in = get_user_knowledges).aggregate(Max('percent'))
            if max_user_kpi['percent__max'] == None:
                max_user_kpi = 0
            else :
                max_user_kpi = max_user_kpi['percent__max'] 

            max_kpi = TblKpiExpertReview.objects.filter(knowledge__in = all_knowledges).aggregate(Max('percent'))
            if max_kpi['percent__max'] == None:
                max_kpi = 0
            else :
                max_kpi = max_kpi['percent__max'] 
            max_user_score = Members.objects.filter(Status = 1).aggregate(Max('score'))
            if max_user_score['score__max'] == None:
                max_user_score = 0
            else :
                max_user_score = max_user_score['score__max'] 

            user_score = score_calculator(get_user)
            reward = user_score + max_user_kpi + obj.admin_point / max_kpi + 100 + max_user_score * obj.salary * obj.base_salary_cofficent
            obj.reward = int(reward)
            if TblUserRewards.objects.filter(date = this_year).filter(user = Members.objects.get(member = get_user)).exists():
                TblUserRewards.objects.filter(date = this_year).filter(user = Members.objects.get(member = get_user)).delete()
            obj.save()

            return HttpResponseRedirect('/report_reward_users/')

            

    context = {
        'members' : members ,
        'form' : form ,
    }
    return render(request,'give_user_reward.html',context)


def get_user_score(request):

    user_id = request.POST.get('user_id')
    user_score = Members.objects.get(member = user_id)

    return JsonResponse({'score':user_score.score,})

@login_required
def knowledge_decition_tree(request):

    comparing_dict_knowledge = {}
    comparing_dict_solution = {}
    context = dict()

    knowledges = TblKnowledge.objects.filter(Status=1).filter(Q(register_status=7) | Q(register_status=9))
    if request.method == 'POST':

        knowledge_keyword = request.POST.getlist('knowledge_keyword')
        matching_percent1 = request.POST.get('matching_percent1')
        
        sulotion_keyword = request.POST.getlist('sulotion_keyword')
        matching_percent2 = request.POST.get('matching_percent2')

        splited_knowledge_keyword = knowledge_keyword[0].split('_')
        splited_sulotion_keyword = sulotion_keyword[0].split('_')

        splited_knowledge_keyword.pop(-1)
        splited_sulotion_keyword.pop(-1)
        
        knowledge_pattern = re.compile('|'.join(splited_knowledge_keyword))
        solution_pattern = re.compile('|'.join(splited_sulotion_keyword))

        for item in knowledges:
            knowledge_summary = item.KnowledgeTextSummary
            solution_summary = item.KnowledgeWhichAction

            knowledge_value = spaces_between_words_dict(knowledge_pattern,knowledge_summary)
            

            if int(knowledge_value) >= int(matching_percent1) :
                comparing_dict_knowledge[item.KnowledgeCode]=knowledge_value

                solution_value = spaces_between_words_dict(solution_pattern,solution_summary)
                if int(solution_value) >= int(matching_percent2) :
                    comparing_dict_solution[item.KnowledgeCode]=solution_value

                    if len(comparing_dict_solution) != 0:
                        max_key = max(comparing_dict_solution, key=comparing_dict_solution.get)
                        knowledges = TblKnowledge.objects.get(KnowledgeCode=max_key)

                    elif len(comparing_dict_solution) == 0 and len(comparing_dict_knowledge) != 0 :
                        max_key = max(comparing_dict_knowledge, key=comparing_dict_knowledge.get)
                        knowledges = TblKnowledge.objects.get(KnowledgeCode=max_key)
            elif len(comparing_dict_knowledge) == 0 :
                        
                context.update({
                        'msg_box' : 'هیچ راه حلی وجود ندارد ' ,
                    })


            
    context.update({
        'knowledges' : knowledges ,
    })

    return render(request,'knowledge_decition_tree.html',context)