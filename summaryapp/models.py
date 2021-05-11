from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    name = models.CharField("お名前", blank=False, null=False, max_length=20)
    text = models.TextField("本文")
    submit_date = models.DateTimeField("投稿時間", auto_now_add=True)

    def __str__(self):
        return self.name