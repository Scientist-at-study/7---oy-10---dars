from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rating']

    def clean(self):
        cleaned_data = super().clean()
        print("Form cleaned data:", cleaned_data)
        print("Form errors:", self.errors)
        return cleaned_data
