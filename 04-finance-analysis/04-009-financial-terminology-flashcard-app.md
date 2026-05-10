---
title: 'Multi-Deck Flashcard App (financial, NATO, latency, acronyms)'
number: '04-009'
category: 'finance-analysis'
difficulty: 'Easy'
time_commitment: '3-5 days'
target_skills: 'React + TypeScript + Vite, Tailwind, React Router, FSRS Spaced Repetition'
status: 'Not Started'
depends_on: []
---

# Multi-Deck Flashcard App

## Description

A web flashcard app using FSRS-4.5 spaced repetition. Originally scoped as a finance-only deck;
re-scoped to a generic multi-deck app so the same engine drives any knowledge bank — financial
terminology, NATO phonetic alphabet, system-design latency numbers, tech acronyms, etc.

Three usage patterns drive the design:

1. **Study one thing** — open a single deck (`/decks/nato`)
2. **Study everything** — review across all decks merged (`/all`)
3. **Study these N things** — save a named **collection** of decks (e.g.
   `interview-prep = [nato, latency, acronyms]`) and review the merged due queue

Local-first (no backend). Single-deck mini-deploys via build-time env flag.

## Stack (locked)

- **Build:** Vite + React 19 + TypeScript
- **Routing:** React Router v7
- **Scheduling:** [`ts-fsrs`](https://github.com/open-spaced-repetition/ts-fsrs) (FSRS-4.5 reference
  implementation — do not reimplement)
- **Styling:** Tailwind CSS v4; dark mode via `prefers-color-scheme`
- **State:** `useReducer` (escalate to Zustand only if prop drilling exceeds 3 levels)
- **Animation:** plain CSS 3D transform for the card flip (no Framer Motion)
- **Tests:** Vitest + @testing-library/react
- **Persistence:** `localStorage`
- **Bundled content:** 4 starter decks shipped as JSON in `public/decks/`
- **Deploy (stretch):** GitHub Pages — multi-deck build + NATO-only locked build

## Concepts

- **Card** — atomic unit. Has FSRS state (D/S/R), `term`, `definition`, `category`, `example`,
  globally unique id (prefixed with deck id, e.g. `nato:a`).
- **Deck** — bundled JSON of cards, immutable content. Loaded from `public/decks/<id>.json`.
- **Collection** — user-saved combo of deck ids: `{ id, name, deckIds, createdAt }`. Persisted in
  localStorage. Reviewing a collection merges due queues across its decks.
- **Pseudo-collections** — `all` (every deck) is hard-coded; not stored as a Collection.

## Data shapes

```ts
type AppCard = FSRSCard & {
  id: string; // e.g. "nato:a"
  deckId: string; // e.g. "nato"
  term: string;
  definition: string;
  category: string;
  example?: string;
};

type Deck = {
  id: string;
  name: string;
  description: string;
  cards: AppCard[];
};

type Collection = {
  id: string; // user-supplied slug
  name: string;
  deckIds: string[];
  createdAt: number;
};
```

localStorage layout:

- `flashcards:cards` — `Record<cardId, FSRSCardState>` — per-card scheduling state, the source of
  truth. Survives deck content edits because card ids are stable.
- `flashcards:collections` — `Collection[]` — user-defined collections.
- `flashcards:reviews` — `Array<{ cardId, ratedAt, rating }>` — review history for streak/stats
  (capped at last 1000 entries).

## Routes

- `/` — home: deck list + saved collections, each with due counts and "review" buttons
- `/decks/:id` — single-deck review session
- `/decks/:id/cards` — deck contents browser (read-only list of all cards in the deck)
- `/collections/:id` — custom-collection review session
- `/all` — review across every bundled deck (pseudo-collection)
- `/manage` — create/edit/delete collections; import deck JSON; reset progress

## Build-time lock

`VITE_LOCKED_DECK=<deckId>` produces a focused single-deck build:

