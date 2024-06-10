#from django.test import TestCase, RequestFactory
#from django.contrib.auth.models import User
#from quiztest.models import Leaderboard
#from userProfiles.consumers import QuizConsumer  
#from channels.generic.websocket import AsyncWebsocketConsumer
#from userProfiles.views import leaderboard 

#class TestUpdateScoreInDb(TestCase):
    #def setUp(self):
        # Create a test user
     #   self.user = User.objects.create_user(username='testuser', password='12345')
      #  self.test_object = QuizConsumer(AsyncWebsocketConsumer)  
       # self.test_object.scope = {'user': self.user}
        #self.test_object.score = 10  

    #def test_update_score_in_db(self):
        # Call the method to test
     #   self.test_object.update_score_in_db()

        # Retrieve the leaderboard entry for the test user
      #  leaderboard_entry = Leaderboard.objects.get(user=self.user)

        # Check that the score was updated correctly
       # self.assertEqual(leaderboard_entry.score, self.test_object.score)
 

#class TestLeaderboardView(TestCase):
  #  def setUp(self):
        # Create a test user
   #     self.user = User.objects.create_user(username='testuser', password='12345')
    #    self.factory = RequestFactory()

        # Create a leaderboard entry for the test user
     #   Leaderboard.objects.create(user=self.user, score=10)

    #def test_leaderboard(self):
        # Create a request
     #   request = self.factory.get('/leaderboard')

        # Attach the test user to the request
      #  request.user = self.user

        # Call the view to test
       # response = leaderboard(request)

        # Check that the response has a status code of 200
      #  self.assertEqual(response.status_code, 200)

        # Check that the context data contains the correct leaderboard
       # expected_leaderboard = [{'username': 'testuser', 'highest_score': 10, 'rank': 1}]
        #self.assertEqual(response.context_data['leaderboard'], expected_leaderboard)
