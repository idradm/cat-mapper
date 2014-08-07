from django.test import TestCase

from map.models import Type, Group, Category, CategoryTypeMapping


# Create your tests here.
class TestCategories(TestCase):

    def setUp(self):
        Type(name='Episode').save()
        Type(name='Series').save()

    def test_mapping(self):
        group = Group(wiki_id=1)
        group.save()
        Category(group_id=group.id, name='Episodes', wiki_id=1).save()
        Category(group_id=group.id, name='Characters', wiki_id=1).save()
        CategoryTypeMapping(type=Type.objects.get(name='Episode'), group_id=group.id).save()

        group = Category.objects.filter(wiki_id=1)
        self.assertEqual(2, len(group))
        self.assertEqual(Type.objects.get(name='Episode'),
                         CategoryTypeMapping.objects.get(group_id=group[0].group_id).type)