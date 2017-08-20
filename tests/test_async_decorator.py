import mock
from tornado.testing import AsyncHTTPTestCase, gen_test

from tests.tornado_client import AsyncCrawler
from tornado_async_server import async_server, get_hdlr_helper


@async_server([('/emulate_host1/ping', 'pong', {'response_delay_sec': 1}),
               ('/emulate_host2/ping', 'pong', {}),
               ('/emulate_host3/ping', 'pong', {'write_error': 500})])
class TestStandartHandler(AsyncHTTPTestCase):
    def setUp(self):
        # no need to call parent class setUp here it will be automatically added by
        # @async_server decorator
        self.__crawler = AsyncCrawler({'emulate_host1', 'emulate_host2', 'emulate_host3', 'emulate_host4'},
                                      '/ping', self.get_http_port())
        # mock url_builder to emulate hosts by handlers
        self.patcher = mock.patch('tests.tornado_client.url_builder',
                                  lambda host, port, url: self.get_url('/{}/{}'.format(host, url)))

        self.patcher.start()

    def tearDown(self):
        # no need to call parent class tearDown here it will be automatically added by
        # @async_server decorator
        self.patcher.stop()

    @gen_test
    def test_crawl(self):
        _, success, failed = yield self.__crawler.crawl()
        assert success == {'emulate_host1', 'emulate_host2', 'emulate_host3'}
        assert failed == {'emulate_host4'}


@async_server([('/emulate_host1/ping', get_hdlr_helper(lambda: 'Hello world!')),  # custom get-handler
               ('/emulate_host2/ping', 'pong', {}),
               ('/emulate_host3/ping', 'pong', {'write_error': 500})])
class TestCustomHandlerResponse(AsyncHTTPTestCase):
    def setUp(self):
        # no need to call parent class setUp here it will be automatically added by
        # @async_server decorator
        self.__crawler = AsyncCrawler({'emulate_host1', 'emulate_host2', 'emulate_host3'},
                                      '/ping', self.get_http_port())
        # mock url_builder to emulate hosts by handlers
        self.patcher = mock.patch('tests.tornado_client.url_builder',
                                  lambda host, port, url: self.get_url('/{}/{}'.format(host, url)))

        self.patcher.start()

    def tearDown(self):
        # no need to call parent class tearDown here it will be automatically added by
        # @async_server decorator
        self.patcher.stop()

    @gen_test
    def test_crawl_response(self):
        results, _, _ = yield self.__crawler.crawl()
        assert results == {'emulate_host1': 'Hello world!',
                           'emulate_host3': '<html><title>500: OK</title><body>500: OK</body></html>',
                           'emulate_host2': 'pong'}


@async_server([('/emulate_host1/id/(\d+)', get_hdlr_helper(lambda id: 'right 1' if int(id) == 1 else 'wrong 1')),  # custom get-handler
               ('/emulate_host2/id/(\d+)', get_hdlr_helper(lambda id: 'right 2' if int(id) == 2 else 'wrong 2')),
               ('/emulate_host3/id/(\d+)', get_hdlr_helper(lambda id: 'right 3' if int(id) == 3 else 'wrong 3'))])
class TestCustomParametrizedCustomHandler(AsyncHTTPTestCase):
    def setUp(self):
        # no need to call parent class setUp here it will be automatically added by
        # @async_server decorator
        self.__crawler = AsyncCrawler({'emulate_host1', 'emulate_host2', 'emulate_host3'},
                                      '/id/2', self.get_http_port())
        # mock url_builder to emulate hosts by handlers
        self.patcher = mock.patch('tests.tornado_client.url_builder',
                                  lambda host, port, url: self.get_url('/{}/{}'.format(host, url)))

        self.patcher.start()

    def tearDown(self):
        # no need to call parent class tearDown here it will be automatically added by
        # @async_server decorator
        self.patcher.stop()

    @gen_test
    def test_crawl_custom_response(self):
        results, _, _ = yield self.__crawler.crawl()
        assert results == {'emulate_host1': 'wrong 1',
                           'emulate_host3': 'wrong 3',
                           'emulate_host2': 'right 2'}
