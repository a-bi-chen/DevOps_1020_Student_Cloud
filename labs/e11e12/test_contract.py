import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pipeline
import server

class Contracts(unittest.TestCase):
    def report(self):return {'schema_version':'e11e12-1','kind':'incremental-check','commit':'a'*40,'status':'SUCCEEDED'}
    def test_accept_current_report(self):pipeline.check_envelope(self.report(),'a'*40,'incremental-check')
    def test_reject_old_commit(self):
        with self.assertRaisesRegex(pipeline.Failure,'another commit'):pipeline.check_envelope(self.report(),'b'*40)
    def test_reject_schema(self):
        r=self.report();r['schema_version']='old'
        with self.assertRaises(pipeline.Failure):pipeline.check_envelope(r,'a'*40)
    def test_reject_failed_upstream(self):
        r=self.report();r['status']='FAILED'
        with self.assertRaises(pipeline.Failure):pipeline.check_envelope(r,'a'*40)
    def test_reject_wrong_artifact_kind(self):
        with self.assertRaises(pipeline.Failure):pipeline.check_envelope(self.report(),'a'*40,'fixed-md')
    def test_artifact_uses_relative_uri_and_content_hash(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);p=root/'x.json';p.write_text('{}')
            a=pipeline.artifact(p,root,'job-1');self.assertEqual(a['uri'],'artifact://job-1/x.json');self.assertEqual(len(a['sha256']),64)
    def test_existing_evidence_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'keep').write_text('keep')
            with self.assertRaises(pipeline.Failure):pipeline.execute({},root)
            self.assertEqual((root/'keep').read_text(),'keep')
    def test_changed_artifact_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'r.json';p.write_text('{}')
            with self.assertRaises(pipeline.Failure):pipeline.load_artifact(p,'0'*64)
    def test_same_key_same_request_same_job(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);store=server.Store(root/'jobs')
            request={'mode':'e11-a','repo':str(pipeline.ROOT/'data/p'),'base':'a','target':'b'}
            with patch.object(store.pool,'submit'):
                one=store.submit(request,'same');two=store.submit(request,'same')
                self.assertEqual(one['job_id'],two['job_id'])
                changed=dict(request,target='c')
                with self.assertRaisesRegex(ValueError,'IDEMPOTENCY_CONFLICT'):store.submit(changed,'same')
            store.pool.shutdown()
    def test_api_rejects_repo_outside_data(self):
        with tempfile.TemporaryDirectory() as d:
            store=server.Store(Path(d)/'jobs')
            with self.assertRaises(ValueError):store.submit({'mode':'e11-a','repo':str(Path(d)),'base':'a','target':'b'},'k')
            store.pool.shutdown()

if __name__=='__main__':unittest.main()

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

