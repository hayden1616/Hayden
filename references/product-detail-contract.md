# Product Detail Contract

Use this contract for industrial B2B product detail pages. The detail route is a procurement surface, not a reduced marketing card and not a generic article page.

## Above-the-fold structure

- Show a breadcrumb that returns to the catalogue and category.
- Use a two-column purchase surface on desktop: a thumbnail gallery with a stable main image on the left, and the decision panel on the right.
- The decision panel must include product family or model code, product title, concise application summary, quotation basis, minimum review or order unit, configuration lead-time language, supply scope, primary technical inquiry action, secondary engineer-contact action, and compact trust markers.
- Industrial products should not invent a public unit price when price depends on range, interface, installation, certification, or quantity. State the quotation basis and the inputs required to confirm it.
- Provide lightweight save/shortlist and share actions when they help repeated procurement work. Keep them secondary to the inquiry action.

## Detail body

- Add a sticky in-page section index for `Specifications`, `Description`, `Applications`, and `Documents`.
- Present specifications as a ruled matrix of label/value rows. Keep technical values scannable and expose configuration-dependent caveats.
- Use a descriptive editorial block for the engineering rationale, with a meaningful product or integration image and a short feature list.
- Add an application-fit section that names operating conditions, installation, control output, and acceptance evidence.
- Add document rows for datasheet, manual, drawing, certificate, or equivalent files. When a file is not public, make the action request-based and provide feedback.
- Finish with related products from the same category first, then adjacent categories, followed by the shared project CTA and footer.

## Interaction states

- Gallery thumbnails and previous/next controls must expose the active image and remain keyboard reachable.
- Save, share, document requests, inquiry, and engineer contact actions need visible success or status feedback.
- Loading and disabled states must preserve the geometry of the purchase panel and primary actions.
- A missing or unknown slug should resolve to a recoverable not-found route, never a blank page.

## Responsive rules

- At desktop, preserve the two-column purchase surface and a 310–360px information rail only when it does not squeeze the primary content.
- At tablet, stack the gallery above the decision panel and retain a two-column spec matrix.
- At mobile, stack gallery, decision panel, specs, description, application fit, documents, and related products. Keep inquiry actions full width and maintain 44px touch targets.

## Content and safety

- Adapt commerce concepts such as price, MOQ, shipping, supplier proof, and company information into domain-appropriate industrial terms such as quotation basis, minimum review unit, project schedule, documentation, calibration, and engineering support.
- Do not include external brands, domains, logos, customer claims, platform guarantees, or source-specific text in the implementation or skill resources. The only concrete brand example allowed by the skill is `GoodJob` when explicitly requested by the user.
