"""Personal regression tests for 241880089 (E13 A-side crosscheck adapter).

These tests exercise the adapter's declaration parsing and its two explicit
rejection paths without running gcc, git or Docker.  They complement the
server evidence under ``evidence/students/241880089/e13-e14/``.
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
ADAPTER = REPO / "labs" / "e13" / "run_crosscheck.py"


def load_adapter():
    spec = importlib.util.spec_from_file_location("e13_crosscheck_241880089", ADAPTER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class StudentE13E14A241880089(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.adapter = load_adapter()

    def project(self, makefile: str) -> Path:
        handle = tempfile.TemporaryDirectory()
        self.addCleanup(handle.cleanup)
        root = Path(handle.name)
        (root / "Makefile").write_text(makefile, encoding="utf-8")
        return root

    def test_b09_style_variable_assignments_are_resolved(self):
        root = self.project(
            "CFLAGS ?= -std=c11 -Wall -Wextra -Werror\n"
            "DEPS := helper.h config.h\n"
            "main.o: main.c $(DEPS)\n"
            "helper.o: helper.c helper.h config.h\n"
        )

        graph, flags = self.adapter.declarations_e13(root)

        self.assertEqual(flags, "-std=c11 -Wall -Wextra -Werror")
        self.assertEqual(graph["main.o"], ["config.h", "helper.h", "main.c"])
        self.assertEqual(graph["helper.o"], ["config.h", "helper.c", "helper.h"])

    def test_order_only_rule_is_rejected(self):
        root = self.project(
            "CFLAGS := -std=c11 -Wall -Wextra -Werror\n"
            "main.o: main.c | order-only\n"
            "helper.o: helper.c\n"
        )

        with self.assertRaisesRegex(ValueError, "UNSUPPORTED_DECLARATION"):
            self.adapter.declarations_e13(root)

    def test_non_allowlisted_flags_are_rejected(self):
        root = self.project(
            "CFLAGS := -O2\n"
            "main.o: main.c\n"
            "helper.o: helper.c\n"
        )

        with self.assertRaisesRegex(ValueError, "UNSUPPORTED_FLAGS"):
            self.adapter.scan_e13(root)


if __name__ == "__main__":
    unittest.main()
