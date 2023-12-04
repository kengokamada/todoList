from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, verbose_name='タイトル')
    description = models.TextField(null = True, blank=True, verbose_name='内容')
    complete = models.BooleanField(default=False, verbose_name='完了チェック')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']
