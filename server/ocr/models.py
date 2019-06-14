from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(verbose_name='Title', max_length=50)
    content = models.TextField(verbose_name='Content')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['title']

    def __str__(self):
        return self.title