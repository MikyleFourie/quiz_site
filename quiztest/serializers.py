from rest_framework import serializers
from .models import Quizzes, Question, Answer


class QuizSerializer(serializers.ModelSerializer): #formulates it to be able to use for front end (Javascript)
    
    class Meta:
        model = Quizzes
        fields = [
            'title',
        ]

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = Answer
        fields = [
            'id',
            'answer_text',
            #'is_right',
        ]

class RandomQuestionSerializer(serializers.ModelSerializer):

    answer = AnswerSerializer(many=True, read_only=True)

    class Meta:
    
        model = Question
        fields = [
            'title','answer',
        ]


class QuestionSerializer(serializers.ModelSerializer):

    answer = AnswerSerializer(many=True, read_only=True)
    quiz = QuizSerializer(read_only=True) #gets quiz title

    class Meta:
    
        model = Question
        fields = [
            'quiz','title','answer',
        ]