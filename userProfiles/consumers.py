from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json
from quiztest.models import *


class QuizConsumer(AsyncWebsocketConsumer):
    #var to keep track of users
    connected_users = {}
    users_completed = 0
    total_users = 0
    user_scores = {}
    
    #Create a global game_state
    game_state = {
        'current_question': 0,
        # 'quizType': {},
        'quizType': '',
        'question': {},
        'answers': {},
        'numOfUsers': 0,
    }

    
    
    #loads the first question in the database, and all its answers into the game_state /class variable/
    @sync_to_async
    def load_initital_game_state(self):
        QuizConsumer.game_state['quizType']  = self.scope['url_route']['kwargs']['title']
        self.quiz_id = Quizzes.objects.get(title=QuizConsumer.game_state['quizType']).id

        #for a random first question  
        question_id = self.question_ids[0]
        question = Question.objects.get(id = question_id)
        #question = Question.objects.first() #for the first question in database
        answers = Answer.objects.filter(question=question)
        question = question.title
        answers_list = [{'id': answer.id,'text': answer.answer_text, 'is_right': answer.is_right} for answer in answers]
        
        QuizConsumer.game_state['numOfUsers'] = QuizConsumer.total_users
        QuizConsumer.game_state['current_question'] = 0
        QuizConsumer.game_state['question'] = question
        QuizConsumer.game_state['answers'] = answers_list
    
    

    #broadcast game state to all consumers connected to the socket
    async def broadcast_game_state(self):
        message = {
            'type': 'game_state',
            'game_state': QuizConsumer.game_state
            }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))



#On Connect Behaviours----------------------
    async def connect(self):
        
        self.room_group_name = 'quiz_group'
        
        #NEW LOGIC
        self.username = self.scope['user'].username
        self.score = 0
        QuizConsumer.connected_users[self.username] = self #Need to write this line again everytime we want to update the connected_users
        QuizConsumer.total_users += 1

        # Load the question IDs from the session or database
        session = self.scope['session']
        self.question_ids = session.get('question_ids', [])
        if not self.question_ids:
            await self.close()
            return

        await self.accept()
       
        #calls load intial game state func
        await self.load_initital_game_state()
        #calls broadcast game state func
        await self.broadcast_game_state()
        await self.broadcast_user_list()
        

#----------------------------------------------

          
 #On Disconnect Behaviours ----------------------------   
    async def disconnect(self, close_code):
        # Remove the user from the connected users set
        #QuizConsumer.connected_users.remove(self)
        if self.username in QuizConsumer.connected_users:
            del QuizConsumer.connected_users[self.username]
        QuizConsumer.total_users -= 1
        
        await self.broadcast_user_list()
 #-----------------------------------------------------
 
 
 #On Receive Behaviours       
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_action = text_data_json.get('type')

        # Process actions that affect shared state
        #if a single user selects an answer
        if user_action == 'answer_selected':
            QuizConsumer.users_completed += 1
            
            # Broadcast user's selection to all connected users
            username = self.username
            await self.broadcast_user_selection(username)
            self.answer_id = text_data_json.get('answer_id')
            
            #scoring logic
            for answer in QuizConsumer.game_state['answers']:
                    if answer["is_right"]==True :
                        correct_answer_id = answer['id']

            #compare and add to score
            if correct_answer_id == self.answer_id:
                self.score += 1
                
                #add user score ??
            
            if QuizConsumer.users_completed >= QuizConsumer.total_users:
                #Get users answer and correct answer
                
                #correct_answer = QuizConsumer.game_state.answers.filter(is_correct=True).first()
                
            
                #Progresses to next question?
                QuizConsumer.game_state['current_question'] += 1
                QuizConsumer.users_completed = 0
                
                #if not at the end of quiz
                if QuizConsumer.game_state['current_question'] < len(self.question_ids):
                    await self.broadcast_user_list()
                    await self.update_game_state()
                    await self.broadcast_game_state()
                    await self.update_score_in_db()
    
    @database_sync_to_async
    def update_score_in_db(self):
        leaderboard_entry, created = Leaderboard.objects.get_or_create(user=self.scope['user'])
        leaderboard_entry.score = self.score
        leaderboard_entry.save()
                    

    @sync_to_async
    def update_game_state(self):
        #gets new question and answers
        question_id = self.question_ids[QuizConsumer.game_state['current_question']]
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        question = question.title
        answers_list = [{'id': answer.id,'text': answer.answer_text, 'is_right': answer.is_right} for answer in answers]

        QuizConsumer.game_state['numOfUsers'] = QuizConsumer.total_users
        QuizConsumer.game_state['question'] = question
        QuizConsumer.game_state['answers'] = answers_list

        
                
            
            

    async def broadcast_user_selection(self, username):
        message = {
            'type': 'user_selection',
            'username': username,
        }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
            

    #Broadcasts entire list of currently connected Users as user-list. List is contained in 'users'
    async def broadcast_user_list(self):
        #user_list = [consumer.user.username for consumer in QuizConsumer.connected_users]
        user_list = [{'username': username, 'score': consumer.score} for username, consumer in QuizConsumer.connected_users.items()]
        message = {
            'type': 'user_list',
            'users': user_list
        }

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
            
    async def broadcast_all_questions(self):
        message = {
            'type': 'question_ids',
            'question_ids': self.question_ids
            
            }
        
        for consumer in QuizConsumer.connected_users.values():
                await consumer.send(text_data=json.dumps(message))

    
         



    