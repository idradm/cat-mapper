from map.models import Type, Group, Category, CategoryTypeMapping

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def main(request, wiki_id):
    cats = ['cat1', 'cat2', 'cat3']
    context = {'categories': cats, 'wid': wiki_id}
    return render(request, 'index.html', context)


def save(request, wiki_id):
    # create new group id
    g = Group(wiki_id=wiki_id)
    g.save()
    for category in request.POST.get('categories'):
        Category(group_id=g.id, name=category, wiki_id=wiki_id).save()
    CategoryTypeMapping(group_id=g.id, type=Type.objects.get(name=request.POST.get('type'))).save()

    return HttpResponse(1, content_type="application/json")
