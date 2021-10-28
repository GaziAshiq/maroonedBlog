from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import News


class NewsPublishForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'cover_photo', 'summary', 'content', 'tags']
        widgets = {
            'content': SummernoteWidget(),
        }
