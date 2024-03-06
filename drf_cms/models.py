from django.db import models
from django_bleach.models import BleachField
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.html import mark_safe

import pathlib
from urllib.parse import urlparse

from .mixins import *


class Page(models.Model):
	site = models.ForeignKey(Site, null=False, on_delete=models.CASCADE)
	key = models.CharField(null=False, max_length=64)
	title = models.CharField(null=False, max_length=128)
	description = models.CharField(blank=True, max_length=256)

	class Meta:
		unique_together = ('site', 'key')

	def __str__(self):
		return '{} - {}'.format(self.key, self.site.domain)


class ContentMixin(models.Model):
	page = models.ForeignKey(Page, null=False, on_delete=models.CASCADE)
	key = models.CharField(null=False, max_length=64)

	class Meta:
		unique_together = ('page', 'key')
		abstract = True

	def __str__(self):
		return self.key


class MetadataMixin(models.Model):
	description = models.CharField(blank=True, max_length=512)
	uploaded_at =  models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.description


class ImageData(MetadataMixin):
	file = models.ImageField(height_field='height', width_field='width')
	height = models.PositiveIntegerField(default=0)
	width = models.PositiveIntegerField(default=0)

	@property
	def url(self):
		return self.file.url

	def preview(self):
		return mark_safe(
			'<div style="background-image: url(\'{0}\'); background-size: cover; background-position: center; width: 225px; height: 130px; margin: 5px 0;"></div>'.format(self.file.url))
	
	preview.short_description = 'Image preview'


class FileData(MetadataMixin):
	file = models.FileField()

	def get_filename(self):
		url = urlparse(self.file.url)
		return pathlib.Path(url.path).stem

	def get_base_url(self):
		return 'https://{}.s3.amazonaws.com/{}'.format(
				settings.AWS_STORAGE_VIDEO_BUCKET_NAME, self.get_filename())

	def is_video(self):
		return pathlib.Path(self.file.url).suffix.lower() == '.mp4'

	def get_hls(self):
		return '{}/HLS/{}.m3u8'.format(self.get_base_url(), self.get_filename())
	
	def get_thumbnail_at(self, index):
		return '{}/Thumbnails/{}.000000{}.jpg'.format(
			self.get_base_url(), self.get_filename(), index)

	def preview(self):
		return mark_safe(
			'<div style="background-image: url(\'{0}\'); background-size: cover; background-position: center; width: 225px; height: 130px; margin: 5px 0;"></div>'.format(self.get_thumbnail_at(1)))

class Text(ContentMixin):
	content = BleachField(null=False, allowed_tags=['a', 'p', 'i', 'b', 'u'], allowed_attributes=['href'])


class Image(ContentMixin):
	content = models.ForeignKey(ImageData, null=False, on_delete=models.PROTECT)

	@property
	def url(self):
		return self.content.url

	@property
	def width(self):
		return self.content.width

	@property
	def height(self):
		return self.content.height


class File(ContentMixin):
	content = models.ForeignKey(FileData, null=False, on_delete=models.PROTECT, related_name='file_data')
