from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название группы",
        help_text="Укажите название группы"
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name="Уникальный адрес группы",
        help_text="Выберите из списка или укажите новый адрес"
    )
    description = models.TextField(
        verbose_name="Описание сообщества",
        help_text="Добавьте описание группы"
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name="Текст поста",
        help_text="Добавьте описание поста"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Автор"
    )
    image = models.ImageField(
        verbose_name="Картинка",
        help_text="Прикрепите изображение",
        upload_to='posts/',
        blank=True,
        null=True,
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        related_name='posts',
        on_delete=models.SET_NULL,
        verbose_name="Группа",
        help_text="Укажите группу в которой опубликуется пост"
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    text = models.TextField(
        verbose_name="Коментарий",
        help_text="Введите текст"
    )
    created = models.DateTimeField(
        verbose_name="Дата создания",
        db_index=True,
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментари к постам"

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name="Пользователь (кто подписался)",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name="Пользователь (на кого подписался)",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='exclude a new subscription when it is valid',
                fields=['user', 'following'],
            ),
            models.CheckConstraint(
                name="disable subscribe to yourself",
                check=~models.Q(user=models.F("following")),
            )
        ]
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
