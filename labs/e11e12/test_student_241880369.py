import tempfile
import unittest
from pathlib import Path

import pipeline
import server


class StudentE11E12A241880369(unittest.TestCase):
    """高嘉程 241880369：fixed_report 必须位于 /course/data 之下。"""

    def test_fixed_report_outside_data_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            store = server.Store(Path(d) / 'jobs')
            request = {
                'mode': 'e11-b',
                'repo': str(pipeline.ROOT / 'data/p'),
                'base': 'a' * 40,
                'target': 'b' * 40,
                'candidate': str(pipeline.ROOT / 'data/candidate.Dockerfile'),
                'fixed_report': str(Path(d) / 'fixed-md.json'),
            }
            try:
                with self.assertRaisesRegex(ValueError, 'fixed_report must be under /course/data'):
                    store.submit(request, 'fixed-report-boundary')
            finally:
                store.pool.shutdown()

if __name__ == '__main__':
    unittest.main()
