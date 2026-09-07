import os, tempfile, unittest, importlib.util
os.environ['DATABASE_PATH']=tempfile.mktemp(suffix='.db')
spec=importlib.util.spec_from_file_location('app','server.py')
app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
class AppTest(unittest.TestCase):
    def test_seed_and_password(self):
        c=app.conn(); self.assertGreater(c.execute('select count(*) from products').fetchone()[0],0)
        u=c.execute('select password from users').fetchone()[0]
        self.assertTrue(app.verify('change-this-before-production',u)); c.close()
    def test_signature(self): self.assertEqual(app.sign('value'),app.sign('value'))
if __name__=='__main__': unittest.main()
