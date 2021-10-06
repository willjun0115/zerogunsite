from django.db import models
from django.contrib.postgres.fields import ArrayField


class Board(models.Model):
    id = models.BigAutoField(help_text="ID", primary_key=True)
    title = models.CharField(max_length=20)
    protected = models.BooleanField(help_text="is protected", default=False, null=True)

    def __str__(self):
        return self.title


class User(models.Model):
    id = models.BigAutoField(help_text="ID", primary_key=True)
    ip = models.GenericIPAddressField(protocol='IPv4', null=True)
    username = models.CharField(max_length=16, default='user')
    date = models.DateTimeField('date created', auto_now_add=True)
    allowed_board_id = ArrayField(models.CharField(max_length=10, blank=True), blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    id = models.BigAutoField(help_text="ID", primary_key=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date = models.DateTimeField('date posted', auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
