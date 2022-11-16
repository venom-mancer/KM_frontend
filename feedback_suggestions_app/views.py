
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from KnowledgeManagement.models import Members, TblChart
from django.urls import resolve, reverse
from feedback_suggestions_app.models import TblCommitteeSpecialty, TblIndicatorAssesment, TblSendSuggestionItToCommittee , TblSuggestion , TblExpertReviewIndicatorAssessment, TblSuggestionTeam,TblRejectSuggestionByIt , TblExpertReview_suggestion, TblWorkingGroupReview_suggestion, TblWorkingGroupSpecialty  , TblIndicatorAssesment_workingroup, TblWorkingroupReviewIndicatorAssessment
from django.db.models import Q
from django.contrib.auth.models import Group
from KnowledgeManagement.views import create_chart_tree, is_IT
from feedback_suggestions_app.forms import TblIndicatorAssesment_Form , TblExpertReview_suggestionForm ,TblSuggestionForm , TblRejectSuggestionByIt_Form , TblIndicatorAssesment_workingroupForm , TblWorkingGroupReview_suggestionForm

@login_required
def home(request):
    return render(request,'templates_feedback/Home.html')

@login_required
def submit_suggestion(request):

    members = Members.objects.all()
    form = TblSuggestionForm()

    context = {
        'teamCount': 1,
        'members' : members,
        'form':form,
    }

    if request.method == "POST":
        memebers_to_save = request.POST.getlist('member')
        join_percentage=request.POST.getlist('percentageJoin')

        if len(join_percentage) > 1:
            if all(flag.isdigit() for  flag in join_percentage):
                join_percentage=list(map(int, join_percentage))
            else:
                join_percentage=[0]

        form = TblSuggestionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.creator_user_id = request.user
            obj.save()
            if len(join_percentage) > 1:
                if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                    for item,percentage in zip(memebers_to_save,join_percentage):
                        obj_Team = TblSuggestionTeam()
                        obj_Team.join_percentage=percentage
                        obj_Team.suggestion_id = obj
                        obj_Team.user = Members.objects.get(member=item)
                        obj_Team.save()
                else:
                    context.update({
                    'errors': 'درصد مشارکت گروهی  درست نیست',
                    'form':form,
                    })
                    return render(request, 'templates_feedback/submit_suggestion.html',context )

            return HttpResponseRedirect(reverse('suggestion_list'))


    return render(request, 'templates_feedback/submit_suggestion.html',context )



@login_required
def edit_submit_suggestion(request , id):
    obj_suggestion = get_object_or_404(TblSuggestion, id=id)
    if obj_suggestion.register_status < 4 and obj_suggestion.creator_user_id == request.user:
        members = Members.objects.all()
        team_users = TblSuggestionTeam.objects.filter(suggestion_id = obj_suggestion).exclude(user = request.user)

        form = TblSuggestionForm(request.POST or None , instance=obj_suggestion)


        context = {
            'form':form,
            'obj_suggestion':obj_suggestion,
            'team_users':team_users,
            'members':members,
            'teamCount': 1,
        }


        if TblSuggestionTeam.objects.filter(suggestion_id = obj_suggestion ,user = request.user ).exists():
            this_user_percentage = TblSuggestionTeam.objects.get(suggestion_id = obj_suggestion ,user = request.user )
            context.update({
            'this_user_percentage':this_user_percentage
            })

        if form.is_valid() and request.method == 'POST' :
            memebers_to_save = request.POST.getlist('member')
            join_percentage=request.POST.getlist('percentageJoin')

            if len(join_percentage) > 1:
                if all(flag.isdigit() for  flag in join_percentage):
                    join_percentage=list(map(int, join_percentage))
                else:
                    join_percentage=[0]


            obj=form.save()

            TblSuggestionTeam.objects.filter(suggestion_id=obj_suggestion).delete()

            if len(join_percentage) > 1:
                if sum(join_percentage) == 100 and len(join_percentage) == len(memebers_to_save):
                    for item,percentage in zip(memebers_to_save,join_percentage):
                        obj_Team = TblSuggestionTeam()
                        obj_Team.join_percentage=percentage
                        obj_Team.suggestion_id = obj
                        obj_Team.user = Members.objects.get(member=item)
                        obj_Team.save()
                else:
                    context.update({
                    'errors': 'درصد مشارکت گروهی  درست نیست',
                    'form':form,
                    })
                    return render(request, 'templates_feedback/edit_submit_suggestion.html',context )

            return HttpResponseRedirect(reverse('suggestion_list'))



        return render(request, 'templates_feedback/edit_submit_suggestion.html',context )
    else:
        return HttpResponseRedirect(reverse('suggestion_list'))



