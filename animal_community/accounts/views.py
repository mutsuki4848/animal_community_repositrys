from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.exceptions import ValidationError
from .models import UserActivateTokens, Pet
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import Http404

def home(request):
    return render(
        request, 'accounts/home.html'
    )
    
def regist(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        try:
            regist_form.save()
            return redirect('accounts:home')
        except ValidationError as e:
            regist_form.add_error('password', e) 
    return render(
        request, 'accounts/regist.html', context={
            'regist_form': regist_form,
        }
    )
    
def activate_user(request, token):
    user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
    return render(
        request, 'accounts/activate_user.html'
    )
    
def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'ログイン完了しました')
                return redirect('accounts:home')
            else:
                messages.warning(request, 'ユーザーがアクティブではありません')
        else:
            messages.warning(request, 'ユーザーかパスワードが間違っています')
    return render(
        request, 'accounts/user_login.html',context={
            'login_form': login_form,
        }
    )
            
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'ログアウトしました')
    return redirect('accounts:home')

@login_required
def user_edit(request):
    user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if user_edit_form.is_valid():
        user = user_edit_form.save(commit=False)
        user.favorite_animals = ''.join(user_edit_form.cleaned_data['favorite_animals'])
        user.save()
        messages.success(request, '更新完了しました。')
        return redirect('accounts:user_profile')
    return render(
            request, 'accounts/user_edit.html', context={
            'user_edit_form': user_edit_form,
        }
    )
        
@login_required
def change_password(request):
    password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
    if password_change_form.is_valid():
        try:
            password_change_form.save()
            messages.success(request, 'パスワードを変更しました')
            update_session_auth_hash(request, request.user)
        except ValidationError as e:
            password_change_form.add_error('password', e)
    return render(
        request, 'accounts/change_password.html', context={
            'password_change_form': password_change_form,
        }
    )


def show_error_page(request, exception):
    return render(
        request, '404.html'
    )
    
@login_required
def user_profile(request):
    user_pets = request.user.pet.all()  # ログインユーザーのペット情報を取得
    return render(
        request, 'accounts/user_profile.html', context={
            'user': request.user,
            'user_pets': user_pets,  # ペット情報をテンプレートに渡す
        }
    )
    

@login_required
def pet_regist(request):
    pet_form = forms.PetRegistForm(request.POST or None, request.FILES or None)
    if pet_form.is_valid():
        pet = pet_form.save(commit=False)
        if not pet.picture:
            pet.picture = 'pet_pictures/default_pet.jpg'
        pet.save()
        request.user.pet.add(pet)
        messages.success(request, 'ペット情報を登録しました。')
        return redirect('accounts:user_profile')
    return render(
        request, 'accounts/pet_regist.html', context={
            'pet_form': pet_form,
        }
    )
    

@login_required
def pet_profile(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    return render(
        request, 'accounts/pet_profile.html', context={
            'pet': pet,
        }
    )

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet not in request.user.pet.all():
        raise Http404

    delete_pet_form = forms.DeletePetForm(request.POST or None)
    
    if request.method == 'POST':
        if delete_pet_form.is_valid():
            if delete_pet_form.cleaned_data['confirm']:
                pet.delete()
                messages.success(request, f'{pet.name}のプロフィールを削除しました。')
                return redirect('accounts:user_profile')
            else:
                messages.error(request, '削除がキャンセルされました。')
    
    return render(
        request, 'accounts/delete_pet.html', context={
            'delete_pet_form': delete_pet_form,
            'pet': pet,
        }
    )
    
@login_required
def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    # ログインユーザーがペットの所有者か確認
    if pet not in request.user.pet.all():
        raise Http404

    pet_form = forms.PetRegistForm(request.POST or None, request.FILES or None, instance=pet)
    
    if pet_form.is_valid():
        pet_form.save()
        messages.success(request, f'{pet.name}の情報を更新しました。')
        return redirect('accounts:pet_profile', pet_id=pet.id)
    
    return render(
        request, 'accounts/pet_edit.html', context={
            'pet_form': pet_form,
            'pet': pet,
        }
    )