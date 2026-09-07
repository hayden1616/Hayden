# Admin Backend Contract

Use this contract when an industrial export website needs authenticated inquiry monitoring, database administration, or controlled delivery to a private downstream system. The public site, operator console, and private receiver share one brand system but remain separate trust zones.

## Trust boundary

- The public browser submits only to a same-origin inquiry endpoint such as `POST /api/leads`. It must not contain a downstream URL, destination identity, shared secret, direct-delivery function, manual retry action, or code that calls the private receiver.
- The website server validates and stores the inquiry locally. It owns the only process allowed to deliver queued records downstream.
- Refer to the destination with neutral operational language such as `private destination`, `delivery connector`, or `downstream system`. Do not expose its product name in public copy, client bundles, analytics payloads, response bodies, or routine logs.
- Protect all operator endpoints with authenticated, role-checked sessions, CSRF defenses for state changes, origin checks, rate limits, and redacted responses. A public site configuration response must contain only display-safe values.
- Default the connector to address-only delivery: collect an HTTPS endpoint, keep it free of embedded credentials, and send an idempotency key. Require the CRM operator to enforce private-network, reverse-proxy, or equivalent access controls. Only add key IDs and signing secrets when the user explicitly chooses signed delivery.

## MySQL persistence

Use MySQL as the system of record when reliable asynchronous delivery is required. Create migrations for these responsibilities, adapting names to the host application:

| Responsibility | Required data |
| --- | --- |
| Inquiry vault | normalized inquiry, source context, consent metadata, created time |
| Transactional outbox | inquiry reference, payload snapshot, state, attempt count, next attempt, lock owner and expiry |
| Attempt ledger | outbox reference, result class, HTTP status, safe error summary, duration, timestamp |
| Connector settings | endpoint, optional key identifier and encrypted secret for signed mode, timeout, enabled state, revision metadata |
| Worker control | enabled state, poll interval, batch size, maximum attempts, updated-by audit metadata |
| Schema migrations | applied migration version and timestamp |

Insert the inquiry and its outbox record in one database transaction. A failed commit must create neither record. Use database constraints for idempotency and state validity. Keep raw credentials and sensitive request content out of migration files, seed data, query strings, and logs.

The `MySQL storage` workspace may test connectivity, show migration health, and apply bundled forward migrations. It must never accept arbitrary SQL. Mask passwords after save, require deliberate confirmation before changing a configured connection, and return actionable failure states without echoing credentials.

## Encrypted runtime configuration

Do not use environment variables, public JSON, frontend storage, source code, or command arguments for the private destination endpoint, optional connector secret, database password, or persistent worker switch. Store database credentials and any optional signed-mode secret in an authenticated-encryption envelope such as AES-256-GCM and keep its separate key file readable only by the service account (`0600`). The endpoint itself remains an authenticated admin setting and must be validated as HTTPS without embedded credentials, query strings, or fragments.

In address-only mode, do not collect or invent a secret. If signed mode is explicitly requested, allow secret input only through an authenticated owner-only control or an interactive standard-input setup command. Never return a saved secret to the browser; return `configured`, a masked identifier, and update metadata instead. Keep non-sensitive display configuration separate from the encrypted runtime store. Environment variables may still bootstrap ordinary process behavior where the host requires it, but they must not become the integration credential store.

## Switchable delivery worker

- Persist the worker switch in the database and default it to off. Starting the web process must not silently enable delivery.
- When off, new inquiries continue to enter the vault and outbox while no unattended outbound request is made. If the product includes a separate owner-only `Run one batch` action, present it as an explicit delivery command and disable it until the connector endpoint is ready.
- Claim work atomically with row locking such as `FOR UPDATE SKIP LOCKED`. Record a lock owner and lease expiry, and recover abandoned leases.
- Use bounded batches, a configurable poll interval, exponential backoff with jitter, and a maximum attempt count. Terminal failures remain inspectable; retries are explicit operator actions.
- Send an idempotency key per inquiry. In signed mode, sign the exact request bytes with HMAC-SHA256 and include a key identifier, timestamp, and nonce; the receiver must verify signature freshness and replay protection before persistence.
- If signed mode is enabled, support key rotation with current and previous verification keys, then provide a deliberate revocation path. Apply timeouts and classify retryable transport/server failures separately from permanent validation failures.
- A worker switch changes automatic future processing only. Do not drain an existing queue during implementation, QA, restart, migration, or manual-batch testing unless the user explicitly authorizes real delivery.

## Operator workspaces

Use one routed `Monitor` workspace for related demand evidence. Show exactly one
visible `Monitor` item in primary navigation. Trends, page performance and
acquisition, product intent, and live sessions belong to that workspace as
ordered ruled sections, without a second-level navigation list. Keep
backward-compatible deep links by mapping legacy section hashes to `#monitor`
and scrolling to the matching section after route activation.

Keep operational records and controls as distinct routed workspaces rather than
one dashboard wall:

1. `Inquiry vault`: searchable, filterable inquiry rows, source and consent context, age, state, and a detail view. It has no direct `send to downstream system` control.
2. `Lead delivery`: connector readiness, redacted configuration, worker switch, queue counts, attempt history, retry controls, and clear off/on consequences.
3. `MySQL storage`: connection health, schema version, migration status, masked configuration, test and controlled migration actions.

Use the shared industrial typography, but increase density relative to marketing. The default control-room visual variant uses a graphite shell, mineral background, paper surfaces, slate-blue navigation/data emphasis, and copper action emphasis; green is semantic-only for healthy, verified, or delivered states. Prefer a compact rail, ruled tables, mono identifiers, square controls, and clear workspace headers. Avoid generic KPI cards, decorative charts, gradients, glass effects, large radii, and repeated panel containers. Status labels must combine text and shape or icon, not color alone.

## Required states

Every workspace needs loading, empty, stale/error with recovery, success, disabled, and permission-denied behavior. Additionally cover: storage unconfigured, schema behind, connector unconfigured, connector disabled, worker off with queued records, delivering, retry scheduled, terminal failure, delivered, address-only mode, and optional signed-mode secret saved but never redisplayed.

On mobile, keep controls at least 44px, move workspace navigation into a sticky utility row, stack forms and evidence, and isolate horizontal scrolling inside wide tables. Tablet uses two-column evidence where useful; desktop uses a 12-column grid without equal-weight card walls.

## QA gate

Before delivery:

- Prove unauthenticated operator requests return `401` or `403`, public configuration is redacted, and no client asset contains the private destination or secret.
- Prove inquiry and outbox writes are atomic, worker-off sends nothing, address-only worker-on posts the expected payload and idempotency key, duplicate delivery is idempotent, optional signed mode verifies replay and stale signatures, retry limits hold, and abandoned locks recover.
- Prove encrypted files exist with restrictive permissions and saved secrets do not appear in command history, API responses, logs, or screenshots.
- Run functional QA for login, workspace routing, connector save, storage test, migration, worker switch, filters, retry, logout, and all recovery paths.
- Run visual QA at 1440px, 768px, and 390px for login and every workspace. Check contrast, focus, clipping, route visibility, table-local overflow, empty/error/loading states, and console errors.

Leave real delivery disabled after QA unless the user explicitly approves enabling it.