@login_required
def suggestion_list(request):

    suggestions = TblSuggestion.objects.filter(creator_user_id=request.user).filter(status__gte=0)


    context = {
        'suggestions' : suggestions ,
    }

    return render(request, 'templates_feedback/suggestion_list.html',context )


@login_required
def delete_submit_suggestion(request,id):

    suggest_obj = TblSuggestion.objects.filter(id=id)

    try:
        suggest_obj.delete()
    
    except:
        suggest_obj = TblSuggestion.objects.get(id=id)
        suggest_obj.status = -1
        suggest_obj.save()

    return HttpResponseRedirect(reverse('suggestion_list'))


@login_required
def send_user_suggestion_it(request,id):

    """
    sends the suggestion of the user to it
    """

    suggest_obj = TblSuggestion.objects.get(id=id)
    suggest_obj.register_status = 2
    suggest_obj.save()

    return HttpResponseRedirect(reverse('suggestion_list'))



@login_required
def public_section_list(request):

    suggestions = TblSuggestion.objects.filter(Q (register_status=2) | Q (register_status = 5) | Q (register_status = 7)).filter(status__gte=0)

    context = {
        'suggestions' : suggestions,
    }
    return render (request , 'templates_feedback/public_section_list.html',context)


@login_required
def rejected_public_section(request,id):

    suggestion = TblSuggestion.objects.get(id=id)
    form = TblRejectSuggestionByIt_Form()

    if request.method == "POST":
        form = TblRejectSuggestionByIt_Form(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.commenter = request.user
            obj.suggestion_id = suggestion
            suggestion.register_status = 3
            suggestion.save()
            obj.save()
            return HttpResponseRedirect(reverse('public_section_list'))
    context = {
        'form' : form,
    }
    return render (request , 'templates_feedback/rejected_public_section.html',context)


@login_required
def accepted_public_section(request,id):

    suggestion_obj = TblSuggestion.objects.get(id = id)

    html_chart = create_chart_tree(None)

    if request.method == "POST":
        opnion = request.POST.get('opnion')
        specialty = request.POST.get('suggestion_specialty')

        # the radio button in the page
        radio_button = request.POST.get('isSpecial')

        obj = TblSendSuggestionItToCommittee() 
        obj.suggestion_id = suggestion_obj
        obj.explenation = opnion
        obj.user_id = request.user
        obj.save()


        if int(radio_button) == 1 :
            if specialty != '':
                suggestion_obj.suggestion_specialty = TblChart.objects.get(Chart = specialty)

        else:
            suggestion_obj.suggestion_specialty = None
            

        if suggestion_obj.register_status == 5:
            suggestion_obj.register_status = 6
        
        elif suggestion_obj.register_status == 7:
            suggestion_obj.register_status = 8
        else:
            suggestion_obj.register_status = 4
        suggestion_obj.save()

        return HttpResponseRedirect(reverse('public_section_list'))


    
    context = {
        'html_chart' : html_chart,
        'suggestion_obj':suggestion_obj
    }
    return render (request , 'templates_feedback/accepted_public_section.html',context)


@login_required
def accepted_proficiency_section(request):

    context = {

    }
    return render (request , 'templates_feedback/accepted_proficiency_section.html',context)

@login_required
def rejected_proficiency_section(request):

    context = {

    }
    return render (request , 'templates_feedback/rejected_proficiency_section.html',context)



@login_required
def suggestion_list_committee(request):

    suggestions = TblSuggestion.objects.filter(status__gte=0).filter(register_status=4)

    context = {
        'suggestions' : suggestions,
    }
    return render(request , 'templates_feedback/suggestion_list_committee.html',context)


@login_required
def committee_comment(request,id):
    
    indicators = TblIndicatorAssesment.objects.filter(Status__gte=0)
    if request.method == "POST":
        scores=request.POST.getlist('indicatorScore')
        form = TblExpertReview_suggestionForm(request.POST)
        if form.is_valid():
            obj_review = form.save()
            obj_review.suggestion =TblSuggestion.objects.get(id=id)
            obj_review.save()
            
            for indicator,score in zip(indicators,scores):
                committee_assessment = TblExpertReviewIndicatorAssessment()
                committee_assessment.committee_review = obj_review
                committee_assessment.indicator_assessment=indicator
                committee_assessment.score=score
                committee_assessment.save()
            suggest_obj = TblSuggestion.objects.get(id=id)
            suggest_obj.register_status = 5
            suggest_obj.save()
            return HttpResponseRedirect(reverse('committee_comment_resultpoint',kwargs={'id': obj_review}))


    context={
        'indicators' : indicators,
        'Title': 'بررسی و نظر',
        'TblExpertReviewForm' : TblExpertReview_suggestionForm(),
    }

    return render(request , 'templates_feedback/committee_comment.html',context)


@login_required
def committee_comment_resultpoint(request,id):

    committee_review = TblExpertReview_suggestion.objects.get(id=id)
    committee_review_scores = TblExpertReviewIndicatorAssessment.objects.filter(committee_review=committee_review)
    
    mean_items = []
    for item in committee_review_scores:
        score = item.score
        weight = item.indicator_assessment.indicator_point
        mean = weight * score
        mean_items.append(mean)
    total_score = sum(mean_items)/len(mean_items)
    committee_review.committe_given_score = total_score
    committee_review.save()
    
    context = {
        'total_score' : total_score,
    }
    return render(request , 'templates_feedback/committee_comment_resultpoint.html',context)


@login_required
def indicator_assessment(request):

    form = TblIndicatorAssesment_Form()
    if request.method == "POST":
        form = TblIndicatorAssesment_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('indicator_assessment_list'))
        else:
            context = {
                'error' : 'بارم شاخص نمیتواند بیش از 10 باشد'
            }
            return render(request, 'templates_feedback/indicator_assessment.html', context)
    context = {
        'form' : form,
    }
    return render(request , 'templates_feedback/indicator_assessment.html',context)


@login_required
def indicator_assessment_list(request):

    indicator = TblIndicatorAssesment.objects.filter(Status__gte=0)

    context = {
        'indicator' : indicator,
        'Title' : 'لیست شاخص های ارزیاب'
    }

    return render(request , 'templates_feedback/indicator_assessment_list.html',context)


@login_required
def delete_indicator_assessment(request,id):

    indicator = TblIndicatorAssesment.objects.get(id=id)
    indicator.Status=-1
    indicator.save()
    return HttpResponseRedirect(reverse('indicator_assessment_list'))


@login_required
def edit_indicator_assessment(request,id):

    obj_indicator = get_object_or_404(TblIndicatorAssesment, id=id)
    indicator = TblIndicatorAssesment_Form(request.POST or None ,instance=obj_indicator)
    point_value = obj_indicator.indicator_point
    text_value = obj_indicator.indicator
    if request.method == "POST":
        points = request.POST.get('indicator_point')
        if indicator.is_valid():
            indicator.save()
            return HttpResponseRedirect(reverse('indicator_assessment_list'))
        else:
            text_value = obj_indicator.indicator
            context = {
                'error' : 'بارم شاخص نمیتواند بیش از 10 باشد',
                'text_value' : text_value,
            }
        return render(request,'templates_feedback/indicator_assessment.html',context)
    context = {
        'indicator' : indicator,
        'Title' : 'ویرایش شاخص کلیدی ارزیاب',
        'point_value': point_value,
        'text_value' : text_value,
    }

    return render(request,'templates_feedback/indicator_assessment.html',context)


@login_required
def suggestion_paperwork(request,id):

    suggest = TblSuggestion.objects.get(id=id)
    suggest_owner = Members.objects.get(member = suggest.creator_user_id.member)
    team = TblSuggestionTeam.objects.filter(suggestion_id=id).exclude(user=suggest_owner)
    if TblSuggestionTeam.objects.filter(suggestion_id=id,user=request.user.member).exists():
        userPercentage = TblSuggestionTeam.objects.get(suggestion_id=id,user=request.user.member)
        userPercentage=userPercentage.join_percentage

    else:
        userPercentage=-1

    context = {
        'suggest_owner' : suggest_owner,
        'suggest' : suggest,
        'team' : team,
        'userPercentage' : userPercentage,
    }
    return render(request , 'templates_feedback/suggestion_paperwork.html',context)


