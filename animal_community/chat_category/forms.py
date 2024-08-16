from django import forms
from .models import Themes, Comments


class CreateThemeForm(forms.ModelForm):
    title = forms.CharField(label='タイトル')
    pet_genre = forms.ChoiceField(label='ペットジャンル', choices=(
        (1, '犬'),
        (2, '猫'),
        (3, '鳥'),
        (4, 'ウサギ'),
        (5, '爬虫類'),
    ), widget=forms.RadioSelect)
    
    class Meta:
        model = Themes
        fields = ('title','pet_genre',)
    

class DeleteThemeForm(forms.ModelForm):
    
    class Meta:
        model = Themes
        fields = []
        

class PostCommentsForm(forms.ModelForm):
    comment = forms.CharField(label='',widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))
    image = forms.ImageField(required=False, label='画像')
    
    class Meta:
        model = Comments
        fields = ('comment', 'image')
        
class DeletePostForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = []