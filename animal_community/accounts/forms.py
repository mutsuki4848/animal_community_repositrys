from typing import Any
from django import forms
from .models import Users, Pet
from django.contrib.auth.password_validation import validate_password


class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = Users
        fields = ('username','age','email','password')
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')
        
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user    
        
class LoginForm(forms.Form):
    email = forms.CharField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    
class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    email = forms.EmailField(label='メールアドレス')
    bio = forms.CharField(
        label='自己紹介',
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        required=False,
    ) 
    favorite_animals  = forms.MultipleChoiceField(label='好きな動物',choices=(
        (1, '犬'),
        (2, '猫'),
        (3, '鳥'),
        (4, 'ウサギ'),
        (5, '爬虫類'),
    ), widget=forms.CheckboxSelectMultiple, required=False)
    picture = forms.ImageField(label='写真', required=False)  
    
    class Meta:
        model = Users
        fields = ('username','age','favorite_animals','email','bio','picture')
    
def clean_picture(self):
    picture = self.cleaned_data.get('picture')
    if self.cleaned_data.get('picture') is None and 'picture-clear' in self.data:
        return None
    return picture

class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())
    
    class Meta():
        model = Users
        fields = ('password',)
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが異なります')
        
        
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user     
    

class PetRegistForm(forms.ModelForm):
    name = forms.CharField(label='ペットの名前')
    age = forms.IntegerField(label='年齢', min_value=0)
    sex = forms.ChoiceField(label='性別', choices=(('1', 'オス'), ('2', 'メス')))
    picture = forms.ImageField(label='ペットの写真', required=False)
    genre = forms.ChoiceField(
        label='種類',
        choices=(
            ('1', '犬'),
            ('2', '猫'),
            ('3', '鳥類'),
            ('4', '齧歯類'),
            ('5', '爬虫類'),
        )
    )
    breed = forms.CharField(label='品種', required=False)  # 入力は不必要
    characteristic = forms.CharField(
        label='性格や特徴',
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False  # 入力は不必要
    )

    class Meta:
        model = Pet
        fields = ('name', 'age', 'sex', 'genre', 'breed', 'characteristic', 'picture')


class DeletePetForm(forms.Form):
    confirm = forms.BooleanField(label='このペットを削除しますか？')