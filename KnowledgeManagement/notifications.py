from KnowledgeManagement.models import TblExamNotification, TblKnowledgeNotificationForEliteUsers, TblKnowledgeRequestNotification, TblKnowledgeStatusNotification, TblMessageUserNotification, TblQuestionRequestNotification, TblSurveyotification
from itertools import chain



def is_expert(user):
    return user.groups.filter(name='Expert').exists()


def is_IT(user):
    return user.groups.filter(name='IT').exists()

def is_Security(user):
    return user.groups.filter(name='Security').exists()

def km_notifications(user):
    """
    notifications for KM app

    """

    #if user has no relation to it and expert he recieve nothing(used this method because i cant refrence object before i assign it)
    IT_has_notification = TblKnowledgeNotificationForEliteUsers.objects.filter(notif_type=99)
    IT_has_notification_len = 0
    Expert_has_notification = TblKnowledgeNotificationForEliteUsers.objects.filter(notif_type=99)
    Expert_has_notification_len = 0
    Security_has_notification = TblKnowledgeNotificationForEliteUsers.objects.filter(notif_type=99)
    Security_has_notification_len = 0
    
    exam_notif = TblExamNotification.objects.filter(user=user)
    exam_notif_len = len(exam_notif)

    survey_notif = TblSurveyotification.objects.filter(user=user)
    survey_notif_len = len(survey_notif)

    knowledge_request_notif = TblKnowledgeRequestNotification.objects.filter(user=user)
    knowledge_request_notif_len = len(knowledge_request_notif)

    question_request_notif = TblQuestionRequestNotification.objects.filter(user=user)
    question_request_notif_len = len(question_request_notif)

    message_notif = TblMessageUserNotification.objects.filter(notif__reciver = user.member)     
    message_notif_len = len(message_notif)


    knowledge_status_notif = TblKnowledgeStatusNotification.objects.filter(notif__CreatorUserID = user)      
    knowledge_status_notif_len = len(knowledge_status_notif)
    
    
    if is_IT(user) and TblKnowledgeNotificationForEliteUsers.objects.filter(user=user).filter(notif_type=10) :

        IT_has_notification = TblKnowledgeNotificationForEliteUsers.objects.filter(notif_type=10).filter(user=user)
        IT_has_notification_len = len(IT_has_notification)

    if is_expert(user) and TblKnowledgeNotificationForEliteUsers.objects.filter(user=user).filter(notif_type=11) :
        
        Expert_has_notification = TblKnowledgeNotificationForEliteUsers.objects.filter(notif_type=11).filter(user=user)

        Expert_has_notification_len = len(Expert_has_notification)

    if is_Security(user) and TblKnowledgeNotificationForEliteUsers.objects.filter(user=user).filter(notif_type=12) :
        
        Security_has_notification = TblKnowledgeNotificationForEliteUsers.objects.filter(notif_type=12).filter(user=user)

        Security_has_notification_len = len(Security_has_notification)
    
    all_notifs = list(chain(exam_notif, survey_notif,knowledge_request_notif,question_request_notif,message_notif,knowledge_status_notif,IT_has_notification,Expert_has_notification,Security_has_notification))
    len_of_notifs = survey_notif_len + exam_notif_len + knowledge_request_notif_len + question_request_notif_len + message_notif_len + knowledge_status_notif_len + IT_has_notification_len + Expert_has_notification_len + Security_has_notification_len

    result_notification = []
    result_notification.append(all_notifs)
    result_notification.append(len_of_notifs)
    return result_notification