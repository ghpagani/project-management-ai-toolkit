import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_review import SKILL


class LocalizedReports(unittest.TestCase):
    def test_markdown_cli_both_languages_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            for lang, heading in [('en', 'Project review'), ('pt-BR', 'Revisão de projeto')]:
                output = Path(directory) / (lang + '.md')
                cmd = [sys.executable, str(SKILL / 'scripts/review.py'), '--input',
                       str(SKILL / 'examples/project.json'), '--out', str(output),
                       '--format', 'md', '--lang', lang]
                result = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                content = output.read_text(encoding='utf-8')
                self.assertIn(heading, content)
                self.assertIn('T001', content)
                self.assertIn('100000000', content)
                self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
                self.assertEqual(output.read_text(encoding='utf-8'), content)
