from django.test import SimpleTestCase
from django.urls import resolve, reverse
from KnowledgeManagement.views import login_route,home,take_survey,edit_topic_node


class TestUrls(SimpleTestCase):

    def test_loging_route_is_resolved(self):
        url = reverse('loginRoute')
        self.assertEquals(resolve(url).func , login_route ) 


    def test_home_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func , home ) 


    def test_take_survey_is_resolved(self):
        url = reverse('take_survey',args=[1])
        self.assertEquals(resolve(url).func , take_survey )

    def test_edit_topic_node_is_resolved(self):
        url = reverse('EditTopicNode',args=[1,1,'string'])
        self.assertEquals(resolve(url).func , edit_topic_node )