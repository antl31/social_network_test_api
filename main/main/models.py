from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('User')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.title}'


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    publications = models.ForeignKey(Post, related_name='Post_id', on_delete=models.CASCADE)
    last_updated = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ['user', 'publications']

    def __str__(self):
        return f'{self.publications.title} - {self.user}'

    @staticmethod
    def like_unlike_post(user_id, post_id):
        like = PostLike.objects.all().filter(user=user_id).filter(publications=post_id)
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        if like:
            like.delete()
        else:
            PostLike.objects.create(user=user, publications=post)

    @staticmethod
    def total_likes():
        return PostLike.objects.all().count()
