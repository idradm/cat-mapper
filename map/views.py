import json
from map.models import Type, Group, Category, CategoryTypeMapping
from catmapper import MWHelper

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def main(request, wiki_id):
    mw_helper = MWHelper.MWHelper()
    cat_list = mw_helper.get_categories(wiki_id)
    cats = []
    for item in cat_list:
        cats.append(item.get('*'))
    context = {'categories': cats, 'types': Type.objects.all(), 'wid': wiki_id}
    return render(request, 'index.html', context)


def pages(request, wiki_id, categories):
    mw_helper = MWHelper.MWHelper()
    articles = mw_helper.get_articles_intersection(wiki_id, categories.split(','))
    context = {'pages': articles}
    return render(request, 'pages.html', context)


def details(request, wiki_id, page_id):
    mw_helper = MWHelper.MWHelper()
    details = mw_helper.get_details(wiki_id, page_id)
    context = {'img': details.get('items').get(str(page_id)).get('thumbnail', ''),
               'snippet': details.get('items').get(str(page_id)).get('abstract', '')}
    return render(request, 'details.html', context)


def save(request, wiki_id):
    # create new group id
    g = Group(wiki_id=wiki_id)
    g.save()
    for category in request.POST.getlist('categories'):
        Category(group_id=g.id, name=category, wiki_id=wiki_id).save()
    CategoryTypeMapping(group_id=g.id, type=Type.objects.get(name=request.POST.get('type'))).save()

    return HttpResponse(1, content_type="application/json")


def groups(request, wiki_id):
    res = Group.objects.filter(wiki_id=wiki_id)
    output = json.dumps([{'id': g.id} for g in res]) if res else 0
    return HttpResponse(output, content_type="application/json")


def group_details(request, wiki_id, group_id):
    mw_helper = MWHelper.MWHelper()
    res = Category.objects.filter(group_id=group_id, wiki_id=wiki_id)
    map = CategoryTypeMapping.objects.get(group_id=group_id)
    cats = [cat.name for cat in res]
    articles = mw_helper.get_articles_intersection(wiki_id, cats)
    output = json.dumps({'categories': cats, 'articles': articles, 'article_type': map.type.name}) if res else 0
    return HttpResponse(output, content_type="application/json")
