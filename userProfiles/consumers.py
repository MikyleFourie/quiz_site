from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
import json
from .models import *

class QuizConsumer(AsyncWebsocketConsumer):
    #var to keep track of users
    connected_users = set()
    #Create a global game_state
    game_state = {
        'current_question': 0,
        # 'quizType': {},
        'quizType': "General Knowledge",
        'question': {},
        'answers': {},
    }
    
    #loads the first question in the database, and all its answers into the game_state /class variable/
    @sync_to_async
    def load_initital_game_state(self):
        question = Question.objects.first()
        answers = Answer.objects.filter(question=question)
        question = question.text
        answers_list = [{'text': answer.text, 'is_correct': answer.is_correct} for answer in answers]
        
        QuizConsumer.game_state['question'] = question
        QuizConsumer.game_state['answers'] = answers_list
    
    

    #broadcast game state to all consumers connected to the socket
    async def broadcast_game_state(self):
        message = {
            'type': 'game_state',
            'game_state': QuizConsumer.game_state
            }
        for consumer in QuizConsumer.connected_users:
            await consumer.send(text_data=json.dumps(message))

#On Connect Behaviours----------------------
    async def connect(self):
        self.room_group_name = 'quiz_group'
        self.user = self.scope['user']
        
        QuizConsumer.connected_users.add(self)
        await self.accept()
        await self.broadcast_user_list()

        #calls load intial game state func
        await self.load_initital_game_state()
        #calls broadcast game state func
        await self.broadcast_game_state()
        
#----------------------------------------------

          
 #On Disconnect Behaviours ----------------------------   
    async def disconnect(self, close_code):
        # Remove the user from the connected users set
        QuizConsumer.connected_users.remove(self)
        await self.broadcast_user_list()
 #-----------------------------------------------------
 
 
 #On Receive Behaviours
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_action = text_data_json.get('type')

        # Process actions that affect shared state
        #if a single user selects an answer
        if user_action == 'answer_selected':
            username = self.user.username
            
            # Broadcast user's selection to all connected users
            await self.broadcast_user_selection(username)

    async def broadcast_user_selection(self, username):
        message = {
            'type': 'user_selection',
            'username': username,
        }
        for consumer in QuizConsumer.connected_users:
            await consumer.send(text_data=json.dumps(message))


    async def broadcast_user_list(self):
        user_list = [consumer.user.username for consumer in QuizConsumer.connected_users]
        message = {
            'type': 'user_list',
            'users': user_list
        }

        for consumer in QuizConsumer.connected_users:
            await consumer.send(text_data=json.dumps(message))

    async def send_to_user(self, username, message):
        # Send the message to the specified consumer instance
        for consumer in self.__class__.connected_users:
            if consumer.user.username == username:
                await consumer.send(text_data=json.dumps(message))
         



    