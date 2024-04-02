from django.contrib import admin

from question.models import Question, Comment


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('id', 'title', 'user', 'count_like', 'count_comment', 'created_at', 'modified_at')
    list_display_links = ('id', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    raw_id_fields = ('question', 'user',)
    list_display = ('id', 'content', 'user', 'count_like', 'created_at', 'modified_at')
    list_display_links = ('id', 'content')
