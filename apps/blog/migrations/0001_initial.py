# Generated by Django 3.1.1 on 2020-11-04 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'NewsTag',
                'verbose_name_plural': 'NewsTags',
                'db_table': 'blog_newstags',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('is_published', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=255, null=True)),
                ('content', models.TextField(default='')),
                ('tags', models.ManyToManyField(blank=True, related_name='news', to='blog.NewsTag')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
                'db_table': 'blog_news',
            },
        ),
    ]
