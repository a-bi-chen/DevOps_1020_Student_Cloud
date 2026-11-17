"""陈玉熙 241880089：macro / mixed 依赖声明补丁位置契约。"""
import tempfile
import unittest
from pathlib import Path

import lab


class StudentE11E12A241880089(unittest.TestCase):
    """MDFixer 必须把缺失依赖补到实际声明位置，且不删除冗余声明。"""

    def test_macro_and_mixed_dependency_patch_lands_on_declaration(self):
        with tempfile.TemporaryDirectory() as d:
            for style in ('macro', 'mixed'):
                project = Path(d) / style
                lab.fixture(project, style)
                commit = lab.run(['git', 'rev-parse', 'HEAD'], project).strip()
                report = {
                    'commit': commit,
                    'findings': [
                        {'type': 'MISSING', 'target': 'main.o', 'dependency': 'config.h'},
                    ],
                }

                diff, edits = lab.patch(project, report)
                patchfile = project / 'candidate.patch'
                patchfile.write_text(diff)
                lab.run(['git', 'apply', str(patchfile.name)], project)

                self.assertEqual(edits[0]['style'], style)
                self.assertIn('config.h', diff)
                makefile = (project / 'Makefile').read_text()
                if style == 'macro':
                    self.assertIn('DEPS = main.c unused.h config.h', makefile)
                    self.assertIn('main.o: $(DEPS)', makefile)
                else:
                    self.assertIn('main.o: main.c $(HEADERS) config.h', makefile)
                # RD 只保留，不因修复 MD 而被删除。
                self.assertIn('unused.h', makefile)


if __name__ == '__main__':
    unittest.main()
