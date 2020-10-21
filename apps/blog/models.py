from django.db import models

from apps.common.models import Slugged, Ownable


class NewsTag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'blog'
        db_table = 'blog__news_tags'
        verbose_name = 'NewsTag'
        verbose_name_plural = 'NewsTags'


class News(Slugged, Ownable):
    title = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    author = models.CharField(max_length=255)
    tags = models.ManyToManyField(to=NewsTag, blank=True, related_name='news')
    content = models.TextField()

    def autofill_author(self):
        if not self.author:
            self.author = f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        self.autofill_author()
        super(News, self).save(*args, **kwargs)

    class Meta:
        app_label = 'blog'
        db_table = 'blog__news'
        verbose_name = 'News'
        verbose_name_plural = 'News'