@login_required
def reject_suggestion_reason(request,id):

    reject_reason = TblRejectSuggestionByIt.objects.filter(suggestion_id=id)

    context = {
        'reject_reason' : reject_reason[::-1],
    }
    return render(request , 'templates_feedback/reject_suggestion_reason.html',context)


@login_required
def mailroom_accepted_suggestion_comment(request,id):

    comments = TblSendSuggestionItToCommittee.objects.filter(suggestion_id=id)

    context = {
        'comments' : comments[::-1],
    }
    return render(request , 'templates_feedback/mailroom_accepted_suggestion_comment.html',context)

@login_required
def committee_comment_for_mailroom(request,id):

    comments = TblExpertReview_suggestion.objects.filter(suggestion=id)

    context = {
        'comments' : comments[::-1],
        'title':'کمیته',
    }
    return render(request , 'templates_feedback/committee_comment_for_mailroom.html',context)


@login_required
def working_group_comment_for_mailroom(request,id):

    comments = TblWorkingGroupReview_suggestion.objects.filter(suggestion=id)

    context = {
        'comments' : comments[::-1],
        'title':'کارگروه',
    }
    return render(request , 'templates_feedback/committee_comment_for_mailroom.html',context)

@login_required
def committe_specialty(request):
    if not is_IT(request.user):
        return HttpResponseRedirect('/login')

    html_chart = create_chart_tree(None)
    users=Members.objects.all()

    if request.method == "POST":

        #gives the member the Committee Role.
        selected_user = request.POST.get('members')
        expert_group = Group.objects.get(name='Committee') 
        expert_group.user_set.add(selected_user)

        #gives the member the chosen charts.
        charts = request.POST.getlist('chart')
        for chart in charts:
            #checks if the member had the chart before or not
            if  not TblCommitteeSpecialty.objects.filter(specialty=TblChart.objects.get(Chart=chart)).exists():
                obj_specialty = TblCommitteeSpecialty()
                obj_specialty.user=Members.objects.get(member=selected_user)
                obj_specialty.specialty=TblChart.objects.get(Chart=chart)
                obj_specialty.save()

        return HttpResponseRedirect(reverse('home_feedback'))

    context={
        'members':users,
        'html_chart': html_chart,
        'title':'تعریف کمیته'
    }

    return render(request, 'templates_feedback/committe_specialty.html', context)


@login_required
def working_group_specialty(request):
    if not is_IT(request.user):
        return HttpResponseRedirect('/login')

    html_chart = create_chart_tree(None)
    users=Members.objects.all()

    if request.method == "POST":

        #gives the member the working group Role.
        selected_user = request.POST.get('members')
        expert_group = Group.objects.get(name='WorkingGroup') 
        expert_group.user_set.add(selected_user)

        #gives the member the chosen charts.
        charts = request.POST.getlist('chart')
        for chart in charts:
            #checks if the member had the chart before or not
            if  not TblWorkingGroupSpecialty.objects.filter(specialty=TblChart.objects.get(Chart=chart)).exists():
                obj_specialty = TblWorkingGroupSpecialty()
                obj_specialty.user=Members.objects.get(member=selected_user)
                obj_specialty.specialty=TblChart.objects.get(Chart=chart)
                obj_specialty.save()

        return HttpResponseRedirect(reverse('home_feedback'))

    context={
        'members':users,
        'html_chart': html_chart,
        'title':'تعریف کارگروه'
    }

    return render(request, 'templates_feedback/committe_specialty.html', context)


@login_required
def work_ingroup_suggesstion_list(request):
    suggestions = TblSuggestion.objects.filter(status__gte=0).filter(register_status=6)

    context = {
        'suggestions' : suggestions,
    }
    return render(request , 'templates_feedback/work_ingroup_suggesstion_list.html',context)


