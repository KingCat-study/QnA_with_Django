from django.db import models

from django.contrib.auth.models import User


class Question(models.Model):
    title = models.CharField("제목", max_length=200)
    content = models.TextField("내용")
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    count_like = models.IntegerField("좋아요 수", default=0, blank=True)
    count_comment = models.IntegerField("답변 수", default=0, blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    modified_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "질문"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.title

    def question_comments(self):
        return self.comment_set.all()


class Comment(models.Model):
    content = models.TextField("답변내용")
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, verbose_name="질문", on_delete=models.CASCADE)
    count_like = models.IntegerField("좋아요 수", default=0, blank=True)
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    modified_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        verbose_name = "답변"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.content[:100]
