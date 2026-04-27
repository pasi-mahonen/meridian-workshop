# Technical Approach

**RFP #MC-2026-0417 — Meridian Components Inventory Dashboard**

---

We have reviewed the source code delivered by the previous vendor and their handoff documentation. Our approach is grounded in the actual state of the codebase — not just the requirements as written. Where we have made assumptions, we have called them out explicitly and flagged them as items to confirm with Meridian before work begins.

---

## R1 — Reports Module Remediation

The previous vendor acknowledged the Reports module was incomplete at contract end. Our audit of the codebase confirms the root causes: filters are not correctly wired to API query parameters, several strings in the Reports view are missing i18n translations, and parts of the view are written using the older Options API pattern inconsistent with the rest of the codebase.

Our approach:

- Conduct a complete audit of the Reports page, documenting every defect against Meridian's logged issue list
- Fix filter wiring so that Time Period, Warehouse, Category, and Order Status filters correctly drive API calls
- Close all i18n gaps in the Reports view
- Migrate Options API usage to Composition API, aligning the view with the rest of the frontend
- Any defects discovered beyond the eight Meridian has logged will be documented and brought to Meridian for prioritization before we act on them — we will not silently expand scope

**Assumption:** The eight logged issues are the full known list. We will treat any additional findings as a scope conversation, not unilateral fixes.

---

## R2 — Restocking Recommendations

This is the largest new capability in the engagement. The goal is to give the operations team a view that recommends purchase orders based on what is in stock, what demand forecasts say is coming, and a budget ceiling the operator sets.

Our approach:

- Add a new `/restocking` route to the Vue frontend, consistent with the existing navigation and design patterns
- The view will take a single operator input: a budget ceiling in USD
- On the backend, a new `/api/restocking` endpoint in FastAPI will combine data from the existing `/api/inventory` (current stock levels) and `/api/demand` (demand forecast) endpoints, apply a prioritization algorithm (lowest stock relative to forecast demand, within budget), and return a ranked list of recommended purchase orders
- Each recommendation will show: item, warehouse, current stock, forecasted demand, recommended order quantity, and estimated cost
- The frontend will display results in a sortable table with a clear total cost indicator

**Assumption:** The existing demand forecast data (`/api/demand`) is sufficient as an input. No new data sources or integrations are required. If Meridian's operations team has additional inputs they want factored in (e.g., supplier lead times, minimum order quantities), we can discuss incorporating them — but that would affect timeline and cost.

---

## R3 — Automated Browser Testing

The absence of test coverage is the reason Meridian IT has blocked changes to the current system. We treat R3 as an enabler for everything else — which is why our QA Engineer is engaged from day one, not parachuted in at the end.

Our approach:

- Use Playwright for end-to-end browser testing (already supported in the project tooling)
- At project kickoff, our QA Engineer will work with Meridian IT to define what constitutes a "critical flow" — we will not make that determination unilaterally
- Baseline flows we expect to cover: dashboard load and summary display, filter interactions across all views, Reports page (including the defects we fix in R1), and the new Restocking view (R2)
- Tests will be committed to the repository and structured so they can be run in a CI pipeline
- QA will maintain a living test coverage log updated throughout the engagement

**Assumption:** Meridian IT will participate in the kickoff session to define critical flows. Their input is required to make R3 meaningful.

---

## R4 — Architecture Documentation

The previous vendor's handoff documentation was two pages. Meridian IT deserves something they can actually use.

Our approach:

- Review the complete codebase and produce a current-state architecture overview
- Deliverable format: an interactive HTML diagram, suitable for display in a browser and easy to share internally
- The document will cover: system components (Vue frontend, FastAPI backend, JSON data layer), data flow, API surface, filter system, and deployment topology
- We will explicitly document the absence of a database — data is stored as JSON files in the server directory — and note this as a consideration for Meridian IT as the system scales

**Assumption:** Format is at vendor discretion per the RFP. We have chosen HTML for accessibility and ease of sharing; if Meridian IT has a preferred format (PDF, Confluence, etc.), we can accommodate that.

---

## Desired Items

### D1 — UI Modernization
We will work within the existing design token set (slate/gray palette, status colors) to tighten visual consistency across the dashboard without a full rebrand. If Meridian has a brand guide or design system they want us to align to, we will need that before work begins.

### D2 — Internationalization
Extend i18n support to all remaining modules so Tokyo warehouse staff can work in Japanese. The existing codebase has partial i18n infrastructure in place; this is an extension, not a rebuild.

### D3 — Dark Mode
Implement an operator-selectable dark theme using CSS variable toggling. The preference will persist across sessions. Suitable for low-light warehouse floor environments.

Each desired item is scoped and priced independently (see Pricing section). Meridian may select any combination.

---

## Assumptions Summary

| # | Assumption | If Wrong |
|---|---|---|
| A1 | Reports defects are limited to the eight logged issues | Additional defects become a scope conversation |
| A2 | Demand forecast data is sufficient input for Restocking | Additional data sources affect timeline and cost |
| A3 | Meridian IT will participate in kickoff to define critical flows | R3 scope defaults to our baseline four flows |
| A4 | Architecture documentation format is at vendor discretion | We can accommodate a preferred format |
| A5 | No design system or brand guide exists for D1 | We will need it before UI work begins |
