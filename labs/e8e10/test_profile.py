import json, tempfile, unittest
from pathlib import Path
from lab import fixture,scan,patch,commit

class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.p=Path(self.tmp.name)/'sample';fixture(self.p)

    def test_independent_known_edges(self):
        r=scan(self.p)
        self.assertEqual(r['actual']['main.o'],['config.h','main.c'])
        self.assertEqual({(f['type'],f['dependency']) for f in r['findings']},{('MISSING','config.h'),('REDUNDANT','unused.h')})

    def test_unchanged_reuses_both_targets(self):
        r=scan(self.p,scan(self.p));self.assertEqual(r['reused'],['main.o','helper.o']);self.assertEqual(r['refreshed'],[])

    def test_include_added_invalidates_cache(self):
        old=scan(self.p)
        (self.p/'main.c').write_text('#include "extra.h"\n'+(self.p/'main.c').read_text());commit(self.p,'new include')
        r=scan(self.p,old)
        self.assertIn(['MISSING','main.o','extra.h'],r['added']);self.assertEqual(len(r['refreshed']),2)

    def test_patch_preserves_redundant_dependency(self):
        r=scan(self.p);diff,plan=patch(self.p,r)
        self.assertIn('+main.o: main.c unused.h config.h',diff)
        self.assertNotIn('-\tgcc',diff)
        self.assertNotIn('config.h',(self.p/'Makefile').read_text())

    def test_old_report_rejected(self):
        r=scan(self.p);r['commit']='0'*40
        with self.assertRaisesRegex(ValueError,'STALE_REPORT'):patch(self.p,r)

    def test_unsafe_dependency_rejected(self):
        r=scan(self.p);r['findings']=[{'type':'MISSING','target':'main.o','dependency':'../outside.h'}]
        with self.assertRaisesRegex(ValueError,'UNSAFE_PATH'):patch(self.p,r)

    def test_unsupported_configuration_rejected(self):
        (self.p/'Makefile').write_text((self.p/'Makefile').read_text().replace('-O0','-include unknown.h'))
        with self.assertRaisesRegex(ValueError,'UNSUPPORTED_FLAGS'):scan(self.p)

# ---------------------------------------------------------------------------
# 个人测试区（模板）：每名成员在本行以下新增一个独立测试类，类名自取
# （如 StudentE8A<学号>），至少覆盖一个新的变化方向并使用独立预期。
# 不要改动上方 ProfileTests 的既有断言；写法参考课程材料《08_个人测试编写示例.md》。
# ---------------------------------------------------------------------------

class StudentE8A089(unittest.TestCase):
    def test_recipe_change_invalidates_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample';fixture(p)
            old=scan(p)
            (p/'Makefile').write_text((p/'Makefile').read_text().replace(
                'gcc $(CFLAGS) -c main.c -o main.o',
                'gcc $(CFLAGS) -Wall -c main.c -o main.o'))
            commit(p,'student: change main.o recipe')
            r=scan(p,old)
            self.assertEqual(set(r['refreshed']),{'main.o','helper.o'})
            self.assertEqual(r['reused'],[])
            self.assertEqual(r['actual'],old['actual'])
            self.assertEqual(r['findings'],old['findings'])

class StudentE9A089(unittest.TestCase):
    def test_macro_value_change_invalidates_without_graph_change(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample';fixture(p)
            old=scan(p)
            (p/'config.h').write_text('#define VALUE 2\n')
            commit(p,'student: change macro value')
            r=scan(p,old)
            self.assertEqual(set(r['refreshed']),{'main.o','helper.o'})
            self.assertEqual(r['reused'],[])
            self.assertEqual(r['actual'],old['actual'])
            self.assertEqual(r['findings'],old['findings'])
            self.assertEqual(r['added'],[])
            self.assertEqual(r['resolved'],[])

class StudentE10A089(unittest.TestCase):
    def test_unrelated_new_header_refreshes_and_matches_full_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample';fixture(p)
            old=scan(p)
            (p/'notes.h').write_text('/* no preprocessor directives */\n')
            commit(p,'student: add unrelated header')
            inc=scan(p,old);full=scan(p)
            self.assertEqual(set(inc['refreshed']),{'main.o','helper.o'})
            self.assertEqual(inc['reused'],[])
            self.assertEqual(inc['actual'],full['actual'])
            self.assertEqual(inc['declared'],full['declared'])
            self.assertEqual(inc['findings'],full['findings'])
            self.assertEqual(inc['actual'],old['actual'])

if __name__=='__main__':unittest.main()
