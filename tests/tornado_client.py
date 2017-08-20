from tornado.httpclient import AsyncHTTPClient
from tornado.web import gen

url_builder = 'http://{host}:{port}/{url}'.format


class AsyncCrawler(object):
    def __init__(self, hosts_list, url, port):
        self.__hosts_list = hosts_list
        self.__url = url
        self.__port = port

    def __prepare_futures(self):
        futures = {}

        http_client = AsyncHTTPClient()

        for host in self.__hosts_list:
            future = http_client.fetch(url_builder(host=host, port=self.__port, url=self.__url.lstrip('/')),
                                       request_timeout=1, allow_ipv6=True)
            futures[future] = host

        return futures

    @gen.coroutine
    def crawl(self):

        success, failed, results = set(), set(), {}

        futures = self.__prepare_futures()
        wait_iterator = gen.WaitIterator(*futures.keys())

        while not wait_iterator.done():
            try:
                result = yield wait_iterator.next()
            except Exception:
                host_name = futures[wait_iterator.current_future]
                failed.add(host_name)
            else:
                host_name = futures[wait_iterator.current_future]
                success.add(host_name)
                results[futures[wait_iterator.current_future]] = result.body

        raise gen.Return((results, success, failed))
