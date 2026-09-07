# Page Routing Contract

Use a shared industrial shell with distinct page templates. The homepage is the only surface that relies on section anchors for in-page proof. Primary navigation must resolve to independent URLs so a buyer can bookmark, share, or revisit a specific decision page.

## Route families

| Family | Example paths | Structure | Primary job |
| --- | --- | --- | --- |
| Homepage | `/` | Full-bleed hero, proof strip, scope, comparison, applications, cases, workflow, FAQ, CTA | Establish trust and route qualified visitors |
| Listing page | `/products`, `/industries`, `/cases`, `/insights` | Page hero, short framing copy, ruled grid or index, filter/entry controls, CTA | Let buyers scan a category and choose a next detail |
| Application page | `/industries/:slug` | Hero, operating conditions, recommended scope, evidence, RFQ CTA | Translate a vertical use case into an engineering brief |
| Detail page | `/products/:slug`, `/materials/:slug`, `/cases/:slug` | Breadcrumb, narrow editorial article, specification rail, related links, CTA | Support one product, material, or project decision |
| FAQ page | `/faq` | Question index, disclosure groups, escalation CTA | Resolve pre-selection objections without overloading the homepage |
| Article page | `/insights/:slug` | Breadcrumb, article metadata, readable body column, related content, contact rail | Support technical education and organic discovery |

## Shared shell

- Keep the wordmark, dark header, language control, RFQ action, and dark footer consistent across routes.
- Mark the active primary navigation item by path, not by scroll position.
- Keep the same CTA language and form behavior, but allow the page-specific CTA to name the decision (`Review material`, `Request application fit`, `Send project brief`).
- Preserve a consistent 44px minimum target and visible focus ring on all route links and controls.

## Navigation rules

- Primary navigation links use real paths and must work on direct load, browser refresh, forward, and back.
- Use hash anchors only for same-page calls to action, comparison rows, FAQ disclosures, or a section explicitly named in the current page context.
- Never map every primary navigation item to a homepage anchor. A route change should reset scroll to the top and update the active item.
- Listing entries link to detail or application pages. Detail pages link back to their listing and to one adjacent decision page.

## Page rhythm

- Listing pages are scan-first: a compact hero followed by a ruled index or asymmetric grid; do not repeat the homepage card sequence.
- Detail pages are read-first: use a narrow text measure, generous whitespace, explicit metadata, and a compact specification rail. Avoid nested cards.
- Application pages lead with operating conditions and recommendation logic before showing product proof.
- Article pages use editorial typography, a sticky or visually distinct contact rail, and related content at the end.
- Every non-home route ends with a project CTA before the shared footer.

## Route QA

Verify each route at 1440px, 768px, and 390px. Check direct deep-link loading, active navigation, browser history, mobile menu close-after-navigation, CTA modal behavior, image loading, empty/error/success states where applicable, and no page-level horizontal overflow.
