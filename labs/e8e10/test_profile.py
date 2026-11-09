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

class StudentE9A089RemovedInclude(unittest.TestCase):
    def test_removed_include_invalidates_and_resolves(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample';fixture(p)
            old=scan(p)
            (p/'main.c').write_text((p/'main.c').read_text().replace(
                '#include "config.h"\n',
                ''))
            commit(p,'student: remove config include')
            r=scan(p,old)
            self.assertEqual(set(r['refreshed']),{'main.o','helper.o'})
            self.assertEqual(r['reused'],[])
            self.assertEqual(r['added'],[])
            self.assertNotIn('config.h',r['actual']['main.o'])
            self.assertIn(['MISSING','main.o','config.h'],r['resolved'])
            self.assertEqual(r['findings'],[{'type':'REDUNDANT','target':'main.o','dependency':'unused.h'}])

# --- 以下为组员个人测试（按其学生分支原样并入） --------------------------------

class StudentE10A(unittest.TestCase):
    """高嘉程 241880369：头文件内部的传递 include。"""
    def test_transitive_include_matches_full_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample'
            fixture(p)
            old=scan(p)
            (p/'config.h').write_text('#include "extra.h"\n#define VALUE 1\n')
            (p/'extra.h').write_text('#include "leaf.h"\n')
            (p/'leaf.h').write_text('#define LEAF 7\n')
            commit(p,'student: transitive include')
            incremental=scan(p,old)
            full=scan(p)
            for key in ['actual','declared','findings']:
                self.assertEqual(incremental[key],full[key])
            self.assertEqual(incremental['actual']['main.o'],['config.h','extra.h','leaf.h','main.c'])
            missing={x['dependency'] for x in incremental['findings'] if x['type']=='MISSING'}
            self.assertEqual(missing,{'config.h','extra.h','leaf.h'})

class StudentE8A(unittest.TestCase):
    """马海川 241880374：只补声明时复用实际图。"""
    def test_declaration_change_reuses_actual_graph(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample'
            fixture(p)
            old=scan(p)
            f=p/'Makefile'
            f.write_text(f.read_text().replace(
                'main.c unused.h',
                'main.c unused.h config.h'))
            commit(p,'student: add missing declaration')
            result=scan(p,old)
            self.assertEqual(result['actual'],old['actual'])
            self.assertEqual(set(result['reused']),{'main.o','helper.o'})
            self.assertEqual(result['refreshed'],[])
            self.assertEqual(
                {(x['type'],x['target'],x['dependency'])
                 for x in result['findings']},
                {('REDUNDANT','main.o','unused.h')})

class StudentE9A(unittest.TestCase):
    """张海洋 241880375：头文件内部新增 include 使缓存失效。"""
    def test_include_inside_header_invalidates(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'sample'
            fixture(p)
            old=scan(p)
            (p/'config.h').write_text('#include "extra.h"\n#define VALUE 1\n')
            commit(p,'student: header includes extra')
            result=scan(p,old)
            self.assertEqual(result['actual']['main.o'],['config.h','extra.h','main.c'])
            self.assertEqual({tuple(x) for x in result['added']},{('MISSING','main.o','extra.h')})
            self.assertEqual(set(result['refreshed']),{'main.o','helper.o'})
            self.assertEqual(result['reused'],[])

if __name__=='__main__':unittest.main()
