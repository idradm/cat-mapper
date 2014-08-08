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

    context = {'categories': cats, 'wid': wiki_id}
    return render(request, 'index.html', context)


def pages(request, wiki_id, category):
    mw_helper = MWHelper.MWHelper()
    pages = mw_helper.get_pages(wiki_id, category)
    context = {'pages': pages}
    return render(request, 'pages.html', context)


def details(request, wiki_id, page_id):
    mw_helper = MWHelper.MWHelper()
    details = mw_helper.get_details(wiki_id, page_id)
    context = {'img': details.get('items').get(str(page_id)).get('thumbnail', ''),
               'snippet': details.get('items').get(str(page_id)).get('abstract', '')}
    return render(request, 'details.html', context)


def save(request, wiki_id):
    # create new group id
    print(request.POST)
    g = Group(wiki_id=wiki_id)
    g.save()
    for category in request.POST.get('categories'):
        Category(group_id=g.id, name=category, wiki_id=wiki_id).save()
    CategoryTypeMapping(group_id=g.id, type=Type.objects.get(name=request.POST.get('type'))).save()

    return HttpResponse(1, content_type="application/json")
