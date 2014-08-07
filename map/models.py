from django.db import models


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    wiki_id = models.IntegerField()
    group_id = models.IntegerField()


class Group(models.Model):
    wiki_id = models.IntegerField()


class CategoryTypeMapping(models.Model):
    group_id = models.IntegerField()
    type = models.ForeignKey(Type)