---
name: lweb
description: "Turn a one-line industrial product brief into a complete industrial-premium B2B export web product with coordinated frontend, backend, admin operations, data boundaries, responsive UX, and QA."
---

# Lweb

Lweb is a product-design-director workflow for Chinese industrial manufacturers serving international buyers. Treat every website request as one coordinated full-stack product: generate the public frontend and its server-side foundation in the same project and delivery pass. Add authenticated product and admin surfaces when the product needs operators, storage, integrations, or ongoing content work. Honor an explicit request for a static marketing-only artifact, but do not silently turn a product brief into a frontend-only mockup. The method is brand-neutral and must not reveal private design inputs, external identities, URLs, trademarks, copy, or proprietary claims.

## Single-sentence delivery contract

One natural-language brief is sufficient: unless the user explicitly narrows the scope, execute the complete Lweb delivery end to end, including product definition, information architecture, design tokens, public marketing frontend, independent listing and detail routes, authenticated product surfaces when the workflow implies them, the server/API and persistence those surfaces require, authenticated admin operations, loading/empty/error/success/disabled/permission states, responsive desktop/tablet/mobile behavior, restrained motion, source sanitization, and functional plus visual QA. Do not pause for page-count, framework, layout, copy, or routine product decisions; choose reversible industrial-premium defaults and document assumptions. Ask only when security, permissions, billing, or persisted data semantics would materially change.

## Product framing

Before implementation, define the primary buyer, buying trigger, proof required for trust, and the single activation event. Prefer domain nouns such as instrument, application, medium, range, protocol, drawing, RFQ, certification, and engineering review over generic AI or SaaS language.

Document the information architecture, critical conversion path, design tokens, backend boundary, data model, and permission model before writing page code. Build frontend and backend contracts together: the UI should have real server routes, validation, persistence, and recovery states rather than placeholder calls. Keep operational surfaces on separate routes and preserve different densities:

- Marketing is spacious, image-led, and editorial.
- Authenticated product surfaces are denser and optimized for repeated work.
- Admin surfaces are compact, permission-aware, and audit-oriented.

## Full-stack delivery default

For a normal Lweb build, produce one runnable repository containing the public frontend and the backend it depends on. Plan and implement these layers as a single product:

- Public pages, shared shell, forms, search, filters, detail routes, and responsive states.
- Server runtime, same-origin API routes, request validation, rate limits, error contracts, health/readiness checks, and structured logs.
- Data model and forward migrations for content, inquiries, settings, audit events, and any asynchronous work; use real persistence where the brief implies retained state.
- Authentication, authorization, session/logout behavior, CSRF/origin controls, and permission-denied states for operator surfaces.
- Admin monitoring and management workspaces when there is data to review or configure. Read [references/admin-backend-contract.md](references/admin-backend-contract.md) before implementing inquiry storage, MySQL controls, private delivery, or a switchable worker.
- Server-owned integrations and background jobs. Private endpoints, credentials, signing keys, and worker switches never belong in browser code or public configuration.
- Functional tests for API and persistence invariants alongside visual tests for the frontend. A page is not complete if its API, empty/error/loading states, or direct route loading are missing.

Do not build a fake backend solely to make a screen look complete. If a dependency cannot be connected safely, implement an explicit disabled/unconfigured state with a recovery path and document the boundary.

Make routine product decisions autonomously. Ask only when a decision materially changes security, permissions, billing, or persisted data semantics.

## Industrial export homepage contract

For a full industrial marketing homepage, preserve this section order and its changes in density:

1. Sticky dark header with a wordmark, eight compact navigation items, language control, and one primary RFQ action.
2. Full-bleed dark industrial hero with an eyebrow, literal H1, technical explanation, primary and secondary actions, and four proof metrics anchored near the bottom.
3. Four-item service-assurance strip.
4. Centered compatibility or customer-proof section with one restrained protocol, certification, or logo row.
5. Three-column product or engineering-scope section led by inspection-grade imagery.
6. Split selection guide with editorial copy on the left and a ruled comparison table on the right.
7. Six industry or application entry points in a ruled grid.
8. Dark three-item case-study section.
9. Four-step engineering, quotation, or delivery workflow.
10. Two-column FAQ section with native disclosure rows.
11. Oxidized burgundy project CTA band.
12. Multi-column dark footer with a primary action, links, contact details, and legal line.

Keep the order recognizable across implementations. Adapt labels and content to the client's actual products and applications. Preserve the desktop rhythm at roughly 1440px, reflow to an intentional tablet composition at 768px, and use a linear mobile reading order at 390px. Only technical tables may scroll horizontally; the page itself must never do so.

## Multi-page extension

