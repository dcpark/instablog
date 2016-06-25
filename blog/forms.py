from django import forms

from .models import Post

class PostNormalForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        # fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data

        if '바보' in cleaned_data['title']:
            self.add_error('title', '제목에서 바보 냄새가 난다')
