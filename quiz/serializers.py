from rest_framework import serializers

from .models import *
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = ("answer_text", "is_right", "question_id")


class QuestionSerializer(serializers.ModelSerializer):
    quiz_id = serializers.IntegerField()
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('technique',
                  'title',
                  'difficulty',
                  'is_active',
                  'quiz_id', "answers")


class QuizSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField()
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ("title", "category_id", "questions")


class CategorySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("title", "owner", "quizzes")
