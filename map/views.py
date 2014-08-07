from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def main(request, wiki_id):
    cats = ['cat1', 'cat2', 'cat3']
    context = {'categories': cats, 'wid': wiki_id}
    return render(request, 'index.html', context)


def save(request, wiki_id):
    print(request.POST)
    return HttpResponse(1, content_type="application/json")