When the brief includes secondary pages, read [references/page-routing-contract.md](references/page-routing-contract.md) before writing page code. Treat the homepage and secondary routes as different compositions under one shared brand system:

- Build a route map before adding page sections. Use real paths for primary navigation and reserve hash anchors for same-page proof or conversion sections.
- Reuse the header, footer, CTA, form, and status primitives, but vary hero scale, content density, and reading measure by template.
- Use listing pages for scanning, application pages for operating conditions, detail pages for one decision, and article pages for technical education. Do not clone the homepage onto every route.
- Support direct deep-link loading, refresh, forward/back history, active navigation by pathname, and menu close-after-navigation. If using a lightweight frontend, a small history-based route registry is sufficient; use the host framework router when one already exists.
- Give every non-home route a page-specific CTA and a visible route-back path such as breadcrumbs or a listing link.
- For product-heavy routes, read [references/product-catalog-contract.md](references/product-catalog-contract.md) and implement category filters, keyword search, result counts, and a ruled multi-column index before falling back to a single-column list.
- For product detail routes, read [references/product-detail-contract.md](references/product-detail-contract.md) and implement the gallery, procurement decision panel, ruled specifications, application-fit notes, document requests, related products, and recoverable interaction states.

## Industrial Premium language

The aesthetic is engineered restraint: inspection-grade imagery, hard geometry, strong typography, editorial grids, whitespace, alignment, and explicit information hierarchy. It must not read as an AI dashboard or generic SaaS template.

- Palette: near-black ink, cold steel or ash surfaces, white paper, safety orange for primary action emphasis, and an oxidized burgundy brand color (`#6B2C3B`) for project CTAs, active filters, and secondary links. A muted green is reserved for semantic success and verification only.
- Typography: use a distinctive modern grotesk for display, a readable sans for body copy, and tabular or mono numerals for technical data.
- Shape: use mostly square geometry and one restrained radius token between 0 and 4px. Use rules, dividers, and whitespace instead of nested cards.
- Composition: vary section structures. Do not repeat identical centered-heading plus card-grid patterns throughout the page.
- Imagery: use real industrial scenes and products. Give every meaningful image an intentional crop, stable aspect ratio, useful alt text, and lazy loading outside the first viewport.
- Prohibited language: no purple or blue AI gradients, glassmorphism, decorative blobs, glowing orbs, excessive rounding, or decorative animation.

## Motion contract

Motion is minimal, causal, and normally 150-300ms. Animate only opacity and transform, and always honor `prefers-reduced-motion`.

Use motion for mobile navigation, anchor transitions, restrained image-hover emphasis, FAQ disclosure, toast or modal feedback, and form loading or success. Do not use scroll-jacking, autoplay carousels, decorative parallax, continuous ambient motion, glow effects, or animation to compensate for weak hierarchy.

## Design system contract

Create tokens before page-specific CSS: color, type scale, spacing on a 4/8px base, borders, radius, shadow, z-index, breakpoints, and motion. Define shared primitives for wordmark, top bar, section heading, status marker, data row, button, input, select, toast, modal, skeleton, empty state, and error state. Use one icon family with consistent stroke weight; icon-only controls require accessible labels and tooltips.

Buttons require clear hierarchy, visible focus rings, 44px minimum touch targets, and loading and disabled feedback. Forms require visible labels, semantic input types, inline validation, and recovery text. Status must never rely on color alone.

## Admin monitoring contract

When building an authenticated monitoring or operations surface, design for a site operator reviewing demand and product intent rather than for a generic SaaS administrator:

Read [references/admin-control-room-components.md](references/admin-control-room-components.md) before implementing the visual component layer. It defines the rail/header/filter/metric/evidence grammar, dark control-room tokens, responsive breakpoints, and required state/QA checks. Keep those rules as one coherent layer rather than appending unrelated theme overrides.

Before implementing inquiry storage, outbound delivery, database controls, or a background synchronizer, read [references/admin-backend-contract.md](references/admin-backend-contract.md). Keep public capture, private storage, and downstream delivery as separate trust zones; the browser must never know the private destination or its credentials.

For the concrete monitoring route map, state machines, UI states, interaction
requirements, and release gate, also read
[references/admin-monitoring-implementation.md](references/admin-monitoring-implementation.md).

