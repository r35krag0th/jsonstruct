from typedjson._samples import Thing

from six import u
import typedjson
import unittest
from warnings import warn

SAMPLE_DATA = {'things': [Thing('data')]}


class BackendTestCase(unittest.TestCase):

    def _is_installed(self, backend):
        if not typedjson.util.is_installed(backend):
            self.fail('%s not available; please install' % backend)

    def set_backend(self, *args):
        backend = args[0]

        self._is_installed(backend)

        typedjson.load_backend(*args)
        typedjson.set_preferred_backend(backend)

    def set_preferred_backend(self, backend):
        self._is_installed(backend)

        typedjson.set_preferred_backend(backend)

    def tearDown(self):
        # always reset to default backend
        typedjson.set_preferred_backend('json')

    def assertEncodeDecode(self, expected_pickled):
        pickled = typedjson.encode(SAMPLE_DATA)

        self.assertEqual(expected_pickled, pickled)
        unpickled = typedjson.decode(pickled)
        self.assertEqual(SAMPLE_DATA['things'][0].name,
                         unpickled['things'][0].name)

class JsonTestCase(BackendTestCase):
    def setUp(self):
        self.set_preferred_backend('json')

    def test(self):
        expected_pickled = (
                '{"things": [{'
                    '"py/object": "typedjson._samples.Thing",'
                    ' "name": "data",'
                    ' "child": null}'
                ']}')
        self.assertEncodeDecode(expected_pickled)

class SimpleJsonTestCase(BackendTestCase):
    def setUp(self):
        self.set_preferred_backend('simplejson')

    def test(self):
        expected_pickled = (
                '{"things": [{'
                    '"py/object": "typedjson._samples.Thing",'
                    ' "name": "data",'
                    ' "child": null}'
                ']}')
        self.assertEncodeDecode(expected_pickled)


def has_module(module):
    try:
        __import__(module)
    except ImportError:
        warn(module + ' module not available for testing, '
             'consider installing')
        return False
    return True

class DemjsonTestCase(BackendTestCase):
    def setUp(self):
        self.set_preferred_backend('demjson')

    def test(self):
        expected_pickled = u(
                '{"things":[{'
                    '"child":null,'
                    '"name":"data",'
                    '"py/object":"typedjson._samples.Thing"}'
                ']}')
        self.assertEncodeDecode(expected_pickled)


class JsonlibTestCase(BackendTestCase):
    def setUp(self):
        self.set_preferred_backend('jsonlib')

    def test(self):
        expected_pickled = (
                '{"things":[{'
                    '"py\/object":"typedjson._samples.Thing",'
                    '"name":"data","child":null}'
                ']}')
        self.assertEncodeDecode(expected_pickled)


class YajlTestCase(BackendTestCase):
    def setUp(self):
        self.set_preferred_backend('yajl')

    def test(self):
        expected_pickled = (
                '{"things":[{'
                    '"py/object":"typedjson._samples.Thing",'
                    '"name":"data","child":null}'
                ']}')
        self.assertEncodeDecode(expected_pickled)



class UJsonTestCase(BackendTestCase):
    def setUp(self):
        self.set_preferred_backend('ujson')

    def test(self):
        expected_pickled = (
                '{"things":[{'
                    '"py\/object":"typedjson._samples.Thing",'
                    '"name":"data","child":null}'
                ']}')
        self.assertEncodeDecode(expected_pickled)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(JsonTestCase))
    suite.addTest(unittest.makeSuite(SimpleJsonTestCase))
    if has_module('demjson'):
        suite.addTest(unittest.makeSuite(DemjsonTestCase))
    if has_module('yajl'):
        suite.addTest(unittest.makeSuite(YajlTestCase))
    if has_module('jsonlib'):
        suite.addTest(unittest.makeSuite(JsonlibTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
