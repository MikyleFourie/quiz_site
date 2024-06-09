import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json
from quiztest.models import *
from django.db.models import F


class QuizConsumer(AsyncWebsocketConsumer):
    # QuizConsumer object is made up of:
    # maxUsers constant
    # list of Connected Users
    # list of user scores
    # number tracking total_users
    # number tracking how many users are complete_statement
    # GameState struct contiaining currentQuestion, QuizType, Question, Answers, numOfUsers

    # Change this maxUsers var to change how many people must be in a quiz session for it to start
    maxUsers = 1
    

    connected_users = {}
    user_scores = {}
    total_users = 0
    users_completed = 0
    # global game_state
    game_state = {
        "current_question": 0,
        "quizType": "",
        "question": {},
        "answers": {},
        "numOfUsers": 0,
    }
    timer_task = None
    all_answers_received = False  # Flag to track if all answers are received

    @sync_to_async
    def load_initial_game_state(self):
        QuizConsumer.game_state["quizType"] = self.scope["url_route"]["kwargs"]["title"]
        self.quiz_id = Quizzes.objects.get(title=QuizConsumer.game_state["quizType"]).id

        question_id = self.question_ids[0]
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        question_title = question.title
        answers_list = [
            {"id": answer.id, "text": answer.answer_text, "is_right": answer.is_right}
            for answer in answers
        ]

        QuizConsumer.game_state["numOfUsers"] = QuizConsumer.total_users
        QuizConsumer.game_state["current_question"] = 0
        QuizConsumer.game_state["question"] = question_title
        QuizConsumer.game_state["answers"] = answers_list

    async def broadcast_game_state(self):
        message = {"type": "game_state", "game_state": QuizConsumer.game_state}
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def start_timer(self):
        # print("timer started")
        await asyncio.sleep(15)  # 15-second timer
        # print("timer ended")
        if self.all_answers_received:
            await self.process_user_answers(
                move_to_next_question=True
            )  # Process if all answers are received
        else:
            await self.process_user_answers()  # Process user answers when timer expires

    async def connect(self):
        self.room_group_name = "quiz_group"
        self.username = self.scope["user"].username
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.score = 0
        print("Current Session ID: " + self.session_id)

        QuizConsumer.connected_users[self.username] = self  # Need to write this line again everytime we want to update the connected_users
        self.answer_id = None  # Clear user answer ID
        QuizConsumer.total_users += 1

        # Gets question from the request.session (check views.py)
        session = self.scope["session"]
        self.question_ids = session.get("question_ids", [])

        if not self.question_ids:
            await self.close()
            return

        await self.accept()
        await self.load_initial_game_state()  # calls load intial game state func
        
        if QuizConsumer.total_users == QuizConsumer.maxUsers:
            print("SESSION IS CLOSED NOW")
            await self.close_session()
            await self.broadcast_game_state()
            await self.broadcast_user_list()  # broadcasts to users
            if not QuizConsumer.timer_task or QuizConsumer.timer_task.done():  # Check if no timer task or the previous task is done
                print("timer on connect")
                QuizConsumer.timer_task = asyncio.create_task(
                    self.start_timer()
                ) 
        


    async def disconnect(self, close_code):
        if self.username in QuizConsumer.connected_users:
            del QuizConsumer.connected_users[self.username]
        QuizConsumer.total_users -= 1

        await self.broadcast_user_list()
        
        if QuizConsumer.total_users == 0:
            await self.end_quiz()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_action = text_data_json.get("type")

        if user_action == "answer_selected":
            # Broadcast user's selection to all connected users
            username = self.username
            self.answer_id = text_data_json.get("answer_id")
            QuizConsumer.users_completed += 1
            await self.broadcast_user_selection(username)

            # scoring logic

            if QuizConsumer.users_completed >= QuizConsumer.total_users:
                self.all_answers_received = True
                # Get users answer and correct answer

                # correct_answer = QuizConsumer.game_state.answers.filter(is_correct=True).first()
                # for answer in QuizConsumer.game_state['answers']:
                # if answer["is_right"]==True :
                # correct_answer_id = answer['id']

                # compare and add to score

                # Progresses to next question?

                # Process user answers before moving to the next question

                # Reset users_completed to 0 for the next question
                # QuizConsumer.users_completed = 0

                # if not at the end of quiz
                # if QuizConsumer.game_state['current_question'] < len(self.question_ids):
                # await self.broadcast_user_list()
            # await self.update_game_state()
            # await self.broadcast_game_state()

    @sync_to_async
    def process_user_answer(self):
        if self.answer_id:
            selected_answer = Answer.objects.get(id=self.answer_id)
            if selected_answer.is_right:
                self.score += 1  # Update the score if the answer is correct
        # Reset user answer ID for the next question
        self.answer_id = None

        # for answer in QuizConsumer.game_state['answers']:
        # if answer["is_right"]==True :
        # correct_answer_id = answer['id']

    async def process_user_answers(self, move_to_next_question=False):
        if move_to_next_question:
            # Ensure we are within the range of questions
            if QuizConsumer.game_state["current_question"] < len(self.question_ids) - 1:
                QuizConsumer.game_state["current_question"] += 1  # move index to next question

                # Process all user answers before moving to the next question
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
                for consumer in QuizConsumer.connected_users.values():
                    await consumer.process_user_answer()

                # Reset users_completed to 0
                QuizConsumer.users_completed = 0

                # Update game state and broadcast it
                await self.update_game_state()
                await self.broadcast_game_state()
                await self.broadcast_user_list()

                print("No More Questions")
                if self.timer_task:
                    self.timer_task.cancel()
                await self.end_quiz()
        else:
            # If move_to_next_question is False, it means the timer expired
            # In this case, process the user answers and move to the next question
            await self.process_user_answers(move_to_next_question=True)

    @sync_to_async
    def update_game_state(self):
        if QuizConsumer.game_state["current_question"] < len(self.question_ids):
            question_id = self.question_ids[QuizConsumer.game_state["current_question"]]
            question = Question.objects.get(id=question_id)
            answers = Answer.objects.filter(question=question)
            question_title = question.title
            answers_list = [
                {
                    "id": answer.id,
                    "text": answer.answer_text,
                    "is_right": answer.is_right,
                }
                for answer in answers
            ]

            QuizConsumer.game_state["numOfUsers"] = QuizConsumer.total_users
            QuizConsumer.game_state["question"] = question_title
            QuizConsumer.game_state["answers"] = answers_list

    @database_sync_to_async
    def update_score_in_db(self):
        leaderboard_entry, created = Leaderboard.objects.get_or_create(user=self.scope['user'])
        print(leaderboard_entry.score)
        if leaderboard_entry.score < self.score:
            leaderboard_entry.score = self.score
            leaderboard_entry.save()

    @sync_to_async
    def update_game_state(self):
        # gets new question and answers
        question_id = self.question_ids[QuizConsumer.game_state["current_question"]]
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        question = question.title
        answers_list = [
            {"id": answer.id, "text": answer.answer_text, "is_right": answer.is_right}
            for answer in answers
        ]

        QuizConsumer.game_state["numOfUsers"] = QuizConsumer.total_users
        QuizConsumer.game_state["question"] = question
        QuizConsumer.game_state["answers"] = answers_list

    @database_sync_to_async
    def get_session(self, session_id):
        try:
            return Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return None

    @database_sync_to_async
    def close_session(self):
        session = Session.objects.get(id=self.session_id)
        session.QuizStatus = "CLOSED"
        session.save()

    async def end_quiz(self):
        
        message = {
            "type": "quiz_end",
            "final_scores": [
                {"username": username, "score": consumer.score}
                for username, consumer in QuizConsumer.connected_users.items()
            ],
        }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
            
        await self.update_score_in_db()

    async def broadcast_user_list(self):
        user_list = [
            {"username": username, "score": consumer.score}
            for username, consumer in QuizConsumer.connected_users.items()
        ]
        message = {"type": "user_list", "users": user_list}

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def broadcast_user_selection(self, username):

        message = {
            "type": "user_selection",
            "username": username,
        }

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))