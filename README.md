# Industrial Export Website

A deployable, same-origin B2B catalogue and RFQ application. Public inquiries and operational records are stored in SQLite; the private delivery connector is disabled by default.

## Run locally

Requires Python 3.10+. Copy `.env.example` to `.env`, change `SESSION_SECRET` and `ADMIN_PASSWORD`, then run:

```bash
python3 server.py
```

Open `http://localhost:8000`. The first start creates `data/industrial.db`, schema, product catalogue, and the administrator from environment variables. Sign in at `/admin`.

## Environment

`DATABASE_PATH`, `PORT`, `SESSION_SECRET`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `SITE_ORIGIN` are server-only. Do not commit `.env`. `DELIVERY_ENDPOINT` is optional; use the authenticated Admin Delivery page to configure it. Only HTTPS endpoints without credentials, query strings, or fragments are accepted. Delivery is off by default.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile server.py
```

## Deploy

Set the environment variables on the host, use a managed persistent volume for `data/`, and run behind a TLS reverse proxy:

```bash
PORT=8000 python3 server.py
```

For a production process manager, point it at `server.py`; terminate TLS at the proxy and set `SITE_ORIGIN` to the public HTTPS origin. Back up the SQLite volume regularly. The readiness probe is `GET /api/health`.

## Data and security

The server validates RFQs, applies per-IP limits, writes inquiry/outbox records in one SQLite transaction, uses signed HttpOnly SameSite cookies, checks origin and CSRF on mutations, and protects all admin APIs with an administrator session. No private connector address is included in public responses or assets.



## Storefront phase one

The public catalogue now supports maintained mock product data through `public/catalog-data.js`, product details, browser-backed cart, an order-request checkout (no payment capture), and an attachment-enabled RFQ form. The front-end data adapter is intentionally isolated so it can later be replaced by a commerce API such as Medusa without changing page components. Orders and RFQ metadata are stored in SQLite; attachments are held in `data/uploads/` and are not publicly served.
