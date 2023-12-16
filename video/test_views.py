
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Video, Video_Likes, Comment, Channel, History

class VideoViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.channel = Channel.objects.create(name='Test Channel', description='Test Description', owner_id=self.user.id)
        self.video = Video.objects.create(title='Test Video', channel=self.channel)

    def test_popular_videos(self):
        # Create some videos with today's timestamp
        for _ in range(5):
            Video.objects.create(title='Popular Video', channel=self.channel, timestamp=timezone.now())

        # Create some videos with different timestamps
        for _ in range(5):
            Video.objects.create(title='Non-Popular Video', channel=self.channel, timestamp=timezone.now() - timezone.timedelta(days=1))

        # Send a GET request to the popular view
        response = self.client.get(reverse('popular'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the popular videos
        self.assertContains(response, 'Popular Video')

    def test_history(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # access the video page
        self.client.get(reverse('show_video', args=[self.video.id]))

        # Send a GET request to the history view
        response = self.client.get(reverse('history'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the user's history
        self.assertContains(response, 'Test Video')


        