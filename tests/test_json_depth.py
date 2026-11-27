import json
import unittest

from test_review import r


class JsonDepthTests(unittest.TestCase):
    def test_boundary_accepts_64_arrays(self):
        raw = b'[' * 64 + b'0' + b']' * 64
        self.assertEqual(r.parse(raw), json.loads(raw))

    def test_rejects_65_mixed_containers(self):
        raw = b'{"a":' * 32 + b'[' * 33 + b'0' + b']' * 33 + b'}' * 32
        with self.assertRaisesRegex(r.Invalid, 'JSON_TOO_DEEP'):
            r.parse(raw)

    def test_delimiters_and_escapes_inside_strings(self):
        value = {'text': '[{' * 100 + '\\"' + '}]' * 100}
        self.assertEqual(r.parse(json.dumps(value).encode()), value)

    def test_malformed_json_rejected(self):
        for raw in (b'{"x":[}', b'{"x":"unterminated}', b'[[1]'):
            with self.subTest(raw=raw), self.assertRaises(r.Invalid):
                r.parse(raw)
