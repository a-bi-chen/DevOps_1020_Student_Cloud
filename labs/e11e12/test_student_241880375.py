import json
import tempfile
import unittest
from pathlib import Path
import pipeline
import server

class StudentE11E12A241880375(unittest.TestCase):
    """张海洋 241880375：服务重启后的任务状态恢复契约。"""

    def test_restart_marks_unfinished_job_and_keeps_completed_job(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'jobs'
            completed = {
                'schema_version': 'e11e12-1', 'job_id': 'job-completed',
                'status': 'SUCCEEDED', 'idempotency_key': 'completed-key',
                'request_hash': 'a' * 64, 'trace_id': 'trace-completed',
            }
            unfinished = {
                'schema_version': 'e11e12-1', 'job_id': 'job-unfinished',
                'status': 'RUNNING', 'idempotency_key': 'unfinished-key',
                'request_hash': 'b' * 64,
            }
            pipeline.save(root / 'job-completed' / 'state.json', completed)
            pipeline.save(root / 'job-unfinished' / 'state.json', unfinished)

            store = server.Store(root)
            try:
                self.assertEqual(store.jobs['job-completed']['status'], 'SUCCEEDED')
                self.assertEqual(store.jobs['job-unfinished']['status'], 'FAILED')
                self.assertEqual(store.jobs['job-unfinished']['error']['code'], 'SERVER_RESTARTED')
                persisted = json.loads(
                    (root / 'job-unfinished' / 'state.json').read_text())
                self.assertEqual(persisted['status'], 'FAILED')
                self.assertEqual(persisted['error']['code'], 'SERVER_RESTARTED')
            finally:
                store.pool.shutdown()

if __name__=='__main__':unittest.main()
