from django.db import models

class ThemesManager(models.Manager):
    
    def fetch_all_themes(self):
        return self.order_by('id').all()


class Themes(models.Model):
    PET_GENRE_CHOICES = (
        (1, '犬'),
        (2, '猫'),
        (3, '鳥'),
        (4, 'ウサギ'),
        (5, '爬虫類'),
    )
    
    title = models.CharField(max_length=255)
    pet_genre = models.IntegerField(choices=PET_GENRE_CHOICES, default=1)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    
    objects = ThemesManager()
    
    class Meta:
        db_table = 'themes'

class CommentsManager(models.Manager):
    def fetch_by_theme_id(self, theme_id):
        return self.filter(theme_id=theme_id).order_by('id').all()
             

class Comments(models.Model):
    
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    theme = models.ForeignKey(
        'Themes', on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='comments_images/', blank=True, null=True)
    objects = CommentsManager()
    
    def like_count(self):
        return self.likes.count()  # 「いいね」の数を取得

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    comment = models.ForeignKey(
        Comments, related_name='likes', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = ('comment', 'user')  # ユーザーが同じコメントに複数回「いいね」できないようにする
        db_table = 'likes'