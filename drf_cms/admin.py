from django.contrib import admin
from django.db import models
from .models import *
from .forms import PreviewSelect


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
	model = Page
	list_filter = ('site',)

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
	model = Text
	list_display = ('key', 'page', )
	list_filter = ('page', 'page__site')

@admin.register(FileData)
class FileDataAdmin(admin.ModelAdmin):
	list_display = ('preview', 'file', 'description', 'uploaded_at',)
	readonly_fields=['uploaded_at']
	search_fields = ['description']
	list_filter = ('description',)
	ordering = ('-uploaded_at', )

@admin.register(ImageData)
class ImageDataAdmin(admin.ModelAdmin):
	list_display = ('preview', 'file', 'description', 'uploaded_at',)
	readonly_fields=['uploaded_at', 'preview', 'height', 'width']
	search_fields = ['description']
	list_filter = ('description',)
	ordering = ('-uploaded_at', )


class PreviewModelAdmin(admin.ModelAdmin):
	formfield_overrides = {models.ForeignKey:{'widget': PreviewSelect}}

class PreviewTabularInline(admin.TabularInline):
	formfield_overrides = {models.ForeignKey:{'widget': PreviewSelect}}