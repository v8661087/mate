from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
#    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True,
 #                             default='users/default.jpg')
    photo = models.URLField(blank=True, default='https://raw.githubusercontent.com/v8661087/v8661087.github.io/master/media/users/default.jpg')
    full_name = models.CharField(max_length=30, blank=True, verbose_name=u"姓名")
    website = models.URLField(blank=True, verbose_name=u"網站")
    personal_profile = models.TextField(max_length=300, blank=True, verbose_name=u"個人簡介")
    phone_number = models.CharField(max_length=30, blank=True, verbose_name=u"電話號碼")
    GENDER_CHOICES = (
        ('M', '男性'),
        ('F', '女性'),
        ('N', '未指定'),
    )
    gender = models.CharField(max_length=10,
                              choices=GENDER_CHOICES,
                              default='N',
                              verbose_name=u"性別")
    def __str__(self):
        return 'Profile for user {}'.format(self.user)




class Contact(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)



# Add following field to User dynamically
User.add_to_class('following',
                  models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))

