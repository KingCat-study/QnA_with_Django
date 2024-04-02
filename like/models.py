from django.db import models


# Create your models here.
class Like(models.Model):
    user = models.ForeignKey('user.User', verbose_name='작성자', on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey('question.Question', verbose_name='질문', on_delete=models.SET_NULL, null=True)
    comment = models.ForeignKey('question.Comment', verbose_name='답변', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = '추천'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.user
