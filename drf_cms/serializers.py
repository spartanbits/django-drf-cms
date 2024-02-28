from rest_framework import serializers
from .models import Page, Text, FileData, ImageData
import pathlib
from django.conf import settings
from urllib.parse import urlparse


class TextSerializer(serializers.ModelSerializer):
    key = serializers.CharField(read_only=True)

    class Meta:
        model = Text
        fields = ('content', 'key')


class PageSerializer(serializers.ModelSerializer):
    texts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Page
        fields = ('key', 'title', 'description', 'texts')

    def get_texts(self, instance):
        texts = instance.text_set.all()
        result = {}
        for text in texts:
            result[text.key] = text.content
        return result


class FileDataSerializer(serializers.ModelSerializer):
	file = serializers.FileField()
	extra = serializers.SerializerMethodField()

	class Meta:
		model = FileData
		fields = ('file', 'id', 'description', 'extra')

	def get_extra(self, instance):
		if not instance.file:
			return None
		if instance.is_video():
			file = {
				'hls': instance.get_hls(),
				'thumbnail': instance.get_thumbnail_at(4),
				'thumbnail_fallback': instance.get_thumbnail_at(2)
			}
			return file
		return None


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ImageData
		fields = ('url', 'id', 'description', 'width', 'height')