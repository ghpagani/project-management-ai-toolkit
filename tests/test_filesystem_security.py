import concurrent.futures
import json
import os
import tempfile
import unittest
from pathlib import Path

from test_review import r


class FilesystemSecurityTests(unittest.TestCase):
    def test_competing_publications_do_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'out.json'
            def publish(number):
                try:
                    r.write_report(target, {'writer': number})
                    return True
                except (r.Invalid, FileExistsError):
                    return False
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(publish, range(8)))
            self.assertEqual(sum(results), 1)
            self.assertIn(json.loads(target.read_text())['writer'], range(8))
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_symlink_input_is_rejected_when_available(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'input.json'
            target.write_text('{}')
            link = Path(directory) / 'link.json'
            try:
                os.symlink(target, link)
            except (OSError, NotImplementedError):
                self.skipTest('Symlink creation unavailable without elevated privileges')
            with self.assertRaisesRegex(r.Invalid, 'INPUT_NOT_REGULAR'):
                r.safe_input(link)
