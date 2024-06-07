import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from quiztest.models import *


class QuizConsumer(AsyncWebsocketConsumer):
    connected_users = {}
    users_completed = 0
    total_users = 0
    user_scores = {}
    game_state = {
        'current_question': 0,
        'quizType': '',
        'question': {},
        'answers': {},
        'numOfUsers': 0,
    }
    timer_task = None

    @sync_to_async
    def load_initial_game_state(self):
        QuizConsumer.game_state['quizType'] = self.scope['url_route']['kwargs']['title']
        self.quiz_id = Quizzes.objects.get(title=QuizConsumer.game_state['quizType']).id

        question_id = self.question_ids[0]
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        question_title = question.title
        answers_list = [{'id': answer.id, 'text': answer.answer_text, 'is_right': answer.is_right} for answer in answers]

        QuizConsumer.game_state['numOfUsers'] = QuizConsumer.total_users
        QuizConsumer.game_state['current_question'] = 0
        QuizConsumer.game_state['question'] = question_title
        QuizConsumer.game_state['answers'] = answers_list

    async def broadcast_game_state(self):
        message = {
            'type': 'game_state',
            'game_state': QuizConsumer.game_state
        }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def start_timer(self):
        await asyncio.sleep(15)  # 15-second timer
        if QuizConsumer.users_completed < QuizConsumer.total_users:
            await self.process_user_answers(move_to_next_question=True)

    async def connect(self):
        self.room_group_name = 'quiz_group'
        self.username = self.scope['user'].username
        self.score = 0
        self.answer_id = None  # Track user answer ID
        QuizConsumer.connected_users[self.username] = self
        QuizConsumer.total_users += 1

        session = self.scope['session']
        self.question_ids = session.get('question_ids', [])
        if not self.question_ids:
            await self.close()
            return

        await self.accept()

        await self.load_initial_game_state()
        await self.broadcast_game_state()
        await self.broadcast_user_list()

        if QuizConsumer.total_users == 1:
            if not self.timer_task or self.timer_task.done():  # Check if no timer task or the previous task is done
                self.timer_task = asyncio.create_task(self.start_timer())  # Start the timer for solo play

    async def disconnect(self, close_code):
        if self.username in QuizConsumer.connected_users:
            del QuizConsumer.connected_users[self.username]
        QuizConsumer.total_users -= 1

        await self.broadcast_user_list()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_action = text_data_json.get('type')

        if user_action == 'answer_selected':
            QuizConsumer.users_completed += 1

            username = self.username
            await self.broadcast_user_selection(username)
            self.answer_id = text_data_json.get('answer_id')

            if QuizConsumer.users_completed >= QuizConsumer.total_users:
                if self.timer_task:
                    self.timer_task.cancel()  # Cancel the current timer
                await self.process_user_answers(move_to_next_question=True)
                if not self.timer_task or self.timer_task.done():  # Start new timer only if no previous task or it's done
                    self.timer_task = asyncio.create_task(self.start_timer())  # Start the timer for the next question

    async def process_user_answers(self, move_to_next_question=False):
        correct_answer_id = None
        for answer in QuizConsumer.game_state['answers']:
            if answer["is_right"]:
                correct_answer_id = answer['id']
                break

        question_id = self.question_ids[QuizConsumer.game_state['current_question']]
        question = await sync_to_async(Question.objects.get)(id=question_id)

        if correct_answer_id == self.answer_id:
            if question.difficulty == 1:
                self.score += 1
            elif question.difficulty == 2:
                self.score += 1.5
            elif question.difficulty == 3:
                self.score += 2

        if move_to_next_question:
            # Ensure we are within the range of questions
            if QuizConsumer.game_state['current_question'] < len(self.question_ids) - 1:
                QuizConsumer.game_state['current_question'] += 1
                QuizConsumer.users_completed = 0
                self.answer_id = None  # Reset answer_id for the next question

                # Update game state and broadcast it
                await self.update_game_state()
                await self.broadcast_game_state()
                await self.broadcast_user_list()

                # Restart timer for the new question
                if self.timer_task:
                    self.timer_task.cancel()
                self.timer_task = asyncio.create_task(self.start_timer())
            else:
                # No more questions, handle the end of the quiz
                await self.end_quiz()

    @sync_to_async
    def update_game_state(self):
        if QuizConsumer.game_state['current_question'] < len(self.question_ids):
            question_id = self.question_ids[QuizConsumer.game_state['current_question']]
            question = Question.objects.get(id=question_id)
            answers = Answer.objects.filter(question=question)
            question_title = question.title
            answers_list = [{'id': answer.id, 'text': answer.answer_text, 'is_right': answer.is_right} for answer in answers]

            QuizConsumer.game_state['numOfUsers'] = QuizConsumer.total_users
            QuizConsumer.game_state['question'] = question_title
            QuizConsumer.game_state['answers'] = answers_list

    async def end_quiz(self):
        message = {
            'type': 'quiz_end',
            'final_scores': [{'username': username, 'score': consumer.score} for username, consumer in QuizConsumer.connected_users.items()]
        }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def broadcast_user_selection(self, username):
        message = {
            'type': 'user_selection',
            'username': username,
        }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def broadcast_user_list(self):
        user_list = [{'username': username, 'score': consumer.score} for username, consumer in
                     QuizConsumer.connected_users.items()]
        message = {
            'type': 'user_list',
            'users': user_list
        }

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
