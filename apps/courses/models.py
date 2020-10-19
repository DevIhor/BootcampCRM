from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'courses'
        verbose_name = 'CourseTemplate'
        verbose_name_plural = 'CourseTemplates'


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    class Meta:
        app_label = 'courses'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'


class LessonTemplate(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(to=CourseTemplate, on_delete=models.CASCADE)

    class Meta:
        app_label = 'courses'
        verbose_name = 'LessonTemplate'
        verbose_name_plural = 'LessonTemplates'
        unique_together = ['name', 'course']


class CourseSchedule(models.Model):
    class Meta:
        app_label = 'courses'
        verbose_name = 'CourseSchedule'
        verbose_name_plural = 'CourseSchedules'
