import os, tempfile, unittest, importlib.util
os.environ['DATABASE_PATH']=tempfile.mktemp(suffix='.db')
spec=importlib.util.spec_from_file_location('app','server.py')
app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)
class AppTest(unittest.TestCase):
    def test_seed_and_password(self):
        c=app.conn(); self.assertGreater(c.execute('select count(*) from products').fetchone()[0],0)
        u=c.execute('select password from users').fetchone()[0]
        self.assertTrue(app.verify('change-this-before-production',u)); c.close()
    def test_order_shipping_fields_are_migrated(self):
        c=app.conn(); columns={row['name'] for row in c.execute('pragma table_info(orders)')}; c.close()
        self.assertTrue({'country','address_line1','city','postal_code','notes'} <= columns)
    def test_product_commerce_fields_are_persisted(self):
        c=app.conn(); row=c.execute("select price_cents,inventory,sku,currency from products where slug='trm-100'").fetchone(); c.close()
        self.assertEqual(dict(row),{'price_cents':18900,'inventory':24,'sku':'TRM-100-STD','currency':'USD'})
    def test_order_price_is_server_owned(self):
        items,total=app.price_order([{'slug':'trm-100','quantity':2,'price_cents':1}])
        self.assertEqual(total,37800); self.assertEqual(items[0]['unit_price_cents'],18900)
    def test_signature(self): self.assertEqual(app.sign('value'),app.sign('value'))
if __name__=='__main__': unittest.main()
