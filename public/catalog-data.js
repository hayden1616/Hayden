window.CatalogData={
  source:'mock',
  async list(){const r=await fetch('/api/products');const j=await r.json();return j.products.map((p,i)=>({...p,price_cents:[18900,23900,31500,27900,34900,21900][i]||19900,price_label:'USD '+(([189,239,315,279,349,219][i]||199).toFixed(2)),sku:p.model+'-STD',image:['https://images.unsplash.com/photo-1581092919535-7146ff1a7a3b?auto=format&fit=crop&w=900&q=80','https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=80','https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=80'][i%3],intro:'Built for repeatable field performance, with configuration support for installation, signal and documentation requirements.'}))},
  async one(slug){return (await this.list()).find(p=>p.slug===slug)||null}
};
