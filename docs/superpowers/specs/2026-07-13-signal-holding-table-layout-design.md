# Signal Holding Table Layout Design

## Goal

Give the Signal application more room for the main content while keeping financial values and dates in the holding-record tables on one line.

## Scope

- Reduce the expanded left navigation width from 200px to 170px through the existing shared CSS variable.
- Apply the change to layouts that consume `--left-menu-max-width`; collapsed and mobile widths remain unchanged.
- On the Holding List page, keep cells in the active-holding table and its expanded operation table on one line.
- Preserve the full content by allowing horizontal scrolling when the available width is insufficient.

## Design

The existing layout already derives its main-content offset and width from `--left-menu-max-width`. Changing that variable keeps the logo, menu, fixed header, tags view, and content area aligned without adding a page-specific layout rule.

The active-holding table will receive a page-local wrapper class. Its table cells will use `white-space: nowrap`, and the table will have a stable minimum width. The wrapper will use horizontal overflow so large numeric values, dates, and paired metrics remain unbroken instead of wrapping or shrinking unpredictably. The nested operation table will use the same no-wrap rule.

The sold-out table is not part of this request and will remain unchanged.

## Error Handling

No new requests, state, or error paths are introduced. Native Element Plus table scrolling remains the fallback for viewports narrower than the table minimum width.

## Verification

- Confirm the root menu width variable is 170px in expanded desktop layouts.
- Confirm the Holding List main and expanded operation tables do not wrap numeric or date text.
- Confirm horizontal scrolling is available rather than clipping content on a constrained desktop viewport.
- Run the Signal type-check/build command available in `signal/package.json`.
