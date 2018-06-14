from django.contrib import admin
from .models import PlayList, Video, VideoCategory


class VideoInLine(admin.TabularInline):
    model = Video


@admin.register(PlayList)
class PlayListAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    inlines = [VideoInLine]
    filter_horizontal = ('categories',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }

