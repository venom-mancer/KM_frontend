from django.test import TestCase,Client
from django.urls import reverse
from KnowledgeManagement.models import Members , TblInform



class CreateTestUser(TestCase):
    def set_up_create_user(self):
        self.user = Members.objects.create(username='testuser',nationalCode = '1235' , mobileNumber = '094562', date_joined = '2021-11-22')
        self.user.set_password('12345')
        self.user.save()
        self.clinet = Client()
        self.clinet.login(username='testuser', password='12345')




class TestInformLogin(CreateTestUser):

    def create_inform(self):
        self.set_up_create_user()
        self.inform_obj = TblInform.objects.create(from_date= 14001112, to_date=14001112, title='title1', text = 'text', Status = 1, Creater_UserID=self.user)
        self.edit_inform_url = reverse('edit_inform', args= [1])



    def test_inform_list_GET(self):
        self.set_up_create_user()

        inform_list_url = reverse('inform_list')
        response = self.clinet.get(inform_list_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response , 'inform_list.html')


    def test_edit_inform_GET(self):
        self.create_inform()
        
        response = self.clinet.get(self.edit_inform_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response , 'inform.html')


    def test_edit_inform_POST(self):
        self.create_inform()

        response = self.clinet.post(self.edit_inform_url,{
                'from_date': 14011112,
                'to_date':14011112,
                'title' :'title2',
                'text' : 'text2',
                'Status' : 1,
            }
        )

        # overwriting inform_obj
        self.inform_obj = TblInform.objects.get(id = 1)


        self.assertEquals(response.status_code,302)
        self.assertEquals(self.inform_obj.title,'title2')
        self.assertEquals(self.inform_obj.text,'text2')
        self.assertEquals(self.inform_obj.from_date,14011112)


    def test_edit_inform_POST_no_data(self):
        self.create_inform()

        response = self.clinet.post(self.edit_inform_url)

        self.assertEquals(response.status_code,200)


    def test_submit_inform_POST(self):
        self.set_up_create_user()

        response = self.clinet.post(reverse('inform'),{
            'from_date': 14011112,
            'to_date':14011112,
            'title' :'title',
            'text' : 65156,
            'Status' : 1,
        }
        )

        self.assertEquals(response.status_code,302)

    def test_submit_inform_GET(self):
        self.set_up_create_user()

        response = self.clinet.get(reverse('inform'))

        self.assertEquals(response.status_code,200)