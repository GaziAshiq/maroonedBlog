from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import News, Tag


# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'author')
    list_filter = ('status',)
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


admin.site.register(News, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', 'tag_slug', 'created_on', 'created_by',)
    prepopulated_fields = {'tag_slug': ('tag_name',)}


admin.site.register(Tag, TagAdmin)
