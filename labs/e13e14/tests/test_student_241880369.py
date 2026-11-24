"""Personal independent tests for student 241880369 (A09 / track A).

These tests are intentionally independent of the shared contract tests:
- a deliberately broken source patch must be rejected and must not modify the
  project Makefile (E13 C5 rollback expectation);
- the runtime log scanner must block an obvious fake key, pass after cleanup,
  and report an incomplete scan (exit 2) for a missing path (E13 C6).
"""

import difflib
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "labs" / "e8e10"))
from lab import validate  # noqa: E402

SCAN = ROOT / "labs" / "e13e14" / "scan_runtime_logs.py"
# Built at runtime on purpose: the source must not contain a contiguous
# credential-looking literal, otherwise the repository secret scanner (and CI)
# would flag this placeholder itself.
FAKE_KEY = "sk-" + "demo" + "241880369" + "abcdefghijkl"


class StudentE13E14A241880369(unittest.TestCase):
    def test_broken_patch_rejected_and_makefile_unchanged(self):
        tmp = Path(tempfile.mkdtemp(prefix="s241880369-c5-"))
        try:
            project = tmp / "project"
            shutil.copytree(ROOT / "fixtures" / "md-rd", project)
            main = project / "main.c"
            original = main.read_text(encoding="utf-8")
            broken = original.replace(
                'printf("%d\\n", VALUE)', 'printf("%d\\n", VALUE + 1)'
            )
            self.assertNotEqual(original, broken, "fixture text must change")
            patch = "".join(
                difflib.unified_diff(
                    original.splitlines(True),
                    broken.splitlines(True),
                    fromfile="a/main.c",
                    tofile="b/main.c",
                )
            )
            patch_file = tmp / "broken.patch"
            patch_file.write_text(patch, encoding="utf-8")
            makefile = project / "Makefile"
            before = hashlib.sha256(makefile.read_bytes()).hexdigest()

            verdict = validate(project, patch_file, tmp / "evidence")

            self.assertFalse(verdict["accepted"], "broken patch must be rejected")
            self.assertTrue(verdict["rollback"])
            self.assertTrue(verdict["source_unchanged"])
            after = hashlib.sha256(makefile.read_bytes()).hexdigest()
            self.assertEqual(before, after, "source Makefile must stay unchanged")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_runtime_log_scan_blocks_fake_key_then_passes_clean(self):
        tmp = Path(tempfile.mkdtemp(prefix="s241880369-c6-"))
        try:
            probe = tmp / "probe.log"
            probe.write_text('api_key = "%s"\n' % FAKE_KEY, encoding="utf-8")
            hit = subprocess.run(
                [sys.executable, str(SCAN), str(probe)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(hit.returncode, 1, hit.stdout + hit.stderr)
            self.assertIn("LLM/API Key", hit.stdout)
            self.assertNotIn(FAKE_KEY, hit.stdout, "scanner must mask the value")

            probe.write_text("clean content for 241880369\n", encoding="utf-8")
            clean = subprocess.run(
                [sys.executable, str(SCAN), str(probe)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(clean.returncode, 0, clean.stdout + clean.stderr)

            missing = subprocess.run(
                [sys.executable, str(SCAN), str(tmp / "does-not-exist.log")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(missing.returncode, 2, missing.stdout + missing.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
