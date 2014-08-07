import solr
import MediaWikiClient


class MWHelper(object):

    def __init__(self, mw_client=None):
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

"""
mw = MWHelper()
results = mw.get_categories(3125)
for res in results:
    print res
"""