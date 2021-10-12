from django.urls import path

from .views import (CategoryListCreateView
                    , QuizListCreateView
                    , QuestionListCreateView
                    , AnswerListCreateView
                    , AnswerDetailView)


urlpatterns = [
    path('category/', CategoryListCreateView.as_view(), name='category'),
    path('quiz/', QuizListCreateView.as_view(), name='quiz'),
    path('question/', QuestionListCreateView.as_view(), name='question'),
    path('answers/', AnswerListCreateView.as_view(), name='answers'),
    path('answer/<pk>/', AnswerDetailView.as_view(), name='answer'),
]
