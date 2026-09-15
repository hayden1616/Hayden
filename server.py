import base64, hashlib, hmac, json, mimetypes, os, secrets, sqlite3, time, uuid
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT=Path(__file__).resolve().parent; DATA=ROOT/'data'; DATA.mkdir(exist_ok=True); UPLOADS=DATA/'uploads'; UPLOADS.mkdir(exist_ok=True); MEDIA=DATA/'product-media'; MEDIA.mkdir(exist_ok=True)
def env(name, default=''):
    # tiny .env loader without adding a runtime dependency
    return os.environ.get(name, default)
for line in (ROOT/'.env').read_text().splitlines() if (ROOT/'.env').exists() else []:
    if '=' in line and not line.lstrip().startswith('#'):
        k,v=line.split('=',1); os.environ.setdefault(k,v)
DB=Path(env('DATABASE_PATH',str(DATA/'industrial.db'))); DB.parent.mkdir(parents=True,exist_ok=True)
SECRET=env('SESSION_SECRET','development-only-change-me').encode(); ORIGIN=env('SITE_ORIGIN','http://localhost:8000').rstrip('/')
PRODUCTS=[
('trm-100','TRM-100','Flow Measurement','Inline flow transmitter for water and compatible process media.','Flow','0.2–12 m/s','4–20 mA / Modbus RTU','IP67'),
('lsg-210','LSG-210','Level Sensing','Guided-wave level switch for vessels and process tanks.','Level','Up to 20 m','PNP / relay','IP68'),
('wcn-320','WCN-320','Weighing','Stainless compression load cell for batching and platform systems.','Weighing','0.5–30 t','mV/V / CANopen','IP68'),
('ana-410','ANA-410','Process Analysis','Conductivity analyser with temperature compensation.','Analysis','0–200 mS/cm','4–20 mA / Ethernet','IP65'),
('ctl-510','CTL-510','Control','Panel controller for mixed-signal process automation.','Control','24 VDC','Modbus TCP / RTU','IP20'),
('int-620','INT-620','Integration','Protocol gateway for legacy field devices and PLC networks.','Integration','-20–70 °C','EtherNet/IP / Modbus','IP30')]
COMMERCE={
 'trm-100':{'price_cents':18900,'inventory':24,'sku':'TRM-100-STD'},
 'lsg-210':{'price_cents':23900,'inventory':18,'sku':'LSG-210-STD'},
 'wcn-320':{'price_cents':31500,'inventory':12,'sku':'WCN-320-STD'},
 'ana-410':{'price_cents':27900,'inventory':16,'sku':'ANA-410-STD'},
 'ctl-510':{'price_cents':34900,'inventory':9,'sku':'CTL-510-STD'},
 'int-620':{'price_cents':21900,'inventory':21,'sku':'INT-620-STD'}
}
def enrich_product(row):
 d=dict(row); d['currency']=d.get('currency') or 'USD'; d['sku']=d.get('sku') or d['model']; d['image_url']=d.get('image_url') or ''; return d
def price_order(items):
 if not isinstance(items,list) or not items: raise ValueError('Add at least one item.')
 priced=[]; total=0; c=conn()
 try:
  for item in items:
   slug=str(item.get('slug','')); quantity=max(1,min(99,int(item.get('quantity',1)))); product=c.execute('select slug,model,title,price_cents,inventory from products where slug=? and published=1',(slug,)).fetchone()
   if not product or product['price_cents']<=0 or quantity>product['inventory']: raise ValueError('A product is unavailable or exceeds available quantity.')
   priced.append({'slug':slug,'model':product['model'],'title':product['title'],'quantity':quantity,'unit_price_cents':product['price_cents']}); total+=product['price_cents']*quantity
 finally: c.close()
 return priced,total
def valid_product_image(filename,data):
 extension=Path(filename).suffix.lower(); signatures={'.jpg':data.startswith(b'\xff\xd8\xff'),'.jpeg':data.startswith(b'\xff\xd8\xff'),'.png':data.startswith(b'\x89PNG\r\n\x1a\n'),'.webp':data.startswith(b'RIFF') and data[8:12]==b'WEBP'}
 return extension in signatures and signatures[extension]
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def hash_pw(p):
    salt=secrets.token_bytes(16); return base64.b64encode(salt+hashlib.pbkdf2_hmac('sha256',p.encode(),salt,200000)).decode()
