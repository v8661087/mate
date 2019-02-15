from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=u"標題")
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    image = ResizedImageField(size=[600, 600], quality=100, crop=['middle', 'left'], upload_to='images/%Y/%m/%d', verbose_name=u"相片")
    description = models.TextField(blank=True,verbose_name=u"描述")
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)
    total_likes = models.PositiveIntegerField(db_index=True,
                                              default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self)
        super(Image, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

