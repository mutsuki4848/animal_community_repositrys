from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Themes, Comments, Like
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse


def create_theme(request):
    create_theme_form = forms.CreateThemeForm(request.POST or None)
    if create_theme_form.is_valid():
        create_theme_form.instance.user = request.user
        create_theme_form.save()
        messages.success(request, 'チャットカテゴリーを作成しました')
        return redirect('chat_category:list_themes')
        
    return render(
        request, 'chat_category/create_theme.html',context={
            'create_theme_form': create_theme_form,
        }
    )
    

def list_themes(request):
    themes = Themes.objects.fetch_all_themes()
    return render(
        request, 'chat_category/list_themes.html', context={
            'themes': themes
        }
    )
    
def edit_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    edit_theme_form = forms.CreateThemeForm(request.POST or None, instance=theme)    
    if edit_theme_form.is_valid():
        edit_theme_form.save()
        messages.success(request, 'グループチャットを更新しました')
        return redirect('chat_category:list_themes')
    return render(
        request, 'chat_category/edit_theme.html', context={
            'edit_theme_form': edit_theme_form,
            'id': id,
        }
    )
    

def delete_theme(request, id):
    theme = get_object_or_404(Themes, id=id)
    if theme.user.id != request.user.id:
        raise Http404
    delete_theme_form = forms.DeleteThemeForm(request.POST or None)
    if delete_theme_form.is_valid():
        theme.delete()
        messages.success(request, 'グループチャットを削除しました')
        return redirect('chat_category:list_themes')
    return render(
        request, 'chat_category/delete_theme.html',context={
            'delete_theme_form': delete_theme_form, 
        }
    )
    

def post_comments(request, theme_id):
    # `theme`を最初に取得
    theme = get_object_or_404(Themes, id=theme_id)  # 追加

    saved_comment = cache.get(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', '')
    
    if request.method == 'POST':  # POSTメソッドであるかを確認
        post_comments_form = forms.PostCommentsForm(request.POST, request.FILES, initial={'comment': saved_comment})  # request.FILESを追加
        if post_comments_form.is_valid():
            if not request.user.is_authenticated:
                raise Http404
            post_comments_form.instance.theme = theme
            post_comments_form.instance.user = request.user
            post_comments_form.save()
            cache.delete(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}')
            return redirect('chat_category:post_comments', theme_id=theme_id)
    else:
        post_comments_form = forms.PostCommentsForm(initial={'comment': saved_comment})

    comments = Comments.objects.fetch_by_theme_id(theme_id)
    return render(
        request, 'chat_category/post_comments.html', context={
            'post_comments_form': post_comments_form,
            'theme': theme,
            'comments': comments,
        }
    )
    
def post_delete(request, id):
    post = get_object_or_404(Comments, id=id)
    if post.user.id != request.user.id:
        raise Http404
    delete_post_form = forms.DeletePostForm(request.POST or None)
    if delete_post_form.is_valid():
        post.delete()
        messages.success(request, '投稿を削除しました')
        return redirect('chat_category:post_comments', theme_id=post.theme.id)
    return render(
        request, 'chat_category/post_delete.html',context={
            'delete_post_form': delete_post_form, 
        }
    )

def save_comment(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = request.GET.get('comment')
        theme_id = request.GET.get('theme_id')
        if comment and theme_id:
            cache.set(f'saved_comment-theme_id={theme_id}-user_id={request.user.id}', comment)
            return  JsonResponse({'message': '一時保存しました。'})
        
def like_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    user = request.user
    like, created = Like.objects.get_or_create(comment=comment, user=user)
    
    if not created:
        like.delete()  # 既に「いいね」している場合は取り消す
    
    return redirect('chat_category:post_comments', theme_id=comment.theme.id)