import io
import unittest

import bottle


class TestRequestReadonlyAttribute(unittest.TestCase):
    def test_body_assignment_is_rejected(self):
        request = bottle.BaseRequest({
            'wsgi.input': io.BytesIO(b'original'),
            'CONTENT_LENGTH': '8',
        })
        with self.assertRaises(AttributeError):
            request.body = 'replacement'
        self.assertNotIn('bottle.request.ext.body', request.environ)
        self.assertEqual(request.body.read(), b'original')

    def test_custom_attribute_remains_write_once(self):
        request = bottle.BaseRequest({})
        request.foo = 'original'
        self.assertEqual(request.foo, 'original')
        self.assertEqual(request.environ['bottle.request.ext.foo'], 'original')
        with self.assertRaises(AttributeError):
            request.foo = 'replacement'
        self.assertEqual(request.foo, 'original')


if __name__ == '__main__':
    unittest.main()
