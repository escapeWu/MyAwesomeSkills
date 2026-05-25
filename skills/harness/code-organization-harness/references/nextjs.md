# Next.js Organization Reference

Use this when changing `frontend/`.

## Routing And Colocation

- This project uses the App Router under `frontend/src/app`.
- Put routable screens in `frontend/src/app/<route>/page.tsx`.
- Use route segment folders for URL structure. Use Next.js route groups
  `(group)` only to organize routes without changing the URL.
- Use private folders such as `_components` for route-local implementation
  details when a page grows multiple private pieces. Do not move one-off local
  UI into global `frontend/src/components` just to make a page shorter.
- Keep `layout.tsx`, `loading.tsx`, `error.tsx`, and `not-found.tsx` in route
  segments only when that segment owns the behavior.

## Components

- Prefer small page-local components for one route.
- Promote to `frontend/src/components/` only when the component is reused across
  routes or clearly represents app-wide UI chrome.
- Keep component names domain-specific: `RunsTable`, `SchedulerTasksPanel`,
  `WorkerStatusPanel`. Avoid `GenericCard` unless it really is shared UI system
  vocabulary.
- Put browser interactivity in leaf components. Add `"use client"` only where
  hooks, browser APIs, event handlers, or client navigation require it.

## Data And Types

- Frontend code must call relative `/api/*` paths through
  `frontend/src/lib/api.ts`; never hardcode backend hosts in pages or
  components.
- Shared response/request types live in `frontend/src/types/index.ts` and must
  match Pydantic schemas.
- Route-specific view models can stay inside the page/component until reused.
- Cross-route formatting helpers live in `frontend/src/lib/`, as with
  `frontend/src/lib/time.ts`.

## Grep Flow

```bash
rg -n "apiGet|apiPost|/api/<path>|TypeName" frontend/src src/api tests
rg --files frontend/src/app frontend/src/components frontend/src/lib frontend/src/types
```

Before adding a component, search the visible label and likely prop names. If a
nearby component already owns the workflow, extend it instead of creating a
parallel panel.

## Validation

Run `make frontend-typecheck` after changing frontend types, API helpers, route
components, or shared components. Use browser verification for meaningful UI
layout or interaction changes.

## Primary Reference

- Next.js App Router project structure:
  https://nextjs.org/docs/app/getting-started/project-structure
