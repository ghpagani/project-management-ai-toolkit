import hashlib, importlib.util, json, tempfile, unittest, subprocess, sys, zipfile
from pathlib import Path
from test_review import ROOT
class PackageTests(unittest.TestCase):
    def run_script(self,*args): return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True)
    def test_validate(self):
        x=self.run_script('scripts/validate_package.py'); self.assertEqual(x.returncode,0,x.stderr)
    def test_packages(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); a=p/'a'; b=p/'b'
            for out in (a,b):
                x=self.run_script('scripts/build_release.py','--out-dir',out); self.assertEqual(x.returncode,0,x.stderr)
            for f in a.iterdir(): self.assertEqual(f.read_bytes(),(b/f.name).read_bytes())
            for kind in ('skill','plugin'):
                f=a/f'project-management-ai-{kind}-0.1.0.zip'; self.assertIn(hashlib.sha256(f.read_bytes()).hexdigest(),(a/'SHA256SUMS').read_text()); dest=p/kind
                with zipfile.ZipFile(f) as z:
                    self.assertIsNone(z.testzip()); self.assertFalse(any('..' in n.split('/') or n.startswith('/') or '__pycache__' in n for n in z.namelist())); z.extractall(dest)
                skill=dest/'project-management-ai'; skill=skill if kind=='skill' else skill/'skills/project-management-ai'
                x=self.run_script(skill/'scripts/review.py','--input',skill/'examples/project.json','--out',p/f'{kind}.json'); self.assertEqual(x.returncode,0,x.stderr)
                self.assertEqual(json.loads((p/f'{kind}.json').read_text())['schedule']['duration_days'],15)
            self.assertNotEqual(self.run_script('scripts/build_release.py','--out-dir',a).returncode,0)
