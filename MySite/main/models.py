from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=20)
    date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Post(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    writer = models.CharField(max_length=20, default='unknown')
    nickname = models.CharField(max_length=20, default='익명')
    date = models.DateTimeField('date posted')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
