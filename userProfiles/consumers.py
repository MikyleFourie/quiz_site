import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from quiztest.models import Quizzes, Question, Answer

class QuizConsumer(AsyncWebsocketConsumer):
    connected_users = {}
    total_users = 0
    users_completed = 0
    user_scores = {}
    game_state = {
        'current_question': 0,
        'quizType': '',
        'question': {},
        'answers': {},
        'numOfUsers': 0,
    }
    timer_task = None
    all_answers_received = False  # Flag to track if all answers are received

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
        if self.all_answers_received:
            await self.process_user_answers(move_to_next_question=True)  # Process if all answers are received
        else:
            await self.process_user_answers()  # Process user answers when timer expires

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
            self.answer_id = text_data_json.get('answer_id')
            QuizConsumer.users_completed += 1  # Increment users_completed when a user submits an answer

            # Broadcast user list to update UI with the latest scores
            await self.broadcast_user_list()

            # If all users have submitted their answers, set the flag
            if QuizConsumer.users_completed >= QuizConsumer.total_users:
                self.all_answers_received = True

    @sync_to_async
    def process_user_answer(self):
        if self.answer_id:
            selected_answer = Answer.objects.get(id=self.answer_id)
            if selected_answer.is_right:
                self.score += 1  # Update the score if the answer is correct
        # Reset user answer ID for the next question
        self.answer_id = None

    async def process_user_answers(self, move_to_next_question=False):
        if move_to_next_question:
            # Ensure we are within the range of questions
            if QuizConsumer.game_state['current_question'] < len(self.question_ids) - 1:
                QuizConsumer.game_state['current_question'] += 1

                # Process user answers before moving to the next question
                for consumer in QuizConsumer.connected_users.values():
                    await consumer.process_user_answer()

                # Reset users_completed to 0 for the next question
                QuizConsumer.users_completed = 0

                # Update game state and broadcast it
                await self.update_game_state()
                await self.broadcast_game_state()
                await self.broadcast_user_list()

                # Restart timer for the new question
                if self.timer_task:
                    self.timer_task.cancel()
                self.timer_task = asyncio.create_task(self.start_timer())

                # Reset the flag for the next question
                self.all_answers_received = False
            else:
                # No more questions, handle the end of the quiz
                await self.end_quiz()
        else:
            # If move_to_next_question is False, it means the timer expired
            # In this case, process the user answers and move to the next question
            await self.process_user_answers(move_to_next_question=True)

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

    async def broadcast_user_list(self):
        user_list = [{'username': username, 'score': consumer.score} for username, consumer in
                     QuizConsumer.connected_users.items()]
        message = {
            'type': 'user_list',
            'users': user_list
        }

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
