from django.contrib.auth.models import User
from django.db import models


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="blog_user_info")
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='photos'
    )

    def __str__(self):
        return f'{self.user} avatar'


class Tag(models.Model):
    tag = models.CharField(max_length=30, verbose_name="Тег")

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


# Create your models here.

class Photo(models.Model):
    image = models.ImageField(upload_to="photos", null=True, blank=True, verbose_name="Photo")
    description = models.CharField(max_length=75)

    def __str__(self):
        return self.description


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Опис")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    tags = models.ManyToManyField(Tag, verbose_name="Теги")
    image = models.ManyToManyField(Photo, verbose_name="Зображення")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default=None)
    name = models.CharField(max_length=30, verbose_name="Комментарій")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата", default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Коментарій"
        verbose_name_plural = "Коментарії"


class Subscribe(models.Model):
    email = models.EmailField(max_length=30, verbose_name="Пошта для розсилки")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Підписка"
        verbose_name_plural = "Підписки"


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Зображення", upload_to="Posts_Photos")