def verify(p,stored):
    raw=base64.b64decode(stored); return hmac.compare_digest(raw[16:],hashlib.pbkdf2_hmac('sha256',p.encode(),raw[:16],200000))
def init():
    c=conn(); c.executescript('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL); CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,slug TEXT UNIQUE,model TEXT,title TEXT,description TEXT,category TEXT,range_text TEXT,interface TEXT,rating TEXT,published INTEGER DEFAULT 1,updated_at TEXT DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS inquiries(id INTEGER PRIMARY KEY,reference TEXT UNIQUE,name TEXT,email TEXT,company TEXT,phone TEXT,product TEXT,message TEXT,consent INTEGER,ip_hash TEXT,state TEXT DEFAULT 'queued',created_at TEXT DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS outbox(id INTEGER PRIMARY KEY,inquiry_id INTEGER UNIQUE,state TEXT DEFAULT 'queued',attempts INTEGER DEFAULT 0,created_at TEXT DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY,reference TEXT UNIQUE,email TEXT,name TEXT,company TEXT,phone TEXT,items_json TEXT,total_cents INTEGER,currency TEXT DEFAULT 'USD',status TEXT DEFAULT 'pending_payment',created_at TEXT DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS rfq_attachments(id INTEGER PRIMARY KEY,inquiry_id INTEGER,filename TEXT,stored_name TEXT,content_type TEXT,size INTEGER); CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT,updated_at TEXT DEFAULT CURRENT_TIMESTAMP); CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,event TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);''')
    if not c.execute('select 1 from users').fetchone(): c.execute('insert into users(email,password,role) values(?,?,?)',(env('ADMIN_EMAIL','admin@example.com'),hash_pw(env('ADMIN_PASSWORD','change-this-before-production')),'admin'))
    if not c.execute('select 1 from products').fetchone(): c.executemany('insert into products(slug,model,title,description,category,range_text,interface,rating) values(?,?,?,?,?,?,?,?)',PRODUCTS)
    columns={row['name'] for row in c.execute('pragma table_info(products)')}; added='price_cents' not in columns
    for name,definition in [('price_cents','INTEGER NOT NULL DEFAULT 0'),('inventory','INTEGER NOT NULL DEFAULT 0'),('sku','TEXT'),('currency',"TEXT NOT NULL DEFAULT 'USD'"),('image_url',"TEXT NOT NULL DEFAULT ''")]:
     if name not in columns: c.execute(f'alter table products add column {name} {definition}')
    if added:
     for slug,meta in COMMERCE.items(): c.execute("update products set price_cents=?,inventory=?,sku=?,currency='USD' where slug=?",(meta['price_cents'],meta['inventory'],meta['sku'],slug))
    c.execute('create unique index if not exists idx_products_sku on products(sku) where sku is not null')
    order_columns={row['name'] for row in c.execute('pragma table_info(orders)')}
    for name,definition in [('country',"TEXT NOT NULL DEFAULT ''"),('address_line1',"TEXT NOT NULL DEFAULT ''"),('address_line2',"TEXT NOT NULL DEFAULT ''"),('city',"TEXT NOT NULL DEFAULT ''"),('region',"TEXT NOT NULL DEFAULT ''"),('postal_code',"TEXT NOT NULL DEFAULT ''"),('notes',"TEXT NOT NULL DEFAULT ''")]:
     if name not in order_columns: c.execute(f'alter table orders add column {name} {definition}')
    c.commit(); c.close()
init()
def sign(v): return base64.urlsafe_b64encode(hmac.new(SECRET,v.encode(),hashlib.sha256).digest()).decode().rstrip('=')
def session(handler):
    ck=SimpleCookie(handler.headers.get('Cookie')); item=ck.get('session')
    if not item: return None
    try:
      value,sig=item.value.rsplit('.',1)
      if hmac.compare_digest(sign(value),sig):
       data=json.loads(base64.urlsafe_b64decode(value+'===')); return data if data.get('exp',0)>int(time.time()) else None
    except Exception: pass
    return None
def api(handler,status,payload,headers=None):
    raw=json.dumps(payload).encode(); handler.send_response(status); handler.send_header('Content-Type','application/json; charset=utf-8'); handler.send_header('Content-Length',str(len(raw))); handler.send_header('X-Content-Type-Options','nosniff'); handler.send_header('Cache-Control','no-store')
    for k,v in (headers or {}).items(): handler.send_header(k,v)
    handler.end_headers(); handler.wfile.write(raw)
