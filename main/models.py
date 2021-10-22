from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from main.tasks import notify_user_func


class Created(models.Model):
    """
    Нужен для того чтобы, во всех моделях не прописывали одно тоже поле,
    все последующие модели будут наследоваться от этого класса и будут принимать его поля
    """
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        """
        Значение abstract = True означает ,
        что при создании файлов миграции для нашей модели эти файлы не будут создаваться
        """
        abstract = True


class Problem(Created):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(
        'account.CustomUser', on_delete=models.CASCADE,
        related_name='problems'
    )

    def __str__(self):
        return self.title


class Picture(Created):
    image = models.ImageField(
        upload_to='pictures'  # куда наша фотография будет выгружаться
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE,
        related_name='pictures'
    )


class Reply(Created):
    text = models.TextField()
    image = models.ImageField(
        upload_to='reply_pictures'
    )
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE,
        related_name='replies'
    )
    author = models.ForeignKey(
        'account.CustomUser', on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return self.text[:10] + '...'


class Comment(Created):
    text = models.TextField()
    author = models.ForeignKey(
        'account.CustomUser', on_delete=models.CASCADE,
        related_name='comments'
    )

    reply = models.ForeignKey(          # связывание класса Comments c классом Reply
        Reply, on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return self.text


@receiver(post_save, sender=Problem)    # post_save это сигналы в модельках
def notify_user(sender, instance, created, **kwargs):
    if created:
        email = instance.author.email
        notify_user_func.delay(email)

# @receiver(pre_save, sender=Problem)
# def a(sender, instance, **kwargs):


