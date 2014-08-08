from django.contrib import admin
from map.models import Type, Group, Category, CategoryTypeMapping

# Register your models here.
admin.site.register(Type)
admin.site.register(Group)
admin.site.register(Category)
admin.site.register(CategoryTypeMapping)
