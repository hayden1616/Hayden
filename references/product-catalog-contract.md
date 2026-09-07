# Product Catalog Contract

Use this contract when a product or instrument route contains more than a few families. A buyer should be able to narrow the catalogue without reading a long one-column list.

## Required structure

- Add a visible category control using short, mutually exclusive labels such as `All`, `Weighing`, `Analysis`, `Level`, `Control`, and `Integration`.
- Add a keyword search field that searches model, product family, application, and short description. The search must update results without a page reload and expose an accessible label.
- Present results as a multi-column, multi-row index: three columns on wide desktop, two on tablet, and one on narrow mobile only when the viewport cannot support a readable grid.
- Each result needs a stable image ratio, model or family code, category, concise description, and a clear route to its detail page.
- Keep the catalogue grid ruled and square-edged. Use borders, numbering, and whitespace to create hierarchy; do not wrap every result in a floating rounded card.

## Interaction states

- Show the result count after category and search filters are applied.
- Preserve the selected category and query while the user scans the current page.
- Provide a clear/reset action when a query is active.
- When no result matches, show a useful empty state with the active filter context and a one-click reset.
- Keep filter controls keyboard reachable with `aria-selected` or an equivalent state, and ensure focus is visible.

## Responsive QA

At 1440px verify a three-column grid with balanced row heights; at 768px verify two columns and a usable filter toolbar; at 390px verify readable single-column fallback, no horizontal page overflow, and a search field that remains at least 44px high.
