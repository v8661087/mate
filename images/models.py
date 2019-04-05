from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.utils import timezone
import math

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=u"標題")
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(verbose_name=u"網址")
 #   image = ResizedImageField(size=[750, 750], quality=100, crop=['middle', 'left'], upload_to='images/%Y/%m/%d', verbose_name=u"相片")
    description = models.TextField(blank=True, verbose_name=u"描述")
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)
    users_save = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_saved',
                                        blank=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self)
        super(Image, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

    def when_published(self):
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "秒前"

            else:
                return str(seconds) + "秒前"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + "分前"

            else:
                return str(minutes) + "分前"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + "小時前"

            else:
                return str(hours) + "小時前"

        # 1 day to 7 days
        if diff.days >= 1 and diff.days < 7:
            days = diff.days

            if days == 1:
                return str(days) + "天前"

            else:
                return str(days) + "天前"

        if diff.days >= 7:
     #       months = math.floor(diff.days / 30)

            if now.year == self.created.year:
                return str(self.created.month) + "月" + str(self.created.day) + "日"

            else:
                return str(self.created.year) + "年" + str(self.created.month) + "月" + str(self.created.day) + "日"

     #   if diff.days >= 365:
    #        years = math.floor(diff.days / 365)

     #       if years == 1:
     #           return self.created

     #       else:
      #          return self.created

class Comment(models.Model):
    post = models.ForeignKey(Image, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    updated = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='comments_liked',
                                        blank=True)


    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)

    def when_published(self):
        now = timezone.now()

        diff = now - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 0:
                return "現在"

            else:
                return str(seconds) + "秒"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + "分"

            else:
                return str(minutes) + "分"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + "小時"

            else:
                return str(hours) + "小時"

        # 1 day to 7 days
        if diff.days >= 1 and diff.days < 7:
            days = diff.days

            if days == 1:
                return str(days) + "天"

            else:
                return str(days) + "天"

        if diff.days >= 7:
            weeks = math.floor(diff.days / 7)
            return  str(weeks) + "週"