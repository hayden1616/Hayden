window.CatalogData={
  source:"mock-api",
  images:[
    "https://images.unsplash.com/photo-1581092919535-7146ff1a7a3b?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1581094794329-c8112a89af12?auto=format&fit=crop&w=900&q=80"
  ],
  async list(){
    const response=await fetch("/api/products");
    if(!response.ok) throw new Error("Catalogue is temporarily unavailable.");
    const data=await response.json();
    return data.products.map((product,index)=>({...product,
      price_label:new Intl.NumberFormat("en-US",{style:"currency",currency:product.currency}).format(product.price_cents/100),
      image:product.image_url||this.images[index%this.images.length],
      intro:"Built for repeatable field performance, with configuration support for installation, signal and documentation requirements."
    }));
  },
  async one(slug){return (await this.list()).find(product=>product.slug===slug)||null}
};
