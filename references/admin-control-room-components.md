# Admin control-room component contract

Read this reference when a Lweb request includes an authenticated monitoring,
operations, catalogue, or storage surface.

## Component grammar

- Keep a fixed desktop rail and a restrained utility header. The rail owns
  workspace navigation; the header owns date range, refresh, export, and
  session actions.
- Start each workspace with a breadcrumb/status line, a single title block,
  and a visible freshness indicator. Do not repeat the product name in every
  panel heading.
- Use a filter row with compact square controls. A filter must show its label,
  selected value, clear affordance, and disabled/unconfigured state.
- Use a ruled metric strip for a small set of high-value numbers. Metric cells
  are equal only when they answer the same operator question; avoid a wall of
  floating cards.
- Build evidence panels with a title, one-line explanation, optional right-side
  status/action, and a ruled body. Tables should be the default for pages,
  products, inquiries, delivery jobs, and migration records.
- Charts are supporting evidence: use a quiet grid, explicit legend, readable
  units, and a text summary for screen readers. No decorative 3D, glow, or
  auto-playing motion.
- Preserve table-local horizontal scrolling for wide schemas. Never allow the
  page itself to scroll horizontally.

## Control-room visual tokens

Use the dark control-room variant unless the product brief explicitly chooses
another approved theme:

- shell `#11181e`, rail `#10161b`, panel `#171f26`, raised panel `#222e37`;
- rules `#2b3943` / `#3c4c57`, text `#e8eef1`, muted `#a6b4bc`, faint
  `#74838d`;
- slate-indigo `#6e79d8` for navigation and data emphasis;
- copper `#d1884b` for primary actions and attention markers;
- green `#58bd76` only for healthy, verified, or delivered states;
- danger `#e27c77` and warning `#e4ae58` for their semantic states.

Keep controls square or nearly square (0–2px radius), use mono numerals for
measurements and timestamps, and reserve color for semantics rather than
decoration. Every interactive control needs a visible focus ring and a stable
44px touch target.

## Responsive behavior

- At desktop widths, retain the rail and a multi-column evidence composition.
- At tablet widths, hide the rail, keep a sticky utility row, expose a compact
  workspace switcher, and move evidence to two columns where it remains
  scannable.
- At mobile widths, stack sections in reading order, keep controls touchable,
  and isolate horizontal scrolling to table wrappers. Test at 390px as well as
  768px and 1440px.

## Required states and checks

Every data module must define loading/skeleton, empty, stale or error with
recovery, success, disabled/unconfigured, and permission-denied states. Status
must be conveyed by text or icon as well as color. Before delivery, verify
direct route loading, back/forward history, filters, refresh, export, logout,
form validation, no console errors, no broken images, no clipped labels, and no
page-level horizontal overflow.