- Use a compact left rail, a restrained utility header, and a clear workspace title with the selected date range and data freshness visible.
- Consolidate related monitoring evidence into a single `Monitor` workspace when the operator is reviewing the same demand signal. Show exactly one visible `Monitor` item in primary navigation; keep Trends, Pages, Product intent, and Live sessions as ordered sections in that page, without a second-level navigation list. Preserve backward-compatible deep links by aliasing legacy section hashes to the Monitor route.
- Establish a 12-column desktop grid: a small set of metric cells, then a trend view, page/source evidence, product interest, funnel quality, and live activity. Do not create a wall of equal-weight KPI cards.
- Prefer ruled tables, index numbers, mono numerals, and deliberate whitespace over nested cards, floating panels, gradient backgrounds, or decorative charts.
- Keep admin density higher than marketing density, but preserve stable 44px controls, visible focus, semantic labels, and readable row heights.
- Use the approved control-room variant for admin active navigation, selected filters, and primary actions; reserve green for healthy, verified, or delivered states.
- When the admin surface needs a distinct visual refresh, use the approved
  control-room variant: graphite shell (`#172831`), mineral background
  (`#e8edef`), paper surface (`#fbfcfb`), slate-blue navigation and data
  emphasis (`#315969`), and copper actions (`#c76f3c`). Keep green semantic
  only for healthy, verified, or delivered states; do not use it to decorate
  ordinary KPI categories. This variant must be applied consistently to the
  header, rail, buttons, fields, tables, status markers, and chart legend.
- Default CRM delivery to an endpoint-only mode: collect the HTTPS address and worker controls, send an idempotency key, and rely on a private network or reverse-proxy access policy. Add key IDs or signing secrets only when the user explicitly requests signed delivery.
- Login is part of the product surface: it should communicate a secure engineering control room with dark ink, steel, paper, and process language. No AI buzzwords, orbit graphics, glass panels, or purple gradients.
- Every data module needs loading, empty, stale/error, and recovery states. Live-session views must be anonymous and disclose freshness without exposing personal form data.
- Responsive behavior: desktop keeps the rail and multi-column evidence; tablet collapses to a two-column evidence layout; mobile uses a sticky utility row and single-column sections with horizontal scroll isolated to wide tables.
- Runtime language must follow the approved product language end to end. If the public site is English, admin markup, injected configuration labels, status messages, empty states, confirmations, formatters, route descriptions, accessibility labels, and test fixtures must also be English; never leave a translated fallback in a runtime branch.
- When legacy admin styles remain loaded for compatibility, append a final Lweb override layer with explicit specificity for active navigation, semantic colors, radii, shadows, gradients, blur, and routed workspace visibility. Do not rely on source-order assumptions alone.
- Routed admin workspaces must respect the native `hidden` contract. If responsive CSS changes `display`, add an explicit route visibility class or inline state so only the selected workspace renders; verify overview and secondary routes independently at mobile width.
- Visual QA should inspect the computed result, not only source tokens: check for legacy neon accents, purple/blue AI treatment, backdrop blur, decorative gradients, duplicate headings, clipped mobile headings, and page-level horizontal overflow.

## Sanitization contract

Treat private design inputs as implementation context only. The only concrete brand name permitted in examples, seeded content, metadata, or UI copy is `GoodJob`, and only when the user explicitly asks for that brand. Otherwise use neutral terms such as `industrial manufacturer`, `operator`, `private destination`, `industrial-premium`, `homepage-contract`, and `engineering-review`. Never include any other company or product name, domain, URL, logo, filename, customer statement, proprietary claim, or copyright text. Preserve general layout principles and interaction rhythm without reproducing an external identity or source-specific content.

## Implementation sequence

1. Write product definition, information architecture, critical flows, design tokens, backend boundary, data model, and permission model.
2. Scaffold the smallest runnable full-stack project with shared UI components and API contracts.
3. Implement the homepage contract, first-viewport proof, and the server routes that power its real forms and states.
4. For secondary pages, read the page-routing contract and implement independent primary-navigation URLs, listing/detail/application/article templates, shared shell, and direct deep-link support.
5. Implement authenticated and admin surfaces in the same pass as their backend storage, permission checks, and operational actions; do not leave them as frontend-only placeholders.
   - When scope includes inquiries, storage, or downstream synchronization, read the admin backend contract and implement its trust boundaries before connecting UI controls.
   - When scope includes monitoring, use the admin monitoring implementation baseline to generate the route map, state machines, redacted contracts, and operator smoke-test matrix before styling the workspaces.
6. Implement loading, empty, error with recovery, success, disabled, and permission-denied states where relevant.
7. Add responsive behavior for desktop, tablet, and mobile.
8. Run functional QA for navigation, history, forms, loading and success feedback, disclosures, and responsive menus.
9. Run visual QA at 1440px, 768px, and 390px; fix clipping, overlap, contrast, blank assets, generic visual language, and page-level overflow before delivery.

## Quality bar

Before completion, verify no console errors, broken images, horizontal mobile overflow, text overflow, or inaccessible focus states. Check stable image dimensions, WCAG AA contrast, and working recovery paths. If the result resembles a generic SaaS or AI template, redesign the hierarchy and composition instead of adding color, gradients, shadows, or animation.
