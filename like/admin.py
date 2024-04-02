from django.contrib import admin

from like.models import Like


# Register your models here.
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    raw_id_fields = ('question', 'comment', 'user')
    list_display = ('question', 'comment', 'user')
    list_display_links = ('question', 'comment', 'user')