@login_required
def work_ingroup_indicator_assessment(request):

    form = TblIndicatorAssesment_workingroupForm()
    if request.method == "POST":
        form = TblIndicatorAssesment_workingroupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('work_ingroup_indicator_assessment_list'))
        else:
            context = {
                'error' : 'بارم شاخص نمیتواند بیش از 10 باشد'
            }
            return render(request, 'templates_feedback/work_ingroup_indicator_assessment.html', context)
    context = {
        'form' : form,
    }
    return render(request , 'templates_feedback/work_ingroup_indicator_assessment.html',context)



@login_required
def work_ingroup_indicator_assessment_list(request):

    workin_group_indicator = TblIndicatorAssesment_workingroup.objects.filter(Status__gte=0)

    context = {
        'workin_group_indicator' : workin_group_indicator,
        'Title' : 'لیست شاخص های ارزیابکار گروه'
    }

    return render(request , 'templates_feedback/work_ingroup_indicator_assessment_list.html',context)


@login_required
def edit_indicator_assessment_work_ingroup(request,id):

    obj_indicator = get_object_or_404(TblIndicatorAssesment_workingroup, id=id)
    indicator = TblIndicatorAssesment_workingroupForm(request.POST or None ,instance=obj_indicator)
    point_value = obj_indicator.indicator_point
    text_value = obj_indicator.indicator
    if request.method == "POST":
        if indicator.is_valid():
            indicator.save()
            return HttpResponseRedirect(reverse('work_ingroup_indicator_assessment_list'))
        else:
            text_value = obj_indicator.indicator
            context = {
                'error' : 'بارم شاخص نمیتواند بیش از 10 باشد',
                'text_value' : text_value,
            }
        return render(request,'templates_feedback/work_ingroup_indicator_assessment.html',context)
    context = {
        'indicator' : indicator,
        'Title' : 'ویرایش شاخص کلیدی ارزیاب',
        'point_value': point_value,
        'text_value' : text_value,
    }

    return render(request,'templates_feedback/work_ingroup_indicator_assessment.html',context)


@login_required
def delete_indicator_assessment_work_ingroup(request,id):

    indicator = TblIndicatorAssesment_workingroup.objects.get(id=id)
    indicator.Status=-1
    indicator.save()
    return HttpResponseRedirect(reverse('work_ingroup_indicator_assessment_list'))


@login_required
def work_ingroup_comment(request,id):
    
    indicators = TblIndicatorAssesment_workingroup.objects.filter(Status__gte=0)
    if request.method == "POST":
        scores=request.POST.getlist('indicatorScore')
        form = TblWorkingGroupReview_suggestionForm(request.POST)
        if form.is_valid():
            obj_review = form.save()
            obj_review.suggestion =TblSuggestion.objects.get(id=id)
            obj_review.save()
            
            for indicator,score in zip(indicators,scores):
                workingroup_assessment = TblWorkingroupReviewIndicatorAssessment()
                workingroup_assessment.workingroup_review = obj_review
                workingroup_assessment.indicator_assessment=indicator
                workingroup_assessment.score=score
                workingroup_assessment.save()
            suggest_obj = TblSuggestion.objects.get(id=id)
            suggest_obj.register_status = 7
            suggest_obj.save()
            return HttpResponseRedirect(reverse('work_ingroup_comment_resultpoint',kwargs={'id': obj_review}))


    context={
        'indicators' : indicators,
        'Title': 'بررسی و نظر',
        'TblwrokingroupReviewForm' : TblWorkingGroupReview_suggestionForm(),
    }

    return render(request , 'templates_feedback/work_ingroup_comment.html',context)


@login_required
def work_ingroup_comment_resultpoint(request,id):

    workingroup_review = TblWorkingGroupReview_suggestion.objects.get(id=id)
    workingroup_review_scores = TblWorkingroupReviewIndicatorAssessment.objects.filter(workingroup_review=workingroup_review)
    
    mean_items = []
    for item in workingroup_review_scores:
        score = item.score
        weight = item.indicator_assessment.indicator_point
        mean = weight * score
        mean_items.append(mean)
    total_score = sum(mean_items)/len(mean_items)
    workingroup_review.workingroup_given_score = total_score
    workingroup_review.save()
    
    context = {
        'total_score' : total_score,
    }
    return render(request , 'templates_feedback/work_ingroup_comment_resultpoint.html',context)