- Router redirects `/` → `/decks/<id>`
- Header chrome (collection picker, manage link) is hidden
- `/manage`, `/collections/*`, `/all` return a 404 component
- Same codebase; deploy multiple instances side-by-side (`flashcards.example.com`,
  `nato.example.com`)

## Exit Criteria

- [ ] FSRS algorithm drives all scheduling: stability (S), difficulty (D), and retrievability (R)
      update correctly on each review; intervals decay realistically when cards are reviewed late
- [ ] App ships with 4 bundled decks: financial (≥50 cards), NATO phonetic (26 cards), latency
      numbers for system design (≥20 cards), tech acronyms (≥50 cards)
- [ ] Card flip UI: tapping a card reveals the back with a CSS 3D flip animation
- [ ] Review session flow: display card front → reveal back on demand → rate with Again / Hard /
      Good / Easy buttons → advance to next card in the merged due queue
- [ ] Due queue logic: cards scheduled for today surface first; new cards mixed in when queue is
      empty; overdue cards penalised (shorter next interval) via FSRS retrievability decay; merged
      queue across N decks sorts by retrievability regardless of source deck
- [ ] Routes work: `/`, `/decks/:id`, `/decks/:id/cards`, `/collections/:id`, `/all`, `/manage`
- [ ] Collections: `/manage` lets the user create a named collection from any subset of decks;
      collection appears on home with a due-count badge; reviewing it merges queues across its
      decks; collections persist across browser refresh
- [ ] Per-deck and per-collection stats: streak, due-today count, total cards, mastery-level
      breakdown (New / Learning / Review / Mastered)
- [ ] Build-time lock: setting `VITE_LOCKED_DECK=nato` in `.env` and running `npm run build`
      produces a build whose root path goes straight to that deck's review with no chrome
- [ ] Local storage persistence: card state, collections, and review history survive a full browser
      refresh
- [ ] App runs locally with `npm run dev` and opens in a browser without errors
- [ ] (Stretch) Deployed to GitHub Pages: multi-deck instance + NATO-only locked instance, both
      reachable via public URLs in the README

## Progress

Each phase ships as its own PR against `gjcourt/flashcards`.

### Phase 1 — Types, FSRS scheduling, tests

- [ ] Define `AppCard`, `Deck`, `Collection` types in `src/types.ts`
- [ ] Wrap `ts-fsrs` in `src/fsrs.ts`: pure functions `rate(card, rating, now)` →
      `{ card: AppCard, log: ReviewLog }`; default to `ts-fsrs` weight presets
- [ ] Unit tests via Vitest: verify S/D/R updates for each rating (Again/Hard/Good/Easy), confirm
      retrievability decays when `t > S`, confirm Again resets stability
- [ ] No UI yet — tests-only PR

### Phase 2 — Bundled decks, deck loader, per-card storage

- [ ] Author `public/decks/financial.json` (≥50 cards across equities, accounting, valuation, fixed
      income — see card list below)
- [ ] Author `public/decks/nato.json` (26 cards: A=Alfa, B=Bravo, …, Z=Zulu, with example
      transmission strings)
- [ ] Author `public/decks/latency.json` (≥20 cards: L1 cache 0.5ns, L2 7ns, RAM 100ns, SSD 150μs,
      disk 10ms, US→Europe RTT 150ms, etc. — Jeff Dean numbers)
- [ ] Author `public/decks/acronyms.json` (≥50 cards: API, CRUD, REST, gRPC, K8s, CNI, CSI, etc.)
- [ ] `public/decks/manifest.json` — `{ decks: [{ id, name, description, path }] }` so the app can
      enumerate available bundled decks at boot
- [ ] `src/decks/load.ts` — `fetchDeck(id)` and `fetchAllDecks()` with JSON schema validation; ids
      stable across loads (so FSRS state survives deck content edits)
- [ ] `src/storage.ts` — `loadCardState() / saveCardState()` for `flashcards:cards`,
      `loadCollections() / saveCollections()` for `flashcards:collections`, with `Date`
      replacer/reviver
- [ ] Tests: rate a card, persist, reload, verify state restored

