import requests


class MediaWikiClient(object):

    res_border = 'http://10.12.64.103/'
    global_domain = 'www.wikia.com'
    api_endpoint = 'api.php'

    def __init__(self, use_res=False):
        self.wiki_id = None
        self.data = {}
        self.use_res = use_res
        self.session = requests.session()
        self.global_url = self._get_url(self.global_domain, self.api_endpoint)
        self.domain_url = None

    def set_wiki_id(self, wiki_id):
        self.data = {}
        self.wiki_id = wiki_id
        self.domain_url = self._get_url(self.get_domain(), self.api_endpoint)
        return self

    def login(self, user, password):
        res = self._call(self.global_url, self._post, {'action': 'login', 'lgname': user, 'lgpassword': password})
        if res:
            r = self._call(self.global_url, self._post, {'action': 'login', 'lgname': user, 'lgpassword': password,
                                             'lgtoken': res.get('login').get('token')})
            return True if r else False
        return False

    def queryList(self, article_id, properties=None):
        list_key = properties.get('list')
        results = self.query(article_id, properties)
        result = results.get('query').get(list_key)
        while 'query-continue' in results:
            continue_key, continue_val = results['query-continue'][list_key].items()[0]
            properties[continue_key] = continue_val
            results = self.query(article_id, properties)
            result += results.get('query').get(list_key)
        return result

    def query(self, article_id, properties=None):
        if not properties: properties = {}
        properties = dict(self._parse_lists(properties).items() + [('action', 'query'), ('pageids', str(article_id))])
        res = self._call(self.domain_url, self._get, params=properties)
        if res:
            return res
        return False

    def parse(self, article_id, properties=None):
        if not properties: properties = {}
        properties = dict(self._parse_lists(properties).items() + [('action', 'parse'), ('pageid', str(article_id))])
        res = self._call(self.domain_url, self._get, params=properties)
        if res:
            return res.get('parse')
        return False

    def get_domain(self):
        if 'domain' not in self.data:
            self._load_wiki_data()
        return self.data.get('domain')

    def get_wiki_lang(self):
        if 'wiki_lang' not in self.data:
            self._load_wiki_data()
        return self.data.get('wiki_lang')

    def _load_wiki_data(self):
        res = self._call(self.global_url, self._get, {'wkwikia': self.wiki_id, 'action': 'query', 'list': 'wkdomains'})
        if res:
            data = res.get('query').get('wkdomains').get(str(self.wiki_id))
            self.data['domain'] = data.get('domain')
            self.data['wiki_lang'] = data.get('lang')
        else:
            raise Exception('Wiki domain not found')

    def _get_url(self, base, path):
        if base and path:
            if self.use_res:
                return self.res_border + path, base
            return 'http://' + base + '/' + path
        raise Exception('Could not create correct url')

    def _call(self, url, method, params=None):
        params = {'format': 'json'} if not params else dict(params.items() + [('format', 'json')])
        try:
            r = method(url[0], params, {'host': url[1]}) if self.use_res else method(url, params)
        except requests.RequestException as e:
            print(e.message)
            return False
        if r and r.status_code is 200:
            if 'application/json' in r.headers['Content-Type']:
                response = r.json()
                if 'error' in response:
                    raise Exception(response.get('error').get('info'))
                return response
            return r.text
        return False

    def _post(self, url, data, headers=None):
        if not headers: headers = {}
        return self.session.post(url, data, headers=headers)

    def _get(self, url, params, headers=None):
        if not headers: headers = {}
        return self.session.get(url, params=params, headers=headers)

    @staticmethod
    def _parse_lists(props):
        result = {}
        for key, value in props.items():
            if isinstance(value, list):
                result[key] = '|'.join(value)
            else:
                result[key] = value
        return result
