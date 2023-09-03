from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Subject_A(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject_B(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("Subject_A", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subject_C(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("Subject_B", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subject_D(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("Subject_C", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title
