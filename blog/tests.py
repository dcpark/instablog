from django.test import TestCase
from django.test import Client
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from .models import Post

User = get_user_model()

class PostTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='hello', password='helloworld')

        self.post1 = Post()
        self.post1.title = '첫번째 테스트 게시물'
        self.post1.content = '테스트 게시물입니다.'
        self.post1.user = self.u1
        self.post1.save()

    def test_add(self):
        self.assertTrue(1 == 1)

    def test_failed_create_post(self):
        new_post = Post()
        new_post.title = 'hello'
        new_post.content = 'world'

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                new_post.save()



    def test_create_post(self):
        new_post = Post()
        new_post.user = self.u1
        new_post.title = 'hello'
        new_post.content = 'world'
        new_post.save()

        self.assertIsNotNone(new_post.pk)

        exists = Post.objects.filter(pk=new_post.pk).exists()
        self.assertTrue(exists)



    def test_client_detail_post(self):
        c = Client()

        p = Post()
        p.user = self.u1
        p.title = 'qqqq'
        p.content = 'zzzz'
        p.save()

        url = reverse('blog:detail', kwargs={'pk':p.pk})
        res = c.get(url)

        self.assertEqual(res.status_code, 200)


    def test_save_post_by_model(self):
        '''Post 모델을 이용해 데이터를 저장하는 테스트.
        검증 방법 : 저장한 뒤 모델 매니저로 저장한 데이터를 가져와서 비교
        '''
        p1 = Post()
        p1.user = self.u1
        p1.title = '테스트'
        p1.content = '테스트입니다.'
        p1.save()

        p2 = Post.objects.get(pk=p1.pk)

        self.assertTrue(p1.pk == p2.pk)




    def test_failed_save_post_by_model(self):
        '''Post 모델을 이용해 데이터를 저장할 때 실패하는 경우에 대한 테스트
        '''

        #에러가 발생하는 다른 케이스를 찾아봤는데
        #user를 이용한 방법밖에 없는거 같아서
        #위에있는 코드랑 모양이 똑같아 졌습니다..
        p1 = Post()
        p1.title = 'hello'
        p1.content = 'world'

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                p1.save()

    def test_get_post_by_url(self):
        '''Django Test Client를 이용해 특정 게시물을 보는 url로 접근하는 테스트
        '''
        client = Client()

        url = reverse('blog:detail', kwargs={'pk':self.post1.pk})
        res = client.get(url)

        self.assertEqual(res.status_code, 200)


    def test_failed_get_post_by_url(self):
        '''Django Test Client를 이용해 특정 게시물을 보지 못하고
        실패하는 경우에 대한 테스트
        '''
        client = Client()

        url = reverse('blog:detail', kwargs={'pk':20160624})

        with transaction.atomic():
            with self.assertRaises(ObjectDoesNotExist):
                res = client.get(url)