class App(SimpleHTTPRequestHandler):
  def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT/'public'),**kw)
  def log_message(self,*a): pass
  def body(self):
    try: return json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')) or 0))
    except: return {}
  def guard(self,mutate=False):
    s=session(self)
    if not s or s.get('role')!='admin': api(self,401,{'error':'Authentication required'}); return None
    if mutate and (self.headers.get('Origin') not in ('',ORIGIN) or self.headers.get('X-CSRF-Token')!=s.get('csrf')): api(self,403,{'error':'Request verification failed'}); return None
    return s
  def do_GET(self):
    p=urlparse(self.path); q=parse_qs(p.query)
    if p.path=='/api/health': return api(self,200,{'status':'ready','database':'sqlite'})
    if p.path.startswith('/media/products/'):
      filename=p.path.rsplit('/',1)[1]; file_path=(MEDIA/filename).resolve()
      if not filename or Path(filename).name!=filename or file_path.parent!=MEDIA.resolve() or not file_path.is_file(): return api(self,404,{'error':'Image not found.'})
      raw=file_path.read_bytes(); self.send_response(200); self.send_header('Content-Type',mimetypes.guess_type(filename)[0] or 'application/octet-stream'); self.send_header('Content-Length',str(len(raw))); self.send_header('Cache-Control','public, max-age=31536000, immutable'); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(raw); return
    if p.path=='/api/products':
      c=conn(); rows=[enrich_product(x) for x in c.execute('select * from products where published=1 order by model')]; c.close(); return api(self,200,{'products':rows})
    if p.path.startswith('/api/products/'):
      c=conn(); x=c.execute('select * from products where slug=? and published=1',(p.path.rsplit('/',1)[1],)).fetchone(); c.close(); return api(self,200,{'product':enrich_product(x) if x else None})
    if p.path=='/api/session':
      s=session(self); return api(self,200,{'authenticated':bool(s),'email':s.get('email') if s else None,'csrf':s.get('csrf') if s else None})
    if p.path.startswith('/api/admin/attachments/'):
      if not self.guard(): return
      try: attachment_id=int(p.path.rsplit('/',1)[1])
      except ValueError: return api(self,404,{'error':'Attachment not found.'})
      c=conn(); record=c.execute('select filename,stored_name,content_type,size from rfq_attachments where id=?',(attachment_id,)).fetchone(); c.close()
      if not record: return api(self,404,{'error':'Attachment not found.'})
      file_path=(UPLOADS/record['stored_name']).resolve()
      if file_path.parent!=UPLOADS.resolve() or not file_path.is_file(): return api(self,404,{'error':'Attachment file is unavailable.'})
      raw=file_path.read_bytes(); self.send_response(200); self.send_header('Content-Type',mimetypes.guess_type(record['filename'])[0] or 'application/octet-stream'); self.send_header('Content-Length',str(len(raw))); self.send_header('Content-Disposition',f"attachment; filename=\"{record['filename']}\""); self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Cache-Control','private, no-store'); self.end_headers(); self.wfile.write(raw); return
    if p.path=='/api/admin/orders':
      if not self.guard(): return
      c=conn(); rows=[]
      for x in c.execute('select id,reference,name,email,company,phone,country,address_line1,address_line2,city,region,postal_code,notes,items_json,total_cents,currency,status,created_at from orders order by id desc'):
       d=dict(x); d['items']=json.loads(d.pop('items_json')); rows.append(d)
      c.close(); return api(self,200,{'orders':rows})
    if p.path=='/api/admin/inquiries':
      if not self.guard(): return
      term=q.get('q',[''])[0].lower(); c=conn(); rows=[]
      for x in c.execute('select id,reference,name,email,company,phone,product,message,state,created_at from inquiries order by id desc'):
       d=dict(x); d['attachments']=[dict(a) for a in c.execute('select id,filename,size from rfq_attachments where inquiry_id=? order by id',(d['id'],))]; d['attachment_count']=len(d['attachments']); rows.append(d)
      c.close(); rows=[x for x in rows if term in json.dumps(x).lower()]; return api(self,200,{'inquiries':rows})
    if p.path=='/api/admin/products':
      if not self.guard(): return
      c=conn(); rows=[dict(x) for x in c.execute('select * from products order by model')]; c.close(); return api(self,200,{'products':rows})
    if p.path=='/api/admin/status':
      if not self.guard(): return
      c=conn(); total=c.execute('select count(*) from inquiries').fetchone()[0]; queued=c.execute("select count(*) from outbox where state='queued'").fetchone()[0]; endpoint=c.execute("select value from settings where key='delivery_endpoint'").fetchone(); orders=c.execute('select count(*) from orders').fetchone()[0]; c.close(); return api(self,200,{'inquiries':total,'orders':orders,'queued':queued,'delivery':'configured' if endpoint else 'unconfigured','worker':'off'})
    # Public routes are client-rendered but must survive a direct load or refresh.
    if p.path in ('/products','/cart','/checkout','/industries','/cases','/insights','/faq','/about','/admin') or p.path.startswith('/products/'):
      self.path='/index.html'
    return super().do_GET()
  def rfq_multipart(self):
    content_type=self.headers.get('Content-Type','')
    if 'multipart/form-data' not in content_type: return api(self,415,{'error':'Use multipart form data.'})
    boundary=content_type.split('boundary=',1)[-1].encode()
    raw=self.rfile.read(min(int(self.headers.get('Content-Length','0') or 0), 5*1024*1024+10000))
    if len(raw)>5*1024*1024: return api(self,413,{'error':'Attachment must be smaller than 5 MB.'})
    fields={}; attachment=None
    for part in raw.split(b'--'+boundary):
      if b'Content-Disposition:' not in part or b'\r\n\r\n' not in part: continue
      head,value=part.split(b'\r\n\r\n',1); value=value.rstrip(b'\r\n-')
      disp=head.decode('utf-8','ignore'); name=''
      if 'name="' in disp: name=disp.split('name="',1)[1].split('"',1)[0]
      if 'filename="' in disp and value:
       fn=disp.split('filename="',1)[1].split('"',1)[0]; attachment=(fn,value, 'application/octet-stream')
      elif name: fields[name]=value.decode('utf-8','ignore').strip()
    required=['name','email','company','message','quantity']
    if any(not fields.get(x) for x in required) or '@' not in fields.get('email',''): return api(self,422,{'error':'Complete name, company, email, quantity and requirements.'})
    ref='RFQ-'+secrets.token_hex(4).upper(); c=conn()
    try:
      c.execute('begin'); c.execute('insert into inquiries(reference,name,email,company,phone,product,message,consent,ip_hash) values(?,?,?,?,?,?,?,?,?)',(ref,fields['name'][:160],fields['email'][:200],fields['company'][:200],fields.get('phone','')[:100],(fields.get('product','')+' × '+fields['quantity'])[:1000],fields['message'][:5000],1,hashlib.sha256(self.client_address[0].encode()).hexdigest()[:16])); iid=c.execute('select last_insert_rowid()').fetchone()[0]; c.execute('insert into outbox(inquiry_id) values(?)',(iid,))
      if attachment:
       if not attachment[0].lower().endswith(('.pdf','.jpg','.jpeg','.png','.doc','.docx')): return api(self,422,{'error':'Attachment must be a PDF, image or Word document.'})
       safe=''.join(ch for ch in attachment[0] if ch.isalnum() or ch in '._-')[:120] or 'attachment'; stored=uuid.uuid4().hex+'-'+safe; (UPLOADS/stored).write_bytes(attachment[1]); c.execute('insert into rfq_attachments(inquiry_id,filename,stored_name,content_type,size) values(?,?,?,?,?)',(iid,safe,stored,attachment[2],len(attachment[1])))
      c.commit()
    except Exception: c.rollback(); return api(self,500,{'error':'We could not save your quote request. Please retry.'})
    finally: c.close()
    return api(self,201,{'reference':ref,'message':'Quote request received. An engineer will respond within one business day.'})
  def product_image_upload(self):
    if not self.guard(True): return
    content_type=self.headers.get('Content-Type',''); length=int(self.headers.get('Content-Length','0') or 0)
    if 'multipart/form-data' not in content_type: return api(self,415,{'error':'Use multipart form data.'})
    if length>4*1024*1024+10000: return api(self,413,{'error':'Product image must be smaller than 4 MB.'})
    boundary=content_type.split('boundary=',1)[-1].encode(); raw=self.rfile.read(length); upload=None
    for part in raw.split(b'--'+boundary):
     if b'filename="' not in part or b'\r\n\r\n' not in part: continue
     head,value=part.split(b'\r\n\r\n',1); filename=head.decode('utf-8','ignore').split('filename="',1)[1].split('"',1)[0]; upload=(filename,value.rstrip(b'\r\n-')); break
    if not upload or not upload[1]: return api(self,422,{'error':'Choose an image to upload.'})
    extension=Path(upload[0]).suffix.lower()
    if not valid_product_image(upload[0],upload[1]): return api(self,422,{'error':'Upload a valid JPG, PNG or WebP image.'})
    stored=uuid.uuid4().hex+extension; (MEDIA/stored).write_bytes(upload[1]); return api(self,201,{'url':'/media/products/'+stored})
  def do_POST(self):
    p=urlparse(self.path).path
    if p=='/api/rfq': return self.rfq_multipart()
    if p=='/api/admin/products/image': return self.product_image_upload()
    data=self.body()
    if p=='/api/orders':
      items=data.get('items',[]); customer=data.get('customer',{})
      if not items or not customer.get('name') or '@' not in str(customer.get('email','')) or any(not str(customer.get(k,'')).strip() for k in ('phone','country','address_line1','city','postal_code')): return api(self,422,{'error':'Complete contact and shipping information.'})
      try: priced_items,total=price_order(items)
      except (ValueError,TypeError): return api(self,422,{'error':'A product is unavailable or its quantity is invalid.'})
      ref='ORD-'+secrets.token_hex(4).upper(); c=conn()
      try:
       c.execute('insert into orders(reference,email,name,company,phone,country,address_line1,address_line2,city,region,postal_code,notes,items_json,total_cents) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(ref,str(customer['email'])[:200],str(customer['name'])[:160],str(customer.get('company',''))[:200],str(customer['phone'])[:80],str(customer['country'])[:100],str(customer['address_line1'])[:250],str(customer.get('address_line2',''))[:250],str(customer['city'])[:120],str(customer.get('region',''))[:120],str(customer['postal_code'])[:40],str(customer.get('notes',''))[:1000],json.dumps(priced_items),total)); c.commit()
      except Exception: c.rollback(); return api(self,500,{'error':'We could not create this order. Please try again.'})
      finally: c.close()
      return api(self,201,{'reference':ref,'status':'pending_payment','message':'Order request received. Payment is not configured yet; our team will confirm next steps.'})
    if p=='/api/login':
      c=conn(); u=c.execute('select * from users where email=?',(str(data.get('email','')).lower(),)).fetchone(); c.close()
      if not u or not verify(str(data.get('password','')),u['password']): return api(self,401,{'error':'Invalid email or password'})
      payload=base64.urlsafe_b64encode(json.dumps({'email':u['email'],'role':u['role'],'csrf':secrets.token_urlsafe(24),'exp':int(time.time())+28800}).encode()).decode().rstrip('='); return api(self,200,{'ok':True}, {'Set-Cookie':f'session={payload}.{sign(payload)}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'})
    if p=='/api/logout': return api(self,200,{'ok':True},{'Set-Cookie':'session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'})
    if p=='/api/inquiries':
      required=['name','email','company','message']; errors={k:'Required' for k in required if not str(data.get(k,'')).strip()}
      if '@' not in str(data.get('email','')): errors['email']='Enter a valid email'
      if not data.get('consent'): errors['consent']='Consent is required'
      if errors:return api(self,422,{'error':'Please correct the highlighted fields','fields':errors})
      ip=self.client_address[0]; ref='RFQ-'+secrets.token_hex(4).upper(); c=conn()
      try:
       c.execute('begin'); c.execute('insert into inquiries(reference,name,email,company,phone,product,message,consent,ip_hash) values(?,?,?,?,?,?,?,?,?)',(ref,*[str(data.get(k,''))[:1000] for k in ('name','email','company','phone','product','message')],1,hashlib.sha256(ip.encode()).hexdigest()[:16])); iid=c.execute('select last_insert_rowid()').fetchone()[0]; c.execute('insert into outbox(inquiry_id) values(?)',(iid,)); c.commit()
      except Exception: c.rollback(); return api(self,500,{'error':'We could not save your request. Please try again.'})
      finally:c.close()
      return api(self,201,{'reference':ref,'message':'Request received. An engineer will review it.'})
    if p=='/api/admin/inquiries/status':
      if not self.guard(True): return
      allowed={'queued','reviewing','quoted','closed'}; status=str(data.get('status',''))
      if status not in allowed: return api(self,422,{'error':'Invalid inquiry status.'})
      c=conn(); result=c.execute('update inquiries set state=? where id=?',(status,int(data.get('id',0)))); c.commit(); c.close()
      if not result.rowcount: return api(self,404,{'error':'Inquiry not found.'})
      return api(self,200,{'ok':True,'status':status})
    if p=='/api/admin/orders/status':
      if not self.guard(True): return
      allowed={'pending_payment','confirmed','processing','shipped','cancelled'}; status=str(data.get('status',''))
      if status not in allowed: return api(self,422,{'error':'Invalid order status.'})
      c=conn(); result=c.execute('update orders set status=? where id=?',(status,int(data.get('id',0)))); c.commit(); c.close()
      if not result.rowcount: return api(self,404,{'error':'Order not found.'})
      return api(self,200,{'ok':True,'status':status})
    if p=='/api/admin/products':
      if not self.guard(True): return
      needed=['slug','model','title','description','category','sku'];
      if any(not str(data.get(k,'')).strip() for k in needed): return api(self,422,{'error':'Complete all required product fields.'})
      try: price_cents=round(float(data.get('price',0))*100); inventory=int(data.get('inventory',0))
      except (ValueError,TypeError): return api(self,422,{'error':'Price and inventory must be valid numbers.'})
      if price_cents<0 or inventory<0: return api(self,422,{'error':'Price and inventory cannot be negative.'})
      image_url=str(data.get('image_url','')).strip(); parsed=urlparse(image_url) if image_url else None
      if image_url and not image_url.startswith('/media/products/') and (parsed.scheme!='https' or not parsed.netloc): return api(self,422,{'error':'Product image must be an uploaded image or valid HTTPS URL.'})
      values=(str(data['slug']).strip().lower()[:120],str(data['model']).strip()[:120],str(data['title']).strip()[:200],str(data['description']).strip()[:2000],str(data['category']).strip()[:100],str(data.get('range_text','Configuration dependent')).strip()[:200],str(data.get('interface','On request')).strip()[:200],str(data.get('rating','On request')).strip()[:100],int(bool(data.get('published'))),price_cents,inventory,str(data['sku']).strip()[:120],image_url)
      c=conn()
      try:
       product_id=int(data.get('id',0) or 0)
       if product_id: result=c.execute('update products set slug=?,model=?,title=?,description=?,category=?,range_text=?,interface=?,rating=?,published=?,price_cents=?,inventory=?,sku=?,image_url=?,updated_at=CURRENT_TIMESTAMP where id=?',values+(product_id,))
       else: result=c.execute('insert into products(slug,model,title,description,category,range_text,interface,rating,published,price_cents,inventory,sku,image_url) values(?,?,?,?,?,?,?,?,?,?,?,?,?)',values)
       c.commit()
      except sqlite3.IntegrityError: c.rollback(); return api(self,409,{'error':'Slug or SKU already exists.'})
      finally: c.close()
      if product_id and not result.rowcount: return api(self,404,{'error':'Product not found.'})
      return api(self,200 if product_id else 201,{'ok':True,'id':product_id or result.lastrowid})
    if p=='/api/admin/delivery':
      if not self.guard(True): return
      endpoint=str(data.get('endpoint','')).strip(); u=urlparse(endpoint)
      if endpoint and (u.scheme!='https' or not u.netloc or u.username or u.query or u.fragment): return api(self,422,{'error':'Use an HTTPS endpoint without credentials, query, or fragment.'})
      c=conn(); c.execute("insert into settings(key,value) values('delivery_endpoint',?) on conflict(key) do update set value=excluded.value,updated_at=CURRENT_TIMESTAMP",(endpoint,)); c.commit(); c.close(); return api(self,200,{'ok':True,'configured':bool(endpoint),'worker':'off'})
    return api(self,404,{'error':'Not found'})
if __name__=='__main__':
 print(f'Industrial site running at http://localhost:{env("PORT","8000")}'); ThreadingHTTPServer(('0.0.0.0',int(env('PORT','8000'))),App).serve_forever()
