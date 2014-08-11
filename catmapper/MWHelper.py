import solr
import requests
import MediaWikiClient


class MWHelper(object):

    def __init__(self, mw_client=None):
        self.solr_conn = None
        if not mw_client:
            self.mw_client = MediaWikiClient.MediaWikiClient()
        else:
            self.mw_client = mw_client

    def get_categories(self, wiki_id):
        self.mw_client.set_wiki_id(wiki_id)
        query = {
            'action': 'query',
            'list': 'allcategories',
            'aclimit': 5000,
            'acprop': 'size|id',
            'acmin': 1
        }

        result = self.mw_client.queryList(0, query)

        return result

    def get_pages(self, wiki_id, category):
        self.mw_client.set_wiki_id(wiki_id)
        query = {
            'action': 'query',
            'list': 'categorymembers',
            'cmlimit': 5000,
            'cmtitle': 'Category:{0}'.format(category),
            'cmnamespace': 0
        }
        result = self.mw_client.queryList(0, query)
        return result

    def get_details(self, wiki_id, page_id):
        self.mw_client.set_wiki_id(wiki_id)
        domain = self.mw_client.get_domain()
        url = 'http://{0}/api/v1/Articles/Details?ids={1}&abstract=500'.format(domain, page_id)
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return False

    def get_articles_intersection(self, wiki_id, categories):
        out = None
        for category in categories:
            articles = self.get_pages(wiki_id, category)
            if not articles:
                return []
            if out is None:
                out = articles
            else:
                ids = set(item['pageid'] for item in out)
                out = [item for item in articles if item['pageid'] in ids]
        return out

    def get_domain(self, wiki_id):
        self.mw_client.set_wiki_id(wiki_id)
        return self.mw_client.get_domain()
