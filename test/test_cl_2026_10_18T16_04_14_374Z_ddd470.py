import io
from pathlib import Path
import unittest
from wsgiref.util import setup_testing_defaults

import bottle


class TestEmptyIfModifiedSince(unittest.TestCase):
    def test_static_file_conditional_requests(self):
        fixture = Path(__file__).resolve().with_name('test_sendfile.py')
        content = fixture.read_bytes()
        mtime = int(fixture.stat().st_mtime)
        app = bottle.Bottle()

        @app.get('/')
        def serve():
            return bottle.static_file(fixture.name, root=str(fixture.parent))

        cases = (
            (None, 200, content),
            (bottle.http_date(mtime), 304, b''),
            (bottle.http_date(mtime - 1), 200, content),
            ('', 200, content),
        )
        for header, expected_status, expected_body in cases:
            with self.subTest(if_modified_since=header):
                environ = {}
                setup_testing_defaults(environ)
                environ['wsgi.errors'] = io.StringIO()
                if header is not None:
                    environ['HTTP_IF_MODIFIED_SINCE'] = header
                statuses = []

                def start_response(status, headers, exc_info=None):
                    statuses.append(int(status.split()[0]))

                result = app(environ, start_response)
                try:
                    body = b''.join(result)
                finally:
                    if hasattr(result, 'close'):
                        result.close()
                self.assertEqual([expected_status], statuses)
                self.assertEqual(expected_body, body)


if __name__ == '__main__':
    unittest.main()
