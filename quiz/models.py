from django.db import models


# Create your models here.
class Questions(models.Model):
    question = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.question}"


class CAnswers(models.Model):
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.correct_answer}"


class IAnswers(models.Model):
    incorrect_answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.incorrect_answer}"


class Player(models.Model):
    current_question = models.IntegerField()
    score = models.IntegerField()

    def __str__(self):
        return f"{self.current_question}"
