---
title: 'Financial Terminology Flashcard App'
number: '04-009'
category: 'finance-analysis'
difficulty: 'Easy'
time_commitment: '1-2 days'
target_skills: 'React Native/Flutter, Spaced Repetition Algorithms'
status: 'Not Started'
depends_on: []
---

# Financial Terminology Flashcard App

## Description

Build a simple mobile or web app using a spaced repetition algorithm (like SuperMemo-2) to memorize
complex financial terminology, accounting principles, and valuation formulas.

## Exit Criteria

- [ ] SM-2 algorithm implemented and covered by unit tests (easiness factor, interval, repetition count all update correctly for each rating)
- [ ] Card flip UI: clicking/tapping a card reveals the back with a CSS 3D flip animation
- [ ] Review session flow: display card front → reveal back on demand → rate with Again / Hard / Good / Easy buttons
- [ ] Due queue logic: cards scheduled for today surface first; new cards mixed in when queue is empty
- [ ] Seed deck of ≥50 financial terms spanning four categories: equities, accounting principles, valuation formulas, fixed income basics
- [ ] Progress stats view showing: current streak, total cards in deck, due-today count, cards broken down by mastery level (New / Learning / Review / Mastered)
- [ ] Local storage persistence: card state and review history survive a full browser refresh (no backend required)
- [ ] App runs locally with `npm run dev` and opens in a browser without errors
- [ ] (Optional stretch) Deployed to GitHub Pages or Vercel at a public URL

## Progress

### Phase 1 – Algorithm & Data Model

- [ ] Research and document SM-2 parameters: easiness factor (EF, default 2.5), interval (days), repetition count
- [ ] Define TypeScript types: `Card`, `Deck`, `ReviewRecord`, `ReviewRating` (`Again=0`, `Hard=1`, `Good=2`, `Easy=3`)
- [ ] Implement `sm2(card: Card, rating: ReviewRating): Card` — returns updated card with new interval, EF, next-review date
- [ ] Write unit tests for SM-2 covering: first review at each rating, EF floor (1.3), interval growth, Again reset to day 1

### Phase 2 – App Scaffold & Persistence

- [ ] Scaffold project: `npm create vite@latest flashcards -- --template react-ts`
- [ ] Install dependencies: `vitest` (tests), `@types/react`, any needed date utility
- [ ] Implement `storage.ts`: `loadDeck() / saveDeck()` using `localStorage` with JSON serialisation
- [ ] Seed `deck.ts`: define ≥50 `Card` objects across four categories
  - Equities (~15): P/E, EPS, market cap, beta, dividend yield, book value, float, short interest, alpha, ROE, ROIC, EV, EBITDA, free cash flow, dilution
  - Accounting principles (~12): accrual basis, matching principle, going concern, materiality, conservatism, revenue recognition, depreciation, amortisation, FIFO/LIFO, goodwill, deferred revenue, working capital
  - Valuation formulas (~13): DCF, WACC, terminal value, Gordon Growth Model, comparable company analysis, precedent transactions, LBO, NAV, price-to-book, EV/EBITDA, PEG ratio, margin of safety, intrinsic value
  - Fixed income basics (~10): coupon rate, yield to maturity, duration, convexity, credit spread, par value, zero-coupon bond, callable bond, inverted yield curve, credit rating

### Phase 3 – Core UI

- [ ] `CardFlip` component: CSS 3D perspective flip; front shows term + category badge; back shows definition and a usage example sentence
- [ ] `ReviewSession` screen: renders due queue one card at a time; "Show Answer" button triggers flip; rating buttons (Again / Hard / Good / Easy) advance to next card and call `sm2`
- [ ] `useDueQueue` hook: derives sorted queue from deck state — overdue cards first, then today's new cards; memoised to avoid re-sorting on every render
- [ ] Wire persistence: call `saveDeck` after every rating so refreshing the page restores progress

### Phase 4 – Progress Dashboard & Polish

- [ ] `StatsView` component: streak counter (consecutive days with ≥1 review), due-today count, total cards, mastery-level breakdown displayed as a simple bar or table
- [ ] Category filter: tab or dropdown to browse cards by category (equities / accounting / valuation / fixed income) independent of the review session
- [ ] Apply clean default styling (CSS Modules or Tailwind; dark-mode via `prefers-color-scheme` media query)
- [ ] Write `README.md`: project description, `npm install && npm run dev` quickstart, how SM-2 scheduling works, deck seed format

### Phase 5 – Optional Stretch

- [ ] Deploy to GitHub Pages (`gh-pages` package) or Vercel; add public URL to README
- [ ] Export deck as JSON via a download button; import via file picker
- [ ] Custom card creation UI: form to add term / definition / category; persisted to local storage alongside seed deck
