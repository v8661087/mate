from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
import math

class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

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
