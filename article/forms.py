from .models import Article, Comment , Like, Tag
from django import forms

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, tag):
        return "%s" % tag.name


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','body','img','tags')
        tags = CustomMMCF(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)



class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)