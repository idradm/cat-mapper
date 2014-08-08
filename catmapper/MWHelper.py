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

        result = self.mw_client.queryList(0, query, True)

        return result['query']['allcategories']

    def get_pages(self, wiki_id, category):
        self.mw_client.set_wiki_id(wiki_id)
        query = {
            'action': 'query',
            'list': 'categorymembers',
            'cmlimit': 5000,
            'cmtitle': 'Category:{0}'.format(category),
            'cmnamespace': 0
        }
        result = self.mw_client.queryList(0, query, True)
        return result['query']['categorymembers']

    def get_details(self, wiki_id, page_id):
        self.mw_client.set_wiki_id(wiki_id)
        domain = self.mw_client.get_domain()
        url = 'http://{0}/api/v1/Articles/Details?ids={1}&abstract=500'.format(domain, page_id)
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return False

    def get_articles_intersection(self, wiki_id, categories):
        c = self._get_solr_connection()
        res = c.select('categories_mv_en:({0})'.format(' AND '.join(categories)),
                       fq='ns:0 AND wid:{0}'.format(wiki_id), fl='url, id', rows=1000)
        return res.get('response').get('docs')

    def _get_solr_connection(self):
        if not self.solr_conn:
            self.solr_conn = solr.SolrConnection('http://search-s11:8983/solr')
        return self.solr_conn

"""
mw = MWHelper()
results = mw.get_categories(3125)
for res in results:
    print res
"""