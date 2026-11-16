import tempfile
import unittest
from pathlib import Path
import pipeline
import server

class StudentE11E12A241880374(unittest.TestCase):
    def test_candidate_outside_data_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            store=server.Store(Path(d)/'jobs')
            req={'mode':'e11-a','repo':str(pipeline.ROOT/'data/p'),
                 'base':'a','target':'b',
                 'candidate':str(Path(d)/'candidate.Dockerfile')}
            try:
                with self.assertRaisesRegex(ValueError,'candidate must be under /course/data'):
                    store.submit(req,'candidate-boundary')
            finally:
                store.pool.shutdown()

if __name__=='__main__':unittest.main()
