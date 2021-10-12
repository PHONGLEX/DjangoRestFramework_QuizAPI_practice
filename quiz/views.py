from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *


class QuizPagination(PageNumberPagination):
    page_size = 20
    page_query_param = "p"
    max_page_size = 100
    page_size_query_param = "count"


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.prefetch_related('quizzes').all()
    pagination_class = QuizPagination
    filter_backends = (SearchFilter,)
    search_fields = ['title', "owner__email"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuizListCreateView(generics.ListCreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Quiz.objects.prefetch_related('questions').all()
    pagination_class = QuizPagination
    filter_backends = (SearchFilter,)
    search_fields = ['title', 'category__title']


class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Question.objects.prefetch_related('answers').all()
    pagination_class = QuizPagination
    filter_backends = (SearchFilter,)
    search_fields = ['quiz__title', 'technique', 'title', 'difficulty', 'is_active']


class AnswerListCreateView(APIView):
    serializer_class = AnswerSerializer

    def get(self, request):
        answers = Answer.objects.all()
        serializer = self.serializer_class(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AnswerSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetailView(APIView):
    serializer_class = AnswerSerializer

    def get(self, request, pk, format=None):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = self.serializer_class(answer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AnswerSerializer)
    def put(self, request, pk, format=None):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = self.serializer_class(instance=answer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @swagger_auto_schema(request_body=AnswerSerializer)
    def delete(self, request, pk, format=None):
        answer = Answer.objects.get(pk=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)