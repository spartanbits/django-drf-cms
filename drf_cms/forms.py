from django import forms
from django.forms.widgets import Select
from .models import FileData, ImageData


class FileUpload(forms.ModelForm):
	class Meta:
		model = FileData
		fields = ('file', 'description')
		def save(self):
			file = super(FileUpload, self).save()
			return file


class ImageUpload(forms.ModelForm):
	class Meta:
		model = ImageData
		fields = ('file', 'description')
		def save(self):
			image = super(ImageUpload, self).save()
			return image


class PreviewSelect(Select):
	def render(self, name, value, attrs=None, *args, **kwargs):
		output = super(PreviewSelect, self).render(name, value, attrs=attrs, *args, **kwargs)
		model = self.choices.field.queryset.model

		if not hasattr(model, 'preview') or not value:
			return output

		try:
			id = int(value)
			obj = model.objects.get(id=id)
			output += obj.preview()
		except model.DoesNotExist:
			pass
		return output
