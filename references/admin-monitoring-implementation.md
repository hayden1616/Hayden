# Admin monitoring implementation baseline

Read this reference after `admin-control-room-components.md` and
`admin-backend-contract.md` whenever a Lweb brief includes monitoring,
inquiry operations, a private delivery connector, MySQL storage, or catalogue
maintenance. It is the implementation baseline for generating the operator UI
and the server behavior together.

## Workspace and route map

Use independent, directly loadable hash routes for operator workspaces. Keep
the primary rail short and task-oriented:

| Route | Operator question | Required surface |
| --- | --- | --- |
| `#overview` | What changed in the selected range? | metric strip, freshness, collection health |
| `#monitor` | Where is demand and product intent moving? | trend, pages/sources, product intent, funnel quality, live activity |
| `#actions` | What should be reviewed next? | prioritized action queue with deep links |
| `#funnel` | Where do inquiries drop? | ruled stage sequence and collection health |
| `#leads` | What inquiries are retained? | searchable/filterable vault and detail view |
| `#delivery` | Is private delivery ready and progressing? | connector, worker, queue, attempts, retry controls |
| `#storage` | Is persistence healthy? | masked connection, test, migration status |
| `#catalog-manager` | Are public product records current? | searchable catalogue, edit, media, publish state |

`Monitor` is the only primary navigation item for trend, page/source,
product-intent, funnel-quality, and live-session evidence. Preserve old deep
links such as `#trend`, `#content`, `#products`, and `#live` by resolving them
to `#monitor` and scrolling to the matching section after activation. A
refresh at any route must restore the same workspace and active navigation.

## Server and browser responsibilities

Keep the browser as a same-origin operator client. The browser may request
aggregates, rows, redacted configuration, and explicit actions, but it must
never own persistence, delivery credentials, worker leases, or retry policy.

Required server contracts:

1. Public capture accepts a normalized inquiry and writes the inquiry and its
   outbox job in one transaction. Return a safe reference and status only.
2. Analytics accepts a small allow-list of anonymous event shapes, rejects
   identifying or unknown shapes, and returns aggregates for the selected
   range. Live activity is anonymous and freshness-labeled.
3. Authenticated admin reads expose only the selected range, redacted rows,
   masked settings, safe error summaries, and audit metadata. Every mutation
   checks session, role, origin/CSRF, validation, and rate limits.
4. Delivery configuration accepts an HTTPS address without embedded
   credentials, query strings, or fragments. Address-only mode is the
   default; there is no security-code field unless signed delivery is an
   explicit product decision.
5. The worker is server-owned and database-backed. `Run one batch` and `Retry`
   are explicit operator commands; a worker switch changes future automatic
   processing only and never drains a queue during startup or QA.
6. Storage actions are limited to connection test and bundled forward
   migrations. Never expose an arbitrary SQL console.
7. Catalogue actions validate product fields server-side, persist a revision,
   scan allowed image assets, and publish only an explicit status change.
   Cover and gallery uploads return managed paths, never executable or
   unvalidated filenames.

## State machines that must be implemented

Use explicit states in the API and render their text labels in the UI. Do not
infer state from a missing field or a color alone.

### Inquiry and delivery

```text
captured -> queued -> processing -> delivered
                         |             |
                         v             v
                   retry_scheduled -> delivered
                         |
                         v
                       failed
```

- `processing` requires a lease owner and expiry; abandoned leases are
  recoverable.
- Retryable transport/server failures schedule bounded exponential backoff
  with jitter. Permanent validation failures become terminal `failed`.
- Every attempt records a safe result class, HTTP status when available,
  duration, timestamp, and redacted error summary.
- Duplicate delivery uses an idempotency key derived from the inquiry
  reference. A repeated key must not create a second downstream record.
- Worker disabled, connector disabled, and connector unconfigured all leave
  new records inspectable in the vault without an outbound request.

### Connector and storage readiness

```text
unconfigured -> configured/disabled -> configured/ready -> enabled
      ^                |                    |               |
      +---- recovery --+------ test --------+---- disable --+
```

MySQL readiness is independently represented as `unconfigured`, `offline`,
`online`, or `schema_behind`. A failed test or migration shows an actionable
recovery message and never echoes a password.

### Catalogue publishing

```text
draft -> in_review -> approved -> published
  ^         |            |          |
  +---------+------------+----------+--> archived
```

Saving a record creates a revision and refreshes the public catalogue from
the server-owned source. Media changes are previewable before save and must
show upload progress, validation errors, and a recoverable retry path.

## UI state contract

Every workspace and every data module implements the same finite UI states:

- `loading`: skeleton or reserved geometry; controls that would duplicate the
  request are disabled.
- `empty`: explain why there are no rows and offer the next valid action.
- `ready`: show freshness, counts, and the primary evidence.
- `stale`: keep the last safe data, disclose its age, and offer refresh.
- `error`: show a concise safe error, preserve the route and inputs, and offer
  retry or configuration recovery.
- `success`: confirm the exact mutation or refresh in a status region/toast.
- `disabled/unconfigured`: explain which setting is missing and why the
  action is unavailable.
- `permission-denied`: do not render mutation controls; provide a safe return
  path.

For forms, keep labels visible, validate inline, preserve user input on
failure, prevent duplicate submits while pending, and restore enabled state
after success or error. For tables, keep row height readable, use text plus
shape/icon for status, and isolate horizontal scrolling to the table wrapper.

## Interaction requirements

The generated surface must support all of these without placeholder behavior:

- date range selection, refresh, export, and sign out;
- active route highlighting, direct deep links, browser back/forward, and
  legacy Monitor aliases;
- Monitor evidence sections with accessible chart summaries;
- inquiry keyword search and status filter with debounced, server-backed
  results; no direct downstream-send control in the vault;
- Action center links that land on the relevant workspace and section;
- connector validation/save, worker enable/disable, explicit one-batch run,
  queue inspection, and per-record retry;
- storage test, masked settings, controlled migration, and migration result;
- catalogue keyword/status filtering, edit/cancel/save, cover and gallery
  upload, preview, publish/unpublish, and revision feedback.

## Release QA gate

Run functional tests against the server contracts and a browser smoke pass
against every route. A release is blocked by any of the following:

- an unauthenticated admin response that is not `401`/`403`;
- a client asset, public config, log, screenshot, or API response containing a
  private destination, password, signing secret, or raw sensitive inquiry;
- worker-off or connector-disabled mode causing an outbound request;
- non-atomic inquiry/outbox writes, duplicate delivery, unrecoverable leases,
  or retry-limit violations;
- a route that cannot be refreshed directly, a broken active-nav state, a
  search/filter that does not change results, or a mutation without success
  and recovery feedback;
- clipped or wrapped button text, contrast below WCAG AA, page-level
  horizontal overflow, broken images, console errors, or a hidden routed
  workspace rendered by responsive CSS.

Score each route on button alignment/readability (30), color/contrast (25),
layout and information density (20), responsive behavior (15), and states/
interaction feedback (10). Require at least 90/100 per route and zero
critical blockers. Inspect computed styles and screenshots at 1440px, 768px,
and 390px; do not accept a page that only passes source-level token checks.

Leave real downstream delivery disabled after QA unless the operator
explicitly authorizes enabling it.
