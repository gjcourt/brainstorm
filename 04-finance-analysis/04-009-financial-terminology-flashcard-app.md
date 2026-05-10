---
title: 'Financial Terminology Flashcard App'
number: '04-009'
category: 'finance-analysis'
difficulty: 'Easy'
time_commitment: '1-2 days'
target_skills: 'React + TypeScript + Vite, Tailwind, FSRS Spaced Repetition'
status: 'Not Started'
depends_on: []
---

# Financial Terminology Flashcard App

## Description

Build a web app using the FSRS-4.5 spaced repetition algorithm to memorize complex financial
terminology, accounting principles, and valuation formulas. Local-first (no backend) with optional
GitHub Pages deploy.

## Stack (locked)

- **Build:** Vite + React + TypeScript
- **Scheduling:** [`ts-fsrs`](https://github.com/open-spaced-repetition/ts-fsrs) (FSRS-4.5 reference
  implementation — do not reimplement)
- **Styling:** Tailwind CSS; dark mode via `prefers-color-scheme`
- **State:** `useReducer` (escalate to Zustand only if prop drilling exceeds 3 levels)
- **Animation:** plain CSS 3D transform for the card flip (no Framer Motion)
- **Tests:** Vitest
- **Persistence:** `localStorage` (no backend)
- **Deploy (stretch):** GitHub Pages

## Exit Criteria

- [ ] FSRS algorithm drives all scheduling: stability (S), difficulty (D), and retrievability (R)
      update correctly on each review; intervals decay realistically when cards are reviewed late
- [ ] Card flip UI: clicking/tapping a card reveals the back with a CSS 3D flip animation
- [ ] Review session flow: display card front → reveal back on demand → rate with Again / Hard /
      Good / Easy buttons
- [ ] Due queue logic: cards scheduled for today surface first; new cards mixed in when queue is
      empty; overdue cards penalised (shorter next interval) via FSRS retrievability decay
- [ ] Seed deck of ≥50 financial terms spanning four categories: equities, accounting principles,
      valuation formulas, fixed income basics
- [ ] Progress stats view showing: current streak, total cards in deck, due-today count, cards
      broken down by mastery level (New / Learning / Review / Mastered)
- [ ] Local storage persistence: card state and review history survive a full browser refresh (no
      backend required)
- [ ] App runs locally with `npm run dev` and opens in a browser without errors
- [ ] (Optional stretch) Deployed to GitHub Pages or Vercel at a public URL

## Progress

### Phase 1 – Algorithm & Data Model

- [ ] Read FSRS-4.5 spec: understand the DSR model (Difficulty, Stability, Retrievability), the
      forgetting curve `R(t) = (1 + FACTOR * t / S)^(-C)`, and the 17 default weight parameters
- [ ] Install `ts-fsrs` package (`npm install ts-fsrs`) — use the reference TypeScript
      implementation rather than reimplementing from scratch
- [ ] Define TypeScript types extending `ts-fsrs`: `AppCard` wraps `FSRSCard` with added fields (id,
      term, definition, category, example)
- [ ] Write unit tests for scheduling via `ts-fsrs`: verify S/D/R updates for each rating
      (Again/Hard/Good/Easy), confirm retrievability decays when `t > S`, confirm Again resets
      stability

### Phase 2 – App Scaffold & Persistence

- [ ] Scaffold project: `npm create vite@latest flashcards -- --template react-ts`
- [ ] Install dependencies: `ts-fsrs`, `vitest` (tests), `@types/react`, any needed date utility
- [ ] Implement `storage.ts`: `loadDeck() / saveDeck()` using `localStorage` with JSON
      serialisation; handle `Date` fields via replacer/reviver
- [ ] Seed `deck.ts`: define ≥50 `AppCard` objects across four categories
  - Equities (~15): P/E, EPS, market cap, beta, dividend yield, book value, float, short interest,
    alpha, ROE, ROIC, EV, EBITDA, free cash flow, dilution
  - Accounting principles (~12): accrual basis, matching principle, going concern, materiality,
    conservatism, revenue recognition, depreciation, amortisation, FIFO/LIFO, goodwill, deferred
    revenue, working capital
  - Valuation formulas (~13): DCF, WACC, terminal value, Gordon Growth Model, comparable company
    analysis, precedent transactions, LBO, NAV, price-to-book, EV/EBITDA, PEG ratio, margin of
    safety, intrinsic value
  - Fixed income basics (~10): coupon rate, yield to maturity, duration, convexity, credit spread,
    par value, zero-coupon bond, callable bond, inverted yield curve, credit rating

### Phase 3 – Core UI

- [ ] `CardFlip` component: CSS 3D perspective flip; front shows term + category badge; back shows
      definition and a usage example sentence
- [ ] `ReviewSession` screen: renders due queue one card at a time; "Show Answer" button triggers
      flip; rating buttons (Again / Hard / Good / Easy) advance to next card and call `ts-fsrs`
      scheduler
- [ ] `useDueQueue` hook: derives sorted queue from deck state — overdue cards first (FSRS
      retrievability already reflects the gap), then today's new cards; memoised to avoid re-sorting
      on every render
- [ ] Deck state managed via `useReducer`; rating dispatches a `RATE_CARD` action that calls
      `ts-fsrs` and persists in the same reducer step
- [ ] Wire persistence: call `saveDeck` after every rating so refreshing the page restores progress

### Phase 4 – Progress Dashboard & Polish

- [ ] `StatsView` component: streak counter (consecutive days with ≥1 review), due-today count,
      total cards, mastery-level breakdown displayed as a simple bar or table
- [ ] Category filter: tab or dropdown to browse cards by category (equities / accounting /
      valuation / fixed income) independent of the review session
- [ ] Apply Tailwind styling; dark mode via `prefers-color-scheme` (no class-based toggle)
- [ ] Write `README.md`: project description, `npm install && npm run dev` quickstart, how FSRS
      scheduling works (stability, retrievability, decay), deck seed format

### Phase 5 – Optional Stretch

- [ ] Deploy to GitHub Pages (`gh-pages` package) or Vercel; add public URL to README
- [ ] Export deck as JSON via a download button; import via file picker
- [ ] Custom card creation UI: form to add term / definition / category; persisted to local storage
      alongside seed deck
