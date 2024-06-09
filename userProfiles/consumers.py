import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from quiztest.models import *

class QuizConsumer(AsyncWebsocketConsumer):
    # Maximum number of users required to start the quiz
    maxUsers = 1

    # Initialize class variables
    connected_users = {}
    user_scores = {}
    total_users = 0
    users_completed = 0
    game_state = {
        "current_question": 0,
        "quizType": "",
        "question": {},
        "answers": {},
        "numOfUsers": 0,
    }
    timer_task = None
    all_answers_received = False

    @sync_to_async
    def load_initial_game_state(self):
        # Load initial game state from the database
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
        # Broadcast the current game state to all connected users
        message = {"type": "game_state", "game_state": QuizConsumer.game_state}
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def start_timer(self):
        # Start a 15-second timer for each question
        await asyncio.sleep(15)
        if self.all_answers_received:
            await self.process_user_answers(move_to_next_question=True)
        else:
            await self.process_user_answers()

    async def connect(self):
        self.room_group_name = "quiz_group"
        self.username = self.scope["user"].username
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.score = 0
        print("Current Session ID: " + self.session_id)

        QuizConsumer.connected_users[self.username] = self
        self.answer_id = None
        QuizConsumer.total_users += 1

        # Retrieve question IDs from session
        session = self.scope["session"]
        self.question_ids = session.get("question_ids", [])

        if not self.question_ids:
            await self.close()
            return

        await self.accept()
        await self.load_initial_game_state()

        # Start the quiz if the required number of users are connected
        if QuizConsumer.total_users == QuizConsumer.maxUsers:
            print("SESSION IS CLOSED NOW")
            await self.close_session()
            await self.broadcast_game_state()
            await self.broadcast_user_list()
            if not QuizConsumer.timer_task or QuizConsumer.timer_task.done():
                print("timer on connect")
                QuizConsumer.timer_task = asyncio.create_task(self.start_timer())

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
            # Handle user answer selection
            username = self.username
            self.answer_id = text_data_json.get("answer_id")
            QuizConsumer.users_completed += 1
            await self.broadcast_user_selection(username)

            if QuizConsumer.users_completed >= QuizConsumer.total_users:
                self.all_answers_received = True

    @sync_to_async
    def process_user_answer(self):
        # Process the user's selected answer and update their score if correct
        if self.answer_id:
            selected_answer = Answer.objects.get(id=self.answer_id)
            if selected_answer.is_right:
                self.score += 1 #score increases by 1...for future purposes this will be modified to consider the difficulty level of the question and add the corresponding score 
        self.answer_id = None

    async def process_user_answers(self, move_to_next_question=False):
        if move_to_next_question:
            # Move to the next question if within the range of questions
            if QuizConsumer.game_state["current_question"] < len(self.question_ids) - 1:
                QuizConsumer.game_state["current_question"] += 1

                for consumer in QuizConsumer.connected_users.values():
                    await consumer.process_user_answer()

                QuizConsumer.users_completed = 0
                await self.update_game_state()
                await self.broadcast_game_state()
                await self.broadcast_user_list()

                if self.timer_task:
                    self.timer_task.cancel()
                self.timer_task = asyncio.create_task(self.start_timer())
                self.all_answers_received = False
            else:
                # End the quiz if there are no more questions
                for consumer in QuizConsumer.connected_users.values():
                    await consumer.process_user_answer()

                QuizConsumer.users_completed = 0
                await self.update_game_state()
                await self.broadcast_game_state()
                await self.broadcast_user_list()

                print("No More Questions")
                if self.timer_task:
                    self.timer_task.cancel()
                await self.end_quiz()
        else:
            await self.process_user_answers(move_to_next_question=True)

    @sync_to_async
    def update_game_state(self):
        # Update the game state with the next question and answers
        question_id = self.question_ids[QuizConsumer.game_state["current_question"]]
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question)
        question_title = question.title
        answers_list = [
            {"id": answer.id, "text": answer.answer_text, "is_right": answer.is_right}
            for answer in answers
        ]

        QuizConsumer.game_state["numOfUsers"] = QuizConsumer.total_users
        QuizConsumer.game_state["question"] = question_title
        QuizConsumer.game_state["answers"] = answers_list

    @database_sync_to_async
    def update_score_in_db(self):
        # Update the user's score in the leaderboard
        leaderboard_entry, created = Leaderboard.objects.get_or_create(user=self.scope['user'])
        if leaderboard_entry.score < self.score: #checks that the current score from that session is greater than the user's previous highest score and updates accordingly 
            leaderboard_entry.score = self.score
            leaderboard_entry.save()

    @database_sync_to_async
    def get_session(self, session_id):
        # Retrieve a session from the database
        try:
            return Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return None

    @database_sync_to_async
    def close_session(self):
        # Close the quiz session
        session = Session.objects.get(id=self.session_id)
        session.QuizStatus = "CLOSED"
        session.save()

    async def end_quiz(self):
        # End the quiz and send final scores to all users
        message = {
            "type": "quiz_end",
            "final_scores": [
                {"username": username, "score": consumer.score}
                for username, consumer in QuizConsumer.connected_users.items()
            ],
        }
        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
            
        await self.update_score_in_db() #leaderboard updated at the end of the quiz 

    async def broadcast_user_list(self):
        # Broadcast the list of users and their scores
        user_list = [
            {"username": username, "score": consumer.score}
            for username, consumer in QuizConsumer.connected_users.items()
        ]
        message = {"type": "user_list", "users": user_list}

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))

    async def broadcast_user_selection(self, username):
        # Broadcast the user's selection to all connected users
        message = {
            "type": "user_selection",
            "username": username,
        }

        for consumer in QuizConsumer.connected_users.values():
            await consumer.send(text_data=json.dumps(message))
