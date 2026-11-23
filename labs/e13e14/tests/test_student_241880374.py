import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scan_runtime_logs


class StudentE13E14A241880374(unittest.TestCase):
    def scan(self, path):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = scan_runtime_logs.main([str(path)])
        return code, out.getvalue(), err.getvalue()

    def test_fake_key_blocks_then_clean_content_passes(self):
        with tempfile.TemporaryDirectory() as d:
            probe = Path(d) / "probe.log"
            # 运行时拼接，避免把形似真实密钥的字面量写进源码与 Git 历史。
            fake = "sk-" + "demo1234567890abcdefghijk"
            probe.write_text('api_key = "' + fake + '"\n', encoding="utf-8")
            code, out, _ = self.scan(probe)
            self.assertEqual(code, 1, "第一次扫描必须阻断")
            self.assertIn("LLM/API Key", out)
            self.assertNotIn(fake, out, "命中值必须脱敏，不能整串打印")

            probe.write_text("probe completed; clean content\n", encoding="utf-8")
            code, out, _ = self.scan(probe)
            self.assertEqual(code, 0, "清理后复扫必须通过")
            self.assertIn("hits=0", out)

    def test_missing_path_is_incomplete_scan(self):
        code, _, err = self.scan("work/does-not-exist-241880374")
        self.assertEqual(code, 2, "路径缺失必须是 2，不能当作通过")
        self.assertIn("missing path", err)


if __name__ == "__main__":
    unittest.main()