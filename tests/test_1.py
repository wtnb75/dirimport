import unittest
import os
import types
import tempfile
from dirimport import gen


class Test1(unittest.TestCase):
    def gendir(self, tmpd):
        with open(os.path.join(tmpd, "xxx.py"), "w") as tmpfp:
            print('print("hello xxx")', file=tmpfp)
            print("a = True", file=tmpfp)
        with open(os.path.join(tmpd, "yyy.py"), "w") as tmpfp:
            print('print("hello yyy")', file=tmpfp)
            print("b = False", file=tmpfp)
        with open(os.path.join(tmpd, "_zzz.py"), "w") as tmpfp:
            print('print("hello zzz")', file=tmpfp)
            print("c = False", file=tmpfp)
        with open(os.path.join(tmpd, ".aaaa.py"), "w") as tmpfp:
            print('print("hello aaa")', file=tmpfp)

    def test_dig(self):
        with tempfile.TemporaryDirectory(dir=".") as tmpd:
            self.gendir(tmpd)
            resd, resf = gen.dig(tmpd)
            self.assertEquals(["xxx", "yyy"], resf, "files")
            self.assertEquals(0, len(resd), "dirs")

            os.mkdir(os.path.join(tmpd, "hello"))
            os.mkdir(os.path.join(tmpd, "world"))
            resd, resf = gen.dig(tmpd)
            self.assertEquals(["xxx", "yyy"], resf, "files")
            self.assertEquals(0, len(resd), "dirs")

            with open(os.path.join(tmpd, "hello", "xyz.py"), "w") as tmpfp:
                print('print("hello xyz")', file=tmpfp)
            resd, resf = gen.dig(tmpd)
            self.assertEquals(["xxx", "yyy"], resf, "files")
            self.assertEquals(1, len(resd), "dirs")

    def test_gen(self):
        with tempfile.TemporaryDirectory(dir=".") as tmpd:
            self.gendir(tmpd)
            gen.generate(gen.dig(tmpd), tmpd)
            with open(os.path.join(tmpd, "__init__.py")) as tmpfp:
                s = tmpfp.read()
                self.assertIn("from .xxx import *", s, "xxx")
                self.assertIn("from .yyy import *", s, "yyy")
                self.assertNotIn("._zzz", s, "zzz")

            os.mkdir(os.path.join(tmpd, "hello"))
            os.mkdir(os.path.join(tmpd, "world"))
            with open(os.path.join(tmpd, "hello", "xyz.py"), "w") as tmpfp:
                print('print("hello xyz")', file=tmpfp)
            gen.generate(gen.dig(tmpd), tmpd, "initinit.py")
            with open(os.path.join(tmpd, "initinit.py")) as tmpfp:
                s = tmpfp.read()
                self.assertIn("from .xxx import *", s, "xxx")
                self.assertIn("from .yyy import *", s, "yyy")
                self.assertNotIn("._zzz", s, "zzz")
                self.assertIn("from . import hello", s, "hello")
                self.assertNotIn("world", s, "world")
                self.assertIn("noqa", s, "noqa")
            with open(os.path.join(tmpd, "hello", "initinit.py")) as tmpfp:
                s = tmpfp.read()
                self.assertIn("xyz", s, "xyz")

    def test_clear(self):
        with tempfile.TemporaryDirectory(dir=".") as tmpd:
            self.gendir(tmpd)
            gen.generate(gen.dig(tmpd), tmpd)
            gen.clear(tmpd)
            self.assertFalse(os.path.exists(
                os.path.join(tmpd, "__init__.py")), "initpy")

    def test_importall1(self):
        with tempfile.TemporaryDirectory(dir=".") as tmpd:
            self.gendir(tmpd)
            mod = gen.importall(tmpd)
            self.assertTrue(isinstance(mod, types.ModuleType), "module")
            self.assertTrue(hasattr(mod, "a"), "a exists")
            self.assertFalse(hasattr(mod, "c"), "c does not exists")
            self.assertTrue(getattr(mod, "a"), "true")
            self.assertFalse(getattr(mod, "b"), "false")

    def test_importall2(self):
        with tempfile.TemporaryDirectory(dir=".") as tmpd:
            self.gendir(tmpd)
            with open(os.path.join(tmpd, "zzz.py"), "w") as tmpfp:
                print('print("hello zzz")', file=tmpfp)
                print("b = True", file=tmpfp)
            os.mkdir(os.path.join(tmpd, "hello"))
            os.mkdir(os.path.join(tmpd, "world"))
            with open(os.path.join(tmpd, "hello", "xyz.py"), "w") as tmpfp:
                print('print("hello xyz")', file=tmpfp)
                print("d = True", file=tmpfp)

            mod = gen.importall(tmpd)
            self.assertTrue(hasattr(mod, "hello"), "hello exists")
            self.assertFalse(hasattr(mod, "world"), "world does not exists")
            self.assertTrue(getattr(getattr(mod, "hello"), "d"), "true")

    def test_diff(self):
        with tempfile.TemporaryDirectory(dir=".") as tmpd:
            self.gendir(tmpd)
            with open(os.path.join(tmpd, "__init__.py"), "w") as tmpfp:
                print("from .xyz import *", file=tmpfp)
            diff = gen.diff(gen.dig(tmpd), tmpd)
            self.assertIn("-from .xyz import *", diff, "xyz")
            self.assertIn("+from .xxx import *", "\n".join(diff), "xxx")

            os.unlink(os.path.join(tmpd, "__init__.py"))
            diff = gen.diff(gen.dig(tmpd), tmpd)
            self.assertIn("+from .xxx import *", "\n".join(diff), "xxx")

            gen.generate(gen.dig(tmpd), tmpd)
            diff = gen.diff(gen.dig(tmpd), tmpd)
            self.assertEquals(0, len(diff), "generated")