### Phase 3 — Routing, home, single-deck review, card flip

- [ ] Install `react-router-dom@7`
- [ ] `src/router.tsx` — routes per the table above; `<Layout>` with header chrome conditionally
      rendered based on `VITE_LOCKED_DECK`
- [ ] `<Home>` — fetches manifest, lists decks with `<DeckTile>` (name, due count, total cards,
      "review" link)
- [ ] `<DeckReview>` (route `/decks/:id`) — loads deck, runs review session
- [ ] `<DeckCards>` (route `/decks/:id/cards`) — read-only table of all cards in the deck
- [ ] `<CardFlip>` — CSS 3D perspective flip; front shows term + category badge; back shows
      definition + optional example
- [ ] `<ReviewSession>` — renders due queue one card at a time; "Show Answer" button triggers flip;
      rating buttons advance to next card and call `rate()` from `fsrs.ts`
- [ ] `useDueQueue(deckIds: string[])` hook — derives sorted queue across the listed decks; overdue
      cards first (FSRS retrievability), then today's new cards; memoised
- [ ] Deck/card state managed via `useReducer` in a small context; rating dispatches `RATE_CARD`
      which calls `rate()` and persists in the same reducer step

### Phase 4 — Collections, /all, /manage

- [ ] `<CollectionReview>` (route `/collections/:id`) — same `<ReviewSession>`, merged queue across
      `collection.deckIds`
- [ ] `<AllReview>` (route `/all`) — same shape, deck ids = every bundled deck
- [ ] `<Manage>` (route `/manage`) — list collections; create new (name + deck checkboxes); delete;
      "reset all progress" button (clears `flashcards:cards`)
- [ ] Home page: collections section above decks section; "+ New collection" link → /manage
- [ ] Tests: create a collection, review it, verify merged queue includes cards from each deck

### Phase 5 — Stats, polish, dark mode

- [ ] `<StatsPanel>` shown above review session: streak (consecutive days with ≥1 review across
      anything), due-today count for the current scope (deck or collection), total cards in scope,
      mastery-level breakdown (New / Learning / Review / Mastered) computed from FSRS stability
      thresholds
- [ ] Tailwind dark mode via `prefers-color-scheme`; no theme toggle
- [ ] Empty states: "no cards due — come back tomorrow" with next-due timestamp
- [ ] Keyboard shortcuts: space=flip, 1/2/3/4=rate Again/Hard/Good/Easy
- [ ] Write app `README.md`: project description, quickstart, route map, how FSRS works, deck JSON
      format with a worked example so someone can author a new deck

### Phase 6 — Stretch: build-time lock, GH Pages deploy

- [ ] Wire `VITE_LOCKED_DECK` into `<Layout>` and `<Router>`; redirect / → /decks/$LOCKED; gate
      `/manage`, `/collections/*`, `/all`
- [ ] GitHub Pages deploy via `gh-pages` package + GitHub Actions workflow
- [ ] Two CI workflows: `deploy-multi.yml` (default build) and `deploy-nato.yml`
      (`VITE_LOCKED_DECK=nato`); deploy to `gh-pages` branch under different paths
- [ ] Add public URLs to README

## Card list — financial deck (Phase 2 reference)

- **Equities (~15):** P/E, EPS, market cap, beta, dividend yield, book value, float, short interest,
  alpha, ROE, ROIC, EV, EBITDA, free cash flow, dilution
- **Accounting principles (~12):** accrual basis, matching principle, going concern, materiality,
  conservatism, revenue recognition, depreciation, amortisation, FIFO/LIFO, goodwill, deferred
  revenue, working capital
- **Valuation formulas (~13):** DCF, WACC, terminal value, Gordon Growth Model, comparable company
  analysis, precedent transactions, LBO, NAV, price-to-book, EV/EBITDA, PEG ratio, margin of safety,
  intrinsic value
- **Fixed income basics (~10):** coupon rate, yield to maturity, duration, convexity, credit spread,
  par value, zero-coupon bond, callable bond, inverted yield curve, credit rating
