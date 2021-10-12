from django.db import models

from authentication.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="categories", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Quiz(models.Model):
    category = models.ForeignKey(Category, related_name="quizzes", on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ("id",)

    def __str__(self):
        return self.title
        
        
class QuestionUpdated(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Question(QuestionUpdated):
    SCALE = (
        (0, 'Fundamental'),
        (1, 'Beginner'),
        (2, 'Intermedia'),
        (3, 'Advanced'),
        (4, 'Expert'),
    )

    TYPE = (
        (0, "Multiple choice"),
    )

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.DO_NOTHING)
    technique = models.IntegerField(choices=TYPE, default=0)
    title = models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=SCALE, default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ("id",)

    def __str__(self):
        return self.title


class Answer(QuestionUpdated):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.DO_NOTHING)
    answer_text = models.CharField(max_length=255)
    is_right = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering = ("id",)
